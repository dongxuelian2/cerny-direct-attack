"""Synthetic rank profiles: an inequality obstruction, NOT DFA instances."""
import argparse
from fractions import Fraction
import json
from pathlib import Path

def profile(n):
    assert n>=4 and n%2==0
    m=n//2
    lam=[0]+[1]*m
    for r in range(m,n-1):
        lam.append(lam[-1]+min((r+1)*(r+2)//2,lam[-1]+r+1))
    return lam

def audit(n,lam):
    gaps=[lam[r+1]-lam[r] for r in range(n-1)]
    assert len(lam)==n and lam[0]==0 and lam[1]==1
    for r,gap in enumerate(gaps):
        assert 0<=gap<=(r+1)*(r+2)//2
        assert gap<=lam[r]+r+1
    # Every singleton-rich Shitov plateau splice inequality on rank lengths.
    # Include the terminal infinite gap, which only gives a tautological cap.
    augmented=gaps+[float('inf')]
    for r in range(1,n//2):
        first=next(t for t,d in enumerate(augmented) if d>2*r)
        assert gaps[r]<=lam[first]+2*r
    return dict(n=n,endpoint=lam[-1],square=(n-1)**2,
                endpoint_over_n3=float(Fraction(lam[-1],n**3)),
                inequality_audit=True,realizable_as_DFA='UNKNOWN; not asserted')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',default='direct_attack/data/abstract_profiles.json')
    args=ap.parse_args()
    reports=[]
    for n in [10,20,50,100,200,500,1000,2000]:
        lam=profile(n)
        reports.append(dict(**audit(n,lam),lambda_corank=lam if n<=100 else None))
    Path(args.out).write_text(json.dumps(reports,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k!='lambda_corank'} for r in reports]))

if __name__=='__main__': main()
