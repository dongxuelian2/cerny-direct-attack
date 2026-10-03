"""Finite exact cube controls for the general shortest-full-history capacity lemma."""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def faces():
    grid=sorted({Fraction(p,q) for p in range(-4,5) for q in range(1,5)});nonzero=[v for v in grid if v]
    h=sha256();hist={};count=0
    for a,b,x in product(nonzero,nonzero,grid):
        valid=sum(v in (0,1) for v in (x,x+a,x+b,x+a+b));assert valid<=3
        h.update(json.dumps([[v.numerator,v.denominator] for v in (a,b,x)]+[valid],separators=(',',':')).encode()+b'\n')
        hist[valid]=hist.get(valid,0)+1;count+=1
    return dict(grid=[[v.numerator,v.denominator] for v in grid],nonzero_coefficients=len(nonzero),faces=count,
                valid_count_histogram={str(k):v for k,v in hist.items()},maximum_valid=3,semantic_sha256=h.hexdigest())

def partition(n,d):
    sizes=[1]*d;extra=n-d
    for i in range(1,d):
        if extra:sizes[i]+=1;extra-=1
    sizes[-1]+=extra;blocks=[];start=0
    for s in sizes:blocks.append(list(range(start,start+s)));start+=s
    vertices=[]
    for mask in range(1<<n):
        if all(len({mask>>q&1 for q in C})==1 for C in blocks):vertices.append(mask)
    c=sizes.count(1);assert c==max(1,2*d-n) and len(vertices)==1<<d
    return dict(n=n,d=d,blocks=blocks,c=c,cube_vertices=len(vertices),vertices_sha256=digest(vertices),
                admissible_full_history_bound=len(vertices)-c-1)

def nonpartition(d):
    n=d+1;vertices=[S for S in range(1<<n) if (S&1)+(S>>1&1)==(S>>2&1)+(S>>3&1)]
    assert len(vertices)==3*(1<<(d-2))
    return dict(n=n,d=d,equation_coefficients=[1,1,-1,-1]+[0]*(n-4),c=d-3,
                cube_vertices=len(vertices),vertices_sha256=digest(vertices),admissible_full_history_bound=len(vertices)-(d-3)-1)

def capacity(n,d):
    p=(1<<d)-1-max(1,2*d-n)
    return p if n==d else max(p,3*(1<<(d-2))-2)

def arithmetic():
    h=sha256();controls=0
    for d,start in ((2,2),(3,3),(4,5)):
        for n in range(start,4097):
            B=capacity(n,d);assert B<=(n-1)*(d-1);controls+=1
            h.update(json.dumps([n,d,B,(n-1)*(d-1)],separators=(',',':')).encode()+b'\n')
    return dict(maximum_n=4096,controls=controls,semantic_sha256=h.hexdigest(),regimes=[[2,2],[3,3],[4,5]])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/full_history_boolean_capacity.json'));args=ap.parse_args()
    out=dict(faces=faces(),partition=[partition(n,d) for n in range(2,13) for d in range(2,n+1)],
             nonpartition=[nonpartition(d) for d in range(4,15)],arithmetic=arithmetic(),
             boundary='PROVED paper ANY globally shortest full inverse history: length <= cube-vertex count minus all available singleton directions minus1; partition/nonpartition capacity gap; cost/rank inequality for d<=3 all n and d4 n>=5. Real-space sharpness examples are NOT DFA-history realizations. General Cerny and unrestricted ALL/SOME cost/rank hypotheses OPEN; no formal claim.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(faces=out['faces']['faces'],partition_scopes=len(out['partition']),nonpartition_scopes=len(out['nonpartition']),arithmetic_controls=out['arithmetic']['controls'],boundary=out['boundary'])),flush=True)

if __name__=='__main__':main()
