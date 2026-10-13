"""Conservative simultaneous-alphabet conjugations of current flag children."""
from collections import deque
from hashlib import sha256

def move(mask,p):
    return sum(1<<p[q] for q in range(len(p)) if mask>>q&1)

def quotient(rows,active,required,basis,fixed,edges,known,choices,index=None,max_active=100000):
    choices=sorted(choices)
    if len(choices)<2 or active.bit_count()>max_active:return None
    n=len(rows[0]);ids=[];bits=active
    assert 0<=active and active.bit_length()<=len(rows) and all(g>=0 for g in required)
    assert set(fixed)<=set(range(n)) and all(0<=m<1<<n for m in [*basis,*known,*choices])
    while bits:
        bit=bits&-bits;bits-=bit;ids.append(bit.bit_length()-1)
    assert all(len(rows[i])==n and all(0<=q<n for q in rows[i]) for i in ids)
    index=index if index is not None else {tuple(r):i for i,r in enumerate(rows)}
    assert len(index)==len(rows)
    constraints=list(basis)+sorted(known);fixed=set(fixed);edges=set(map(tuple,edges));cells={}
    for q in range(n):
        if q in fixed:continue
        cells.setdefault(tuple(bool(m>>q&1) for m in constraints),[]).append(q)
    candidates=[];choice_set=set(choices)
    for cell in cells.values():
        for a,b in zip(cell,cell[1:]):
            if all(bool(m>>a&1)==bool(m>>b&1) for m in choices):continue
            p=list(range(n));p[a],p[b]=p[b],p[a]
            if {tuple(sorted((p[u],p[v]))) for u,v in edges}!=edges:continue
            if any(move(m,p) not in choice_set for m in choices):continue
            candidates.append(p)
    if not candidates:return None
    membership={i:sum(1<<j for j,g in enumerate(required) if g>>i&1) for i in ids}
    generators=[]
    for p in candidates:
        transport=[]
        for i in ids:
            row=rows[i];new=[None]*n
            for q in range(n):new[p[q]]=p[row[q]]
            j=index.get(tuple(new))
            if j is None or not(active>>j&1) or membership[i]!=membership[j]:break
            transport.append((i,j))
        else:
            assert len({j for i,j in transport})==len(ids)
            h=sha256()
            for i,j in transport:h.update(i.to_bytes(4,'little')+j.to_bytes(4,'little'))
            generators.append(dict(permutation=p,active_row_transport_sha256=h.hexdigest(),active_rows=len(ids)))
    if not generators:return None
    unseen=set(choices);transports=[];representatives=[]
    while unseen:
        rep=min(unseen);representatives.append(rep);unseen.remove(rep)
        paths={rep:()};todo=deque([rep])
        while todo:
            m=todo.popleft()
            for g,record in enumerate(generators):
                y=move(m,record['permutation']);assert y in choice_set
                if y not in paths:
                    paths[y]=paths[m]+(g,);todo.append(y);unseen.discard(y)
        for m,path in paths.items():transports.append(dict(image=m,representative=rep,steps=list(reversed(path))))
    if len(representatives)==len(choices):return None
    return dict(fixed_states=sorted(fixed),generators=generators,representatives=representatives,
                transports=sorted(transports,key=lambda z:z['image']),choices=len(choices))
