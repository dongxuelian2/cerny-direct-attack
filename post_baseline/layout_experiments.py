"""Independent concrete enumeration for arbitrary anchor layouts."""
from collections import deque
from itertools import combinations
from math import gcd
import csv
from pathlib import Path


def quotient(n,anchors):
    ids={}
    alpha=[-1]*(1<<n)
    def feature(s):
        return (s.bit_count(),sum(((s>>q)&1)<<i for i,q in enumerate(anchors)))
    for s in range(1,1<<n):
        key=feature(s)
        if key not in ids:
            ids[key]=len(ids)
        alpha[s]=ids[key]
    rev=[set() for _ in ids]
    for s in range(1,1<<n):
        a=((s<<1)&((1<<n)-1))|(s>>(n-1))
        b=(s&((1<<(n-1))-1))|(s>>(n-1))
        rev[alpha[a]].add(alpha[s])
        rev[alpha[b]].add(alpha[s])
    d=[-1]*len(ids)
    q=deque({alpha[1<<i] for i in range(n)})
    for target in q:
        d[target]=0
    while q:
        t=q.popleft()
        for s in rev[t]:
            if d[s]<0:
                d[s]=d[t]+1
                q.append(s)
    return d[alpha[-1]]


def main():
    rows=[]
    for n in range(2,13):
        for q in range(n):
            B=quotient(n,[q])
            expected=n-1 if q==0 else 2*n-3 if q==n-1 else n
            assert B==expected,(n,q,B,expected)
    print('All one-anchor placements verified for n=2..12',flush=True)
    for n in range(4,13):
        for u,v in combinations(range(n),2):
            anchors=[q for q in range(n) if q not in (u,v)]
            B=quotient(n,anchors)
            g=gcd(v-u,n)
            assert B>=(g-1)**2
            rows.append(dict(n=n,hidden_u=u,hidden_v=v,gcd=g,B=B,
                             projection_lower=(g-1)**2))
        print(n,'adjacent',next(x['B'] for x in rows if x['n']==n and (x['hidden_u'],x['hidden_v'])==(1,2)),
              'antipodal',[(x['hidden_u'],x['B']) for x in rows if x['n']==n and x['hidden_v']-x['hidden_u']==n//2] if n%2==0 else [],flush=True)
    dest=Path('post_baseline/sprint_results/layout_pairs.csv')
    with dest.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__=='__main__':
    main()
