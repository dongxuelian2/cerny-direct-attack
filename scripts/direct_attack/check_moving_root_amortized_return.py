"""Independent literal core/full counts and growth-weighted compatibility."""
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
    parameters={(M,d) for M in range(3,41) for d in range(1,M) if 1<gcd(M,d) and M//gcd(M,d)>=3}
    parameters|={(60,20),(63,3),(63,21),(255,85),(256,2),(256,64),(300,100)}
    records=data['records'];assert len(records)==len(parameters) and {(z['M'],z['d']) for z in records}==parameters
    particles=extensions=two_subset=one_chain=two_chain=0
    for z in records:
        M=z['M'];d=z['d'];r=M;L=M-d;g=gcd(M,d);t=M//g;full=(1<<M)-1;F=z['rows'];assert g>1 and t>=3
        assert len(F)==2 and all(len(f)==M+1 and all(type(q) is int and 0<=q<=M for q in f) for f in F)
        for q in range(M+1):
            assert F[0][q]==(0 if q==r else r if q in (0,L) else q)
            assert F[1][q]==(r if q==r else (q+1)%M)
        v=z['avoidance_word'];R=z['return_word'];assert v==[0]+[1]*L+[0]+[1]*d+[0] and R==[0,1]+v
        T=literal(F,v);A=literal(F,R);particles+=(M+1)*(len(v)+len(R))
        assert T[r]==0 and set(T)==set(range(M))-{L}
        for q in range(M):assert T[q]==(d if q in (0,L) else 0 if q==d else q)
        assert A[r]==1 and set(A)<=set(range(M))
        core=[A[:M].count(q)-(1 if q<M else 0) for q in range(M+1)]
        expected=[0]*(M+1)
        for q,delta in [(0,2),(d,1),(L,-1),(1,-1),(L+1,-1)]:expected[q]+=delta
        assert core==expected
        total=[A.count(q)-1 for q in range(M+1)];expected[1]+=1;expected[r]-=1;assert total==expected
        def verify_extension(U,h):
            nonlocal extensions,two_subset
            w=h['word'];growth=h['growth'];mode=h['mode'];assert type(growth) is int and growth in (1,2)
            assert 0<U<full and len(w)<=(M+1)*growth
            if growth==1:
                assert mode=='unit' and w[:2]==[0,0] and all(i==1 for i in w[2:]) and len(w)<=M+1
            else:
                assert mode=='two-point return' and w[:len(R)]==R and all(i==1 for i in w[len(R):])
                assert len(w)-len(R)<g and len(w)<=M+g+4<=2*(M+1)
                assert all((U>>q&1)==(U>>((q+d)%M)&1) for q in range(M))
                j=len(w)-len(R);assert U>>j&1 and not U>>((j+1)%g)&1
                assert M-U.bit_count()>=t>=3;two_subset+=1
            V=U
            for i in reversed(w):V=pull(V,F[i])
            assert V<=full and V.bit_count()==U.bit_count()+growth;extensions+=1;return V
        masks=[h['U'] for h in z['extensions']];assert len(masks)==len(set(masks))
        if M<=10:assert z['subset_scope']=='ALL proper core subsets' and set(masks)==set(range(1,full))
        else:
            assert z['subset_scope']=='64 retained proper core subsets including a whole coset' and len(masks)==64
            assert sum(1<<q for q in range(M) if q%g==0) in masks
        for h in z['extensions']:verify_extension(h['U'],h)
        U=pull(1<<r,F[0]);assert U==(1<<0)|(1<<L);s=[0];gain=cost=0
        for h in z['reset_factors']:
            assert U.bit_count()<M-1;V=verify_extension(U,h);assert V.bit_count()<=M-1;U=V
            gain+=h['growth'];cost+=len(h['word']);s=h['word']+s
            one_chain+=h['growth']==1;two_chain+=h['growth']==2
        assert gain==M-3 and cost<=(M+1)*gain and U.bit_count()==M-1
        assert s==z['reset_suffix'] and len(s)==cost+1
        p=next(q for q in range(M) if not U>>q&1);k=z['alignment'];assert type(k) is int and k==(p-L)%M
        w=z['reset_word'];assert w==v+[1]*k+s and len(w)<=M*M
        state=literal(F,w);particles+=(M+1)*len(w);assert state==[r]*(M+1)
    assert two_chain>0 and two_subset>0
    return dict(verified=True,inputs=len(records),core_extension_controls=extensions,two_point_controls=two_subset,
                one_point_chain_factors=one_chain,two_point_chain_factors=two_chain,literal_particle_controls=particles,
                boundary='Independent ALL noncoprime SYNC parameter pairs M3..40 plus seven large controls; literal core/full row defects, original-r endpoint, two proportional-budget branches, exact compatible growth sum/word/rotation/reset. No generator/solver/preceding checker imports. PROVED paper all-sync-family square, finite controls COMPUTATIONALLY VERIFIED; not formal, novel or a general Cerny proof.')

def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/moving_root_amortized_return.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(10):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:bad['records'].pop()
        if mode==1:z['return_word'].pop(1)
        if mode==2:z['rows'][0][z['M']]=1
        if mode==3:z['avoidance_word'].append(1)
        if mode==4:next(h for h in z['extensions'] if h['growth']==2)['growth']=1
        if mode==5:next(h for h in z['extensions'] if h['growth']==2)['word'].append(0)
        if mode==6:z['reset_suffix'].append(1)
        if mode==7:z['alignment']=(z['alignment']+1)%z['M']
        if mode==8:z['extensions'].pop()
        if mode==9:z['reset_factors'].pop()
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError('accepted corruption '+str(mode))
    out['corruptions_rejected']=rejected
    (ROOT/'scripts/direct_attack/data/moving_root_amortized_return_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
