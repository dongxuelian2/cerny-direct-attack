"""Independent arbitrary-tail primitive coverage and actual compatible words."""
from pathlib import Path
from math import gcd,factorial
import json
import copy
from .check_order_two_weighted_endpoints import particles

ROOT=Path(__file__).resolve().parents[2]


def model(F):
    a,b=F;M=len(a)-1;L=M//2;K=[q for q in range(M) if a[q]==M]
    assert M>=6 and M%2==0 and a[M]==0 and b==list(range(1,M))+[0,M]
    assert len(K)==2 and K[1]==K[0]+L and sorted(a[q] for q in range(M) if q not in K)==[q for q in range(M) if q not in(0,L)]
    d=L
    for j in range(L):d=gcd(d,a[j]-a[j+L])
    assert d==1;return M,L,K


def new_scope(a):
    M=len(a)-1;L=M//2;cycle=[M];x=a[M]
    while x!=M:assert x not in cycle;cycle.append(x);x=a[x]
    tail=[L]
    while tail[-1]!=M:assert a[tail[-1]] not in tail;tail.append(a[tail[-1]])
    return len(tail)-1<len(cycle) and tail[:-1]!=[(x+L)%M for x in cycle[1:]]


def expected():
    out=set()
    for M in(6,8):
        L=M//2
        for H in range(1,L):
            R=[q for q in range(M) if q not in(H,H+L)];O=[q for q in range(M) if q not in(0,L)]
            for rank in range(factorial(M-2)):
                rem=O[:];a=[0]*(M+1);a[H]=a[H+L]=M;index=rank
                for i,q in enumerate(R):
                    f=factorial(len(R)-1-i);digit,index=divmod(index,f);a[q]=rem.pop(digit)
                d=L
                for j in range(L):d=gcd(d,a[j]-a[j+L])
                if d==1 and new_scope(a):out.add(tuple(a))
    return out


def check(data,coverage=True):
    seen=set();stages=save=forward=0;max_n=0
    for z in data['chains']:
        F=z['rows'];M,L,K=model(F);assert z['bound']==M*M-L+1
        if z['scope']=='complete_NEW_d1_unpaired_short_M6_M8':
            assert M in(6,8) and K[0]>0 and new_scope(F[0]);row=tuple(F[0]);assert row not in seen;seen.add(row)
        S=1<<M;reset=[];nsaved=0;assert len(z['stages'])==M
        for k,st in enumerate(z['stages']):
            assert st['source']==S and S>>M&1 and S.bit_count()==k+1
            img=particles(F,st['word']);T=sum(1<<q for q,x in enumerate(img) if S>>x&1)
            assert T==st['target'] and T>>M&1 and T.bit_count()==k+2 and len(st['word'])<=M
            if k>0 and k%2==0:assert len(st['word'])<=M-1;nsaved+=1
            reset=st['word']+reset;S=T;stages+=1
        assert nsaved==L-1 and S==2**(M+1)-1 and reset==z['reset_word'] and len(reset)<=z['bound']
        assert particles(F,reset)==[M]*(M+1);save+=nsaved;forward+=(M+1)*len(reset);max_n=max(max_n,M+1)
        for direction,key in ((1,'positive_endpoint'),(-1,'negative_endpoint')):
            word=z[key];img=particles(F,word);pre=sum(1<<q for q,x in enumerate(img) if x==M)
            mass=pre.bit_count()+int(bool(pre>>M&1));assert mass==2+direction and len(word)<=M
            assert bool(img[M]==M)==(direction==1)
    if coverage:assert seen==expected()
    targets=wordparticles=0
    for z in data['whole_models']:
        F=z['rows'];M,L,K=model(F);sig=set();assert len(z['targets'])==2*(2**L-2)
        for c in z['targets']:
            mask,root=c['mask'],c['root'];assert 0<mask<2**L-1 and type(root) is bool and (mask,root) not in sig;sig.add((mask,root))
            S=(mask|(mask<<L))|(int(root)<<M);img=particles(F,c['word']);T=sum(1<<q for q,x in enumerate(img) if S>>x&1)
            mass=lambda X:X.bit_count()+int(bool(X>>M&1))
            assert mass(T)==mass(S)+1 and T>>M&1 and len(c['word'])<=M-1
            if root:assert T.bit_count()==S.bit_count()+1
            targets+=1;wordparticles+=(M+1)*len(c['word'])
        assert sig=={(mask,root) for mask in range(1,2**L-1) for root in(False,True)}
    return dict(verified=True,chains=len(data['chains']),complete_NEW=len(seen),root_retaining_unit_stages=stages,
        saved_even_stages=save,reset_forward_particles=forward,maximum_n=max_n,complete_both_root_flag_whole_targets=targets,
        whole_word_particles=wordparticles,
        status='Finite NEW arbitrary-tail primitive controls COMPUTATIONALLY VERIFIED; ALL-n d1 and ALL prime half-core L synchronizing opposite-kernel binary inputs PROVED paper. Not formal; general Cerny OPEN.')


def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/opposite_kernel_primitive_square.json').read_text());out=check(data);rejected=[]
    for mode in range(7):
        bad=copy.deepcopy(data)
        if mode==0:bad['chains'].pop(0)
        if mode==1:bad['chains'][1]=copy.deepcopy(bad['chains'][0])
        if mode==2:bad['chains'][0]['stages'][0]['target']^=1
        if mode==3:bad['chains'][0]['bound']-=1
        if mode==4:bad['chains'][0]['reset_word'].pop()
        if mode==5:bad['chains'][0]['negative_endpoint']=bad['chains'][0]['positive_endpoint']
        if mode==6:bad['whole_models'][0]['targets'][0]['word']=[0]
        try:check(bad,mode==0)
        except(AssertionError,ValueError,KeyError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected;print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
