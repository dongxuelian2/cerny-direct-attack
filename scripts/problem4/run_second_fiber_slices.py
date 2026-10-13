"""Refine the six canonical B slices with the proved common second fiber.

Necessary cuts learned by the previous runs are retained. Solver failure
does not certify any global upper, and no previous slice is overwritten.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from alphabet_check import verify
from run_fiber_slices import CASES
ROOT=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--letters',type=int,choices=[2,3],required=True)
 ap.add_argument('--cases',default=','.join(CASES));ap.add_argument('--timeout-ms',type=int,default=30000)
 ap.add_argument('--total-seconds',type=int,default=90);args=ap.parse_args()
 names=args.cases.split(',');assert all(name in CASES for name in names)
 reports=[];status='diagnostic_slices_finished'
 for name in names:
  out=ROOT/f'second_fiber_slice_{name}_k{args.letters}.json'
  prior=ROOT/f'fiber_slice_{name}_k{args.letters}.json'
  cmd=[sys.executable,str(ROOT/'synthesize_flag_boolean.py'),'13','9','1',
       '--letters',str(args.letters),'--no-flag','--span-cover-h','5','--cover-by-images',
       '--protected-state','3','--protected-predecessor-size','0',
       '--fixed-predecessor',','.join(map(str,CASES[name])),'--second-predecessor',
       '--local-prefix-depth','2','--protected-isolation-depth','2','--minimal-traps',
       '--resume',str(prior),'--timeout-ms',str(args.timeout_ms),
       '--total-seconds',str(args.total_seconds),'--out',str(out)]
  print(json.dumps(dict(starting=name,alphabet=args.letters)),flush=True)
  subprocess.run(cmd,cwd=ROOT,check=True)
  z=json.loads(out.read_text(encoding='utf-8'));reports.append(dict(case=name,file=out.name,
              status=z['status'],iterations=z['iterations'],seconds=z['seconds'],
              safe_words=len(z['safe_constraints']),trap_cuts=len(z['trap_cuts']),
              sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
  if z['witness'] is not None:
   assert z['status']=='witness_verified' and verify(z['witness']) and z['witness']['value']==12
   status='witness_verified';break
 files=[Path(__file__).name,'run_fiber_slices.py','synthesize_flag_boolean.py','alphabet_check.py',
        'PROOF.md#problem4-second-entrance-fiber','second_entrance_audit.json']
 result=dict(status=status,n=13,s=9,r=1,target=12,alphabet_size=args.letters,
             requested_cases=names,reports=reports,
             source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
             scope='Complete symbolic B-slice admission with a common second fiber; bounded synthesis only, no negative upper certificate.')
 (ROOT/f'second_fiber_slices_k{args.letters}_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result),flush=True)
if __name__=='__main__':main()
