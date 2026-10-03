"""Exact all-subset extension maximum from the ordered-pair conjugate graph."""
from collections import deque

def split(rows):
    n=len(rows[0]);assert n>=2 and all(len(r)==n for r in rows)
    P=[];U=[]
    for i,row in enumerate(rows):
        assert all(type(q)==int and 0<=q<n for q in row)
        if sorted(row)==list(range(n)):P.append(i)
        else:
            change=[q for q in range(n) if row[q]!=q];assert len(change)==1
            s=change[0];U.append((i,s,row[s]))
    assert U
    return P,U

def strong(n,arcs):
    out=[[] for _ in range(n)];rev=[[] for _ in range(n)]
    for s,t in arcs:out[s].append(t);rev[t].append(s)
    for graph in [out,rev]:
        seen={0};queue=[0]
        for s in queue:
            for t in graph[s]:
                if t not in seen:seen.add(t);queue.append(t)
        if len(seen)!=n:return False
    return True

def forward_closed(n,arcs):
    out=[[] for _ in range(n)]
    for s,t in arcs:out[s].append(t)
    for start in range(n):
        seen={start};queue=[start]
        for s in queue:
            for t in out[s]:
                if t not in seen:seen.add(t);queue.append(t)
        if len(seen)<n:return seen
    raise AssertionError('Graph is already strongly connected')

def profile(rows,details=False):
    n=len(rows[0]);P,U=split(rows);d={};parents={};origins={};queue=[]
    for i,s,t in U:
        if (s,t) not in d:d[s,t]=0;parents[s,t]=None;origins[s,t]=i;queue.append((s,t))
    for s,t in queue:
        for i in P:
            a=rows[i];pair=(a[s],a[t])
            if pair not in d:
                d[pair]=d[s,t]+1;parents[pair]=((s,t),i);origins[pair]=origins[s,t];queue.append(pair)
    if not strong(n,d):return None
    bylevel={}
    for pair,v in d.items():bylevel.setdefault(v,[]).append(pair)
    arcs=set();threshold=None
    for level in sorted(bylevel):
        previous=set(arcs);arcs.update(bylevel[level])
        if strong(n,arcs):threshold=level+1;break
    assert threshold is not None
    closed=forward_closed(n,previous);S=set(range(n))-closed
    growing=[pair for pair,v in d.items() if pair[0] not in S and pair[1] in S]
    pair=min(growing,key=lambda pair:(d[pair],pair));assert d[pair]+1==threshold
    letters=[];q=pair
    while parents[q] is not None:
        q,i=parents[q];letters.append(i)
    word=[origins[pair]]+list(reversed(letters))
    T={q for q in range(n) if _image(q,word,rows) in S}
    assert len(T)==len(S)+1 and len(word)==threshold
    # Group orbit count is independent of the unit arcs.
    unseen=set(range(n));orbits=[]
    while unseen:
        start=min(unseen);C={start};bfs=[start]
        for s in bfs:
            for i in P:
                t=rows[i][s]
                if t not in C:C.add(t);bfs.append(t)
        unseen-=C;orbits.append(sorted(C))
    result=dict(n=n,rows=rows,max_extension=threshold,pair_vertices=len(d),group_orbits=orbits,
                target=sorted(S),larger_preimage=sorted(T),extension_word=word,
                commuting=all(rows[i][rows[j][q]]==rows[j][rows[i][q]] for i in P for j in P for q in range(n)))
    if details:
        result['pairs']=[dict(source=s,target=t,distance=d[s,t],origin=origins[s,t],
                              parent=None if parents[s,t] is None else [list(parents[s,t][0]),parents[s,t][1]]) for s,t in queue]
    return result

def _image(q,word,rows):
    for i in word:q=rows[i][q]
    return q
