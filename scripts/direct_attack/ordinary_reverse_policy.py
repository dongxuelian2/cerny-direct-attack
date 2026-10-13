"""Independent per-target reverse BFS of the ordinary reachable-image graph."""
from collections import deque


def profile(rows):
    Q=frozenset(range(len(rows[0])));R=[Q];index={Q:0};forward=[0];edges=[]
    for i,T in enumerate(R):
        children=[]
        for row in rows:
            U=frozenset(row[q] for q in T)
            if U not in index:index[U]=len(R);R.append(U);forward.append(forward[i]+1)
            children.append(index[U])
        edges.append(children)
    if any(frozenset([q]) not in index for q in range(len(rows[0]))):return None
    reverse=[[] for T in R]
    for i,children in enumerate(edges):
        for j in children:reverse[j].append(i)
    e={};G={0:0};W={0:0}
    for si in sorted(range(1,len(R)),key=lambda i:len(R[i]),reverse=True):
        S=R[si];d=[-1]*len(R);queue=deque()
        for i,T in enumerate(R):
            if T<=S:d[i]=0;queue.append(i)
        while queue:
            i=queue.popleft()
            for j in reverse[i]:
                if d[j]<0:d[j]=d[i]+1;queue.append(j)
        cost=min(d[i] for i,T in enumerate(R) if len(T)>len(S) and d[i]>=0)
        assert cost>0
        winners=[i for i,T in enumerate(R) if len(T)>len(S) and d[i]==cost]
        e[si]=cost;G[si]=cost+min(G[i] for i in winners);W[si]=cost+max(W[i] for i in winners)
    mask=lambda T:sum(1<<q for q in T)
    return dict(extension={mask(R[i]):v for i,v in e.items()},best={mask(R[i]):v for i,v in G.items()},
                worst={mask(R[i]):v for i,v in W.items()},forward={mask(R[i]):v for i,v in enumerate(forward)})
