"""Complete unfiltered first-pair scope for the small retained control.

Canonicalization need not identify every symmetry orbit: it transports
every labelled pair and its whole P1 graph to a stored representative.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import hashlib,json
from c1_word_staircase_letter_generator import pool
from enumerate_c1_word_staircase import tree
ROOT=Path(__file__).resolve().parent
PAIRS=list(combinations(range(13),2));BITS={e:1<<i for i,e in enumerate(PAIRS)}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    frozen=read('b2_c5_first_pair_scope.json');active=read(frozen['baseline']);cp=read(frozen['checkpoint'])
    for n,h in frozen['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert sha(ROOT/frozen['baseline'])==cp['source_sha256']['active_research.json']
    name='b2_mixed_c5_third3';z=next(z for z in read('small_first_third_inventory.json')['records'] if z['id']==name)
    parent=next(z for z in read('b1_b2_inverse_union_inventory.json')['records'] if z['id']==name)
    keep={c['P1_mask']:c for c in parent['records'] if c['reason']=='retained_overapproximation'};assert len(keep)==4
    controls=[{0,1,2},{3},set(z['B']),set(z['C']),set(z['D'])]
    classes=[];counts=Counter();transports=[]
    for graph,c in sorted(keep.items()):
        G=set(map(tuple,c['G']))
        frames=[set(S) for S in combinations(range(13),9) if 3 in S and all(len(set(S)&X)==1 for X in controls[2:]) and not any(set(e)<=set(S) for e in G)]
        classes.append(dict(P1_mask=graph,G=c['G'],frames=[sorted(S) for S in frames]))
        for si,S in enumerate(frames):
            for ti,T in enumerate(frames):
                if si==ti:continue
                cells={}
                for q in range(13):cells.setdefault(tuple(q in X for X in controls),[]).append(q)
                perm={}
                for cell in cells.values():perm.update(zip(sorted(cell,key=lambda q:(q in S,q in T,q)),sorted(cell)))
                assert set(perm)==set(perm.values())==set(range(13)) and all({perm[q] for q in X}==X for X in controls)
                target_graph=sum(BITS[tuple(sorted((perm[u],perm[v])))] for i,(u,v) in enumerate(PAIRS) if graph>>i&1)
                assert target_graph in keep
                target_G={tuple(sorted((perm[u],perm[v]))) for u,v in G};assert target_G==set(map(tuple,keep[target_graph]['G']))
                assert {perm[q] for q in parent['mandatory']}==set(parent['mandatory'])
                for field in parent['fields']:
                    for key in ('preA','preB','preC'):assert {perm[q] for q in field[key]}==set(field[key])
                    transformed={sum(BITS[tuple(sorted((perm[u],perm[v])))] for i,(u,v) in enumerate(PAIRS) if mask>>i&1) for mask in field['compatible_kernel_masks']}
                    assert transformed==set(field['compatible_kernel_masks'])
                basis=tuple(sum(1<<perm[q] for q in X) for X in (S,T));counts[(target_graph,basis)]+=1
                transports.append(dict(P1_mask=graph,pair=[si,ti],target_P1=target_graph,basis=list(basis),permutation=[perm[q] for q in range(13)]))
    prefixes=[dict(P1_mask=g,basis=list(b),multiplicity=v) for (g,b),v in sorted(counts.items())]
    assert len(transports)==12320 and len(prefixes)==64
    entries=[];total=Counter()
    for index,prefix in enumerate(prefixes):
        c=keep[prefix['P1_mask']];p=dict(mandatory=parent['mandatory'],required_P3_edges=c['G'],fields=parent['fields']);view=dict(extra_pair=None,field_kernel_masks=c['field_kernel_masks'])
        S,T=[{q for q in range(13) if m>>q&1} for m in prefix['basis']]
        rows,G=pool(p,view,S,T,set(z['B']),set(z['C']),set(z['D']))
        proof,stats=tree(rows,prefix['basis'],set(z['B']),set(z['C']),set(z['D']),G)
        entries.append(dict(**prefix,letter_count=len(rows),rows_sha256=hashlib.sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest(),flags_sha256=hashlib.sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest(),tree=proof,tree_stats=stats))
        total.update(stats);total['prefixes']+=1;total['literal_letters']+=len(rows)
        if (index+1)%8==0:print('prefixes',index+1,'/64',flush=True)
    assert total['nodes']==20072 and total['literal_letters']==1002240 and total.get('word_rounds',0)==0
    sources=[Path(__file__).name,'b2_c5_first_pair_scope.json','B2_C5_FIRST_PAIR_STAIRCASE_EXCLUSION.md',frozen['baseline'],frozen['checkpoint'],'small_first_third_inventory.json','b1_b2_inverse_union_inventory.json','c1_word_staircase_letter_generator.py','enumerate_c1_word_staircase.py','enumerate_b3_staircase.py','b3_staircase_letter_generator.py','enumerate_b3_staircase_first.py']
    result=dict(status='complete_necessary_exclusion_inventory',parameter=[13,9,1],id=name,B=z['B'],C=z['C'],D=z['D'],classes=classes,transports=transports,prefixes=entries,stats=dict(total),scope=frozen['scope'],source_sha256={n:sha(ROOT/n) for n in sources})
    (ROOT/'b2_c5_first_pair_inventory.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('classes','transports','prefixes','source_sha256')}),flush=True)
if __name__=='__main__':main()
