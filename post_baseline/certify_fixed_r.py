"""Generate finite affine certificates establishing ALL n>=r+2 for fixed r.

Not a sweep of n: finite unbounded-counter transition representatives certify
an infinite family through AFFINE_CERTIFICATES.md's extension lemma.
Use check_affine_certificates.py to check saved data without calling BFS.
"""
import argparse
import hashlib
import json
from pathlib import Path
from anchor_quotient import path
from dense_quotient import solve_dense
from check_affine_certificates import check


def conjectured_base(r):
    L=(r-1).bit_length()-1
    return (L+3)*r-(1<<(L+1))+3


def generate(r, out):
    cutoff=r+2
    N=1<<r
    d=solve_dense(r,cutoff+2)
    base=solve_dense(r,2)
    states={(j,x):base[j*N+x] for j in range(3) for x in range(N) if j or x}
    witness=path(r+2,r,states)
    target=base[3*N-1]
    assert target==conjectured_base(r),(r,target,conjectured_base(r))
    for J in range(2,cutoff+1):
        table=d[:(J+1)*N]
        table[0]=0  # empty class excluded; never inspected by checker
        data={'r':r,'J':J,'slope':3,'base_value':target,
              'potential':list(table),'base_path':witness,
              'claim':'B_r(n)=3*(n-r-2)+base_value for every n>=r+2',
              'proof':'AFFINE_CERTIFICATES.md, extension lemma'}
        try:
            check(data)
        except AssertionError:
            continue
        break
    else:
        raise RuntimeError(f'No affine certificate found for r={r}')
    dest=out/f'r{r}.json'
    dest.write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(r,target,'intercept',target-3*(r+2),'cutoff',J,flush=True)
    return {'r':r,'J':J,'base_value':target,'intercept':target-3*(r+2),
            'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--max-r',type=int,default=14)
    args=p.parse_args()
    out=Path('post_baseline/affine_certificates')
    out.mkdir(exist_ok=True)
    records=[generate(r,out) for r in range(2,args.max_r+1)]
    (out/'index.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':
    main()
