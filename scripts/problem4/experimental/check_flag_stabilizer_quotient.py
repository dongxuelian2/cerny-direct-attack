"""Independent literal conjugation and complete child-transport verification."""
from hashlib import sha256

def relabel(states,p):return {p[q] for q in states}
def as_set(mask,n):return {q for q in range(n) if mask&(1<<q)}

def check_quotient(rows,active,required,basis,fixed,edges,known,choices,proof,index=None):
    n=len(rows[0]);indices=[i for i in range(len(rows)) if active&(1<<i)]
    assert 0<=active and active.bit_length()<=len(rows) and all(g>=0 for g in required)
    assert set(fixed)<=set(range(n)) and all(0<=m<1<<n for m in [*basis,*known,*choices])
    assert indices and rows and all(len(row)==n and set(row)<=set(range(n)) for row in rows)
    index=index if index is not None else {tuple(row):i for i,row in enumerate(rows)}
    assert len(index)==len(rows)
    index_set=set(indices)
    domains=[{i for i in indices if g&(1<<i)} for g in required]
    fixed=set(fixed);edges={frozenset(e) for e in edges};targets=set(choices)
    assert proof['fixed_states']==sorted(fixed) and proof['choices']==len(targets)==len(choices)
    assert proof['generators'] and len(targets)>=2
    for record in proof['generators']:
        p=record['permutation'];assert len(p)==n and set(p)==set(range(n))
        # The stored generators are involutions; reverse a path to invert it.
        assert all(p[p[q]]==q for q in range(n))
        assert all(p[q]==q for q in fixed)
        assert all(relabel(as_set(m,n),p)==as_set(m,n) for m in [*basis,*known])
        assert {frozenset(p[q] for q in e) for e in edges}==edges
        assert {sum(1<<q for q in relabel(as_set(m,n),p)) for m in targets}==targets
        rowmap={};h=sha256()
        for i in indices:
            candidate=[None]*n
            for source,target in enumerate(rows[i]):candidate[p[source]]=p[target]
            j=index.get(tuple(candidate));assert j is not None and j in index_set
            assert list(rows[j])==candidate
            rowmap[i]=j;h.update(i.to_bytes(4,'little')+j.to_bytes(4,'little'))
        assert len(set(rowmap.values()))==len(indices)
        assert record['active_rows']==len(indices) and record['active_row_transport_sha256']==h.hexdigest()
        assert all({rowmap[i] for i in R}==R for R in domains)
    reps=proof['representatives'];assert reps==sorted(set(reps)) and set(reps)<=targets
    transports=proof['transports'];assert [z['image'] for z in transports]==sorted(targets)
    represented=set()
    for record in transports:
        m=record['image'];rep=record['representative'];assert rep in reps
        states=as_set(m,n)
        for g in record['steps']:
            assert isinstance(g,int) and 0<=g<len(proof['generators'])
            states=relabel(states,proof['generators'][g]['permutation'])
        assert states==as_set(rep,n);represented.add(rep)
        if m==rep:assert not record['steps']
    assert represented==set(reps) and len(reps)<len(targets)
    return dict(choices=len(targets),representatives=len(reps),omitted=len(targets)-len(reps),generators=len(proof['generators']))
