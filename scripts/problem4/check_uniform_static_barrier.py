"""Small exact controls for PROOF.md#problem4-real-safe-family-rank-barrier.

All graphs, state maps, and safe starting families are recomputed directly.
The arbitrary-parameter result is a paper proof, not this finite check.
"""
from itertools import combinations
from collections import deque
from fractions import Fraction

def exact_rank(rows):
    pivots = {}
    for row in rows:
        r = list(map(Fraction, row))
        for j, b in sorted(pivots.items()):
            if r[j]:
                z = r[j]
                r = [x-z*y for x,y in zip(r,b)]
        j = next((j for j,x in enumerate(r) if x), None)
        if j is not None:
            z = r[j]
            pivots[j] = [x/z for x in r]
    return len(pivots)

for m in range(2, 5):
    n = 4*m-1
    h, p = 2*m-2, 2*m-1
    a = tuple((i+1)%n for i in range(n))
    b = tuple(0 if i==n-1 else i for i in range(n))
    letters = (a,b)
    full = (1<<n)-1
    B = sum(1<<i for i in range(1,p+1))
    edges = {frozenset((n-1-i,(n-i)%n)) for i in range(h)}
    # Independently compute P_h by forward breadth-first search for each pair.
    literal_edges = set()
    for pair in combinations(range(n),2):
        frontier, seen = {pair}, {pair}
        merged = False
        for depth in range(1,h+1):
            nxt = set()
            for x,y in frontier:
                for f in letters:
                    u,v = f[x],f[y]
                    if u==v:
                        merged = True
                    else:
                        z = tuple(sorted((u,v)))
                        if z not in seen:
                            seen.add(z)
                            nxt.add(z)
            frontier = nxt
        if merged:
            literal_edges.add(frozenset(pair))
    assert literal_edges == edges
    def im(mask,f):
        ans = 0
        for q in range(n):
            if mask>>q&1:
                ans |= 1<<f[q]
        return ans
    rows = []
    checked = 0
    for holes in combinations(range(n),m):
        T = full ^ sum(1<<i for i in holes)
        predicted = T&B==B and all(not all(T>>v&1 for v in e) for e in edges)
        safe = bool(T>>p&1)
        frontier, seen = {T}, {T}
        for depth in range(1,h+1):
            if not safe:
                break
            nxt = set()
            for X in frontier:
                for f in letters:
                    Y = im(X,f)
                    if Y.bit_count()!=n-m or not(Y>>p&1):
                        safe = False
                    if Y not in seen:
                        seen.add(Y)
                        nxt.add(Y)
            frontier = nxt
        assert safe == predicted, (m,holes,safe,predicted)
        checked += 1
        if safe:
            rows.append([T>>q&1 for q in range(n)])
    rank = exact_rank(rows)
    assert rank == n-2*m+1, (m,rank)
    # Check the exact adjacent deletion transformations used in reachability.
    for i in range(n):
        images = list(range(n))
        for f in (a,)*(n-1-i)+(b,)+(a,)*(i+1):
            images = [f[x] for x in images]
        assert images == [(i+1)%n if q==i else q for q in range(n)]
    print(f'm={m} n={n} h={h}: checked_initial_sets={checked} '
          f'actual_safe_family={len(rows)} rank={rank}; all claims agree')
