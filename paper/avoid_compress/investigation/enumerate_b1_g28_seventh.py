"""Seventh entrance for E6/F7/G28, with the pair target's capacity2.

Every Boolean companion is retained before cover/disjointness cuts.
This is necessary geometry and field admission, not model existence.
"""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};E={6};F={7};G={2,8};K={1,2};O=Q-A
KNOWN=(B,C,D,E,F,G);KEYS=('preA','preB','preC','preD','preE','preF')

def rank(rows):
    work=[[Fraction(x) for x in row] for row in rows];r=0
    for j in range(len(work[0])):
        i=next((i for i in range(r,len(work)) if work[i][j]),None)
        if i is None:continue
        work[r],work[i]=work[i],work[r];v=work[r][j];work[r]=[x/v for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j];work[i]=[x-v*y for x,y in zip(work[i],work[r])]
        r+=1
    return r

def solve(rows,values):
    work=[[Fraction(x) for x in row]+[Fraction(v)] for row,v in zip(rows,values)]
    for j in range(8):
        i=next(i for i in range(j,8) if work[i][j]);work[j],work[i]=work[i],work[j]
        v=work[j][j];work[j]=[x/v for x in work[j]]
        for i in range(8):
            if i!=j:
                v=work[i][j];work[i]=[x-v*y for x,y in zip(work[i],work[j])]
    return [row[-1] for row in work]

def inc(X,Y):return not X<=Y and not Y<=X

def fibers(H):
    known=(*KNOWN,H)
    cells={key:{q for q in O if tuple(int(q in X) for X in known)==key} for key in product((0,1),repeat=7)}
    cells={key:cell for key,cell in cells.items() if cell};rows=[[1,*key] for key in cells]
    basis=next(ix for ix in combinations(range(len(rows)),8) if rank([rows[i] for i in ix])==8)
    result=[]
    for values in product((0,1),repeat=8):
        coeff=solve([rows[i] for i in basis],values)
        out=[sum(c*x for c,x in zip(coeff,row)) for row in rows]
        if any(v not in (0,1) for v in out) or 8*coeff[0]+sum(coeff[1:])!=1:continue
        R=set().union(*(cell for cell,v in zip(cells.values(),out) if v))
        if R:result.append(dict(R=sorted(R),coefficients=list(map(str,coeff)),covered_by_K=len(R-K)<=1,
            incomparable_with_distinct_known=all(R==X or inc(R,X) for X in known)))
    return sorted(result,key=lambda z:z['R'])

