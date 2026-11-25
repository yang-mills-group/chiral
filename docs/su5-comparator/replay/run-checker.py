#!/usr/bin/env python3
"""Linux-side replay with real Lake sandboxing, logging, and resource records."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, platform, shutil, signal, subprocess, time
OUT=Path('/evidence')
state=json.loads((OUT/'status.json').read_text())
state.update(status='running',stage='comparator',pid=os.getpid(),completed_stages=['linux-setup','controls'])
def now(): return datetime.now(timezone.utc).isoformat()
def save(**kw):
    state.update(updated_utc=now(),**kw)
    for name in ('memory.current','memory.peak','memory.events'):
        p=Path('/sys/fs/cgroup')/name
        if p.exists(): state[name]=p.read_text().strip()
    p=OUT/'status.json.tmp'; p.write_text(json.dumps(state,indent=2)+'\n'); p.replace(OUT/'status.json')
try:
    controls=json.loads((OUT/'controls.json').read_text())
    if controls['status']!='passed' or len(controls['results'])!=7:
        raise RuntimeError('All seven controls must pass before replay')
    commit=subprocess.check_output(['/tools/bin/lean','--githash'],text=True).strip()
    if commit!='eb6cafb7290e8bd5f2937522d8d804f58f02bafc': raise RuntimeError('Checker compiler pin mismatch')
    config=json.loads(Path('/checks/comparator.json').read_text())
    if config['permitted_axioms']!=['propext','Classical.choice','Quot.sound'] or config['external_kernels']!={'con-ron':['/tools/bin/con-ron','--verified','--jobs=2']}:
        raise RuntimeError('Unexpected axiom or checker configuration')
    command=['/tools/bin/lake','comparator','--config','/checks/comparator.json','--challenge-from-export','/exports/reference.ndjson','--solution-from-export','/exports/solution.ndjson']
    save(checker_started_utc=now(),command=command,checker_commit=commit,platform=platform.platform(),note='Comparing the reference definitions and theorem, then checking the solution with con-ron and Lean. All seven controls passed.')
    with (OUT/'comparator.log').open('x') as f:
        proc=subprocess.Popen(command,cwd='/runcheck',stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
        save(child_pid=proc.pid)
        while proc.poll() is None:
            if shutil.disk_usage(OUT).free<30*2**30:
                os.killpg(proc.pid,signal.SIGTERM); proc.wait(timeout=20)
                raise RuntimeError('Stopped to preserve 30 GiB free host disk')
            save()
            time.sleep(15)
    text=(OUT/'comparator.log').read_text()
    markers=['con-ron kernel accepts the solution','Lean default kernel accepts the solution','Your solution is okay!']
    if proc.returncode!=0 or [line for line in text.splitlines() if line in markers]!=markers or text.splitlines()[-1:]!=markers[-1:] or 'Sandbox disabled' in text:
        raise RuntimeError(f'Comparator exit {proc.returncode}; required clean dual-kernel verdict not present')
    state['completed_stages'].append('comparator')
    save(stage='final-validation',checker_exit=proc.returncode,child_pid=None,checker_finished_utc=now(),note='Comparator and both kernels accepted. Checking final input hashes and evidence records.')
except Exception as e:
    save(status='failed',error=str(e),finished_utc=now(),child_pid=None)
    raise
