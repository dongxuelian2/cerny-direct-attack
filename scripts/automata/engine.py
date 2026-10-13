"""Finite-state synchronization search and experimental abstraction baselines."""
from __future__ import annotations
from collections import deque
from pathlib import Path
import json
import time
from .check_certificate import validate_automaton, check

SEED = 20260927

def cerny(n: int) -> dict:
    if not 2<=n<=16:
        raise ValueError('Cerny instances require 2 <= n <= 16')
    return {'name':f'Cerny C{n}', 'n':n, 'letters':['a','b'],
            'transitions':[[(q+1)%n for q in range(n)],list(range(n-1))+[0]]}

def image(mask: int, row: list[int]) -> int:
    out=0
    while mask:
        bit=mask & -mask
        out |= 1 << row[bit.bit_length()-1]
        mask ^= bit
    return out

def build_graph(a: dict) -> list[list[int]]:
    n,letters,rows=validate_automaton(a)
    return [[image(s,row) for row in rows] for s in range(1<<n)]

def distances(graph: list[list[int]], goals: list[int]) -> list[int]:
    reverse=[[] for _ in graph]
    for s,row in enumerate(graph):
        for t in row:
            reverse[t].append(s)
    d=[-1]*len(graph)
    queue=deque()
    for g in goals:
        d[g]=0
        queue.append(g)
    while queue:
        t=queue.popleft()
        for s in reverse[t]:
            if d[s]<0:
                d[s]=d[t]+1
                queue.append(s)
    return d

def exact(a: dict) -> dict:
    n,letters,rows=validate_automaton(a)
    graph=build_graph(a)
    d=distances(graph,[1<<q for q in range(n)])
    full=(1<<n)-1
    base={'schema':'orion.sync-certificate.v1','automaton':a}
    if d[full]<0:
        visited={full}
        queue=deque([full])
        while queue:
            s=queue.popleft()
            for t in graph[s]:
                if t not in visited:
                    visited.add(t);queue.append(t)
        cert={**base,'kind':'nonsynchronizing','closed_masks':sorted(visited)}
    else:
        # If Q synchronizes, every nonempty subset does too.
        if any(v<0 for v in d[1:]):
            raise RuntimeError('Unexpected unreachable nonempty subset')
        d[0]=0
        word=[]
        s=full
        while d[s]>0:
            x=next(i for i,t in enumerate(graph[s]) if d[t]==d[s]-1)
            word.append(x);s=graph[s][x]
        cert={**base,'kind':'exact','potential':d,'word':word,
              'lower_bound':d[full],'upper_bound':len(word),'method':'reverse_bfs'}
    check(cert)
    return cert

def feature(mask: int,n: int,mode: str) -> tuple:
    qs=[q for q in range(n) if mask>>q & 1]
    k=len(qs)
    if mode=='cardinality':
        return (k,)
    if mode=='marked':
        return (k,int(0 in qs),int(n-1 in qs))
    gaps=[(qs[(i+1)%k]-q)%n or n for i,q in enumerate(qs)]
    if mode=='maxgap':
        return (k,max(gaps))
    if mode=='gap_multiset':
        return (k,*sorted(gaps))
    if mode=='identity':
        return (mask,)
    raise ValueError(f'Unknown feature: {mode}')

FEATURES=('cardinality','marked','maxgap','gap_multiset','identity')

def abstract(a: dict, mode: str, exact_cert: dict | None=None) -> tuple[dict,dict]:
    start=time.perf_counter()
    n,_,_=validate_automaton(a)
    ex=exact_cert or exact(a)
    if ex['kind']=='nonsynchronizing':
        raise ValueError('Abstraction experiment requires a synchronizing automaton')
    graph=build_graph(a)
    ids={}
    alpha=[-1]*(1<<n)
    for s in range(1,1<<n):
        key=feature(s,n,mode)
        if key not in ids:
            ids[key]=len(ids)
        alpha[s]=ids[key]
    abstract_edges=[set() for _ in ids]
    for s in range(1,1<<n):
        for t in graph[s]:
            abstract_edges[alpha[s]].add(alpha[t])
    goal_classes=sorted({alpha[1<<q] for q in range(n)})
    ad=distances([sorted(es) for es in abstract_edges],goal_classes)
    if any(x<0 for x in ad):
        raise RuntimeError('Abstract class cannot reach a singleton')
    d=[0]+[ad[alpha[s]] for s in range(1,1<<n)]
    lower,upper=d[-1],ex['upper_bound']
    cert={'schema':'orion.sync-certificate.v1','kind':'exact' if lower==upper else 'bounds',
          'automaton':a,'potential':d,'word':ex['word'],
          'lower_bound':lower,'upper_bound':upper,'method':f'feature_quotient:{mode}'}
    check(cert)
    data={'n':n,'feature':mode,'concrete_subsets':(1<<n)-1,
          'abstract_classes':len(ids),'lower_bound':lower,'optimal_length':upper,
          'bound_ratio':round(lower/upper,6) if upper else 1.0,
          'construction_seconds':round(time.perf_counter()-start,6),
          'expanded_certificate_bytes':len(json.dumps(cert).encode('utf-8')),
          'note':'All concrete subsets were enumerated; no asymptotic speedup claimed.'}
    return cert,data

def write_json(path: str | Path,obj: dict) -> None:
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def forward_distance(a: dict) -> int | None:
    # Independent-direction cross-check; not used by certificate construction.
    n,_,rows=validate_automaton(a)
    start=(1<<n)-1
    queue=deque([(start,0)]);seen={start}
    while queue:
        s,l=queue.popleft()
        if s & (s-1)==0:
            return l
        for row in rows:
            t=image(s,row)
            if t not in seen:
                seen.add(t);queue.append((t,l+1))
    return None

def landmark_experiment(a: dict, r: int) -> tuple[dict,dict]:
    """Track cardinality plus r anchored bits: 0, n-1, n-2, ... .
    The concrete powerset is still enumerated; this is a research baseline.
    """
    n,_,_=validate_automaton(a)
    if not 0<=r<=n:
        raise ValueError('r must be in [0,n]')
    ex=exact(a)
    if ex['kind']=='nonsynchronizing':
        raise ValueError('A synchronizing input is required')
    anchors=([0]+list(range(n-1,n-r,-1))) if r else []
    ids={};alpha=[-1]*(1<<n);g=build_graph(a)
    for s in range(1,1<<n):
        key=(s.bit_count(),*(s>>q&1 for q in anchors))
        if key not in ids:ids[key]=len(ids)
        alpha[s]=ids[key]
    ag=[set() for _ in ids]
    for s in range(1,1<<n):
        for t in g[s]:ag[alpha[s]].add(alpha[t])
    d=distances([sorted(x) for x in ag],sorted({alpha[1<<q] for q in range(n)}))
    pd=[0]+[d[alpha[s]] for s in range(1,1<<n)]
    low,up=pd[-1],ex['upper_bound']
    cert={'schema':'orion.sync-certificate.v1','kind':'exact' if low==up else 'bounds',
          'automaton':a,'potential':pd,'word':ex['word'],'lower_bound':low,'upper_bound':up,
          'method':f'landmarks:{r}'}
    check(cert)
    row={'n':n,'r':r,'anchors':','.join(map(str,anchors)),
         'abstract_classes':len(ids),'lower_bound':low,'optimal_length':up,
         'bound_ratio':round(low/up,6) if up else 1.0}
    return cert,row
