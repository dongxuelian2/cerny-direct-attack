"""Uniform candidate for codimension two in the compression-dominated range."""
from math import lcm

def construct(n,r):
    assert n>=7 and 1<=r<=n-6
    L=n-3;z=L-1;w=L;v=L+1;u=L+2
    a=list(range(n));a[z]=u;a[u]=z;a[v]=z
    b=[(q+1)%L for q in range(L)]+[v,u,w]
    N=lcm(L,3);e='aa';f='b'*(N-1)+e+'b';k=e+f;c=k+'a'+f+'a'+k
    return dict(n=n,s=n-2,r=r,L=L,rows=[a,b],S=list(range(L))+[v],A=list(range(2,2+r)),
                value=6,reaching=k+'b',attaining='ababba',reset=c+('b'+c)*(L-1),
                short_unit=e,second_unit=f,short_collapse=k,root_macro=c)

def construct_one(n,r):
    assert n>=4 and 1<=r<=n-3
    u,v,z=0,1,2;a=list(range(n));a[z]=u;a[u]=z;a[v]=z
    b=list(range(1,n))+[0];e='aa'
    return dict(n=n,s=n-1,r=r,rows=[a,b],S=list(range(1,n)),A=list(range(3,3+r)),
                value=3,reaching='a'+'b'*(n-1),attaining='bba',reset=e+('b'+e)*(n-2),short_unit=e)
