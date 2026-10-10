"""Complete native scans; no bounded SAT search or time cutoff."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from alphabet_check import certificate,verify
ROOT=Path(__file__).resolve().parent
CASES=['inside1','inside2','outside1','outside2','common1','absent2']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('n',type=int,choices=[9,13])
 ap.add_argument('--sanitized',action='store_true');ap.add_argument('--executable',type=Path)
 args=ap.parse_args();suffix='_sanitized' if args.sanitized else ''
 stem='probe_overlap_three_kernel'+suffix+('.exe' if sys.platform=='win32' else '')
 executable=(args.executable or ROOT/stem).resolve();records=[]
 for name in CASES:
  out=ROOT/f'overlap_three_kernel_{name}{suffix}_n{args.n}.json'
  subprocess.run([str(executable),str(args.n),name,str(out)],cwd=ROOT,check=True)
  data=json.loads(out.read_text(encoding='utf-8'))
  if data['witness_found']:
   z=certificate(data['rows'],data['S'],1);assert z and verify(z) and z['value']==args.n-1
   (ROOT/f'overlap_three_kernel_witness_{name}_n{args.n}.json').write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
  records.append(dict(case=name,file=out.name,complete=data['complete_normalized_family'],
   witness_found=data['witness_found'],row_assignments=data['row_assignments'],sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
 sources=[Path(__file__).name,'probe_overlap_three_kernel.cpp','kernel_probe_base.hpp',
  'OVERLAP_THREE_KERNEL_NORMALIZATION.md','LOCALIZED_BINARY_ENTRANCE_KERNEL.md','alphabet_check.py']
 result=dict(status='complete' if all(z['complete'] for z in records) else 'witness_verified',
  n=args.n,s=args.n-4,r=1,sanitized=args.sanitized,reports=records,
  source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
  scope='Complete six-shape conditional B3, overlapping-C with one new point normalized family. No other-entrance or unrestricted exclusion.')
 (ROOT/f'overlap_three_kernel_scans{suffix}_n{args.n}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status=result['status'],n=args.n,sanitized=args.sanitized,cases=len(records),rows=sum(z['row_assignments'] for z in records))))

if __name__=='__main__':main()
