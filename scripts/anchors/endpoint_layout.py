"""Search-free witnesses for B_A(n)=2*n-k-2, H={1,...,k-1,n-1}."""
from layout_experiments import quotient


def check(n,k):
    assert 2<=k<=n-1
    hidden=set(range(1,k))|{n-1}
    anchors=set(range(n))-hidden
    I=set(range(k,n-1))
    j=k
    observed=anchors.copy()
    length=0
    def feature(s):
        return len(s&hidden),s&anchors
    def transition(s,letter,expected):
        nonlocal j,observed,length
        assert feature(s)==(j,observed)
        image={(q+1)%n for q in s} if letter=='a' else {0 if q==n-1 else q for q in s}
        assert feature(image)==expected
        j,observed=expected
        length+=1
    for _ in range(k-1):
        chosen=set(range(1,j))|{n-1}
        transition(observed|chosen,'b',(j-1,observed.copy()))
    for _ in range(n-k-1):
        new_I={q+1 for q in I if q<n-2}
        transition(observed|{n-1},'a',(2,{0}|new_I))
        I=new_I
        transition(observed|{1,n-1},'b',(1,observed.copy()))
    transition(observed|{n-1},'b',(0,{0}))
    assert length==2*n-k-2
    return length


def main():
    points=0
    for n in range(3,13):
        for k in range(2,n):
            expected=check(n,k)
            hidden=set(range(1,k))|{n-1}
            B=quotient(n,[q for q in range(n) if q not in hidden])
            assert B==expected,(n,k,B,expected)
            points+=1
    for n in [16,31,32,33,100,1000]:
        for k in sorted({2,3,n//2,n-2,n-1}):
            check(n,k)
    print('Endpoint exact family: complete concrete BFS at',points,'points; large witnesses through n=1000')


if __name__=='__main__':
    main()
