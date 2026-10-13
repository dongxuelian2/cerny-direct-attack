"""Independent edge enumeration and symbolic verification of the r=3 potential.

The finite k checks represent every integer k: above 4 the potential is affine
with slope 3, so local differences do not depend on k. This is not a claim
that finite n experiments alone prove an infinite family.
"""
from itertools import product
from anchor_quotient import edges, solve
from dense_quotient import solve_dense


P3 = {
    2: {'000':4,'001':3,'010':5,'011':2,'100':4,'101':6,'110':1},
    3: {'000':8,'001':7,'010':8,'011':6,'100':8,'101':7,'110':5,'111':6},
    4: {'000':-1,'001':-2,'010':-1,'011':-3,
        '100':-1,'101':-2,'110':-3,'111':-4},
}


def p3(k, bits):
    if k == 1:
        return 0
    key=''.join(map(str,bits))
    return P3[k][key] if k < 4 else 3*k+P3[4][key]


def check_symbolic_p3():
    checked=0
    for k in range(1,6):
        for u,v,w in product((0,1),repeat=3):
            j=k-u-v-w
            if j<0:
                continue
            before=p3(k,(u,v,w))
            after=p3(k-u*v,(u|v,0,w))
            assert before <= 1+after, ('b',k,u,v,w)
            checked+=1
            for t in (0,1):
                if t>j:
                    continue
                after=p3(k,(v,w,t))
                assert before <= 1+after, ('a',k,u,v,w,t)
                checked+=1
    return checked


def direct_edges(n,r):
    anchors=[0]+list(range(n-1,n-r,-1))
    result={}
    def feature(s):
        x=sum(((s>>q)&1)<<i for i,q in enumerate(anchors))
        return (s.bit_count()-x.bit_count(),x)
    for s in range(1,1<<n):
        key=feature(s)
        a=((s<<1)&((1<<n)-1)) | (s>>(n-1))
        b=(s&((1<<(n-1))-1)) | (s>>(n-1))
        result.setdefault(key,set()).update([('a',feature(a)),('b',feature(b))])
    return result


def main():
    print('Symbolic P3 representative inequalities:',check_symbolic_p3())
    count=0
    for n in range(3,11):
        for r in range(1,n):
            direct=direct_edges(n,r)
            for s, expected in direct.items():
                assert set(edges(n,r,s))==expected,(n,r,s)
            count+=1
    print('Concrete powerset/analytic quotient edge equality:',count,'parameter pairs')
    count=0
    for r in range(2,11):
        for m in (2,5):
            sparse=solve(r+m,r)
            dense=solve_dense(r,m)
            assert all(dense[j*(1<<r)+x]==v for (j,x),v in sparse.items())
            count+=1
    print('Dense analytic predecessors/sparse forward-edge BFS agreement:',count,'pairs')
    for n in range(5,101):
        d=solve(n,3)
        assert d[n-3,7]==3*n-4
        for (j,x),v in d.items():
            bits=tuple(x>>i&1 for i in range(3))
            assert v==p3(j+x.bit_count(),bits),(n,j,x,v)
    print('P3 equals every quotient distance for n=5..100')


if __name__=='__main__':
    main()
