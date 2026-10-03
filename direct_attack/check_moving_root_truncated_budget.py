"""Independent finite cover, literal preimages/resets, and all-subset Bellman audit."""
from copy import deepcopy
from math import factorial,gcd
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def preimage(U,f):
    V=0
    for q in range(len(f)):
        if U&(1<<f[q]):V|=1<<q
    return V

def inverse_word(U,F,w):
    assert isinstance(w,list) and all(type(i) is int and i in (0,1) for i in w)
    for i in w[::-1]:U=preimage(U,F[i])
    return U

def images(F,w):
    states=list(range(len(F[0])))
    for i in w:states=[F[i][q] for q in states]
    return states

def bellman(D,F,goal):
    assert len(D)==1<<len(F[0]);edges=0
    for U,cost in enumerate(D):
        assert cost is None or type(cost) is int and cost>=0
        if goal(U):assert cost==0
        else:
            values=[D[preimage(U,f)] for f in F]
            finite=[v for v in values if v is not None]
            assert cost==(1+min(finite) if finite else None);edges+=len(F)
    return edges

def check_boundary(z):
    F=z['rows'];assert F==[[9,8,2,9,4,5,6,7,1,0],[1,2,3,4,5,6,7,8,0,9]] and z['U']==438
    assert len(z['exact_core_sizes'])==3;edges=0
    for c,K,cost,target in zip(z['exact_core_sizes'],[7,8,9],[11,11,15],[431,447,511]):
        assert c['target_size']==K and c['target']==target
        edges+=bellman(c['distances'],F,lambda V:V<512 and V.bit_count()==K)
        assert c['distances'][438]==len(c['word'])==cost
        assert inverse_word(438,F,c['word'])==target
    assert min(c['distances'][438] for c in z['exact_core_sizes'])==11>10
    edges+=bellman(z['unrestricted_distances'],F,lambda V:V.bit_count()>6)
    assert z['unrestricted_distances'][438]==len(z['unrestricted_word'])==9
    assert inverse_word(438,F,z['unrestricted_word'])==z['unrestricted_target']==877 and 877>>9&1
    return edges

