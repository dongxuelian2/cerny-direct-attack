"""Common fourth fiber for B0,C14,D5, with K12 cover.

The common-fiber assertion is proved for this particular geometry.
No general common-third/fourth-fiber assertion is made.
"""
from itertools import combinations,product
from pathlib import Path
import hashlib,json,math
from enumerate_small_first_third import incomparable,rank
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};K={1,2};O=Q-A

def typed(E):
    old=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    source=next(z for z in old['records'] if z['id']=='b1_in_c3_third2')
    keys=list(product((0,1),repeat=4))
    targets={key:{q for q in Q if tuple(int(q in X) for X in (A,B,C,D))==key} for key in keys}
    rows=[];pair_records=[]
    for i,oldrow in enumerate(source['rows']):
        for preD in (A,B,C,D,E):
            fields=[set(oldrow[key]) for key in ('preA','preB','preC')]+[preD]
            inputs={key:{q for q in Q if tuple(int(q in X) for X in fields)==key} for key in keys}
            if any(inputs[key] and not targets[key] for key in keys):continue
            forced={p for key in keys if len(targets[key])==1 for p in combinations(sorted(inputs[key]),2)}
            if any(not set(p)&K or set(p)&(A|B|D) for p in forced):continue
            if len(forced)>4:continue
            rows.append(dict(old_row=i,preA=oldrow['preA'],preB=oldrow['preB'],preC=oldrow['preC'],
                preD=sorted(preD),forced_pairs=[list(p) for p in sorted(forced)],
                capacity=[min(len(inputs[key]),len(targets[key])) for key in keys]))
    for original_pair in source['binary_profile_pairs']:
        x,y=original_pair;matches=[]
        for i,left in enumerate(rows):
            if left['old_row']!=x:continue
            for j,right in enumerate(rows):
                if right['old_row']!=y:continue
                if x==y and i>j:continue
                if not any(set(row['preD'])==E for row in (left,right)):continue
                if any(left['capacity'][h]+right['capacity'][h]<len(targets[key]) for h,key in enumerate(keys)):continue
                if len({tuple(p) for row in (left,right) for p in row['forced_pairs']})>4:continue
                matches.append([i,j])
        pair_records.append(dict(original_rows=original_pair,fourth_field_pairs=matches))
    return rows,pair_records

def inventory():
    allS=[A|set(T) for T in combinations(sorted(O),8)]
    parent=[T for T in allS if all(len(T&X)==1 for X in (B,C,D))]
    cells=[{q for q in O if tuple(int(q in X) for X in (K,B,C,D))==key} for key in product((0,1),repeat=4)]
    candidates={}
    for size in range(1,4):
        for chosen in combinations(sorted(O),size):
            E=set(chosen)
            if len(E-K)>1 or any(not incomparable(E,X) for X in (B,C,D)):continue
            forms=[T for T in parent if len(T&E)==1]
            if not forms or rank([[1,int(q in B),int(q in C),int(q in D),int(q in E)] for q in sorted(O)])!=5:continue
            sig=tuple(len(E&cell) for cell in cells)
            if sig in candidates:candidates[sig]['labelled_E']+=1;continue
            canonical=set().union(*(set(sorted(cell)[:take]) for cell,take in zip(cells,sig)))
            assert canonical==E
            mandatory=set.intersection(*forms);remaining=K-mandatory
            rows,pairs=typed(E)
            candidates[sig]=dict(E=sorted(E),cell_signature=list(sig),labelled_E=1,
                orbit_size=math.prod(math.comb(len(cell),take) for cell,take in zip(cells,sig)),
                feasible_nine_sets=len(forms),mandatory_through_seven=sorted(mandatory),
                remaining_P3_cover=sorted(remaining),excluded_by_known_bound=len(remaining)<=1,
                rows=rows,pairs=pairs)
    records=[]
    for i,z in enumerate(candidates.values(),1):
        assert z['labelled_E']==z['orbit_size'];z['id']='b1_in_c3_third2_fourth'+str(i);records.append(z)
    names=[Path(__file__).name,'enumerate_small_first_third.py','small_first_third_inventory.json']
    return dict(status='necessary_common_fourth_inventory',parameter=[13,9,1],B=sorted(B),C=sorted(C),D=sorted(D),
        cover=sorted(K),records=records,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete necessary B0,C14,D5 fourth geometry and binary field-pair admission. '
              'Common E is geometry-specific; preserves original pairs, uses K12 rather than C as cover. No F value.')

if __name__=='__main__':
    result=inventory();(ROOT/'b1_partial_cover_fourth_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([dict(E=z['E'],labelled=z['labelled_E'],excluded=z['excluded_by_known_bound'],
        rows=len(z['rows']),pairs=sum(len(p['fourth_field_pairs']) for p in z['pairs'])) for z in result['records']]))
