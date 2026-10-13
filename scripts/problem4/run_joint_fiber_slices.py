"""Bounded synthesis in each admitted joint B,C orbit; no negative proof."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from alphabet_check import verify
from enumerate_joint_fiber_orbits import inventory
ROOT=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--letters',type=int,choices=[2,3],required=True)
 ap.add_argument('--timeout-ms',type=int,default=5000);ap.add_argument('--total-seconds',type=int,default=15)
 ap.add_argument('--ids');args=ap.parse_args()
 records,_=inventory()
 if args.ids:
  selected=set(args.ids.split(','));assert selected<={z['id'] for z in records}
  records=[z for z in records if z['id'] in selected]
 reports=[];status='diagnostic_joint_slices_finished'
 for z in records:
  name=z['id'];out=ROOT/f'joint_fiber_{name}_k{args.letters}.json'
  prior=ROOT/f"second_fiber_slice_{z['B_case']}_k{args.letters}.json"
  cmd=[sys.executable,str(ROOT/'synthesize_flag_boolean.py'),'13','9','1','--letters',str(args.letters),
   '--no-flag','--span-cover-h','5','--cover-by-images','--protected-state','3',
   '--protected-predecessor-size','0','--fixed-predecessor',','.join(map(str,z['B'])),
   '--second-predecessor','--fixed-second-predecessor',','.join(map(str,z['C'])),
   '--local-prefix-depth','2','--protected-isolation-depth','2','--minimal-traps',
   '--resume',str(prior),'--timeout-ms',str(args.timeout_ms),'--total-seconds',str(args.total_seconds),'--out',str(out)]
  print(json.dumps(dict(starting=name,B=z['B'],C=z['C'],alphabet=args.letters)),flush=True)
  subprocess.run(cmd,cwd=ROOT,check=True)
  data=json.loads(out.read_text(encoding='utf-8'));reports.append(dict(id=name,file=out.name,
   B=z['B'],C=z['C'],status=data['status'],iterations=data['iterations'],seconds=data['seconds'],
   safe_words=len(data['safe_constraints']),trap_cuts=len(data['trap_cuts']),sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
  if data['witness'] is not None:
   assert data['status']=='witness_verified' and verify(data['witness']) and data['witness']['value']==12
   status='witness_verified';break
 files=[Path(__file__).name,'enumerate_joint_fiber_orbits.py','synthesize_flag_boolean.py','alphabet_check.py','joint_fiber_orbits.json']
 result=dict(status=status,n=13,s=9,r=1,target=12,alphabet_size=args.letters,
  admitted_orbits=43,requested_orbits=[z['id'] for z in records],reports=reports,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
  scope='All requested joint fiber cases admitted, including overlaps. Bounded synthesis only: neither timeout nor uncertified UNSAT is an upper certificate.')
 (ROOT/f'joint_fiber_slices_k{args.letters}_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result),flush=True)
if __name__=='__main__':main()
