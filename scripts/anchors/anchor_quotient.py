"""Direct exact anchor quotient: no enumeration of concrete subsets.

x bit i records anchor i (0,n-1,...); j counts the m=n-r hidden ones.
Run from the repository root. Only standard-library Python is required.
"""
from collections import deque
import argparse


def edges(n, r, state):
    j, x = state
    m = n-r
    if r == 1:
        # b sees a hidden n-1; its membership can be chosen existentially.
        if j < m:
            yield 'b', (j, x)
        if j:
            yield 'b', (j-1, 1)
    else:
        u, v = x & 1, (x >> 1) & 1
        yield 'b', (j, (x & ~3) | (u | v))
    for t in (0, 1):
        if t <= j and j-t <= m-1:
            yield 'a', (j+(x & 1)-t, (x >> 1) | (t << (r-1)))


def solve(n, r):
    assert 1 <= r < n
    states = [(j, x) for j in range(n-r+1) for x in range(1 << r)
              if j+x.bit_count()]
    rev = {s: [] for s in states}
    for s in states:
        for label, t in edges(n, r, s):
            rev[t].append(s)
    d = {s: 0 for s in states if s[0]+s[1].bit_count() == 1}
    q = deque(d)
    while q:
        t = q.popleft()
        for s in rev[t]:
            if s not in d:
                d[s] = d[t]+1
                q.append(s)
    assert len(d) == len(states)
    return d


def path(n, r, d):
    s = (n-r, (1 << r)-1)
    result = [(s, d[s], '')]
    while d[s]:
        label, t = next((label, t) for label, t in edges(n, r, s)
                        if d[t] == d[s]-1)
        s = t
        result.append((s, d[s], label))
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--n', type=int, default=10)
    p.add_argument('--r', type=int, default=3)
    p.add_argument('--table', action='store_true')
    p.add_argument('--path', action='store_true')
    args = p.parse_args()
    d = solve(args.n, args.r)
    print(f'B_{args.r}({args.n})={d[(args.n-args.r,(1<<args.r)-1)]}')
    if args.table:
        for k in range(1, args.n+1):
            print(k, {''.join(str(x>>i & 1) for i in range(args.r)): v
                      for (j,x),v in d.items() if j+x.bit_count()==k})
    if args.path:
        for (j,x),v,label in path(args.n,args.r,d):
            print(label, j+x.bit_count(), ''.join(str(x>>i & 1) for i in range(args.r)), j,v)


if __name__ == '__main__':
    main()
