"""Finite adversarial check of the proposed uniform pair-distance potential."""
from itertools import combinations
import json
from pathlib import Path
from two_block_probe import construct

def potential(p,t,x,y):
    if x==y:return 0
    x,y=sorted((x,y));L=3*t+2
    def rho(i):return min(i,p-2)
    if y<p or (x<p and y<p+t):return L
    if x<p:
        if y==p+2*t:return min(L,2*t+2+rho(x))
        return min(L,max(L-(y-p-t+1),2*t+3+rho(x)))
    i,j=x-p+1,y-p+1
    if j<=t:return L
    if i<=t:
        if j==2*t+1:return 2*t-i+1
        h=j-t
        if h==i:return t-i+1
        if h>i:return 2*t-i+1
        return L-h
    if j==2*t+1:return 2*t+1
    return L-(j-t)

def main():
    pairs=edges=0
    for t in range(2,41):
        for p in sorted({4,5,t+1,t+2,t+3,2*t+5}):
            if p<4:continue
            rows,S,_,_,_=construct(p,t)
            for x,y in combinations(range(len(rows[0])),2):
                d=potential(p,t,x,y);pairs+=1
                if x in S and y in S:assert d==3*t+2
                for row in rows:
                    u,v=row[x],row[y]
                    assert d<=1+potential(p,t,u,v),(p,t,x,y,u,v,d,potential(p,t,u,v))
                    edges+=1
    out=dict(verified=True,pair_checks=pairs,transition_checks=edges,maximum_t=40,
             scope="Finite audit of a uniform symbolic potential, not a proof by extrapolation.")
    Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out))

if __name__=="__main__":main()
