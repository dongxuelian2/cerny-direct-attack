"""Right action: S(uv)=(Su)v. All nonempty-subset distances are exact."""
from collections import deque
from itertools import combinations, permutations

def table(row):
    out = [0] * (1 << len(row))
    for s in range(1, len(out)):
        b = s & -s
        out[s] = out[s ^ b] | (1 << row[b.bit_length()-1])
    return out

def graph(rows):
    ts = [table(r) for r in rows]
    return [tuple(t[s] for t in ts) for s in range(len(ts[0]))]

def bfs(g, starts):
    d = [-1] * len(g)
    q = deque(starts)
    for s in starts: d[s] = 0
    while q:
        s = q.popleft()
        for t in g[s]:
            if d[t] < 0:
                d[t] = d[s]+1
                q.append(t)
    return d

def reverse(g):
    rev = [[] for _ in g]
    for s, row in enumerate(g):
        for t in row: rev[t].append(s)
    return rev

def strongly_connected(rows):
    g = [tuple(r[q] for r in rows) for q in range(len(rows[0]))]
    return all(x >= 0 for x in bfs(g, [0])) and all(x >= 0 for x in bfs(reverse(g), [0]))

def canonical(rows):
    best = None
    for p in permutations(range(len(rows[0]))):
        new = []
        for row in rows:
            r = [0] * len(row)
            for q in range(len(row)): r[p[q]] = p[row[q]]
            new.append(tuple(r))
        key = tuple(sorted(new))
        if best is None or key < best: best = key
    return best

def canonical_map(row, perms):
    best = tuple(row)
    for p in perms:
        r = [0] * len(row)
        for q in range(len(row)): r[p[q]] = p[row[q]]
        best = min(best, tuple(r))
    return best

def analyze(rows):
    n = len(rows[0])
    g = graph(rows)
    d = bfs(reverse(g), [1 << q for q in range(n)])
    if d[-1] < 0: return None
    f = bfs(g, [len(g)-1])
    sizes = [s.bit_count() for s in range(len(g))]
    c = [-1] * len(g)
    pair = {s:d[s] for s in range(1,len(g)) if sizes[s] == 2}
    for s in range(1,len(g)):
        if sizes[s] >= 2:
            qs = [q for q in range(n) if s >> q & 1]
            c[s] = min(pair[(1<<p)|(1<<q)] for p,q in combinations(qs,2))
    # Earliest possible first rank drop, optimizing over ALL tie choices.
    greedy_min, greedy_max = [0]*len(g), [0]*len(g)
    for s in sorted(range(1,len(g)),key=lambda s:(sizes[s],c[s])):
        if sizes[s] == 1: continue
        allowed = [t for t in g[s] if (sizes[t]<sizes[s] and c[s]==1)
                   or (sizes[t]==sizes[s] and c[t]==c[s]-1)]
        assert allowed
        greedy_min[s] = 1+min(greedy_min[t] for t in allowed)
        greedy_max[s] = 1+max(greedy_max[t] for t in allowed)
    lam = [min(f[s] for s in range(1,len(g)) if f[s]>=0 and sizes[s]<=n-r) for r in range(n)]
    avoiding = [min((f[s] for s in range(1,len(g)) if f[s]>=0 and not (s>>q&1)),default=None) for q in range(n)]
    word, s = [], len(g)-1
    while d[s]:
        a = next(a for a,t in enumerate(g[s]) if d[t]==d[s]-1)
        word.append(a)
        s = g[s][a]
    return dict(n=n,rows=rows,graph=g,distance=d,forward=f,compression=c,
                greedy_min=greedy_min,greedy_max=greedy_max,lambda_corank=lam,
                gaps=[lam[r+1]-lam[r] for r in range(n-1)],avoiding=avoiding,word=word,rt=d[-1],
                max_compression_by_rank=[max((c[s] for s in range(1,len(g)) if sizes[s]==k),default=-1) for k in range(n+1)],
                max_reachable_compression_by_rank=[max((c[s] for s in range(1,len(g)) if sizes[s]==k and f[s]>=0),default=-1) for k in range(n+1)])

def first_drop_endpoints(g,s):
    k = s.bit_count()
    dist, queue, ends = {s:0}, deque([s]), {}
    while queue:
        x = queue.popleft()
        for t in g[x]:
            cost = dist[x]+1
            if t.bit_count()<k: ends[t] = min(ends.get(t,cost),cost)
            elif t not in dist:
                dist[t] = cost
                queue.append(t)
    return ends

def enrich(p,semigroup_limit=200000):
    n,g,d = p['n'],p['graph'],p['distance']
    bottleneck,capped,ob = [0]*len(g),[None]*len(g),[0]*len(g)
    for s in sorted(range(1,len(g)),key=int.bit_count):
        if s.bit_count()==1:
            capped[s] = 0
            continue
        ends = first_drop_endpoints(g,s)
        bottleneck[s] = min(max(cost,bottleneck[t]) for t,cost in ends.items())
        capped[s] = min((cost+capped[t] for t,cost in ends.items() if cost<=n and capped[t] is not None),default=None)
        ob[s] = min(max(cost,ob[t]) for t,cost in ends.items() if cost+d[t]==d[s])
    pre = [[sum(1<<q for q in range(n) if s>>row[q]&1) for row in p['rows']] for s in range(len(g))]
    extension = [-1]*len(g)
    for s in range(1,len(g)-1):
        ds = bfs(pre,[s])
        extension[s] = min(ds[t] for t in range(1,len(g)) if ds[t]>=0 and t.bit_count()>s.bit_count())
    identity = tuple(range(n))
    seen,queue,complete = {identity},deque([identity]),True
    while queue:
        t = queue.popleft()
        for row in p['rows']:
            u = tuple(row[q] for q in t)
            if u not in seen:
                seen.add(u)
                queue.append(u)
        if len(seen)>semigroup_limit:
            complete = False
            break
    return dict(bottleneck=bottleneck,capped_n=capped,optimal_bottleneck=ob,extension=extension,
                semigroup_size=len(seen),semigroup_complete=complete,
                semigroup_rank_distribution=[sum(len(set(t))==k for t in seen) for k in range(n+1)])

def public(p): return {k:v for k,v in p.items() if k!='graph'}

def certificate(p):
    n = p['n']
    return dict(schema='orion.sync-certificate.v1',kind='exact',
                automaton=dict(n=n,letters=[chr(97+i) for i in range(len(p['rows']))],transitions=[list(r) for r in p['rows']]),
                potential=[0]+p['distance'][1:],word=p['word'],lower_bound=p['rt'],upper_bound=p['rt'],
                method='direct_attack_reverse_bfs')
