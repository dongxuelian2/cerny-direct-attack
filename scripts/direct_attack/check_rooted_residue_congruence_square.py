"""Independent literal words, complete finite targets, and congruence certificates."""
from pathlib import Path
from math import gcd,factorial
import json
import copy
from .check_order_two_weighted_endpoints import model,particles

ROOT=Path(__file__).resolve().parents[2]


def least_period(d,mask):
    for p in range(1,d+1):
        if d%p==0 and all((mask>>q&1)==(mask>>((q+p)%d)&1) for q in range(d)):return p
    raise AssertionError('no period')


def invariant_check(a,p):
    M=len(a)-1;L=M//2;R=[q for q in range(M) if q not in(0,L)];power={q:q for q in R}
    parent={q:q for q in R}
    def find(q):
        while parent[q]!=q:q=parent[q]
        return q
    def join(x,y):parent[find(x)]=find(y)
    counts=[]
    for k in range(L-p+1):
        for j in range(1,L):
            x,y=power[j],power[j+L];assert x%p==y%p;join(x,y)
        counts.append(len({find(q) for q in R}))
        power={q:a[x] for q,x in power.items()}
    assert counts[0]==L-1 and all(c>=p for c in counts)
    stable=next(i for i in range(len(counts)-1) if counts[i]==counts[i+1])
    inv={a[q]:q for q in R}
    assert all(inv[j]%p==inv[j+L]%p for j in range(1,L))
    mixed=[j for j in range(1,L) if a[j]%L!=a[j+L]%L]
    assert len(mixed)>=2 and min(mixed)<=L-p-1
    return stable,counts


def check(data,deep=True):
    assert data['complete_M8']==672
    seen=set();stages=saved=forward=0;max_n=max_cost=0
    for i,z in enumerate(data['chains']):
        F=z['rows'];M,L=model(F);a,b=F;d=L
        for j in range(1,L):d=gcd(d,a[j]-a[j+L])
        assert d<L and d==z['d'] and z['bound']==M*M-L+d
        if i<672:
            assert M==8;signature=tuple(a[q] for q in range(M) if q not in(0,L));assert signature not in seen;seen.add(signature)
        S=1<<M;reset=[];count_saved=0
        assert len(z['stages'])==M
        for k,st in enumerate(z['stages']):
            assert st['source']==S and S>>M&1 and S.bit_count()==k+1
            U=S&(2**M-1);periodic=all((U>>q&1)==(U>>((q+d)%M)&1) for q in range(M))
            if st['kind']=='periodic':
                assert periodic and 0<U<2**M-1 and st['p']==least_period(d,U&(2**d-1))
            else:assert st['p']==0 and not st['fallback']
            image=particles(F,st['word']);T=sum(1<<q for q,x in enumerate(image) if S>>x&1)
            assert T==st['target'] and T>>M&1 and T.bit_count()==k+2 and len(st['word'])<=M
            save=k>0 and k%2==0 and not periodic
            assert st['saved_even']==save and (not save or len(st['word'])<=M-1)
            if k==2:assert S==(1<<M)|1|(1<<L)
            count_saved+=save;reset=st['word']+reset;S=T;stages+=1
        assert count_saved>=L-d and reset==z['reset_word'] and len(reset)<=z['bound']<M*M
        assert S==2**(M+1)-1 and particles(F,reset)==[M]*(M+1)
        saved+=count_saved;forward+=(M+1)*len(reset);max_n=max(max_n,M+1);max_cost=max(max_cost,len(reset))
    assert len(seen)==factorial(6)-2**3*factorial(3)
    targets=fallbacks=word_particles=stable_cases=0
    for z in data['periodic_models']:
        F=z['rows'];M,L=model(F);a,b=F;d=L
        for j in range(1,L):d=gcd(d,a[j]-a[j+L])
        assert d==z['d']<L and len(z['controls'])==2*(2**d-2)
        checked=set()
        for i,c in enumerate(z['controls']):
            mask,root=c['mask'],c['root'];assert mask==1+i//2 and type(root) is bool and root==bool(i%2)
            p=least_period(d,mask);assert c['p']==p and p<=L//2
            S=sum(1<<q for q in range(M) if mask>>(q%d)&1)|(int(root)<<M)
            image=particles(F,c['word']);T=sum(1<<q for q,x in enumerate(image) if S>>x&1)
            mass=lambda X:X.bit_count()+int(bool(X>>M&1))
            assert len(c['word'])<=M and mass(T)==mass(S)+1
            assert T>>M&1 and (not root or T.bit_count()==S.bit_count()+1)
            if c['fallback']:
                fallbacks+=1
                if deep and p not in checked:invariant_check(a,p);checked.add(p);stable_cases+=1
            else:assert len(c['word'])<=M-1
            targets+=1;word_particles+=(M+1)*len(c['word'])
    return dict(verified=True,chains=len(data['chains']),complete_M8=672,rooted_unit_stages=stages,
        saved_even_stages=saved,reset_forward_particles=forward,maximum_n=max_n,maximum_reset_cost=max_cost,
        complete_periodic_models=len(data['periodic_models']),complete_both_root_flag_targets=targets,
        periodic_forward_particles=word_particles,fallback_targets=fallbacks,distinct_partition_stabilization_checks=stable_cases,
        status='Finite controls COMPUTATIONALLY VERIFIED; all-n residue-congruence WEXT and square PROVED paper, not formal. General Cerny OPEN.')


def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/rooted_residue_congruence_square.json').read_text());out=check(data);rejected=[]
    for mode in range(6):
        bad=copy.deepcopy(data)
        if mode==0:bad['chains'][0]['stages'][0]['target']^=1
        if mode==1:bad['chains'][0]['bound']-=1
        if mode==2:bad['chains'][0]['reset_word'].pop()
        if mode==3:bad['periodic_models'][0]['controls'][0]['root']=True
        if mode==4:bad['periodic_models'][0]['controls'][0]['word']=[0]
        if mode==5:
            index=next(i for i,c in enumerate(bad['periodic_models'][0]['controls']) if c['p']>1)
            bad['periodic_models'][0]['controls'][index]['p']=1
        try:check(bad,False)
        except(AssertionError,ValueError,KeyError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected;print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
