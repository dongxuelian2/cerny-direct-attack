"""Sixth entrances in E26/F17,F27, with overlapping targets.

Every Boolean companion is retained before cover/disjointness cuts.
This is necessary geometry and field admission, not model existence.
"""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};E={2,6};F=None;G=None;K={1,2};O=Q-A
KNOWN=();KEYS=('preA','preB','preC','preD','preE')

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
    assert len(rows)==len(values)==7
    work=[[Fraction(x) for x in row]+[Fraction(v)] for row,v in zip(rows,values)]
    for j in range(7):
        i=next(i for i in range(j,7) if work[i][j]);work[j],work[i]=work[i],work[j]
        v=work[j][j];work[j]=[x/v for x in work[j]]
        for i in range(7):
            if i!=j:
                v=work[i][j];work[i]=[x-v*y for x,y in zip(work[i],work[j])]
    return [row[-1] for row in work]

def inc(X,Y):return not X<=Y and not Y<=X

def fibers(H):
    known=(*KNOWN,H)
    cells={key:{q for q in O if tuple(int(q in X) for X in known)==key} for key in product((0,1),repeat=6)}
    cells={key:cell for key,cell in cells.items() if cell};rows=[[1,*key] for key in cells]
    basis=next(ix for ix in combinations(range(len(rows)),7) if rank([rows[i] for i in ix])==7)
    result=[]
    for values in product((0,1),repeat=7):
        coeff=solve([rows[i] for i in basis],values)
        out=[sum(c*x for c,x in zip(coeff,row)) for row in rows]
        if any(v not in (0,1) for v in out) or 8*coeff[0]+sum(coeff[1:])!=1:continue
        R=set().union(*(cell for cell,v in zip(cells.values(),out) if v))
        if R:result.append(dict(R=sorted(R),coefficients=list(map(str,coeff)),covered_by_K=len(R-K)<=1,
            incomparable_with_distinct_known=all(R==X or inc(R,X) for X in known)))
    assert len(result)==len({tuple(z['R']) for z in result})
    return sorted(result,key=lambda z:z['R'])

def atoms():
    targets=(A,B,C,D,E,F);output={}
    for q in range(13):
        sig=tuple(int(q in X) for X in targets);output.setdefault(sig,set()).add(q)
    return [(sig,sorted(points)) for sig,points in output.items()]

