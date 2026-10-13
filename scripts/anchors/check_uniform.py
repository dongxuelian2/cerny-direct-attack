"""Independent concrete-set witness checker and adversarial lemma checks."""
import itertools
import random
from uniform_construction import clocks, forward_witness
from latest_schedule import times
from anchor_quotient import edges, solve


def concrete_check(r,m,states,labels):
    n=r+m
    anchors=[0]+list(range(n-1,n-r,-1))
    hidden=list(range(1,m+1))
    for source,target,label in zip(states,states[1:],labels):
        j,x=source
        observed={q for i,q in enumerate(anchors) if x>>i&1}
        ok=False
        for chosen in itertools.combinations(hidden,j):
            subset=observed|set(chosen)
            if label=='a':
                image={(q+1)%n for q in subset}
            else:
                image={0 if q==n-1 else q for q in subset}
            xx=sum((q in image)<<i for i,q in enumerate(anchors))
            jj=len(image)-xx.bit_count()
            if (jj,xx)==target:
                ok=True
                break
        assert ok,(r,m,source,target,label)
    assert states[0]==(m,(1<<r)-1)
    j,x=states[-1]
    assert j+x.bit_count()==1


def genealogy_check(n,r,steps):
    m=n-r
    window=list(range(r))
    hidden=list(range(r,n))
    creation={}
    clock=0
    merge_clocks=[]
    next_id=n
    ineffective=0
    for label,t in steps:
        if label=='a':
            assert t<=len(hidden)<=m-1+t
            chosen=hidden.pop(0) if t else None
            if window[0] is not None:
                hidden.append(window[0])
            window=window[1:]+[chosen]
            clock+=1
        elif window[0] is not None and window[1] is not None:
            for i,delay in ((0,r+1),(1,r)):
                token=window[i]
                if token in creation:
                    assert clock-creation[token]>=delay,('latency',n,r,clock,creation[token],i)
            if merge_clocks:
                assert clock-merge_clocks[-1]>=2
            merge_clocks.append(clock)
            window[0]=next_id
            window[1]=None
            creation[next_id]=clock
            next_id+=1
        else:
            if window[1] is not None:
                window[0],window[1]=window[1],None
            clock+=1
            ineffective+=1
    assert len(merge_clocks)==n-1
    reverse=[clock-c for c in reversed(merge_clocks)]
    for k in range(2,n):
        assert reverse[k-1]>=reverse[k-2]+2
        assert reverse[k-1]>=reverse[k//2-1]+r+(k%2)
    return ineffective


def main():
    count=0
    for r in list(range(2,101))+[127,128,129,255,256,257,511,512,513,1023,1024,1025]:
        assert clocks(r)==times(r)
        states,labels=forward_witness(r)
        concrete_check(r,2,states,labels)
        for m in (3,5):
            if r<=20:
                states,labels=forward_witness(r,m)
                concrete_check(r,m,states,labels)
        count+=1
    print('Independent concrete witness checks:',count,'r values; dangerous dyadic boundaries included')
    rng=random.Random(20260928)
    count=ineffective=0
    for n in range(4,11):
        for r in range(2,n):
            d=solve(n,r)
            for trial in range(50):
                s=(n-r,(1<<r)-1)
                trace=[]
                for k in range(30):
                    label,target=rng.choice(list(edges(n,r,s)))
                    t=(target[1]>>(r-1)) if label=='a' else 0
                    trace.append((label,t))
                    s=target
                while d[s]:
                    label,target=rng.choice([(a,t) for a,t in edges(n,r,s) if d[t]==d[s]-1])
                    t=(target[1]>>(r-1)) if label=='a' else 0
                    trace.append((label,t))
                    s=target
                ineffective+=genealogy_check(n,r,trace)
                count+=1
    print('Adversarial genealogy checks:',count,'paths,',ineffective,'ineffective b letters')
    # Large r arithmetic interlacing checks require no powerset, no SMT.
    for r in [2,3,4,7,8,9,17,31,32,33,63,64,65,127,128,129,
              1023,1024,1025,8191,8192,8193,65535,65536,65537]:
        s=clocks(r)
        K=r+1
        assert s[0]==0
        assert all(b-a>=2 for a,b in zip(s,s[1:]))
        for k in range(2,K+2):
            q=s[k//2-1]+r+k%2
            if k<=K:
                assert q<=s[k-1]
            assert s[k-2]<=q
        assert s[(K+2)//2-1]+r+(K+2)%2==s[-1]+1
    print('Large-r release interlacing checked through r=65537')


if __name__=='__main__':
    main()
