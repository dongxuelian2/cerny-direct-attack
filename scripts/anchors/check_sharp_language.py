"""Adversarial sharp-capacity checks beyond exhaustive small enumeration."""
import random
from uniform_construction import clocks
from earliest_capacity_two import earliest


def run(r,s,m,concrete=False):
    A=s[-1]
    events=set(s+[A+2*i for i in range(1,m-1)])
    end=A+2*(m-2)
    full=(1<<r)-1
    j,x=0,1
    n=r+m
    anchors=[0]+list(range(n-1,n-r,-1))
    def feature(subset):
        xx=sum((q in subset)<<i for i,q in enumerate(anchors))
        return len(subset)-xx.bit_count(),xx
    for t in range(end+1):
        if t:
            u=int(t in events)
            if not u<=j<=m-1+u:
                return ('input',t,j,u)
            out=x>>(r-1)
            nxt=(j-u+out,((x<<1)&full)|u)
            if concrete:
                current={q for i,q in enumerate(anchors) if x>>i&1}
                current |= ({1} if u else set()) | set(range(2,2+j-u))
                assert feature(current)==(j,x)
                predecessor={(q-1)%n for q in current}
                assert feature(predecessor)==nxt
            j,x=nxt
        if t in events:
            if x&3!=1:
                return ('split',t,j,x&3)
            if concrete:
                current={q for i,q in enumerate(anchors) if x>>i&1}|set(range(1,j+1))
                predecessor=current|{n-1}
                image={0 if q==n-1 else q for q in predecessor}
                assert image==current and feature(predecessor)==(j,x|2)
            x|=2
    return None if (j,x)==(m,full) else ('endpoint',j,x)


def random_schedule(r,rng):
    latest=clocks(r)
    L=(r-1).bit_length()-1
    p=1<<L
    C=L*r-2*p
    s=[]
    for i in range(1,r+2):
        lower=0 if i==1 else max(s[-1]+2,s[i//2-1]+r+i%2)
        fixed=(i&(i-1)==0 and i<=p) or i>=p
        t=C+2*i if i>=p else (i.bit_length()-1)*r if fixed else rng.randint(lower,latest[i-1])
        assert lower<=t<=latest[i-1]
        s.append(t)
    return s


def main():
    rng=random.Random(2026092803)
    tests=0
    points=list(range(3,129))+[255,256,257,511,512,513,1023,1024,1025]
    for r in points:
        L=(r-1).bit_length()-1
        p=1<<L
        M=p//2+1
        for trial in range(10):
            s=random_schedule(r,rng)
            assert run(r,s,M,concrete=trial==0) is None
            assert run(r,s,M+3) is None
            tests+=2
        if r>=5:
            fail=run(r,earliest(r),M-1)
            assert fail is not None and fail[0]=='input'
            assert fail[1]==L*r+p-1,(r,fail)
    print('Sharp threshold:',tests,'random optimal-clock witnesses; concrete-set reverse checks at',len(points),'r values')
    print('Earliest universal lower obstruction matched at every tested r>=5, through r=1025')


if __name__=='__main__':
    main()
