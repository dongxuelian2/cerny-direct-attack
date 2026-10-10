"""Kernel admission for B0,C14, with effective cover K12, not C.

No original typed row/profile pair is silently discarded. This is only
necessary finite admission, not a transition-table existence theorem.
"""
from itertools import combinations,product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={1,4};K={1,2};PROTECTED=A|B

def partitions(X):
    if not X:yield [];return
    q=min(X)
    for old in partitions(X-{q}):
        yield [frozenset({q}),*old]
        if q in PROTECTED:continue
        for i,block in enumerate(old):
            enlarged=block|{q}
            if block&PROTECTED or len(enlarged-K)>1:continue
            yield [*old[:i],enlarged,*old[i+1:]]

def edges(fields):return {tuple(p) for field in fields for block in field for p in combinations(sorted(block),2)}

def patterns(n,row,D):
    # A singleton D is mandatory through eight, hence isolated in P4.
    # At depth one no such point can share any kernel block.
    protected=PROTECTED|(D if len(D)==1 else set())
    inputs=[set(row[key]) for key in ('preA','preB','preC')]
    inputs.append(set(range(n))-set().union(*inputs))
    answer=[]
    for fields in product(*[[p for p in partitions(X) if len(p)<=cap]
                            for X,cap in zip(inputs,[1,1,2,n-4])]):
        kernel=edges(fields)
        if any(set(pair)&protected for pair in kernel):continue
        answer.append(dict(fields=[[sorted(block) for block in field] for field in fields],
                           kernel=[list(p) for p in sorted(kernel)]))
    return answer

def inventory(n=13):
    old=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    profiles=[]
    for record in old['records']:
        if record['joint_id']!='b1_in_c3':continue
        D=set(record['D'])
        rows=[dict(preA=r['preA'],preB=r['preB'],preC=r['preC'],patterns=patterns(n,r,D)) for r in record['rows']]
        pairs=[dict(rows=[x,y],kernel_pairs=[[i,j] for i,j in product(range(len(rows[x]['patterns'])),range(len(rows[y]['patterns'])))])
               for x,y in record['binary_profile_pairs']]
        profiles.append(dict(id=record['id'],D=record['D'],rows=rows,pairs=pairs))
    return dict(status='necessary_partial_cover_inventory',parameter=[13,9,1],n=n,cover=[1,2],C=[1,4],
        profiles=profiles,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
            [Path(__file__).name,'small_first_third_inventory.json']},
        scope='Complete kernel admission under K12 cover and protected singleton isolation. K is not C. '
              'No full row search, geometric exclusion, F value or alphabet separation.')

if __name__=='__main__':
    result=inventory();(ROOT/'b1_partial_cover_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(D=z['D'],original_pairs=len(z['pairs']),row_patterns=sum(len(r['patterns']) for r in z['rows']),
        kernel_pairs=sum(len(p['kernel_pairs']) for p in z['pairs'])) for z in result['profiles']]))
