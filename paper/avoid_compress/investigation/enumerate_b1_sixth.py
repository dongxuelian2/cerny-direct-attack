"""Sixth admission in three disjoint residual E/F geometries.

All Boolean fibers, including uncovered companions, are preserved.
Necessary fields only: no automaton existence or extremal F value.
"""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};K={1,2};O=Q-A
SELECTED=(({6},{7}),({6},{2,7}),({2,6},{7}))
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
    for j in range(7):
        i=next(i for i in range(j,7) if work[i][j]);work[j],work[i]=work[i],work[j]
        v=work[j][j];work[j]=[x/v for x in work[j]]
        for i in range(7):
            if i!=j:
                v=work[i][j];work[i]=[x-v*y for x,y in zip(work[i],work[j])]
    return [row[-1] for row in work]
def inc(X,Y):return not X<=Y and not Y<=X
def fibers(known):
    cells={key:{q for q in O if tuple(int(q in X) for X in known)==key} for key in product((0,1),repeat=6)}
    cells={key:cell for key,cell in cells.items() if cell};rows=[[1,*key] for key in cells]
    basis=next(ix for ix in combinations(range(len(rows)),7) if rank([rows[i] for i in ix])==7)
    result=[]
    for vals in product((0,1),repeat=7):
        coeff=solve([rows[i] for i in basis],vals);out=[sum(c*x for c,x in zip(coeff,row)) for row in rows]
        if any(v not in (0,1) for v in out) or 8*coeff[0]+sum(coeff[1:])!=1:continue
        R=set().union(*(cell for cell,v in zip(cells.values(),out) if v))
        if R:result.append(dict(R=sorted(R),coefficients=list(map(str,coeff)),covered_by_K=len(R-K)<=1,
            incomparable_with_distinct_known=all(R==X or inc(R,X) for X in known)))
    return sorted(result,key=lambda z:z['R'])
def fields(E,F,G,allowed,parent,mandatory):
    caps=[1,1,2,1,len(E),len(F),8-len(E)-len(F)];rows=[];records=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            inputs=[set(old[key]) for key in ('preA','preB','preC','preD','preE')]+[R]
            if any(inputs[i]&inputs[j] for i,j in combinations(range(6),2)):continue
            inputs.append(Q-set().union(*inputs))
            forced={p for X,cap in zip(inputs,caps) if cap==1 for p in combinations(sorted(X),2)}
            if len(forced)>4 or any(not set(p)&K or set(p)&mandatory for p in forced):continue
            rows.append(dict(parent_row=i,**{key:old[key] for key in ('preA','preB','preC','preD','preE')},preF=sorted(R),
                forced_pairs=[list(p) for p in sorted(forced)],capacity=[min(len(X),cap) for X,cap in zip(inputs,caps)]))
    for previous in parent['pairs']:
        for x,y in previous['fifth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                if left['parent_row']!=x:continue
                for j,right in enumerate(rows):
                    if right['parent_row']!=y or (x==y and i>j):continue
                    if left['preF']!=sorted(G) and right['preF']!=sorted(G):continue
                    if any(left['capacity'][h]+right['capacity'][h]<cap for h,cap in enumerate(caps)):continue
                    if len({tuple(p) for row in (left,right) for p in row['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=previous['original_third_rows'],original_fourth_rows=previous['original_fourth_rows'],
                original_fifth_rows=[x,y],sixth_field_pairs=pairs))
    return rows,records
def main():
    parents=json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'))['records']
    allS=[A|set(X) for X in combinations(sorted(O),8)]
    candidates=[set(X) for n in range(1,4) for X in combinations(sorted(O),n) if len(set(X)-K)<=1]
    profiles=[];counts=[]
    for E,F in SELECTED:
        parent=next(p for p in parents if set(p['E'])==E and set(p['F'])==F);known=(B,C,D,E,F)
        cells=[{q for q in O if tuple(int(q in X) for X in (K,*known))==key} for key in product((0,1),repeat=6)]
        current={}
        for G in candidates:
            if any(not inc(G,X) for X in known):continue
            forms=[S for S in allS if all(len(S&X)==1 for X in (*known,G))]
            if not forms or rank([[1,*[int(q in X) for X in (*known,G)]] for q in sorted(O)])!=7:continue
            signature=tuple(len(G&cell) for cell in cells)
            if signature in current:current[signature]['labelled_G']+=1;continue
            assert set().union(*(set(sorted(cell)[:take]) for cell,take in zip(cells,signature)))==G
            bools=fibers((*known,G));allowed=[set(v['R']) for v in bools if v['covered_by_K'] and v['incomparable_with_distinct_known']]
            mandatory=set.intersection(*forms);rows,pairs=fields(E,F,G,allowed,parent,mandatory)
            current[signature]=dict(E=sorted(E),F=sorted(F),G=sorted(G),cell_signature=list(signature),labelled_G=1,
                orbit_size=math.prod(math.comb(len(cell),take) for cell,take in zip(cells,signature)),feasible_nine_sets=len(forms),
                mandatory_through_five=sorted(mandatory),remaining_P1_cover=sorted(K-mandatory),
                all_Boolean_one_count_fibers=bools,allowed_preF_fibers=[sorted(X) for X in allowed],
                additional_Boolean_fibers=[v['R'] for v in bools if set(v['R']) not in known and set(v['R'])!=G],
                additional_covered_fibers=[sorted(X) for X in allowed if X not in known and X!=G],rows=rows,pairs=pairs)
        for i,z in enumerate(current.values(),1):
            assert z['labelled_G']==z['orbit_size'];z['id']=parent['id']+'_sixth'+str(i);profiles.append(z)
        counts.append(dict(E=sorted(E),F=sorted(F),geometric_orbits=len(current),labelled_G=sum(z['labelled_G'] for z in current.values()),
            additional_Boolean_orbits=sum(bool(z['additional_Boolean_fibers']) for z in current.values()),
            binary_typed_orbits=sum(any(p['sixth_field_pairs'] for p in z['pairs']) for z in current.values()),
            binary_field_pairs=sum(len(p['sixth_field_pairs']) for z in current.values() for p in z['pairs'])))
    names=[Path(__file__).name,'b1_fifth_inventory.json','B1_FIFTH_ENTRANCE.md','LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md']
    result=dict(status='necessary_sixth_inventory',parameter=[13,9,1],counts=counts,records=profiles,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete necessary sixth geometry/Boolean fibers and binary fields for three disjoint E/F branches. No exclusion, automaton existence, full branch classification or F value.')
    (ROOT/'b1_sixth_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(counts=counts,profiles=len(profiles))))
if __name__=='__main__':main()