def fields(G,allowed,parent,protected):
    target_atoms=atoms();output_sigs={sig for sig,points in target_atoms}
    caps=[len(points) for sig,points in target_atoms];rows=[];records=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            inputs=[set(old[key]) for key in KEYS]+[R]
            classes={sig:{q for q in Q if tuple(int(q in X) for X in inputs)==sig}
                for sig in product((0,1),repeat=6)}
            if any(cell and sig not in output_sigs for sig,cell in classes.items()):continue
            groups=[classes[sig] for sig,points in target_atoms]
            forced={p for X,cap in zip(groups,caps) if cap==1 for p in combinations(sorted(X),2)}
            if len(forced)>4 or any(not set(p)&K or set(p)&protected for p in forced):continue
            rows.append(dict(parent_row=i,**{key:old[key] for key in KEYS},preF=sorted(R),
                atom_inputs=[sorted(X) for X in groups],forced_pairs=[list(p) for p in sorted(forced)],
                capacity=[min(len(X),cap) for X,cap in zip(groups,caps)]))
    for previous in parent['pairs']:
        for x,y in previous['fifth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                if left['parent_row']!=x:continue
                for j,right in enumerate(rows):
                    if right['parent_row']!=y or (x==y and i>j):continue
                    if left['preF']!=sorted(G) and right['preF']!=sorted(G):continue
                    if any(left['capacity'][h]+right['capacity'][h]<caps[h] for h in range(len(caps))):continue
                    if len({tuple(p) for row in (left,right) for p in row['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=previous['original_third_rows'],original_fourth_rows=previous['original_fourth_rows'],
                original_fifth_rows=[x,y],sixth_field_pairs=pairs))
    return rows,records

def main():
    global F,KNOWN
    parents=json.loads((ROOT/'b1_fifth_inventory.json').read_text())['records']
    allS=[A|set(X) for X in combinations(sorted(O),8)]
    candidates=[set(X) for n in range(1,4) for X in combinations(sorted(O),n) if len(set(X)-K)<=1]
    records=[];counts=[]
    for F in ({1,7},{2,7}):
        KNOWN=(B,C,D,E,F)
        parent=next(z for z in parents if z['E']==[2,6] and z['F']==sorted(F))
        assert parent['additional_Boolean_fibers']==[] and {tuple(v) for v in parent['allowed_preE_fibers']}=={tuple(sorted(X)) for X in KNOWN}
        cells=[{q for q in O if tuple(int(q in X) for X in (K,*KNOWN))==key} for key in product((0,1),repeat=6)]
        orbits={}
        for G in candidates:
            if any(not inc(G,X) for X in KNOWN):continue
            forms=[S for S in allS if all(len(S&X)==1 for X in (*KNOWN,G))]
            if not forms or rank([[1,*[int(q in X) for X in (*KNOWN,G)]] for q in sorted(O)])!=7:continue
            sig=tuple(len(G&cell) for cell in cells)
            if sig in orbits:orbits[sig]['labelled_G']+=1;continue
            assert set().union(*(set(sorted(cell)[:take]) for cell,take in zip(cells,sig)))==G
            bools=fibers(G);allowed=[set(v['R']) for v in bools if v['covered_by_K'] and v['incomparable_with_distinct_known']]
            mandatory=set.intersection(*forms);rows,pairs=fields(G,allowed,parent,mandatory)
            orbits[sig]=dict(E=[2,6],F=sorted(F),G=sorted(G),cell_signature=list(sig),labelled_G=1,
                orbit_size=math.prod(math.comb(len(cell),take) for cell,take in zip(cells,sig)),
                feasible_nine_sets=len(forms),mandatory_through_five=sorted(mandatory),mandatory_core_isolation_depth=7,
                preF_clique_depth=3,target_atoms=[dict(membership=list(sig),targets=targets) for sig,targets in atoms()],
                all_Boolean_one_count_fibers=bools,allowed_preF_fibers=[sorted(X) for X in allowed],
                additional_Boolean_fibers=[v['R'] for v in bools if set(v['R']) not in KNOWN and set(v['R'])!=G],
                additional_covered_fibers=[sorted(X) for X in allowed if X not in KNOWN and X!=G],rows=rows,pairs=pairs)
        for i,z in enumerate(orbits.values(),1):
            assert z['labelled_G']==z['orbit_size'];z['id']=parent['id']+'_sixth'+str(i);records.append(z)
        counts.append(dict(F=sorted(F),geometric_orbits=len(orbits),labelled_G=sum(z['labelled_G'] for z in orbits.values()),
            binary_field_pairs=sum(len(p['sixth_field_pairs']) for z in orbits.values() for p in z['pairs'])))
    names=[Path(__file__).name,'b1_fifth_inventory.json','b1_fifth_audit.json','B1_FIFTH_ENTRANCE.md',
        'B1_E26_OVERLAP_SIXTH.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md']
    result=dict(status='necessary_E26_overlap_sixth_inventory',parameter=[13,9,1],E=[2,6],counts=counts,records=records,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete necessary sixth geometry, every Boolean companion and exact overlapping-output atoms for E26/F17,F27. Inventory alone gives no model or exclusion; no whole E/F/third/joint or F value.')
    (ROOT/'b1_e26_overlap_sixth_inventory.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps([dict(F=z['F'],G=z['G'],labels=z['labelled_G'],forms=z['feasible_nine_sets'],mandatory=z['mandatory_through_five'],
        extras=z['additional_Boolean_fibers'],covered_extras=z['additional_covered_fibers'],rows=len(z['rows']),
        supply_rows=sum(r['preF']==z['G'] for r in z['rows']),pairs=sum(len(p['sixth_field_pairs']) for p in z['pairs'])) for z in records]))
if __name__=='__main__':main()
