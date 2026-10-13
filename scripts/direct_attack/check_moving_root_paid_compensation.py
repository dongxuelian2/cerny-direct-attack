"""Independent literal paid words, pair/avoidance Bellman and weight audit."""
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

def image(U,f):
    V=0
    for q,p in enumerate(f):
        if U>>q&1:V|=1<<p
    return V

def literal(rows,word):
    n=len(rows[0]);states=list(range(n))
    assert all(type(i) is int and 0<=i<len(rows) for i in word)
    for i in word:states=[rows[i][q] for q in states]
    counts=[0]*n
    for q in states:counts[q]+=1
    return states,counts,n*len(word)

def check(data):
    parameters={(M,d) for M in range(3,21) for d in range(1,M)}
    for M in (31,63,127,256):parameters|={(M,d) for d in {1,2,3,M-2,M-1,M//2}}
    records=data['records'];assert len(records)==len(parameters)==213
    assert {(z['M'],z['d']) for z in records}==parameters
    particles=pair_edges=avoid_edges=extensions=sync=coprime=quotients=0
    for z in records:
        M=z['M'];d=z['d'];L=M-d;r=M;n=M+1;g=gcd(M,d);t=M//g;rows=z['rows']
        assert len(rows)==2 and all(len(f)==n and all(type(q) is int and 0<=q<n for q in f) for f in rows)
        a,b=rows
        for q in range(n):
            assert a[q]==(0 if q==r else r if q in (0,L) else q)
            assert b[q]==(r if q==r else (q+1)%M)
        assert len(set(a))==M and sorted(b)==list(range(n))
        D=z['pair_distances'];assert len(D)==n*n
        for x in range(n):
            for y in range(n):
                v=D[n*x+y];assert v is None or type(v) is int and v>=0
                if x==y:assert v==0;continue
                candidates=[D[n*f[x]+f[y]] for f in rows];finite=[u for u in candidates if u is not None]
                assert v==(1+min(finite) if finite else None);pair_edges+=2
        assert all(v is not None for v in D)==(t>=3)
        if M<=9:
            A=z['avoidance_distances'];assert len(A)==1<<n
            for U,v in enumerate(A):
                assert v is None or type(v) is int and v>=0
                if not U>>r&1:assert v==0;continue
                finite=[A[image(U,f)] for f in rows if A[image(U,f)] is not None]
                assert v==(1+min(finite) if finite else None);avoid_edges+=2
            assert A[-1]==(M+3 if t>=3 else None)
        else:assert 'avoidance_distances' not in z
        if t==2:
            Q=z['quotient'];assert Q==[q%g for q in range(M)]+[g];assert g+1>=2
            for f in rows:
                targets=[]
                for c in range(g+1):
                    V={Q[f[q]] for q in range(n) if Q[q]==c};assert len(V)==1;targets.append(next(iter(V)))
                assert sorted(targets)==list(range(g+1))
            assert 'avoidance_word' not in z and 'reset_word' not in z;quotients+=1;continue
        sync+=1
        v=z['avoidance_word'];assert v==[0]+[1]*L+[0]+[1]*d+[0] and len(v)==n+2
        state,c,cost=literal(rows,v);particles+=cost
        assert set(state)==set(range(M))-{L}
        expected=[1]*n;expected[r]-=1;expected[L]-=1;expected[0]+=1;expected[d]+=1;assert c==expected
        alpha=z['balancing_alpha'];assert alpha==1
        defect=[a.count(q)-1 for q in range(n)];assert defect[r]==1 and defect[L]==-1
        support=z['balancing_support'];assert len(support)==t
        assert support[0]==dict(word=v,beta=1)
        for i,h in enumerate(support):
            w=h['word'];beta=h['beta'];assert type(beta) is int and beta>0
            if i:
                j=i*d%M;assert w==[0,0]+[1]*j and beta==(1 if i==1 else 2)
            assert w[0]==0 and len(w)<=n+2
            _,c,cost=literal(rows,w);particles+=cost
            if i:
                expected=[1]*n;expected[j]+=1;expected[(j-d)%M]-=1;assert c==expected
            defect=[x+beta*(y-1) for x,y in zip(defect,c)]
        assert defect==[0]*n
        if g!=1:assert 'reset_word' not in z;continue
        coprime+=1
        witnesses=z['extensions'];masks=[h['U'] for h in witnesses];full=(1<<M)-1
        assert len(masks)==len(set(masks)) and all(type(U) is int and 0<U<full for U in masks)
        if M<=10:assert z['subset_scope']=='ALL proper core subsets' and set(masks)==set(range(1,full))
        else:assert z['subset_scope']=='64 retained proper core subsets' and len(masks)==64
        for h in witnesses:
            U=h['U'];w=h['word'];assert len(w)<=M+1 and w[:2]==[0,0] and all(i==1 for i in w[2:])
            V=U
            for i in reversed(w):V=pull(V,rows[i])
            assert V.bit_count()==U.bit_count()+1 and V<=full;extensions+=1
        factors=z['reset_factors'];assert len(factors)==M-3
        U=pull(1<<r,a);s=[0];assert U==(1<<0)|(1<<L)
        for w in factors:
            assert w[:2]==[0,0] and len(w)<=M+1 and all(i==1 for i in w[2:])
            V=U
            for i in reversed(w):V=pull(V,rows[i])
            assert V.bit_count()==U.bit_count()+1 and V<=full;U=V;s=w+s
        assert U.bit_count()==M-1 and s==z['reset_suffix'] and len(s)<=1+(M-3)*(M+1)
        p=next(q for q in range(M) if not U>>q&1);k=z['alignment'];assert type(k) is int and k==(p-L)%M
        word=z['reset_word'];assert word==v+[1]*k+s and len(word)<=M*M
        result,_,cost=literal(rows,word);particles+=cost;assert result==[r]*n
    return dict(verified=True,inputs=len(records),SYNC=sync,permutation_quotients=quotients,coprime_square_inputs=coprime,
                proper_core_extensions=extensions,pair_bellman_edges=pair_edges,avoidance_bellman_edges=avoid_edges,literal_particle_controls=particles,
                boundary='Independent213 parameter inputs: ALL d at M3..20 plus selected31/63/127/256; positive-original-a exact integer balance, literal avoid word, complete pair and small avoidance Bellman, order-two permutation quotient, complete small/64 large proper-core extensions and ONE paid compatible square on coprime inputs. Generator/solver not imported. ALLn math is PROVED paper, not formal; noncoprime family square/general Cerny OPEN here. No weaker-stationarity/cost conflation or novelty claim.')

def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/moving_root_paid_compensation.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(12):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:bad['records'].pop()
        if mode==1:z['rows'][0][0]=0
        if mode==2:z['balancing_alpha']=0
        if mode==3:z['avoidance_word'].pop(1)
        if mode==4:z['balancing_support'][1]['beta']=2
        if mode==5:z['extensions'][0]['word'].pop()
        if mode==6:z['alignment']=(z['alignment']+1)%z['M']
        if mode==7:z['reset_suffix'].append(1)
        if mode==8:z['avoidance_distances'][-1]=z['M']+2
        if mode==9:z['pair_distances'][0]=1
        if mode==10:next(h for h in bad['records'] if 'quotient' in h)['quotient'][0]=1
        if mode==11:z['extensions'].pop()
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError('accepted corruption '+str(mode))
    out['corruptions_rejected']=rejected
    (ROOT/'scripts/direct_attack/data/moving_root_paid_compensation_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
