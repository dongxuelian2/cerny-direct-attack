"""Complete E16 field-kernel admission, retaining ordinary extra2 pairs."""
from pathlib import Path
from itertools import combinations,product
import hashlib,json
ROOT=Path(__file__).resolve().parent
K={1,2};PROTECTED={0,3,5}
def partitions(X):
    if not X:yield [];return
    q=min(X)
    for old in partitions(X-{q}):
        yield [frozenset({q}),*old]
        for i,block in enumerate(old):
            enlarged=block|{q}
            if len(enlarged-K)>1 or enlarged&PROTECTED:continue
            yield [*old[:i],enlarged,*old[i+1:]]
def patterns(row):
    fields=[set(row[key]) for key in ('preA','preB','preC','preD')]
    fields.append(set(range(13))-set().union(*fields))
    return [dict(fields=[[sorted(b) for b in p] for p in parts],kernel=[list(edge) for edge in sorted(
        {edge for p in parts for block in p for edge in combinations(sorted(block),2)})])
        for parts in product(*[[p for p in partitions(X) if len(p)<=cap] for X,cap in zip(fields,[1,1,2,1,8])])]
def inventory():
    old=json.loads((ROOT/'b1_partial_cover_fourth_inventory.json').read_text(encoding='utf-8'))
    source=next(z for z in old['records'] if z['E']==[1,6])
    rows=[dict(old_row=v['old_row'],preA=v['preA'],preB=v['preB'],preC=v['preC'],preD=v['preD'],patterns=patterns(v)) for v in source['rows']]
    pairs=[dict(original_third_rows=p['original_rows'],rows=[x,y],kernel_pairs=[list(ij) for ij in
        product(range(len(rows[x]['patterns'])),range(len(rows[y]['patterns'])))]) for p in source['pairs'] for x,y in p['fourth_field_pairs']]
    names=[Path(__file__).name,'b1_partial_cover_fourth_inventory.json']
    return dict(status='necessary_E16_kernel_inventory',parameter=[13,9,1],E=[1,6],rows=rows,pairs=pairs,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='All original E16 field pairs with K12-covered protected kernels; no outside-C injectivity or higher-layer edge cap.')
if __name__=='__main__':
    result=inventory();(ROOT/'b1_partial_cover_e16_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(field_pairs=len(result['pairs']),row_patterns=sum(len(r['patterns']) for r in result['rows']),
        kernel_pairs=sum(len(p['kernel_pairs']) for p in result['pairs']))))
