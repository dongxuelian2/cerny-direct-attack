"""Independent full-cover and literal permuted-return compatibility audit."""
from collections import defaultdict
from copy import deepcopy
from math import factorial,gcd
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
    state=list(range(len(F[0])))
    for i in w:state=[F[i][q] for q in state]
    return state

def check(data):
    records=data['records'];assert len(records)==996
    complete=defaultdict(set);sampled=defaultdict(set);large=set();particles=extensions=nonunit=longprep=0
    for z in records:
        M=z['M'];d=z['d'];r=M;L=M-d;full=(1<<M)-1;F=z['rows'];assert M>=3 and 0<d<M and gcd(M,d)==1
        assert len(F)==2 and all(len(f)==M+1 and all(type(q) is int and 0<=q<=M for q in f) for f in F)
        a,b=F;rest=[q for q in range(M) if q not in (0,L)]
        assert a[r]==0 and a[0]==a[L]==r and sorted(a[q] for q in rest)==rest
        assert b==[(q+1)%M for q in range(M)]+[r]
        tail=tuple(a[q] for q in rest);key=(M,d)
        if z['mode']=='complete M3..7':assert 3<=M<=7 and tail not in complete[key];complete[key].add(tail)
        elif z['mode']=='four distinct deterministic samples per parameter':assert 8<=M<=14 and tail not in sampled[key];sampled[key].add(tail)
        else:
            assert z['mode']=='selected large arbitrary permutation' and M in (31,63,127,256) and d in {1,2,3,M-1} and key not in large;large.add(key)
        c=[a[a[q]] for q in range(M+1)];assert c[r]==r and c[0]==c[L]==0
        count=[c[:M].count(q) for q in range(M+1)];expected=[1]*M+[0];expected[0]+=1;expected[L]-=1;assert count==expected
        nonunit+=any(c[q]!=q for q in rest)
        p=next(q for q in rest if a[q]==2*L%M);j=(p-L)%M
        v=z['preparation'];assert v==[0]+[1]*j+[0]+[1]*d+[0] and len(v)<=M+d+2
        state=literal(F,v);particles+=(M+1)*len(v);assert set(state)==set(range(M))-{L}
        longprep+=len(v)>M+3
        masks=[h[0] for h in z['extensions']];assert len(masks)==len(set(masks))
        if M<=7:assert z['subset_scope']=='ALL proper core subsets' and set(masks)==set(range(1,full))
        else:assert z['subset_scope']=='64 retained proper core subsets' and len(masks)==64
        def extend(U,k):
            assert type(U) is int and 0<U<full and type(k) is int and 0<=k<M
            w=[0,0]+[1]*k;V=U
            for i in reversed(w):V=pull(V,F[i])
            assert V<=full and V.bit_count()==U.bit_count()+1;return V,w
        for U,k in z['extensions']:extend(U,k);extensions+=1
        U=pull(1<<r,a);assert U==(1<<0)|(1<<L);s=[0];factors=z['factor_exponents'];assert len(factors)==M-3
        if M>=4:assert factors[0]==L
        for k in factors:
            U,w=extend(U,k);s=w+s
        assert U.bit_count()==M-1 and s==z['reset_suffix']
        if M>=4:
            assert len(s)<=1+(M-d+2)+(M-4)*(M+1)
            assert (M+d+2)+(M-1)+1+(M-d+2)+(M-4)*(M+1)==M*M
        else:assert s==[0] and len(v)==M+3
        q=next(q for q in range(M) if not U>>q&1);k=z['alignment'];assert type(k) is int and k==(q-L)%M
        word=z['reset_word'];assert word==v+[1]*k+s and len(word)<=M*M
        state=literal(F,word);particles+=(M+1)*len(word);assert state==[r]*(M+1)
    small={(M,d) for M in range(3,8) for d in range(1,M) if gcd(M,d)==1}
    mid={(M,d) for M in range(8,15) for d in range(1,M) if gcd(M,d)==1}
    big={(M,d) for M in (31,63,127,256) for d in {1,2,3,M-1} if gcd(M,d)==1}
    assert set(complete)==small and all(len(v)==factorial(M-2) for (M,d),v in complete.items())
    assert set(sampled)==mid and all(len(v)==4 for v in sampled.values()) and large==big
    assert nonunit>0 and longprep>0
    return dict(verified=True,inputs=len(records),complete_core_permutation_inputs=sum(map(len,complete.values())),sampled_core_inputs=sum(map(len,sampled.values())),large_inputs=len(large),
                nonunit_squared_returns=nonunit,longer_than_n_plus_two_preparations=longprep,proper_core_extensions=extensions,literal_particle_controls=particles,
                boundary='Independent exact factorial ALL remaining-core permutations/coprime d M3..7, four distinct deterministic samples each M8..14, selected large controls. Literal a^2 is permitted to permute remaining points; variable preparation, forced first growth saving, compatible square and all particles checked. No generator/solver imports. PROVED paper arbitrary-n class, finite COMPUTATIONALLY VERIFIED only, not formal/novel/general Cerny; broader noncoprime case OPEN here.')

def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/moving_root_core_permutations.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(10):
        bad=deepcopy(data);z=bad['records'][2]
        if mode==0:bad['records'].pop(0)
        if mode==1:z['rows'][0][0]=0
        if mode==2:z['preparation'].append(1)
        if mode==3:z['factor_exponents'][0]=0
        if mode==4:z['alignment']=(z['alignment']+1)%z['M']
        if mode==5:z['reset_suffix'].append(1)
        if mode==6:z['extensions'].pop()
        if mode==7:z['extensions'][0][1]=z['M']
        if mode==8:bad['records'][0]=deepcopy(bad['records'][1])
        if mode==9:z['mode']='sampled'
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError('accepted corruption '+str(mode))
    out['corruptions_rejected']=rejected
    (ROOT/'scripts/direct_attack/data/moving_root_core_permutations_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
