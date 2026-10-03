"""Independent complete concrete-subset checker for a word-language boundary."""
from collections import defaultdict


def check(n,r,word):
    full=(1<<n)-1
    anchors=[0]+list(range(n-1,n-r,-1))
    def feature(s):
        return s.bit_count(),sum(((s>>q)&1)<<i for i,q in enumerate(anchors))
    relation=defaultdict(set)
    for s in range(1,full+1):
        a=((s<<1)&full)|(s>>(n-1))
        b=(s&((1<<(n-1))-1))|(s>>(n-1))
        relation[(feature(s),'a')].add(feature(a))
        relation[(feature(s),'b')].add(feature(b))
    reachable={feature(full)}
    widths=[1]
    for letter in word:
        reachable={target for source in reachable for target in relation[(source,letter)]}
        widths.append(len(reachable))
    goals=sorted(x for x in reachable if x[0]==1)
    return goals,widths


def main():
    w='baa'*2+'b'+'a'*3+'b'+'a'*2+'b'+'a'*5+'b'
    assert len(w)==20
    goals,widths=check(7,5,w)
    assert not goals
    print('Capacity2:',len(w),'letters, no singleton; complete reachable widths',widths)
    goals,widths=check(8,5,'baa'+w)
    assert goals==[(1,1)]
    print('Capacity3:',len(w)+3,'letters, singleton',goals,'widths',widths)
    # Verify the explicit reverse trace independently of forward propagation.
    j,x=0,1
    events={0,5,7,10,12,14,16}
    trace=[]
    for t in range(17):
        if t:
            u=int(t in events)
            assert u<=j<=2+u
            j=j-u+(x>>4)
            x=((x<<1)&31)|u
        if t in events:
            assert x&3==1
            x|=2
        trace.append((t,j,x))
    assert (j,x)==(3,31)
    print('Reverse capacity3 trace:',trace)


if __name__=='__main__':
    main()
