"""Test latest feasible heap-indexed birth schedules at the exact deadline."""


def times(r):
    h=(r-1).bit_length()
    A=(h+1)*r-(1<<h)+2
    K=r+1
    s=[None]*(K+1)
    s[K]=A
    for i in range(K-1,0,-1):
        bounds=[s[i+1]-2]
        if 2*i<=K:
            bounds.append(s[2*i]-r)
        if 2*i+1<=K:
            bounds.append(s[2*i+1]-r-1)
        s[i]=min(bounds)
    assert s[1]==0
    return s[1:]


def verify(r,s):
    j,x=0,3
    full=(1<<r)-1
    birthset=set(s)
    peak=0
    first_bad=None
    for t in range(1,s[-1]+1):
        u=int(t in birthset)
        if not u<=j<=1+u and first_bad is None:
            first_bad=(t,j,u)
        out=x>>(r-1)
        j+=out-u
        x=((x<<1)&full)|u
        if u:
            assert x&3==1
            x|=2
        peak=max(peak,j)
    return peak,first_bad,j,x==full


def main():
    bad=[]
    for r in range(2,2001):
        s=times(r)
        result=verify(r,s)
        if result[1] is not None or result[2:]!=(2,True):
            bad.append((r,result,s))
            if len(bad)<=5:
                print('FAIL',bad[-1],flush=True)
    print('failures',len(bad),'first',bad[:1])
    for r in (9,10,17,24,31,32,33):
        print(r,times(r),verify(r,times(r)))


if __name__=='__main__':
    main()
