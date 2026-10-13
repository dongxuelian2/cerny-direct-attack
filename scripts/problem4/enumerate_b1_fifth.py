"""Fifth entrance space for residual B0/C14/D5/E6 and E26.

All Boolean one-count columns are recorded, including uncovered columns.
Only necessary geometric/field admission is claimed by this generator.
"""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};K={1,2};O=Q-A

def rank(rows):
    work=[[Fraction(x) for x in row] for row in rows];r=0
    for j in range(len(work[0])):
        i=next((i for i in range(r,len(work)) if work[i][j]),None)
        if i is None:continue
        work[r],work[i]=work[i],work[r];scale=work[r][j];work[r]=[x/scale for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j];work[i]=[x-v*y for x,y in zip(work[i],work[r])]
        r+=1
    return r
def solve(rows,values):
    work=[[Fraction(x) for x in row]+[Fraction(y)] for row,y in zip(rows,values)]
    for j in range(6):
        i=next(i for i in range(j,6) if work[i][j]);work[j],work[i]=work[i],work[j]
        scale=work[j][j];work[j]=[x/scale for x in work[j]]
        for i in range(6):
            if i==j:continue
            v=work[i][j];work[i]=[x-v*y for x,y in zip(work[i],work[j])]
    return [work[i][-1] for i in range(6)]
def incomparable(X,Y):return not X<=Y and not Y<=X
def boolean_fibers(E,F):
    known=(B,C,D,E,F)
    cells={key:{q for q in O if tuple(int(q in X) for X in known)==key} for key in product((0,1),repeat=5)}
    keys=[key for key in cells if cells[key]];rows=[[1,*key] for key in keys]
    inds=next(ix for ix in combinations(range(len(rows)),6) if rank([rows[i] for i in ix])==6)
    answer=[]
    for vals in product((0,1),repeat=6):
        coef=solve([rows[i] for i in inds],vals)
        out=[sum(c*x for c,x in zip(coef,row)) for row in rows]
        if any(v not in (0,1) for v in out) or coef[0]*8+sum(coef[1:])!=1:continue
        R=set().union(*(cells[key] for key,v in zip(keys,out) if v))
        if not R:continue
        answer.append(dict(R=sorted(R),coefficients=[str(c) for c in coef],
            covered_by_K=len(R-K)<=1,
            incomparable_with_distinct_known=all(R==X or incomparable(R,X) for X in known)))
    return sorted(answer,key=lambda z:z['R'])
