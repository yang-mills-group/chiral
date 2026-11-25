#!/usr/bin/env python3
"""Make small independent 4.32 exports for positive and rejection controls."""
from pathlib import Path
import hashlib, json, os, subprocess
ROOT=Path(__file__).resolve().parent
DEST=ROOT/'controls'
DEST.mkdir(exist_ok=True)
LEAN=Path('/Users/oai/.elan/toolchains/leanprover--lean4---v4.32.0')
EXPORTER=Path('/Users/oai/Documents/Codex/2026-11-15/wha/work/qcd-mac-20261116/tools/bin/lean4export')
sources={
 'Challenge':'theorem comm (n m : Nat) : n + m = m + n := by sorry\n',
 'Solution':'theorem comm (n m : Nat) : n + m = m + n := Nat.add_comm n m\n',
 'Wrong':'theorem comm (n m : Nat) : n + m = n + m := rfl\n',
 'Forbidden':'axiom forged (n m : Nat) : n + m = m + n\ntheorem comm (n m : Nat) : n + m = m + n := forged n m\n',
 'Sorry':'theorem comm (n m : Nat) : n + m = m + n := by sorry\n',
 'DefinitionChallenge':'def chosen : Nat := 0\ntheorem comm : chosen = chosen := rfl\n',
 'DefinitionWrong':'def chosen : Nat := 1\ntheorem comm : chosen = chosen := rfl\n',
}
primitives='Quot Quot.mk Quot.lift Quot.ind Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList Char.ofNat List eagerReduce Nat String String.mk Char optParam autoParam semiOutParam outParam'.split()
axioms=['propext','Classical.choice','Quot.sound']
env=dict(os.environ)
for key in ('LEAN_PATH','LEAN_SYSROOT','LEAN_SRC_PATH','ELAN_TOOLCHAIN'): env.pop(key,None)
env.update(PATH=f'{LEAN}/bin:/usr/bin:/bin',LEAN_PATH=str(DEST),LEAN_SYSROOT=str(LEAN))
records={}
for module,source in sources.items():
 p=DEST/(module+'.lean'); p.write_text(source)
 subprocess.run([LEAN/'bin/lean','-o',DEST/(module+'.olean'),p],cwd=DEST,env=env,check=True)
 target=DEST/(module+'.ndjson')
 with target.open('wb') as f:
  subprocess.run([EXPORTER,module,'--','comm',*axioms,*primitives],cwd=DEST,env=env,stdout=f,check=True)
 records[module]={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'export_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size}
cfg={'challenge_module':'Challenge','solution_module':'Solution','theorem_names':['comm'],'permitted_axioms':axioms,'external_kernels':{'con-ron':['/tools/bin/con-ron','--verified','--jobs=2']}}
(DEST/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
(ROOT.parents[1]/'outputs/su5-comparator/control-inputs.json').write_text(json.dumps(records,indent=2)+'\n')
print('Prepared',len(sources),'control exports.')
