"""Linear-size bounded-model search for matching capacity2 constructions.

Requires z3-solver, installed locally in ignored _sprint_deps. Does not share
the BFS implementation. Witness verification is explicit forward arithmetic.
"""
import argparse
import json
import sys
import time
from pathlib import Path
sys.path.insert(0,'scripts/anchors/_sprint_deps')
import z3


def verify(r,A,inputs,births):
    full=(1<<r)-1
    j,x=0,1
    history=[(j,x)]
    # A reverse b expansion must be the inverse of an actual forward merge.
    for t in range(A+1):
        if t:
            u=inputs[t]
            assert u<=j<=1+u,(r,t,j,u)
            out=x>>(r-1)
            jj=j-u+out
            y=((x<<1)&full)|u
            # Verify forward a from the candidate predecessor to current.
            assert (j,x)==(jj+(y&1)-out,(y>>1)|(out<<(r-1)))
            assert out<=jj<=1+out
            j,x=jj,y
            history.append((j,x))
        if births[t]:
            assert x&3==1
            x|=2
            assert ((x&~3)|((x&1)|((x>>1)&1)))==history[-1][1]
            history.append((j,x))
    assert (j,x)==(2,full)
    assert sum(births)==r+1
    return history


def solve(r,timeout):
    h=(r-1).bit_length()
    A=(h+1)*r-(1<<h)+2
    s=z3.SolverFor('QF_FD')
    s.set(timeout=timeout)
    us=[z3.Int(f'u{t}') for t in range(A+1)]
    bs=[z3.Int(f'b{t}') for t in range(A+1)]
    js=[z3.Int(f'j{t}') for t in range(A+1)]
    def U(t):
        return us[t] if t>=0 else 0
    def B(t):
        return bs[t] if t>=0 else 0
    s.add(us[0]==1,bs[0]==1,js[0]==0)
    for t in range(1,A+1):
        s.add(us[t]>=0,us[t]<=1,bs[t]>=0,bs[t]<=1,
              js[t]>=0,js[t]<=2)
        s.add(us[t]<=js[t-1],js[t-1]<=1+us[t])
        s.add(bs[t]<=us[t],bs[t]+us[t-1]<=1)
        s.add(bs[t]>=us[t]-us[t-1])
        s.add(js[t]==js[t-1]-us[t]+U(t-r)+B(t-r+1))
    s.add(js[A]==2,us[A]==1,z3.Sum(bs)==r+1)
    for i in range(1,r):
        s.add(U(A-i)+B(A-i+1)==1)
    start=time.monotonic()
    answer=s.check()
    if answer!=z3.sat:
        return dict(r=r,A=A,status=str(answer),reason=s.reason_unknown(),
                    seconds=round(time.monotonic()-start,3))
    model=s.model()
    inputs=[model.eval(v).as_long() for v in us]
    births=[model.eval(v).as_long() for v in bs]
    verify(r,A,inputs,births)
    return dict(r=r,A=A,length=A+r+1,status='SAT, independently verified witness',
                inputs=inputs,births=births,
                birth_times=[t for t,b in enumerate(births) if b],
                seconds=round(time.monotonic()-start,3))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--r',nargs='+',type=int,default=[24,31,32,33,63,64,65])
    p.add_argument('--timeout-ms',type=int,default=45000)
    args=p.parse_args()
    out=Path('scripts/anchors/sprint_results')
    out.mkdir(exist_ok=True)
    for r in args.r:
        result=solve(r,args.timeout_ms)
        print({k:v for k,v in result.items() if k not in ('inputs','births')},flush=True)
        (out/f'symbolic_upper_r{r}.json').write_text(json.dumps(result,indent=2)+'\n',
                              encoding='utf-8',newline='\n')


if __name__=='__main__':
    main()
