"""Necessary complete kernels for binary E6/F17 and F24 fields."""
from itertools import combinations,product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
K={1,2};P={0,3,5,6};KEYS=('preA','preB','preC','preD','preE')
def partitions(X):
    if not X:yield [];return
    q=min(X)
    for old in partitions(X-{q}):
        yield [frozenset({q}),*old]
        for i,block in enumerate(old):
            enlarged=block|{q}
            if len(enlarged-K)>1 or enlarged&P:continue
            yield [*old[:i],enlarged,*old[i+1:]]
def patterns(row):
    fields=[set(row[key]) for key in KEYS];fields.append(set(range(13))-set().union(*fields))
    return [dict(fields=[[sorted(block) for block in part] for part in parts],
        kernel=[list(edge) for edge in sorted({edge for part in parts for block in part for edge in combinations(sorted(block),2)})])
        for parts in product(*[[v for v in partitions(X) if len(v)<=cap] for X,cap in zip(fields,[1,1,2,1,1,7])])]
def main():
    inv=json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'));profiles=[]
    for z in inv['records']:
        if z['E']!=[6] or z['F'] not in ([1,7],[2,4]):continue
        rows=[dict(parent_row=i,**{key:row[key] for key in KEYS},patterns=patterns(row)) for i,row in enumerate(z['rows'])]
        pairs=[dict(original_third_rows=p['original_third_rows'],original_fourth_rows=p['original_fourth_rows'],rows=[x,y],
            kernel_pairs=[list(ij) for ij in product(range(len(rows[x]['patterns'])),range(len(rows[y]['patterns'])))])
            for p in z['pairs'] for x,y in p['fifth_field_pairs']]
        profiles.append(dict(id=z['id'],E=z['E'],F=z['F'],rows=rows,pairs=pairs))
    assert len(profiles)==2 and all(len(z['pairs'])==12 for z in profiles)
    names=[Path(__file__).name,'b1_fifth_inventory.json']
    result=dict(status='necessary_overlap_fifth_kernel_inventory',parameter=[13,9,1],profiles=profiles,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='All original F17/F24 fifth field pairs with every protected K-cover kernel and unused row. No existence/exclusion or F value claimed by this generator.')
    (ROOT/'b1_e6_overlap_fifth_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(F=z['F'],field_pairs=len(z['pairs']),row_patterns=sum(len(r['patterns']) for r in z['rows']),
        kernel_pairs=sum(len(p['kernel_pairs']) for p in z['pairs'])) for z in profiles]))
if __name__=='__main__':main()
