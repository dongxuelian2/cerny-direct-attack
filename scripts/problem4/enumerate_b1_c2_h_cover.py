"""Outside-C injective kernel admission for B=0,C=12 at thirteen states."""
from itertools import combinations,product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={1,2}

def partition(X):
    if not X:yield [];return
    q=min(X)
    for old in partition(X-{q}):
        yield [frozenset({q}),*old]
        if q in A|B:continue
        for i,block in enumerate(old):
            if block&(A|B) or len((set(block)|{q})-C)>1:continue
            yield [*old[:i],block|{q},*old[i+1:]]

def K(fields):return {tuple(z) for f in fields for b in f for z in combinations(sorted(b),2)}

def patterns(n,row):
    inputs=[set(row[k]) for k in ('preA','preB','preC')];inputs.append(set(range(n))-set().union(*inputs))
    choices=[[p for p in partition(X) if len(p)<=cap] for X,cap in zip(inputs,[1,1,2,n-4])]
    return [dict(fields=[[sorted(b) for b in p] for p in fs],kernel=[list(p) for p in sorted(K(fs))])
        for fs in product(*choices)]

def inventory(n=13):
    data=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'));profiles=[]
    for old in data['records']:
        if old['joint_id']!='b1_in_c4':continue
        rows=[dict(preA=v['preA'],preB=v['preB'],preC=v['preC'],patterns=patterns(n,v)) for v in old['rows']]
        pairs=[]
        for x,y in old['binary_profile_pairs']:
            pairs.append(dict(rows=[x,y],kernel_pairs=[[i,j] for i,j in product(range(len(rows[x]['patterns'])),range(len(rows[y]['patterns'])))]))
        profiles.append(dict(id=old['id'],D=old['D'],rows=rows,pairs=pairs))
    return dict(status='necessary_outside_C_injective_inventory',n=n,parameter=[13,9,1],profiles=profiles,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
            [Path(__file__).name,'small_first_third_inventory.json']},
        scope='Complete kernel admission under C-cover and protected isolation; no C3 kernel budget or full transition scan.')

if __name__=='__main__':
    result=inventory();(ROOT/'b1_c2_h_cover_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(D=v['D'],original_pairs=len(v['pairs']),row_patterns=sum(len(r['patterns']) for r in v['rows']),
        kernel_pairs=sum(len(p['kernel_pairs']) for p in v['pairs'])) for v in result['profiles']]))