def fields(E,F,allowed,parent,mandatory):
    rows=[];records=[];caps=[1,1,2,1,len(E),8-len(E)]
    for i,oldrow in enumerate(parent['rows']):
        first=[set(oldrow[key]) for key in ('preA','preB','preC','preD')]
        for R in [A]+allowed:
            groups=first+[R]
            if any(groups[i]&groups[j] for i,j in combinations(range(5),2)):continue
            groups.append(Q-set().union(*groups))
            forced={edge for X,cap in zip(groups,caps) if cap==1 for edge in combinations(sorted(X),2)}
            if len(forced)>4 or any(not set(edge)&K or set(edge)&mandatory for edge in forced):continue
            rows.append(dict(parent_row=i,preA=oldrow['preA'],preB=oldrow['preB'],preC=oldrow['preC'],
                preD=oldrow['preD'],preE=sorted(R),forced_pairs=[list(edge) for edge in sorted(forced)],
                capacity=[min(len(X),cap) for X,cap in zip(groups,caps)]))
    for oldpair in parent['pairs']:
        for x,y in oldpair['fourth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                if left['parent_row']!=x:continue
                for j,right in enumerate(rows):
                    if right['parent_row']!=y or (x==y and i>j):continue
                    if not any(set(row['preE'])==F for row in (left,right)):continue
                    if any(left['capacity'][h]+right['capacity'][h]<cap for h,cap in enumerate(caps)):continue
                    if len({tuple(edge) for row in (left,right) for edge in row['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=oldpair['original_rows'],original_fourth_rows=[x,y],fifth_field_pairs=pairs))
    return rows,records
def inventory():
    parents=json.loads((ROOT/'b1_partial_cover_fourth_inventory.json').read_text(encoding='utf-8'))['records']
    allS=[A|set(X) for X in combinations(sorted(O),8)]
    candidatesF=[set(X) for n in range(1,4) for X in combinations(sorted(O),n) if len(set(X)-K)<=1]
    profiles=[];counts={}
    for E in ({6},{2,6}):
        parent=next(z for z in parents if set(z['E'])==E)
        forms0=[X for X in allS if all(len(X&R)==1 for R in (B,C,D,E))]
        cells=[{q for q in O if tuple(int(q in R) for R in (K,B,C,D,E))==key} for key in product((0,1),repeat=5)]
        orbits={}
        for F in candidatesF:
            if any(not incomparable(F,R) for R in (B,C,D,E)):continue
            forms=[X for X in forms0 if len(X&F)==1]
            if not forms or rank([[1,*[int(q in R) for R in (B,C,D,E,F)]] for q in sorted(O)])!=6:continue
            sig=tuple(len(F&cell) for cell in cells)
            if sig in orbits:orbits[sig]['labelled_F']+=1;continue
            canonical=set().union(*(set(sorted(cell)[:take]) for cell,take in zip(cells,sig)))
            assert canonical==F
            bools=boolean_fibers(E,F)
            allowed=[set(z['R']) for z in bools if z['covered_by_K'] and z['incomparable_with_distinct_known']]
            mandatory=set.intersection(*forms);rows,pairs=fields(E,F,allowed,parent,mandatory)
            orbits[sig]=dict(E=sorted(E),F=sorted(F),cell_signature=list(sig),labelled_F=1,
                orbit_size=math.prod(math.comb(len(cell),take) for cell,take in zip(cells,sig)),
                feasible_nine_sets=len(forms),mandatory_through_six=sorted(mandatory),
                remaining_P2_cover=sorted(K-mandatory),all_Boolean_one_count_fibers=bools,
                allowed_preE_fibers=[sorted(R) for R in allowed],
                additional_Boolean_fibers=[z['R'] for z in bools if set(z['R']) not in (B,C,D,E,F)],
                additional_covered_fibers=[sorted(R) for R in allowed if R not in (B,C,D,E,F)],
                rows=rows,pairs=pairs)
        for i,z in enumerate(orbits.values(),1):
            assert z['labelled_F']==z['orbit_size'];z['id']=parent['id']+'_fifth'+str(i);profiles.append(z)
        key=','.join(map(str,sorted(E)))
        counts[key]=dict(geometric_orbits=len(orbits),labelled_F=sum(z['labelled_F'] for z in orbits.values()),
            additional_Boolean_orbits=sum(bool(z['additional_Boolean_fibers']) for z in orbits.values()),
            additional_covered_orbits=sum(bool(z['additional_covered_fibers']) for z in orbits.values()),
            binary_typed_orbits=sum(any(p['fifth_field_pairs'] for p in z['pairs']) for z in orbits.values()),
            binary_fifth_field_pairs=sum(len(p['fifth_field_pairs']) for z in orbits.values() for p in z['pairs']))
    names=[Path(__file__).name,'b1_partial_cover_fourth_inventory.json','PROOF.md#problem4-local-equality-flag',
        'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-b1-partial-cover-fourth']
    return dict(status='necessary_fifth_inventory',parameter=[13,9,1],counts=counts,records=profiles,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete necessary fifth geometry and binary field admission for residual E6/E26, preserving all Boolean columns including uncovered ones. No exclusion, automaton existence or F value is asserted by this inventory.')
if __name__=='__main__':
    result=inventory();(ROOT/'b1_fifth_inventory.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(counts=result['counts'],profiles=len(result['records']))))
