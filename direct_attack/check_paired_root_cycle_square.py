"""Independent paired model, combinatorial complete coverage and literal chains."""
from pathlib import Path
from math import gcd,factorial
import json
import copy
from .check_order_two_weighted_endpoints import particles
from .check_rooted_residue_congruence_square import least_period

ROOT=Path(__file__).resolve().parents[1]


def model(F):
    a,b=F;M=len(a)-1;L=M//2;assert M%2==0 and M>=6 and a[M]==0
    assert b==list(range(1,M))+[0,M]
    V=[];x=0
    while x!=M:assert x not in V;V.append(x);x=a[x]
    labels={x%L for x in V};assert V[0]==0 and len(labels)==len(V)
    for x in V:
        y=a[x];assert a[(x+L)%M]==(y+L)%M if y<M else a[(x+L)%M]==M
    R=[q for q in range(M) if q%L not in labels];assert sorted(a[q] for q in R)==R
    assert sorted(a)==sorted([M,M,0]+[q for q in range(M) if q not in(0,L)])
    d=L
    for j in range(L):d=gcd(d,a[j]-a[j+L])
    assert d<L;return M,L,V,R,d


def partition(a,R,p):
    M=len(a)-1;L=M//2;J=[j for j in R if j<L];B=len(J);p0=len({x%p for x in R});K=B-p0+1
    parent={q:q for q in R};power={q:q for q in R};counts=[]
    def find(q):
        while parent[q]!=q:q=parent[q]
        return q
    for k in range(K+1):
        for j in J:
            x,y=power[j],power[j+L];assert x%p==y%p;parent[find(x)]=find(y)
        counts.append(len({find(q) for q in R}));power={q:a[x] for q,x in power.items()}
    assert counts[0]==B and all(c>=p0 for c in counts) and any(x==y for x,y in zip(counts,counts[1:]))
    inv={a[q]:q for q in R};assert all(inv[j]%p==inv[j+L]%p for j in J)
    mixed=[j for j in J if a[j]%L!=a[j+L]%L];assert min(mixed)<=L-p-1


def parameters(L,V,R,p):
    p0=len({q%p for q in R});B=len(R)//2;K=B-p0+1
    assert p0>=p-(len(V)//(L//p)) and p-p0<=len(V)
    assert L-1+K+p-1+1<=2*L
    return p0,K


def check(data,deep=True):
    signatures={};stages=saved=forward=0;max_n=max_tau=0
    for z in data['chains']:
        F=z['rows'];M,L,V,R,d=model(F);assert V==z['V'] and d==z['d'] and z['bound']==M*M-L+d
        if z['scope']=='complete_NEW_paired_M8_M10_tau>=3':
            tau=len(V)+1;assert L in(4,5) and 3<=tau<L
            seen=signatures.setdefault((L,tau),set());row=tuple(F[0]);assert row not in seen;seen.add(row)
        S=1<<M;reset=[];nsave=0;assert len(z['stages'])==M
        for k,st in enumerate(z['stages']):
            assert st['source']==S and S>>M&1 and S.bit_count()==k+1
            U=S&(2**M-1);periodic=all((U>>q&1)==(U>>((q+d)%M)&1) for q in range(M))
            if st['kind']=='periodic':
                p=least_period(d,U&(2**d-1));p0,K=parameters(L,V,R,p)
                assert (st['p'],st['p0'],st['K'])==(p,p0,K)
            else:assert st['p']==st['p0']==st['K']==0 and not st['fallback']
            img=particles(F,st['word']);T=sum(1<<q for q,x in enumerate(img) if S>>x&1)
            assert T==st['target'] and T>>M&1 and T.bit_count()==k+2 and len(st['word'])<=M
            save=k>0 and k%2==0 and not periodic;assert st['saved']==save and (not save or len(st['word'])<=M-1)
            nsave+=save;stages+=1;reset=st['word']+reset;S=T
        assert nsave>=L-d and S==2**(M+1)-1 and reset==z['reset_word'] and len(reset)<=z['bound']
        assert particles(F,reset)==[M]*(M+1);saved+=nsave;forward+=(M+1)*len(reset)
        max_n=max(max_n,M+1);max_tau=max(max_tau,len(V)+1)
    expected={(L,tau):(factorial(L-1)//factorial(L-tau+1))*2**(tau-2)*
        (factorial(2*(L-tau+1))-2**(L-tau+1)*factorial(L-tau+1))
        for L in(4,5) for tau in range(3,L)}
    assert set(signatures)==set(expected) and all(len(signatures[k])==v for k,v in expected.items())
    targets=fallbacks=target_particles=missing_classes=partitions=0
    for z in data['periodic_models']:
        F=z['rows'];M,L,V,R,d=model(F);assert z['V']==V and z['d']==d
        seen=set();checked=set()
        for c in z['targets']:
            mask,root=c['mask'],c['root'];assert 0<mask<2**d-1 and type(root) is bool and (mask,root) not in seen;seen.add((mask,root))
            p=least_period(d,mask);p0,K=parameters(L,V,R,p);assert (c['p'],c['p0'],c['K'])==(p,p0,K)
            S=sum(1<<q for q in range(M) if mask>>(q%d)&1)|(int(root)<<M)
            img=particles(F,c['word']);T=sum(1<<q for q,x in enumerate(img) if S>>x&1)
            mass=lambda X:X.bit_count()+int(bool(X>>M&1))
            assert len(c['word'])<=M and mass(T)==mass(S)+1 and T>>M&1
            if root:assert T.bit_count()==S.bit_count()+1
            if c['fallback']:
                fallbacks+=1
                if deep and p not in checked:partition(F[0],R,p);checked.add(p);partitions+=1
            targets+=1;target_particles+=(M+1)*len(c['word']);missing_classes+=p0<p
        if z['scope']=='complete':assert seen=={(mask,flag) for mask in range(1,2**d-1) for flag in(False,True)}
        else:assert z['scope']=='named'
    return dict(verified=True,chains=len(data['chains']),complete_NEW=sum(expected.values()),complete_by_L_tau={str(k):v for k,v in expected.items()},
        root_retaining_unit_stages=stages,saved_even_stages=saved,reset_forward_particles=forward,maximum_n=max_n,maximum_root_cycle=max_tau,
        periodic_targets=targets,periodic_forward_particles=target_particles,fallback_targets=fallbacks,missing_residue_class_targets=missing_classes,
        distinct_partition_checks=partitions,status='Finite controls COMPUTATIONALLY VERIFIED; all-n paired-root-cycle square/WEXT PROVED paper, not formal. General Cerny OPEN.')


def main():
    data=json.loads((ROOT/'direct_attack/data/paired_root_cycle_square.json').read_text());out=check(data);rejected=[]
    for mode in range(6):
        bad=copy.deepcopy(data)
        if mode==0:bad['chains'].pop(0)
        if mode==1:bad['chains'][1]=copy.deepcopy(bad['chains'][0])
        if mode==2:bad['chains'][0]['stages'][0]['target']^=1
        if mode==3:bad['chains'][0]['reset_word'].pop()
        if mode==4:bad['periodic_models'][0]['targets'][0]['p0']+=1
        if mode==5:bad['periodic_models'][0]['targets'][0]['word']=[0]
        try:check(bad,False)
        except(AssertionError,ValueError,KeyError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected;print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
