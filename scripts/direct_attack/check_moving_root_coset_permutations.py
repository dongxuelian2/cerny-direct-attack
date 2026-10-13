"""Independent coset/permutation row, proportional cost and local boundary audit."""
from copy import deepcopy
from math import gcd
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]

def pull(U,f):
    V=0
    for q,p in enumerate(f):
        if U>>p&1:V|=1<<q
    return V

def literal(F,w):
    assert all(type(i) is int and i in (0,1) for i in w)
    states=list(range(len(F[0])))
    for i in w:states=[F[i][q] for q in states]
    return states

def check(data):
    parameters={(M,d) for M in range(6,31) for d in range(1,M) if 1<gcd(M,d) and M//gcd(M,d)>=3}
    parameters|={(60,20),(63,3),(63,21),(255,85),(256,2),(256,64),(300,100)}
    records=data['records'];assert len(records)==len(parameters) and {(z['M'],z['d']) for z in records}==parameters
    particles=extensions=two_factors=nontrivial_phi=0
    for z in records:
        M=z['M'];d=z['d'];g=gcd(M,d);L=M-d;r=M;t=M//g;full=(1<<M)-1;F=z['rows'];a,b=F;phi=z['phi']
        assert len(a)==len(b)==M+1 and a[r]==0 and a[0]==a[L]==r
        rest=[q for q in range(M) if q not in (0,L)];assert sorted(a[q] for q in rest)==rest
        assert b==[(q+1)%M for q in range(M)]+[r] and sorted(phi)==list(range(g)) and phi[0]==0
        assert all(a[q]%g==phi[q%g] for q in rest);nontrivial_phi+=phi!=list(range(g))
        p=next(q for q in rest if a[q]==2*L%M);j=(p-L)%M;v=z['preparation'];assert j%g==0 and j<=M-g
        assert v==[0]+[1]*j+[0]+[1]*d+[0] and len(v)<=M-g+d+3
        T=literal(F,v);assert set(T)==set(range(M))-{L} and T[r]%g==0
        expected=[1]*M+[0];expected[0]+=1;expected[a[d]]+=1;expected[L]-=1
        assert [T.count(q) for q in range(M+1)]==expected
        assert all(T[q]%g==(0 if q%g==0 else phi[phi[phi[q%g]]]) for q in range(M))
        R=z['return_word'];h=len(R)-len(v)-1;assert 1<=h<g and phi[phi[phi[h]]]==1 and R==[0]+[1]*h+v
        A=literal(F,R);assert set(A)<=set(range(M)) and A[r]%g==1
        exact=[0]*(M+1)
        for q,delta in [(0,1),(a[d],1),(L,-1),(T[r],1),(T[(L+h)%M],-1),(r,-1)]:exact[q]+=delta
        assert [A.count(q)-1 for q in range(M+1)]==exact
        projected=[sum(A.count(q)-1 for q in range(M) if q%g==c) for c in range(g)]
        assert projected==[2,-1]+[0]*(g-2) and A.count(r)-1==-1
        particles+=(M+1)*(len(v)+len(R))
        def verify(U,factor):
            nonlocal extensions,two_factors
            growth=factor['growth'];w=factor['word'];assert type(U) is int and 0<U<full and growth in (1,2) and len(w)<=(M+1)*growth
            if growth==1:assert w[:2]==[0,0] and all(i==1 for i in w[2:]) and len(w)<=M+1
            else:
                assert w[:len(R)]==R and all(i==1 for i in w[len(R):])
                k=len(w)-len(R);assert 0<=k<g and len(w)<=2*(M+1)
                assert all((U>>q&1)==(U>>((q+d)%M)&1) for q in range(M))
                assert U>>k&1 and not U>>((k+1)%g)&1 and M-U.bit_count()>=t>=3;two_factors+=1
            V=U
            for i in reversed(w):V=pull(V,F[i])
            assert V<=full and V.bit_count()==U.bit_count()+growth;extensions+=1;return V
        masks=[f['U'] for f in z['extensions']];assert len(masks)==len(set(masks))
        if M<=10:assert set(masks)==set(range(1,full))
        else:assert len(masks)==64 and sum(1<<q for q in range(M) if q%g==0) in masks
        for f in z['extensions']:verify(f['U'],f)
        U=pull(1<<r,a);s=[0];factors=z['reset_factors'];assert factors[0]==dict(word=[0,0]+[1]*L,growth=1)
        for f in factors:assert U.bit_count()<M-1;U=verify(U,f);assert U.bit_count()<=M-1;s=f['word']+s
        assert U.bit_count()==M-1 and s==z['reset_suffix'] and len(s)<=1+(M-d+2)+(M-4)*(M+1)
        q=next(q for q in range(M) if not U>>q&1);k=z['alignment'];assert k==(q-L)%M
        w=z['reset_word'];assert w==v+[1]*k+s and len(w)<=M*M-g+1
        assert literal(F,w)==[r]*(M+1);particles+=(M+1)*len(w)
    assert two_factors>0 and nontrivial_phi>0
    z=data['boundary_example'];F=z['rows'];U=z['U'];assert F==[[6,2,1,3,6,5,0],[1,2,3,4,5,0,6]] and U==21
    v=z['preparation'];assert v==[0,1,1,1,0,1,1,0] and set(literal(F,v))==set(range(6))-{4}
    R=[0,1]+v
    for k,expected in [(0,70),(1,57)]:
        V=U
        for i in reversed(R+[1]*k):V=pull(V,F[i])
        assert V==expected and V.bit_count()-3==k
    D=z['core_extension_distances'];assert len(D)==128;edges=0
    for U0,cost in enumerate(D):
        assert cost is None or type(cost) is int and cost>=0
        if U0<64 and U0.bit_count()>3:assert cost==0;continue
        finite=[D[pull(U0,f)] for f in F if D[pull(U0,f)] is not None]
        assert cost==(1+min(finite) if finite else None);edges+=2
    w=z['core_extension_word'];assert w==[0,1,0,1,0] and D[21]==len(w)==5
    V=21
    for i in reversed(w):V=pull(V,F[i])
    assert V==57
    assert len(set(literal(F,z['reset_word'])))==1 and len(z['reset_word'])<=36
    return dict(verified=True,inputs=len(records),proper_core_and_chain_extensions=extensions,two_point_controls=two_factors,
                nonidentity_coset_permutations=nontrivial_phi,literal_particle_controls=particles,boundary_bellman_edges=edges,
                boundary='Independent named noncoprime parameter cover with sampled coset/within-coset permutations, exact full-Q/class rows, original-r endpoint, forced first saving, proportional compatible square M^2-g+1. Mixed seven-state old-return pool fails TWO-growth but complete128-subset Bellman certifies alternative core extension5. No generator/solver import, universal noncoprime arbitrary-A proof, novelty or formal claim; general Cerny OPEN.')

def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/moving_root_coset_permutations.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(10):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:bad['records'].pop()
        if mode==1:z['phi'][0]=1
        if mode==2:z['return_word'].pop()
        if mode==3:z['reset_factors'][0]['word'].pop()
        if mode==4:z['extensions'].pop()
        if mode==5:z['alignment']=(z['alignment']+1)%z['M']
        if mode==6:bad['boundary_example']['core_extension_distances'][21]=4
        if mode==7:bad['boundary_example']['core_extension_word'].pop()
        if mode==8:bad['boundary_example']['rows'][0][1]=1
        if mode==9:z['reset_suffix'].append(1)
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError('accepted corruption '+str(mode))
    out['corruptions_rejected']=rejected
    (ROOT/'scripts/direct_attack/data/moving_root_coset_permutations_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
