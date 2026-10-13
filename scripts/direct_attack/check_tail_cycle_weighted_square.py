"""Independent factoradic coverage, root preimages and original words."""
from pathlib import Path
from math import factorial,gcd
import json
import copy

ROOT=Path(__file__).resolve().parents[2]


def decomposition(a,L):
    M=len(a)-1;cycle=[M];x=a[M]
    while x!=M:assert x not in cycle;cycle.append(x);x=a[x]
    tail=[L]
    while tail[-1]!=M:assert a[tail[-1]] not in tail;tail.append(a[tail[-1]])
    return cycle,tail


def expected_rows():
    expected=set()
    for M in range(3,9):
        for L in range(1,M):
            g=gcd(M,L)
            if g<=2:continue
            for u in range(M):
                for v in range(u+1,M):
                    K={u,v}
                    if any(j+g<=M and (j+L)%M not in K for j in K):continue
                    R=[j for j in range(M) if j not in K];outputs=[j for j in range(M) if j not in(0,L)]
                    for rank in range(factorial(M-2)):
                        rem=outputs[:];a=[M]*M+[0];index=rank
                        for i,q in enumerate(R):
                            f=factorial(len(R)-i-1);digit,index=divmod(index,f);a[q]=rem.pop(digit)
                        cycle,tail=decomposition(a,L)
                        if len(tail)-1>=len(cycle):expected.add((L,tuple(a)))
    return expected


def check(data,coverage=True):
    complete=set();stages=particles=whole=average_controls=nontrivial_q=0;max_n=max_h=max_q=0
    for z in data['records']:
        a,b=z['rows'];M=len(a)-1;L=z['L'];g=gcd(M,L);K=[j for j in range(M) if a[j]==M]
        assert M>=3 and 0<L<M and a[M]==0 and len(K)==2 and K==z['kernel']
        assert sorted(a[j] for j in range(M) if j not in K)==[j for j in range(M) if j not in(0,L)]
        assert b==list(range(1,M))+[0,M] and not any(j+g<=M and (j+L)%M not in K for j in K)
        cycle,tail=decomposition(a,L);tau=len(cycle);h=len(tail)-1;q=h//tau
        assert z['root_cycle']==cycle and z['tail_path']==tail and q==z['q']>=1
        assert not set(cycle)&set(tail[:-1]) and tau+h<=M+1 and tau+g-1<=M-1
        if z['scope']=='complete_NEW_excluded_M3..8':
            assert M<=8 and g>2;signature=(L,tuple(a));assert signature not in complete;complete.add(signature)
        def image(word):
            nonlocal particles
            out=list(range(M+1))
            for c in word:assert type(c) is int and c in(0,1);out=[z['rows'][c][x] for x in out]
            particles+=(M+1)*len(word);return out
        def pre(S,img):return sum(1<<j for j,x in enumerate(img) if S>>x&1)
        f=image([0]*tau);assert f[M]==M and pre(1<<M,f).bit_count()==2
        seed=[0]*(q*tau);assert z['seed']==seed
        S=pre(1<<M,image(seed));assert S>>M&1 and S.bit_count()==q+1
        assert S==(1<<M)|sum(1<<tail[h-m*tau] for m in range(1,q+1))
        reset=seed[:]
        for st in z['stages']:
            assert st['source']==S and S>>M&1 and S<2**(M+1)-1
            U=S&(2**M-1);iswhole=all((U>>j&1)==(U>>((j+L)%M)&1) for j in range(M))
            assert (st['kind']=='whole')==iswhole
            w=st['word'];T=pre(S,image(w));assert T==st['target'] and T>>M&1 and T.bit_count()>S.bit_count()
            assert len(w)<=M and (not iswhole or len(w)<=M-1)
            if iswhole:assert w[:tau]==[0]*tau and all(c==1 for c in w[tau:]);whole+=1
            else:assert w[0]==0 and all(c==1 for c in w[1:]) and T.bit_count()==S.bit_count()+1
            reset=w+reset;S=T;stages+=1
        assert len(z['stages'])<=M-q and S==2**(M+1)-1 and reset==z['reset_word']
        assert z['bound']==M*M-q*(M-tau) and len(reset)<=z['bound']<=M*M
        assert image(reset)==[M]*(M+1)
        seen=set()
        for c in z['whole_controls']:
            mask=c['mask'];assert 0<mask<2**g-1 and mask not in seen;seen.add(mask)
            U=sum(1<<j for j in range(M) if mask>>(j%g)&1);S=(1<<M)|U;gains=[]
            nu_mass=lambda X:X.bit_count()+int(bool(X>>M&1))
            for s in range(g):
                img=[M if x==M else (x+s)%M for x in f];T=pre(S,img);assert T>>M&1
                gains.append(nu_mass(T)-nu_mass(S))
            assert gains==c['gains'] and sum(gains)==g-mask.bit_count() and max(gains)>0;average_controls+=1
        if g<=5:assert z['whole_scope']=='complete' and seen==set(range(1,2**g-1))
        else:assert z['whole_scope']=='named sampled controls'
        max_n=max(max_n,M+1);max_h=max(max_h,h);max_q=max(max_q,q);nontrivial_q+=q>1
    if coverage:assert complete==expected_rows()
    return dict(verified=True,records=len(data['records']),complete_NEW=len(complete),maximum_n=max_n,maximum_tail=max_h,maximum_q=max_q,
        q_greater_than_one_controls=nontrivial_q,original_forward_particles=particles,root_retaining_stages=stages,
        whole_chain_stages=whole,weighted_average_target_controls=average_controls,
        status='Finite complete NEW coverage and original compatible resets COMPUTATIONALLY VERIFIED; all-n h>=tau square PROVED paper, not formal; general Cerny OPEN.')


def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/tail_cycle_weighted_square.json').read_text());out=check(data);rejected=[]
    for mode in range(7):
        bad=copy.deepcopy(data)
        if mode==0:bad['records'].pop(0)
        if mode==1:bad['records'][1]=copy.deepcopy(bad['records'][0])
        if mode==2:bad['records'][0]['q']+=1
        if mode==3:bad['records'][0]['seed'].pop()
        if mode==4:bad['records'][0]['bound']-=1
        if mode==5:bad['records'][0]['whole_controls'][0]['gains'][0]+=1
        if mode==6:bad['records'][0]['reset_word'].pop()
        try:check(bad,mode==0)
        except(AssertionError,ValueError,KeyError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected;print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
