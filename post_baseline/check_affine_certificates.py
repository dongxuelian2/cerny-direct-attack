"""Check affine proof certificates independently of any shortest-path search.

Every local check uses direct tuple/bit arithmetic. Checking j=0..J+1
is exhaustive for the infinite affine extension, as proved in the paper.
No imports from either BFS implementation or the quotient edge generator.
"""
import argparse
import hashlib
import json
from pathlib import Path


def check(data):
    r,J=data['r'],data['J']
    N=1<<r
    table=data['potential']
    assert data['slope']==3 and J>=2
    assert len(table)==(J+1)*N
    assert all(type(v) is int and v>=0 for v in table)
    def P(j,x):
        return table[min(j,J)*N+x]+3*max(j-J,0)
    for i in range(r):
        assert P(0,1<<i)==0
    assert P(1,0)==0
    inequalities=0
    for j in range(J+2):
        for x in range(N):
            if not (j or x):
                continue
            u=x&1
            v=(x>>1)&1
            y=(x&~3)|(u|v)
            assert P(j,x)<=1+P(j,y),('b',j,x)
            inequalities+=1
            for t in (0,1):
                if t>j:
                    continue
                jj=j+u-t
                y=(x>>1)|(t<<(r-1))
                assert P(j,x)<=1+P(jj,y),('a',j,x,t)
                inequalities+=1
    value=data['base_value']
    for j in range(2,J+2):
        assert P(j,N-1)==3*(j-2)+value
    # Check an actual quotient path at capacity 2; source and target are
    # recomputed, not trusted. Distances in the witness are not used.
    witness=data['base_path']
    assert tuple(witness[0][0])==(2,N-1)
    assert len(witness)-1==value
    for left,right in zip(witness,witness[1:]):
        j,x=left[0]
        jj,y=right[0]
        label=right[2]
        assert 0<=j<=2 and 0<=jj<=2 and 0<=x<N and 0<=y<N
        if label=='b':
            assert (jj,y)==(j,(x&~3)|((x&1)|((x>>1)&1)))
        else:
            assert label=='a'
            t=y>>(r-1)
            assert t<=j<=1+t
            assert (jj,y)==(j+(x&1)-t,(x>>1)|(t<<(r-1)))
        assert jj+y.bit_count()>=1
    j,x=witness[-1][0]
    assert j+x.bit_count()==1
    return inequalities


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--dir',default='post_baseline/affine_certificates')
    args=p.parse_args()
    root=Path(args.dir)
    index=json.loads((root/'index.json').read_text(encoding='utf-8'))
    total=0
    for row in index:
        dest=root/f"r{row['r']}.json"
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==row['sha256']
        data=json.loads(dest.read_text(encoding='utf-8'))
        assert data['r']==row['r'] and data['base_value']==row['base_value']
        assert data['J']==row['J']
        assert row['intercept']==data['base_value']-3*(data['r']+2)
        L=(data['r']-1).bit_length()-1
        assert row['intercept']==L*data['r']-(1<<(L+1))-3
        count=check(data)
        total+=count
        print(f"r={data['r']}: ALL n>=r+2; B=3n{row['intercept']:+}; inequalities={count}",flush=True)
    print('PASS; infinite affine families checked; local representatives:',total)


if __name__=='__main__':
    main()
