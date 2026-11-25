#!/usr/bin/env python3
"""Run small real Comparator controls with both kernels and real bubblewrap."""
from pathlib import Path
import datetime, json, os, subprocess, time
OUT=Path('/evidence')
OUT.mkdir(exist_ok=True)
ns={k:os.readlink('/proc/self/ns/'+k) for k in ('user','mnt','pid','net')}
(OUT/'outer-namespaces.json').write_text(json.dumps(ns,indent=2)+'\n')
os.environ['SU5_PRIVATE_SENTINEL']='must-not-enter-checker'
cfg=json.loads(Path('/controls/config.json').read_text())
results=[]
def control(name, challenge, solution, expected, marker, kernels=None):
    conf=dict(cfg)
    if kernels is not None: conf['external_kernels']=kernels
    p=OUT/(name+'-config.json'); p.write_text(json.dumps(conf,indent=2)+'\n')
    command=['/tools/bin/lake','comparator','--config',str(p),'--challenge-from-export','/controls/'+challenge+'.ndjson','--solution-from-export','/controls/'+solution+'.ndjson']
    log=OUT/(name+'.log'); start=time.monotonic()
    with log.open('w') as f:
        proc=subprocess.run(command,cwd='/runcheck',stdout=f,stderr=subprocess.STDOUT,timeout=300)
    content=log.read_text()
    if proc.returncode != expected or marker not in content or 'Sandbox disabled' in content:
        raise RuntimeError(f'Control {name} failed: exit {proc.returncode}; {content[-2000:]}')
    if name=='positive':
        for required in ['con-ron kernel accepts the solution','Lean default kernel accepts the solution']:
            if required not in content: raise RuntimeError('Missing '+required)
    results.append({'name':name,'exit_code':proc.returncode,'expected_exit':expected,'marker':marker,'elapsed_seconds':round(time.monotonic()-start,3),'passed':True})
    (OUT/'controls.json').write_text(json.dumps({'status':'running','results':results},indent=2)+'\n')
    print('PASSED',name,flush=True)
try:
    control('positive','Challenge','Solution',0,'Your solution is okay!')
    control('statement-mismatch','Challenge','Wrong',1,'statement do not match')
    control('forbidden-axiom','Challenge','Forbidden',1,'forged')
    control('sorry-rejected','Challenge','Sorry',1,'sorryAx')
    control('definition-mismatch','DefinitionChallenge','DefinitionWrong',1,"Const does not match between challenge and target 'chosen'")
    control('external-kernel-rejection','Challenge','Solution',1,'INTENTIONAL_KERNEL_REJECTION',{'reject-probe':['/usr/bin/python3','/checks/containment-probe.py','--reject']})
    control('containment','Challenge','Solution',0,'CONTAINMENT_PASSED',{'containment-probe':['/usr/bin/python3','/checks/containment-probe.py']})
    (OUT/'controls.json').write_text(json.dumps({'status':'passed','results':results,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
except Exception as e:
    (OUT/'controls.json').write_text(json.dumps({'status':'failed','results':results,'error':str(e)},indent=2)+'\n')
    raise