def check_root_present(rows):
    seen={n:set() for n in range(3,8)};controls=0
    for a in rows:
        n=len(a);r=n-1;assert n in seen and tuple(a) not in seen[n];seen[n].add(tuple(a))
        assert all(type(p) is int and 0<=p<n for p in a)
        assert [a.count(p) for p in range(n)]==[0]+[1]*(n-2)+[2]
        b=list(range(1,r))+[0,r]
        for mask in range((1<<r)-1):
            U=mask|(1<<r);j=next(j for j in range(r) if not mask>>j&1)
            w=[0]+[1]*j;V=inverse_word(U,[a,b],w)
            assert V.bit_count()==U.bit_count()+1 and len(w)<=U.bit_count();controls+=1
    assert all(len(seen[n])==factorial(n)//2 for n in seen)
    assert len(rows)==2955 and controls==170913
    return controls

def check(data):
    parameters={(M,d) for M in range(6,10) for d in range(1,M) if gcd(M,d)>1 and M//gcd(M,d)>=3}
    seen={p:set() for p in parameters};extensions=particles=factors=multi=cheap_mixed=0;worst_num=0;worst_den=1
    for z in data['records']:
        M=z['M'];d=z['d'];assert (M,d) in parameters;g=gcd(M,d);L=M-d;full=(1<<M)-1;rest=[q for q in range(M) if q not in (0,L)]
        A=z['permutation'];assert sorted(A)==rest and tuple(A) not in seen[M,d];seen[M,d].add(tuple(A))
        a=list(range(M+1));a[M]=0;a[0]=a[L]=M
        for q,p in zip(rest,A):a[q]=p
        b=list(range(1,M))+[0,M];F=[a,b];c=[a[a[q]] for q in range(M+1)]
        assert c[M]==M and [sum(c[q]==p for q in range(M)) for p in range(M)]==[2 if p==0 else 0 if p==L else 1 for p in range(M)]
        expected={sum(1<<q for q in range(M) if pattern>>(q%g)&1) for pattern in range(1,(1<<g)-1)}
        controls=z['extensions'];assert len(controls)==len(expected) and {t[0] for t in controls}==expected
        lookup={}
        for U,w in controls:
            V=inverse_word(U,F,w);growth=V.bit_count()-U.bit_count()
            assert 0<U<full and V<full and growth>0 and V.bit_count()<=M-1 and len(w)<=(M+1)*growth
            lookup[U]=w;extensions+=1;multi+=growth>1;particles+=(M+1)*len(w)
            if len(w)*worst_den>worst_num*growth:worst_num,worst_den=len(w),growth
            if not U&1:
                X=preimage(U,a);assert X<full and X.bit_count()==U.bit_count()
                positive=[j for j in range(M) if X>>j&1 and not X>>((L+j)%M)&1]
                if positive:
                    assert len(positive)>=2 and positive[0]<=M-2
                    cheap=[0,0]+[1]*positive[0]+[0];W=inverse_word(U,F,cheap)
                    assert W<full and W.bit_count()==U.bit_count()+1 and len(cheap)<=M+1
                    cheap_mixed+=1;particles+=(M+1)*len(cheap)
        U=(1<<0)|(1<<L);suffix=[0];assert z['reset_factors'] and z['reset_factors'][0]==[0,0]+[1]*L
        for index,w in enumerate(z['reset_factors']):
            assert U.bit_count()<M-1;V=inverse_word(U,F,w);growth=V.bit_count()-U.bit_count()
            assert 0<V<full and growth>0 and len(w)<=(M+1)*growth and V.bit_count()<=M-1
            if index==0:assert growth==1 and len(w)==M-d+2
            elif U in lookup:assert w==lookup[U]
            else:
                assert w[:2]==[0,0] and all(i==1 for i in w[2:]) and len(w)<=M+1 and growth==1
                k=len(w)-2;assert U>>k&1 and not U>>((L+k)%M)&1
            U=V;suffix=w+suffix;factors+=1
        assert U.bit_count()==M-1 and len(suffix)<=1+(M-d+2)+(M-4)*(M+1)
        q=next(q for q in range(M) if not U>>q&1);k=(q-L)%M;p=next(q for q in rest if a[q]==2*L%M);j=(p-L)%M
        v=[0]+[1]*j+[0]+[1]*d+[0];assert set(images(F,v))==set(range(M))-{L}
        w=z['reset_word'];assert w==v+[1]*k+suffix and len(w)<=M*M and images(F,w)==[M]*(M+1)
        particles+=(M+1)*(len(v)+len(w))
    assert all(len(seen[M,d])==factorial(M-2) for M,d in parameters)
    assert len(data['records'])==11568 and extensions==63456 and multi>0
    root_controls=check_root_present(data['root_present_rows'])
    return dict(verified=True,inputs=11568,whole_coset_extensions=extensions,multiple_growth_witnesses=multi,
                compatible_chain_factors=factors,literal_particle_controls=particles,
                canonical_root_present_rows=2955,root_present_controls=root_controls,
                cheap_mixed_preimage_controls=cheap_mixed,
                max_retained_cost_growth_ratio=[worst_num,worst_den],boundary_bellman_edges=check_boundary(data['boundary']),
                status='COMPUTATIONALLY VERIFIED exact finite parameter/permutation cover M6..9, truncated proportional core extensions and compatible square resets; complete canonical rank-one n3..7 root-present controls and mixed-preimage branch. Boundary minimum core-staying positive extension11>n10, exact size7/8 minima11 and size9 minimum15; unrestricted minimum9. Root-present |S|-extension and cheap mixed-preimage lemmas, and conditional arbitrary-n square PROVED paper. Universal mixed-core truncated budget CONJECTURED/OPEN, general Cerny OPEN; not formal or a novelty claim.')

def main():
    data=json.loads((ROOT/'direct_attack/data/moving_root_truncated_budget.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(8):
        z=deepcopy(data['boundary'])
        if mode==0:z['U']=439
        if mode==1:z['rows'][0][1]=1
        if mode==2:z['exact_core_sizes'][0]['distances'][438]=10
        if mode==3:z['exact_core_sizes'][1]['word'].pop()
        if mode==4:z['exact_core_sizes'][2]['target']=447
        if mode==5:z['unrestricted_distances'][438]=8
        if mode==6:z['unrestricted_target']=438
        if mode==7:z['exact_core_sizes'].pop()
        try:check_boundary(z)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted boundary corruption',mode))
    for mode in [8,9]:
        z=dict(data);z['records']=list(data['records'])
        if mode==8:z['records'].append(z['records'][0])
        else:
            bad=deepcopy(z['records'][0]);bad['extensions'][0][1]=[];z['records'][0]=bad
        try:check(z)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted coverage corruption',mode))
    out['corruptions_rejected']=rejected
    (ROOT/'direct_attack/data/moving_root_truncated_budget_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
