"""Independent NEW tail-order coverage and original reset/extension checks."""
from pathlib import Path
from math import gcd,factorial
import json
import copy
from .check_order_two_weighted_endpoints import particles
from .check_rooted_residue_congruence_square import least_period
from .check_paired_root_cycle_square import partition,parameters

ROOT=Path(__file__).resolve().parents[2]


def model(F):
    a,b=F;M=len(a)-1;L=M//2;assert M%2==0 and a[M]==0 and b==list(range(1,M))+[0,M]
    V=[];x=0
    while x!=M:assert x not in V;V.append(x);x=a[x]
    W=[];x=L
    while x!=M:assert x not in W;W.append(x);x=a[x]
    labels={x%L for x in V};assert V[0]==0 and len(labels)==len(V)
    assert len(W)==len(V) and set(W)=={(x+L)%M for x in V} and W[0]==L and W[-1]==(V[-1]+L)%M
    assert W!=[(x+L)%M for x in V]
    R=[q for q in range(M) if q%L not in labels];assert sorted(a[q] for q in R)==R
    assert any(a[j]%L!=a[j+L]%L for j in R if j<L)
    assert sorted(a)==sorted([M,M,0]+[q for q in range(M) if q not in(0,L)])
    d=L
    for j in range(L):d=gcd(d,a[j]-a[j+L])
    assert d<L and len(V)<=L-2
    return M,L,V,W,R,d


def early(V,W,p):return any((x-y)%p for x,y in zip(V,W))


def early_word_check(V,W,p,w):
    i=next(i for i,(x,y) in enumerate(zip(V,W)) if (x-y)%p)
    assert w[:i+1]==[0]*(i+1) and all(c==1 for c in w[i+1:]) and len(w)-(i+1)<p
    assert len(w)<=len(V)+p-1


def check(data,deep=True):
    seen=set();stages=saved=forward=early_stages=0;max_n=max_tau=0
    for z in data['chains']:
        F=z['rows'];M,L,V,W,R,d=model(F);assert V==z['V'] and W==z['W'] and d==z['d'] and z['bound']==M*M-L+d
        if z['scope']=='complete_NEW_M12_tau5_permuted_shadow':
            assert M==12 and len(V)==4 and W==[(V[i]+L)%M for i in(0,2,1,3)]
            row=tuple(F[0]);assert row not in seen;seen.add(row)
        S=1<<M;reset=[];nsave=0;assert len(z['stages'])==M
        for k,st in enumerate(z['stages']):
            assert st['source']==S and S>>M&1 and S.bit_count()==k+1
            U=S&(2**M-1);periodic=all((U>>q&1)==(U>>((q+d)%M)&1) for q in range(M))
            if st['kind']=='periodic':
                p=least_period(d,U&(2**d-1));p0,K=parameters(L,V,R,p)
                assert (st['p'],st['p0'],st['K'])==(p,p0,K) and st['early_shadow']==early(V,W,p)
                if st['early_shadow']:early_word_check(V,W,p,st['word']);assert not st['fallback'];early_stages+=1
            else:assert st['p']==st['p0']==st['K']==0 and not st['fallback'] and not st['early_shadow']
            img=particles(F,st['word']);T=sum(1<<q for q,x in enumerate(img) if S>>x&1)
            assert T==st['target'] and T>>M&1 and T.bit_count()==k+2 and len(st['word'])<=M
            save=k>0 and k%2==0 and not periodic;assert st['saved']==save and (not save or len(st['word'])<=M-1)
            nsave+=save;stages+=1;reset=st['word']+reset;S=T
        assert nsave>=L-d and S==2**(M+1)-1 and reset==z['reset_word'] and len(reset)<=z['bound']
        assert particles(F,reset)==[M]*(M+1);saved+=nsave;forward+=(M+1)*len(reset)
        max_n=max(max_n,M+1);max_tau=max(max_tau,len(V)+1)
    expected=(factorial(5)//factorial(2))*2**3*(factorial(4)-2**2*factorial(2))*(factorial(2)-1)
    assert len(seen)==expected==7680
    targets=target_particles=early_targets=fall=direct=partitions=0
    for z in data['periodic_models']:
        F=z['rows'];M,L,V,W,R,d=model(F);assert z['V']==V and z['W']==W and z['d']==d
        sig=set();checked=set()
        for c in z['targets']:
            mask,root=c['mask'],c['root'];assert 0<mask<2**d-1 and type(root) is bool and (mask,root) not in sig;sig.add((mask,root))
            p=least_period(d,mask);p0,K=parameters(L,V,R,p);assert (c['p'],c['p0'],c['K'])==(p,p0,K)
            assert c['early_shadow']==early(V,W,p)
            if c['early_shadow']:early_word_check(V,W,p,c['word']);assert not c['fallback'];early_targets+=1
            elif c['fallback']:
                fall+=1
                if deep and p not in checked:partition(F[0],R,p);checked.add(p);partitions+=1
            else:direct+=1
            S=sum(1<<q for q in range(M) if mask>>(q%d)&1)|(int(root)<<M)
            img=particles(F,c['word']);T=sum(1<<q for q,x in enumerate(img) if S>>x&1)
            mass=lambda X:X.bit_count()+int(bool(X>>M&1))
            assert len(c['word'])<=M and mass(T)==mass(S)+1 and T>>M&1
            if root:assert T.bit_count()==S.bit_count()+1
            targets+=1;target_particles+=(M+1)*len(c['word'])
        if z['scope']=='complete':assert sig=={(mask,flag) for mask in range(1,2**d-1) for flag in(False,True)}
        else:assert z['scope']=='named'
    return dict(verified=True,chains=len(data['chains']),complete_NEW=len(seen),root_retaining_unit_stages=stages,
        saved_even_stages=saved,reset_forward_particles=forward,maximum_n=max_n,maximum_root_cycle=max_tau,
        early_shadow_chain_stages=early_stages,periodic_targets=targets,periodic_forward_particles=target_particles,
        early_shadow_targets=early_targets,direct_core_targets=direct,root_fallback_targets=fall,distinct_partition_checks=partitions,
        status='Finite NEW permuted-shadow controls COMPUTATIONALLY VERIFIED; all-n square/WEXT with MIXED remaining A PROVED paper, not formal. General Cerny OPEN.')


def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/permuted_shadow_square.json').read_text());out=check(data);rejected=[]
    for mode in range(6):
        bad=copy.deepcopy(data)
        if mode==0:bad['chains'].pop(0)
        if mode==1:bad['chains'][1]=copy.deepcopy(bad['chains'][0])
        if mode==2:bad['chains'][0]['stages'][0]['target']^=1
        if mode==3:bad['chains'][0]['reset_word'].pop()
        if mode==4:bad['periodic_models'][1]['targets'][0]['early_shadow']=False
        if mode==5:bad['periodic_models'][0]['targets'][0]['word']=[0]
        try:check(bad,False)
        except(AssertionError,ValueError,KeyError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected;print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
