"""Independent particle replay, row identities, periods, seeds and square budgets."""
from collections import Counter,defaultdict
from copy import deepcopy
from math import gcd,factorial
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]

def check(data):
    records=data['records'];counts=defaultdict(set)
    for z in records:
        if z['mode']=='complete_new_noncp_M6..9':
            key=(z['M'],z['d']);signature=tuple(z['rows'][0]);assert signature not in counts[key];counts[key].add(signature)
    expected={(M,d):factorial(M-2) for M in range(6,10) for d in range(1,M) if gcd(M,d)>1 and M//gcd(M,d)>=3}
    assert set(counts)==set(expected) and all(len(counts[k])==v for k,v in expected.items())
    stats=Counter();branches=Counter();seeds=Counter();completions=Counter();rules=Counter();maxlength=0
    for z in records:
        M=z['M'];n=M+1;d=z['d'];L=M-d;g=gcd(M,d);t=M//g;Q=(1<<n)-1;C=(1<<M)-1;F=z['rows'];a,b=F
        assert M>=3 and 1<=d<M and t>=3
        rest=set(range(M))-{0,L};assert len(a)==n and a[M]==0 and a[0]==a[L]==M and {a[q] for q in rest}==rest
        assert b==list(range(1,M))+[0,M]
        def run(w):
            assert isinstance(w,list) and all(type(i) is int and i in (0,1) for i in w)
            image=list(range(n))
            for letter in w:image=[F[letter][q] for q in image]
            stats['literal_particle_controls']+=n*len(w);return image
        def inv(U,w):
            assert isinstance(U,int) and 0<=U<=Q
            return sum(1<<q for q,x in enumerate(run(w)) if U>>x&1)
        def periodic(U):return all((U>>q&1)==(U>>((q+L)%M)&1) for q in range(M))
        def word(c):
            rule=c['rule'];j=c.get('j',0);assert type(j) is int and 0<=j<M
            if rule in ('root_keep','core_return'):
                return [0]*(1 if rule=='root_keep' else 2)+[1]*j
            if rule=='three_a':
                s=c['s'];assert type(s) is int and 0<=s<g
                return [0]+[1]*j+[0]+[1]*d+[0]+[1]*s
            assert rule=='root_coset';s=c['s'];assert type(s) is int and 0<=s<g
            return [0]+[1]*L+[0]+[1]*s
        c=run([0,0]);assert c[M]==M and all(c[q]<M for q in range(M))
        assert [c.count(q)-1 for q in range(n)]==[1 if q==0 else -1 if q==L else 0 for q in range(n)]
        f=[0]+[1]*L+[0];ff=run(f);zp=a[2*L%M]
        assert ff[M]==M and [ff.count(q)-1 for q in range(n)]==[int(q==M)+int(q==0)-int(q==L)-int(q==zp) for q in range(n)]
        assert inv(1<<M,f)==(1<<M)|(1<<a.index(d))
        def verify_factor(e,root=False,low_whole=False):
            U=e['U'];w=word(e);assert len(w)<=n
            if root:
                assert U>>M&1 and U<Q
                if e['rule']=='root_keep':
                    assert not periodic(U&C) and len(w)<=n-1
                    assert U>>e['j']&1 and not U>>((e['j']+L)%M)&1
                else:
                    assert e['rule']=='root_coset' and periodic(U&C)
                    assert not U>>((zp+e['s'])%M)&1 and len(w)<=L+g+1<=n
            elif e['rule']=='core_return':assert not U>>M&1 and U>>e['j']&1 and not U>>((e['j']+L)%M)&1
            if low_whole:
                assert 2*d<=M and 0<U<C and periodic(U)
                p=e['p'];assert p==next(k for k in range(1,M+1) if all((U>>q&1)==(U>>((q+k)%M)&1) for q in range(M)))
                assert p>=2 and g%p==0 and M%p==0 and M//p>=3
                image=run([0]+[1]*d+[0]);z0=a[d];T=M//p
                expected_row=[1+int(q==0)-int(q==L)-int(q==z0) for q in range(n)]
                assert [image[:M].count(q) for q in range(n)]==expected_row
                neutral=[q for q in range(M) if image[q]<M and image[q]%p==z0%p]
                assert len(neutral)==T-1;stats['neutral_class_particle_controls']+=M
                assert e['rule']=='three_a';j=e['j'];s=e['s'];Fj=image[(L+j)%M]
                assert j==next(j for j in range(T) if image[(L+j)%M]==M or image[(L+j)%M]%p!=z0%p)
                assert j<T and s<p and U>>((z0+s)%M)&1
                assert Fj==M or not U>>((Fj+s)%M)&1
                if d+T+p>M:
                    assert p==2 and T%2 and d==T-1 and g==2 and image[L]==image[0]==0
                    if z0%2==0 and not U&1:assert j<=T-2
                    if z0%2==1 and U&1:assert j==0
                    stats['low_arithmetic_exception_controls']+=1
            V=inv(U,w);assert V.bit_count()==U.bit_count()+1
            if root:assert V>>M&1
            stats['literal_extension_controls']+=1;rules[e['rule']]+=1
            return V,w
        branch=z['branch'];branches[branch]+=1
        assert branch==('preceding_coprime' if g==1 else 'low_half' if 2*d<=M else 'high_half')
        seed=z['seed'];U=inv(1<<M,seed);suffix=seed[:]
        if branch=='preceding_coprime':
            assert seed==[0]
            for index,e in enumerate(z['factors']):
                assert e['U']==U and e['rule']=='core_return'
                if index==0:assert e['j']==L
                U,w=verify_factor(e);suffix=w+suffix
            assert U<C and U.bit_count()==M-1
        elif branch=='low_half':
            assert seed==[0,0]+[1]*L+[0] and not U>>M&1 and U.bit_count()==3
            for e in z['factors']:
                assert e['U']==U
                if U>>M&1:U,w=verify_factor(e,root=True)
                else:
                    assert U.bit_count()<M-1
                    U,w=verify_factor(e,low_whole=e['rule']!='core_return')
                suffix=w+suffix
            if z['completion']=='root_policy':
                assert U==Q and len(suffix)<=M*M-d+1
            else:assert z['completion']=='paid_preparation' and not U>>M&1 and U.bit_count()==M-1
            completions[z['completion']]+=1
        else:
            p=a.index(d);zp=a[2*L%M];assert z['p']==p and z['z']==zp and d-L>=2
            assert U>>M&1 and U.bit_count()==3
            rule=z['seed_rule'];seeds[rule]+=1
            if p<=d-1:assert rule=='three_a' and seed==[0]+[1]*p+f and len(seed)<=n+1
            elif p!=zp:assert rule=='f_squared' and seed==f+f and len(seed)<=n+1
            else:assert rule=='f_b_f' and seed==f+[1]+f and len(seed)<=n+2 and p>=L+2
            if len(seed)==n+2:
                assert d-L==2 and not periodic(U&C) and z['factors'][0]['rule']=='root_keep'
                stats['extra_seed_letter_compensations']+=1
            for e in z['factors']:
                assert e['U']==U;U,w=verify_factor(e,root=True);suffix=w+suffix
            assert U==Q and len(suffix)<=M*M
        if branch=='preceding_coprime' or branch=='low_half' and z['completion']=='paid_preparation':
            p=a.index(2*L%M);j=(p-L)%M;v=z['preparation'];assert v==[0]+[1]*j+[0]+[1]*d+[0]
            assert set(run(v))==set(range(M))-{L} and len(v)<=M+d+2
            q=next(q for q in range(M) if not U>>q&1);k=z['alignment'];assert k==(q-L)%M
            suffix=v+[1]*k+suffix
        assert suffix==z['reset_word'] and len(suffix)<=M*M and run(suffix)==[M]*n
        maxlength=max(maxlength,len(suffix));stats['compatible_reset_words']+=1
        controls=z['whole_controls'];assert all(e['rule']=='three_a' for e in controls)
        if g>1 and 2*d<=M:
            want={sum(1<<q for q in range(M) if pattern>>(q%g)&1) for pattern in range(1,(1<<g)-1)}
            assert {e['U'] for e in controls}==want and len(controls)==len(want)
            for e in controls:verify_factor(e,low_whole=True)
        else:assert not controls
        roots=z['root_controls']
        if g>1:
            if M<=8:assert z['root_subset_scope']=='ALL proper root-present subsets' and {e['U'] for e in roots}=={U|(1<<M) for U in range(C)} and len(roots)==C
            else:assert z['root_subset_scope']=='16 retained proper root-present subsets' and len(roots)==16 and len({e['U'] for e in roots})==16
            for e in roots:verify_factor(e,root=True)
        else:assert not roots
        stats['root_present_controls']+=len(roots);stats['whole_core_controls']+=len(controls)
    assert stats['extra_seed_letter_compensations']>0 and completions['root_policy']>0
    return dict(verified=True,inputs=len(records),complete_new_inputs=sum(expected.values()),maximum_n=max(z['M']+1 for z in records),maximum_literal_reset= maxlength,
                branches=dict(branches),seeds=dict(seeds),low_completions=dict(completions),rules=dict(rules),**dict(stats),
                status='PROVED paper ALL t>=3 arbitrary remaining-core model square; finite independent literal/row/coverage controls COMPUTATIONALLY VERIFIED, not FORMALLY VERIFIED. Mixed SYNC order-two and general Cerny OPEN. Native full M12 pressure EXPLORATORY.')

def main():
    data=json.loads((ROOT/'scripts/direct_attack/data/moving_root_all_high_order.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    high=next(i for i,z in enumerate(data['records']) if z['branch']=='high_half')
    for mode in range(10):
        bad=deepcopy(data);z=bad['records'][0]
        if mode==0:bad['records'].pop(0)
        if mode==1:bad['records'][1]=deepcopy(z)
        if mode==2:z['rows'][0][0]=0
        if mode==3:z['seed'].pop()
        if mode==4:z['factors'][0]['U']^=1<<z['M']
        if mode==5:z['whole_controls'][0]['p']=1
        if mode==6:z['whole_controls'][0]['j']=z['M']
        if mode==7:z['root_controls'][0]['U']=1<<(z['M']+1)
        if mode==8:z['alignment']=(z['alignment']+1)%z['M']
        if mode==9:bad['records'][high]['seed_rule']='invalid'
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError,StopIteration):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected
    (ROOT/'scripts/direct_attack/data/moving_root_all_high_order_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
