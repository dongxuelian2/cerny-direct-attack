"""Finite exact controls for paper hyperplane/actual-letter guard refinements."""
import argparse,json,math
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations,combinations_with_replacement
from pathlib import Path

def digest(z):return sha256(json.dumps(z,separators=(',',':')).encode()).hexdigest()

def rank(masks,n):
    basis={}
    for mask in masks:
        row=[Fraction(mask>>q&1) for q in range(n)]
        for p,b in sorted(basis.items()):
            if row[p]:a=row[p];row=[x-a*y for x,y in zip(row,b)]
        p=next((q for q,x in enumerate(row) if x),None)
        if p is not None:a=row[p];basis[p]=[x/a for x in row]
    return len(basis)

def hyperplane(normal):
    n=len(normal);s=sum(a!=0 for a in normal)
    vertices=[v for v in range(1<<n) if sum(a*(v>>q&1) for q,a in enumerate(normal))==0]
    c=sum((1<<q) in vertices for q in range(n));d=rank(vertices,n)
    z=dict(normal=normal,n=n,support=s,boolean_span_rank=d,singletons=c,vertices=len(vertices),vertices_sha256=digest(vertices))
    if d==n-1:
        B=len(vertices)-c-1;z['history_count_bound']=B
        if s==2:assert len(vertices)==1<<(n-1)
        elif s==4:assert sorted(a for a in normal if a)==[-1,-1,1,1] and B==3*2**(n-3)-n+3
        else:
            assert s>=5 and len(vertices)<=5*2**(n-4)
            assert B<=3*2**(n-3)-n+3
            if n==6:assert B<=14
    return z

def graphs(d):
    edges=list(combinations(range(d),2));stream=sha256();profiles=0;hist=Counter();bipartite=0;binary_graphs=0
    for bits in range(1,1<<len(edges)):
        chosen=[e for i,e in enumerate(edges) if bits>>i&1]
        forbidden=[v for v in range(1<<d) if all((v>>p&1)!=(v>>q&1) for p,q in chosen)]
        badsingletons=sum(1<<q for q in range(d) if (1<<q) in forbidden)
        F=len(forbidden);bipartite+=bool(F);binary_graphs+=len(chosen)<=2
        stream.update(json.dumps([bits,F,badsingletons],separators=(',',':')).encode()+b'\n')
        for C in range(1,1<<d):
            c=C.bit_count();t=(C&badsingletons).bit_count()
            if c==t:continue
            B=(1<<d)-F-c+t-1;assert B<=(1<<d)-c-1;profiles+=1;hist[B]+=1
            if len(chosen)==1:assert B<=(1<<(d-1))-c+1
            if len(chosen)==2:assert B<=3*(1<<(d-2))-c
    return dict(d=d,nonempty_graphs=(1<<len(edges))-1,bipartite_graphs=bipartite,binary_graphs=binary_graphs,
                admissible_singleton_profiles=profiles,length_bound_histogram={str(k):hist[k] for k in sorted(hist)},semantic_sha256=stream.hexdigest())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/history_hyperplane_guards.json'));args=ap.parse_args()
    normals=[]
    for s in range(2,9):
        for aa in combinations_with_replacement((-3,-2,-1,1,2,3),s):
            if sum(aa)==0 and math.gcd(*aa)==1:normals.append(list(aa)+[0])
    models=[hyperplane(a) for a in normals]
    balanced=[hyperplane([1,1,-1,-1]+[0]*(n-4)) for n in range(5,16)]
    gg=[graphs(d) for d in range(2,7)]
    arithmetic=[]
    for d in range(4,65):
        for s in range(5,d+1):
            assert math.comb(s,s//2)*16<=5*2**s
        p=3*2**(d-2)-d+2;q=5*2**(d-3)-2;assert p>q
        arithmetic.append([d,p,q])
    out=dict(schema='orion.history-hyperplane-guards.v1',integer_normal_scope='all sorted primitive zero-sum nonzero coefficients from +/-1,+/-2,+/-3, support2..8, with one appended zero',
             normal_models=models,balanced_models=balanced,guard_graphs=gg,arithmetic=arithmetic,
             boundary='PROVED paper support/counting and actual-letter guard bounds; finite controls only, not all real normals or all DFAs. Conditional quotient use explicitly requires its smaller Cerny bound. General Cerny and ALL/SOME history cost/rank remain OPEN; no formal proof.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(normal_models=len(models),balanced_models=len(balanced),guard_graphs=sum(z['nonempty_graphs'] for z in gg),singleton_profiles=sum(z['admissible_singleton_profiles'] for z in gg),arithmetic=len(arithmetic))),flush=True)

if __name__=='__main__':main()
