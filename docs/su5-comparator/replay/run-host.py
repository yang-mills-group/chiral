#!/usr/bin/env python3
"""Start the isolated replay only after Docker memory approval/configuration."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,subprocess,time
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parents[1]/'outputs/su5-comparator'
DOCKER=['docker','--host','unix:///Users/oai/.docker/run/docker.sock']
def now(): return datetime.now(timezone.utc).isoformat()
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def save(**kw):
    p=OUT/'status.json'; state=json.loads(p.read_text()); state.update(updated_utc=now(),**kw)
    t=p.with_name(p.name+'.tmp'); t.write_text(json.dumps(state,indent=2)+'\n');t.replace(p)
def source_check():
    project=ROOT.parent/'su5-native-build/project'; bundle=ROOT.parent/'su5-inspection/chiral-su5'
    count=0
    for line in (bundle/'SHA256SUMS').read_text().splitlines():
        sha,name=line.split('  ',1)
        if name.endswith('.lean') or name in ('lakefile.toml','lake-manifest.json','lean-toolchain'):
            if digest(project/name)!=sha: raise RuntimeError('Source/config mismatch: '+name)
            count+=name.endswith('.lean')
    if count!=16523: raise RuntimeError('Unexpected source count')
    return count
try:
    info=json.loads(subprocess.check_output(DOCKER+['info','--format','{{json .}}'],text=True))
    if info['MemTotal']<60*2**30:
        raise RuntimeError('Docker still has less than 60 GiB. The requested memory change must be approved and applied before starting.')
    if shutil.disk_usage(ROOT).free<35*2**30: raise RuntimeError('Insufficient free host disk reserve')
    e=json.loads((OUT/'export-status.json').read_text())
    if e['status']!='passed': raise RuntimeError('Exports incomplete')
    if json.loads((OUT/'controls.json').read_text())['status']!='passed': raise RuntimeError('Controls incomplete')
    image=subprocess.check_output(DOCKER+['image','inspect','su5-comparator-checker:20261124','--format','{{.Id}}'],text=True).strip()
    command=DOCKER+['run','--name','su5-comparator-main','--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--security-opt','systempaths=unconfined','--security-opt','seccomp='+str(ROOT/'checker-seccomp.json'),'--user',f'{os.getuid()}:{os.getgid()}','--memory','60g','--memory-swap','60g','--cpus','8','--pids-limit','512','--tmpfs','/tmp:rw,nosuid,nodev,size=2g','--tmpfs','/runcheck:rw,nosuid,nodev,size=64m']
    for src,dest in [(ROOT/'linux-tools','/tools'),(ROOT/'exports','/exports'),(ROOT,'/checks')]:
        command+=['--mount',f'type=bind,source={src},target={dest},readonly']
    command+=['--mount',f'type=bind,source={OUT},target=/evidence',image,'python3','/checks/run-checker.py']
    provenance={'started_utc':now(),'docker_server_version':info['ServerVersion'],'docker_memory_bytes':info['MemTotal'],'image_id':image,'command':command,'verified_source_files':source_check(),'tool_hashes':{name:digest(ROOT/'linux-tools/bin'/name) for name in ('lean','lake','leanchecker','con-ron')},'configuration_sha256':digest(ROOT/'comparator.json'),'seccomp_sha256':digest(ROOT/'checker-seccomp.json'),'exports':e['exports'],'scope':'Native macOS build and export; Linux Comparator and both kernel checks with real bubblewrap. No fresh Linux source rebuild.'}
    (OUT/'run-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    with (OUT/'container-run.log').open('x') as f:
        proc=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT)
    inspect=json.loads(subprocess.check_output(DOCKER+['inspect','su5-comparator-main'],text=True))[0]
    (OUT/'container-final-state.json').write_text(json.dumps(inspect['State'],indent=2)+'\n')
    if proc.returncode: raise RuntimeError(f'Checker container exited {proc.returncode}; see container-run.log and comparator.log')
    state=json.loads((OUT/'status.json').read_text())
    if 'comparator' not in state['completed_stages']: raise RuntimeError('No successful Comparator stage recorded')
    source_count=source_check()
    for side,record in e['exports'].items():
        if digest(Path(record['path']))!=record['sha256']: raise RuntimeError('Export changed: '+side)
    for name,sha in provenance['tool_hashes'].items():
        if digest(ROOT/'linux-tools/bin'/name)!=sha: raise RuntimeError('Tool changed: '+name)
    if digest(ROOT/'comparator.json')!=provenance['configuration_sha256']: raise RuntimeError('Config changed')
    acceptance={'status':'accepted','finished_utc':now(),'theorem':'ChiralSU5.exists_interacting_three_generation_theory_with_exact_running','verified_sources':source_count,'checker_exit':0,'kernels':['con-ron --verified --jobs=2','Lean default kernel'],'allowed_axioms':['propext','Classical.choice','Quot.sound'],'controls':json.loads((OUT/'controls.json').read_text()),'comparison_log_sha256':digest(OUT/'comparator.log'),'export_hashes':{k:v['sha256'] for k,v in e['exports'].items()},'matches_supplied_export_hashes':{k:v['matches_supplied_hash'] for k,v in e['exports'].items()},'scope':provenance['scope']}
    (OUT/'acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n')
    save(status='passed',stage='complete',completed_stages=['linux-setup','controls','comparator','final-validation'],finished_utc=now(),note='Comparator and both kernels accepted the unchanged proof exports. All seven control tests passed. Final source, export, configuration and tool hashes verified.')
except Exception as e:
    save(status='failed',error=str(e),finished_utc=now())
    raise
