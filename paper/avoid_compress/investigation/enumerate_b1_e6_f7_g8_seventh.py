"""All K-covered kernel partitions for four paired seventh fibers.

This preserves all parent field pairs; the inventory itself makes no
exclusion claim. Kernel assignments are not complete transition rows.
"""
from itertools import combinations, product
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));K={1,2};P={0,3,5,6,7,8}
KEYS=('preA','preB','preC','preD','preE','preF','preG')
CAPS=(1,1,2,1,1,1,1,5)

def partitions(X):
    if not X:
        yield [];return
    q=min(X)
    for old in partitions(X-{q}):
        yield [frozenset({q}),*old]
        for i,block in enumerate(old):
            enlarged=block|{q}
            if len(enlarged-K)>1 or enlarged&P:continue
            yield [*old[:i],enlarged,*old[i+1:]]

def patterns(row):
    groups=[set(row[key]) for key in KEYS]
    groups.append(Q-set().union(*groups))
    return [dict(fields=[[sorted(b) for b in part] for part in parts],
        kernel=[list(e) for e in sorted({e for part in parts for block in part
            for e in combinations(sorted(block),2)})])
        for parts in product(*[[v for v in partitions(X) if len(v)<=cap]
            for X,cap in zip(groups,CAPS)])]

def main():
    parent=json.loads((ROOT/'b1_seventh_inventory.json').read_text(encoding='utf-8'))
    profiles=[]
    for z in parent['records']:
        if z['H'] not in ([1,2],[1,9],[2,4],[1,2,9]):continue
        assert z['mandatory_through_four']==sorted(P)
        rows=[dict(parent_row=i,**{key:row[key] for key in KEYS},
            patterns=patterns(row)) for i,row in enumerate(z['rows'])]
        pairs=[dict(original_third_rows=p['original_third_rows'],
            original_fourth_rows=p['original_fourth_rows'],
            original_fifth_rows=p['original_fifth_rows'],
            original_sixth_rows=p['original_sixth_rows'],rows=[x,y],
            kernel_pairs=[list(ij) for ij in product(range(len(rows[x]['patterns'])),
                range(len(rows[y]['patterns'])))])
            for p in z['pairs'] for x,y in p['seventh_field_pairs']]
        profiles.append(dict(id=z['id'],H=z['H'],protected=sorted(P),rows=rows,pairs=pairs))
    assert len(profiles)==4
    names=[Path(__file__).name,'b1_seventh_inventory.json',
        'B1_E6_F7_G8_PAIRED_SEVENTH_EXCLUSIONS.md','MANDATORY_CORE_ISOLATION.md']
    result=dict(status='necessary_paired_seventh_kernel_inventory',parameter=[13,9,1],
        branch=dict(E=[6],F=[7],G=[8]),profiles=profiles,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Every original field pair and K-covered protected kernel partition for four paired H geometries. Necessary admission only; generator does not prove exclusions or automaton existence.')
    (ROOT/'b1_e6_f7_g8_seventh_kernel_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(H=z['H'],field_pairs=len(z['pairs']),
        row_patterns=sum(len(r['patterns']) for r in z['rows']),
        kernel_pairs=sum(len(p['kernel_pairs']) for p in z['pairs'])) for z in profiles]))
if __name__=='__main__':main()
