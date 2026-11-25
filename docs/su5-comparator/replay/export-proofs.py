#!/usr/bin/env python3
"""Export the unchanged, already compiled SU(5) reference and solution."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, signal, subprocess, time

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parents[1]
PROJECT = ROOT.parent / 'su5-native-build/project'
BUNDLE = ROOT.parent / 'su5-inspection/chiral-su5'
OUT = BASE / 'outputs/su5-comparator'
LEAN = Path('/Users/oai/.elan/toolchains/leanprover--lean4---v4.32.0')
EXPORTER = Path('/Users/oai/Documents/Codex/2026-11-15/wha/work/qcd-mac-20261116/tools/bin/lean4export')
THEOREM = 'ChiralSU5.exists_interacting_three_generation_theory_with_exact_running'
AXIOMS = ['propext', 'Classical.choice', 'Quot.sound']
PRIMITIVES = '''Quot Quot.mk Quot.lift Quot.ind
Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble
Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight
String.ofList Char.ofNat List eagerReduce Nat String String.mk Char
optParam autoParam semiOutParam outParam'''.split()
OUT.mkdir(parents=True, exist_ok=True)
(ROOT / 'exports').mkdir(exist_ok=True)
state = {'status': 'running', 'completed_stages': [], 'pid': os.getpid(), 'exports': {}}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def save(**kw):
    state.update(updated_utc=now(), free_gib=round(shutil.disk_usage(ROOT).free/2**30, 2), **kw)
    p = OUT / 'export-status.json.tmp'
    p.write_text(json.dumps(state, indent=2)+'\n')
    p.replace(OUT / 'export-status.json')

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def check_sources():
    count = 0
    for line in (BUNDLE / 'SHA256SUMS').read_text().splitlines():
        sha, name = line.split('  ', 1)
        if name.endswith('.lean') or name in ('lakefile.toml', 'lake-manifest.json', 'lean-toolchain'):
            if digest(PROJECT / name) != sha:
                raise RuntimeError('Source/config mismatch: '+name)
            count += name.endswith('.lean')
    if count != 16523:
        raise RuntimeError('Unexpected source count')
    return count

try:
    save(started_utc=now(), stage='source-and-tool-checks')
    expected = 'ef1d0587c57f9d9aabf2a54952203a4405eeb4b8f613254e93b5b83e1a74769e'
    if digest(EXPORTER) != expected:
        raise RuntimeError('Exporter executable hash mismatch')
    commit = subprocess.check_output([LEAN/'bin/lean', '--githash'], text=True).strip()
    if commit != '8c9756b28d64dab099da31a4c09229a9e6a2ef35':
        raise RuntimeError('Lean compiler commit mismatch')
    save(verified_sources=check_sources(), compiler_commit=commit, exporter_sha256=expected,
         exporter_source_commit='4e7915201d3f9f04470d9eae002fa695f7cdc589')
    manifest = json.loads((PROJECT/'lake-manifest.json').read_text())
    libraries = [PROJECT/'.lake/build/lib/lean'] + [PROJECT/manifest['packagesDir']/p['name']/'.lake/build/lib/lean' for p in manifest['packages']]
    env = dict(os.environ)
    for key in ('LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','ELAN_TOOLCHAIN','LAKE_HOME','LAKE'):
        env.pop(key, None)
    env.update(PATH=f'{LEAN}/bin:/usr/bin:/bin', LEAN_PATH=os.pathsep.join(map(str, libraries)),
               LEAN_SYSROOT=str(LEAN), LEAN_NUM_THREADS='4', LEAN_ABORT_ON_PANIC='1')
    supplied = json.loads((BUNDLE/'verification/acceptance.json').read_text())['exports']
    for side, module in [('reference','SU5ExactJointChallenge'),('solution','SU5ExactJointSolution')]:
        partial = ROOT / 'exports' / (side+'.partial')
        command = [str(EXPORTER), module, '--', THEOREM, *AXIOMS, *PRIMITIVES]
        save(stage=side+'-export', command=command)
        with partial.open('xb') as target, (OUT/(side+'-export.log')).open('x') as log:
            proc = subprocess.Popen(command, cwd=PROJECT, env=env, stdout=target, stderr=log, start_new_session=True)
            save(child_pid=proc.pid)
            while proc.poll() is None:
                if shutil.disk_usage(ROOT).free < 30*2**30:
                    os.killpg(proc.pid, signal.SIGTERM)
                    proc.wait(timeout=20)
                    raise RuntimeError('Stopped export to preserve 30 GiB free')
                save(exported_bytes=partial.stat().st_size)
                time.sleep(10)
        if proc.returncode:
            raise RuntimeError(f'{side} exporter exited {proc.returncode}')
        with partial.open('rb') as f:
            meta = json.loads(f.readline(65536))['meta']
        if meta['lean']['githash'] != commit or meta['format']['version'] != '3.1.0' or meta['exporter'] != {'name':'lean4export','version':'3.1.0'}:
            raise RuntimeError('Unexpected export metadata')
        final = partial.with_suffix('.ndjson')
        partial.rename(final)
        final.chmod(0o400)
        actual = digest(final)
        state['exports'][side] = {'path':str(final), 'bytes':final.stat().st_size, 'sha256':actual,
                                  'matches_supplied_hash':actual == supplied[side]['sha256'], 'metadata':meta}
        state['completed_stages'].append(side+'-export')
        save(child_pid=None, exported_bytes=final.stat().st_size)
    save(verified_sources=check_sources(), status='passed', stage='complete', finished_utc=now(), child_pid=None, command=None)
except Exception as e:
    save(status='failed', error=str(e), finished_utc=now())
    raise
