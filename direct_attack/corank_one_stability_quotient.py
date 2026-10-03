"""Small forward-pair controls and the all-parameter sharp class-range family."""
import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def partition(n, edges):
    parent = list(range(n))
    def root(q):
        while parent[q] != q:
            q = parent[q]
        return q
    for x, y in edges:
        parent[root(x)] = root(y)
    return sorted(sorted(q for q in range(n) if root(q) == r) for r in {root(q) for q in range(n)})


def strongly_connected(rows):
    n = len(rows[0])
    reverse = [[] for _ in range(n)]
    for f in rows:
        for x, y in enumerate(f):
            reverse[y].append(x)
    for backwards in (False, True):
        seen = {0}
        todo = [0]
        while todo:
            q = todo.pop()
            for t in reverse[q] if backwards else [f[q] for f in rows]:
                if t not in seen:
                    seen.add(t)
                    todo.append(t)
        if len(seen) != n:
            return False
    return True


def mergeable(rows):
    n = len(rows[0])
    edges = []
    for seed in combinations(range(n), 2):
        seen = {seed}
        todo = deque([seed])
        found = False
        while todo and not found:
            x, y = todo.popleft()
            for f in rows:
                P = tuple(sorted((f[x], f[y])))
                if P[0] == P[1]:
                    found = True
                    break
                if P not in seen:
                    seen.add(P)
                    todo.append(P)
        if found:
            edges.append(seed)
    return edges


def permutation_quotient(rows):
    n = len(rows[0])
    current = [[q] for q in range(n)]
    rounds = 0
    while True:
        ids = {q: i for i, C in enumerate(current) for q in C}
        quotient = [[ids[f[C[0]]] for C in current] for f in rows]
        assert all(len({ids[f[q]] for q in C}) == 1 for f in rows for C in current)
        m = len(current)
        assert all(len(set(f)) >= m - 1 for f in quotient)
        if all(len(set(f)) == m for f in quotient):
            break
        edges = {P for P in combinations(range(m), 2) if any(f[P[0]] == f[P[1]] for f in quotient)}
        old = partition(m, edges)
        while True:
            new = edges | {tuple(sorted((f[x], f[y]))) for f in quotient for x, y in edges if f[x] != f[y]}
            joined = partition(m, new)
            if joined == old:
                break
            old, edges = joined, new
        current = sorted(sorted(q for i in C for q in current[i]) for C in old)
        rounds += 1
    assert rounds <= n - 1
    return current


def scope(n):
    maps = [f for f in product(range(n), repeat=n) if len(set(f)) >= n - 1]
    stream = sha256()
    count = sync = maximum_range = 0
    histogram = {}
    for a, b in product(maps, repeat=2):
        rows = [a, b]
        if not strongly_connected(rows):
            continue
        edges = mergeable(rows)
        P = partition(n, edges)
        ids = {q: i for i, C in enumerate(P) for q in C}
        assert set(edges) == {p for p in combinations(range(n), 2) if ids[p[0]] == ids[p[1]]}
        assert all(ids[f[x]] == ids[f[y]] for f in rows for x, y in edges)
        assert all(len({ids[f[C[0]]] for C in P}) == len(P) for f in rows)
        beta = permutation_quotient(rows)
        assert beta == P
        span = max(map(len, P)) - min(map(len, P))
        assert span <= sum(len(set(f)) < n for f in rows)
        count += 1
        sync += len(P) == 1
        maximum_range = max(maximum_range, span)
        histogram[len(P)] = histogram.get(len(P), 0) + 1
        stream.update(json.dumps([a, b, P, beta, len(P)], separators=(',', ':')).encode() + b'\n')
    return dict(n=n,all_labeled_binary_inputs=len(maps)**2,strongly_connected=count,
                synchronizing=sync,minimum_rank_histogram=histogram,maximum_class_size_range=maximum_range,
                semantic_sha256=stream.hexdigest())


def family_rows(s):
    classes = []
    for h in range(1, s + 2):
        base = h * (h - 1) // 2
        classes.append(list(range(base, base + h)))
    n = (s + 1) * (s + 2) // 2
    g = list(range(n))
    for C in classes:
        for i, q in enumerate(C):
            g[q] = C[(i + 1) % len(C)]
    rows = [g]
    for j in range(1, s + 1):
        f = list(range(n))
        small, large = classes[j-1:j+1]
        for x, y in zip(small, large):
            f[x], f[y] = y, x
        f[large[-1]] = small[0]
        rows.append(f)
    return classes, rows


def mixed_scope(n):
    allmaps=list(product(range(n),repeat=n))
    defect=[f for f in allmaps if len(set(f))==n-1]
    stream=sha256();count=0
    for a,b in product(defect,allmaps):
        rows=[a,b]
        if not strongly_connected(rows):continue
        K=next(P for P in combinations(range(n),2) if a[P[0]]==a[P[1]])
        orbit={K};todo=[K]
        while todo:
            x,y=todo.pop()
            for f in rows:
                P=tuple(sorted((f[x],f[y])))
                if P not in orbit:orbit.add(P);todo.append(P)
        good=set(mergeable(rows));assert all(x==y or (x,y) in good for x,y in orbit)
        Q=frozenset(range(n));images={Q};queue=deque([Q]);rank=n
        while queue:
            S=queue.popleft();rank=min(rank,len(S))
            for f in rows:
                T=frozenset(f[q] for q in S)
                if T not in images:images.add(T);queue.append(T)
        count+=1
        stream.update(json.dumps([a,b,K,sorted(orbit),rank],separators=(',',':')).encode()+b'\n')
    return dict(n=n,all_defect_one_arbitrary_binary_inputs=len(defect)*len(allmaps),strongly_connected=count,semantic_sha256=stream.hexdigest())


def family(s):
    classes, rows = family_rows(s)
    n = len(rows[0])
    assert strongly_connected(rows)
    assert [len(set(f)) for f in rows] == [n] + [n-1] * s
    programs = [dict(h=h,unit_letters=[h-1,h-1],root_g_power=h-1,
                     root_tail_letters=[h-1,h-1],root_repetitions=h-2,charged_length=h*(h-1)) for h in range(2,s+2)]
    return dict(s=s,n=n,rows_sha256=digest(rows),stable_class_sizes=list(range(1,s+2)),
                stable_partition_sha256=digest(classes),minimum_rank=s+1,class_size_range=s,
                charged_rank_word_length=s*(s+1)*(s+2)//3,programs=programs,
                strongly_connected=True,original_letter_ranks=[n]+[n-1]*s)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,default=Path('direct_attack/data/corank_one_stability_quotient.json'))
    args=ap.parse_args()
    out=dict(scopes=[scope(n) for n in range(2,5)],mixed_scopes=[mixed_scope(n) for n in range(2,5)],
             sharp_families=[family(s) for s in list(range(1,17))+[20,24,32,64,128]],
             non_sc=dict(rows=[[0,0,2],[0,2,2]],mergeable_pair=[0,1],prefix=[1],deadlock_image=[0,2]),
             boundary='PROVED paper stable defect-one kernel for SC inputs with arbitrary other ranks; SC all corank<=1 mergeability equals stability and least group quotient, unique minimum-rank kernel, class-size range<=number of singular letters, sharp EVERY s>=1. Finite computational scopes only; qualitative reconstruction/generalization, priority and general Cerny OPEN, no formal kernel or short reset bound.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(scopes=out['scopes'],sharp_parameters=len(out['sharp_families']),maximum_n=max(z['n'] for z in out['sharp_families']))),flush=True)


if __name__=='__main__':main()