def fields(H,allowed,parent,protected):
    caps=[1,1,2,1,1,1,2,4];rows=[];records=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            groups=[set(old[key]) for key in KEYS]+[R]
            if any(groups[i]&groups[j] for i,j in combinations(range(7),2)):continue
            groups.append(Q-set().union(*groups))
            forced={p for X,cap in zip(groups,caps) if cap==1 for p in combinations(sorted(X),2)}
            if len(forced)>4 or any(not set(p)&K or set(p)&protected for p in forced):continue
            rows.append(dict(parent_row=i,**{key:old[key] for key in KEYS},preG=sorted(R),
                forced_pairs=[list(p) for p in sorted(forced)],capacity=[min(len(X),cap) for X,cap in zip(groups,caps)]))
    for previous in parent['pairs']:
        for x,y in previous['sixth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                if left['parent_row']!=x:continue
                for j,right in enumerate(rows):
                    if right['parent_row']!=y or (x==y and i>j):continue
                    if left['preG']!=sorted(H) and right['preG']!=sorted(H):continue
                    if any(left['capacity'][h]+right['capacity'][h]<caps[h] for h in range(8)):continue
                    if len({tuple(p) for row in (left,right) for p in row['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=previous['original_third_rows'],original_fourth_rows=previous['original_fourth_rows'],
                original_fifth_rows=previous['original_fifth_rows'],original_sixth_rows=[x,y],seventh_field_pairs=pairs))
    return rows,records

def main():
    parent=next(z for z in json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))['records']
        if z['E']==[6] and z['F']==[7] and z['G']==[2,8])
    assert parent['additional_Boolean_fibers']==[] and {tuple(v) for v in parent['allowed_preF_fibers']}=={tuple(sorted(X)) for X in KNOWN}
    allS=[A|set(X) for X in combinations(sorted(O),8)]
    candidates=[set(X) for n in range(1,4) for X in combinations(sorted(O),n) if len(set(X)-K)<=1]
    cells=[{q for q in O if tuple(int(q in X) for X in (K,*KNOWN))==key} for key in product((0,1),repeat=7)]
    orbits={}
    for H in candidates:
        if any(not inc(H,X) for X in KNOWN):continue
        forms=[S for S in allS if all(len(S&X)==1 for X in (*KNOWN,H))]
        if not forms or rank([[1,*[int(q in X) for X in (*KNOWN,H)]] for q in sorted(O)])!=8:continue
        sig=tuple(len(H&cell) for cell in cells)
        if sig in orbits:orbits[sig]['labelled_H']+=1;continue
        assert set().union(*(set(sorted(cell)[:take]) for cell,take in zip(cells,sig)))==H
        bools=fibers(H);allowed=[set(v['R']) for v in bools if v['covered_by_K'] and v['incomparable_with_distinct_known']]
        mandatory=set.intersection(*forms);rows,pairs=fields(H,allowed,parent,mandatory)
        orbits[sig]=dict(H=sorted(H),cell_signature=list(sig),labelled_H=1,
            orbit_size=math.prod(math.comb(len(cell),take) for cell,take in zip(cells,sig)),
            feasible_nine_sets=len(forms),mandatory_through_four=sorted(mandatory),mandatory_core_isolation_depth=7,
            preG_target_capacity=2,remaining_target_capacity=4,all_Boolean_one_count_fibers=bools,
            allowed_preG_fibers=[sorted(X) for X in allowed],
            additional_Boolean_fibers=[v['R'] for v in bools if set(v['R']) not in KNOWN and set(v['R'])!=H],
            additional_covered_fibers=[sorted(X) for X in allowed if X not in KNOWN and X!=H],rows=rows,pairs=pairs)
    profiles=[]
    for i,z in enumerate(orbits.values(),1):
        assert z['labelled_H']==z['orbit_size'];z['id']=parent['id']+'_seventh'+str(i);profiles.append(z)
    names=[Path(__file__).name,'b1_sixth_inventory.json','b1_sixth_audit.json','B1_SIXTH_ENTRANCE.md',
        'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md']
    result=dict(status='necessary_G28_seventh_inventory',parameter=[13,9,1],E=[6],F=[7],G=[2,8],
        geometric_orbits=len(profiles),labelled_H=sum(z['labelled_H'] for z in profiles),
        additional_Boolean_orbits=sum(bool(z['additional_Boolean_fibers']) for z in profiles),
        additional_covered_orbits=sum(bool(z['additional_covered_fibers']) for z in profiles),
        binary_field_pairs=sum(len(p['seventh_field_pairs']) for z in profiles for p in z['pairs']),records=profiles,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete necessary seventh geometry, all Boolean companions and capacity2 field admission for G28. Only literal-family core protected. Inventory alone makes no exclusion or F-value claim.')
    (ROOT/'b1_g28_seventh_inventory.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    print(json.dumps([dict(H=z['H'],labels=z['labelled_H'],forms=z['feasible_nine_sets'],
        mandatory=z['mandatory_through_four'],extras=z['additional_Boolean_fibers'],covered_extras=z['additional_covered_fibers'],
        rows=len(z['rows']),pairs=sum(len(p['seventh_field_pairs']) for p in z['pairs'])) for z in profiles]))
if __name__=='__main__':main()
