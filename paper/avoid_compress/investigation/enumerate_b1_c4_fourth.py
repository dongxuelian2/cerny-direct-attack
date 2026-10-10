"""Complete fourth spaces for D1,D5,D12,D15,D125, with all companions."""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={4};K={1,2};O=Q-A
KEYS=('preA','preB','preC')

def rank(rows):
    a=[[Fraction(v) for v in r] for r in rows];i=0
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
        for k in range(i+1,len(a)):
            v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[i])]
        i+=1
    return i
def solve(rows,values):
    a=[[Fraction(x) for x in r]+[Fraction(v)] for r,v in zip(rows,values)]
    for j in range(5):
        k=next(k for k in range(j,5) if a[k][j]);a[j],a[k]=a[k],a[j]
        v=a[j][j];a[j]=[x/v for x in a[j]]
        for k in range(5):
            if k!=j:
                v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[j])]
    return [r[-1] for r in a]
def inc(X,Y):return not X<=Y and not Y<=X
def fibers(D,E):
    known=(B,C,D,E);cells={}
    for q in sorted(O):cells.setdefault(tuple(int(q in X) for X in known),set()).add(q)
    rows=[[1,*sig] for sig in cells]
    basis=next(ix for ix in combinations(range(len(rows)),5) if rank([rows[i] for i in ix])==5)
    result=[]
    for values in product((0,1),repeat=5):
        co=solve([rows[i] for i in basis],values)
        out=[sum(v*x for v,x in zip(co,row)) for row in rows]
        if any(v not in (0,1) for v in out) or 8*co[0]+sum(co[1:])!=1:continue
        R=set().union(*(cell for cell,v in zip(cells.values(),out) if v))
        if R:result.append(dict(R=sorted(R),coefficients=list(map(str,co)),covered_by_K=len(R-K)<=1,
            incomparable_with_distinct_known=all(R==X or inc(R,X) for X in known)))
    assert len(result)==len({tuple(v['R']) for v in result})
    return sorted(result,key=lambda z:z['R'])
def atoms(D):
    known=(A,B,C,D);cells={}
    for q in range(13):cells.setdefault(tuple(int(q in X) for X in known),[]).append(q)
    return list(cells.items())
def fields(D,E,allowed,parent,protected):
    targets=atoms(D);sigs={s for s,t in targets};caps=[len(t) for s,t in targets];rows=[];records=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            cols=[set(old[key]) for key in KEYS]+[R]
            cells={sig:{q for q in Q if tuple(int(q in X) for X in cols)==sig} for sig in product((0,1),repeat=4)}
            if any(cell and sig not in sigs for sig,cell in cells.items()):continue
            groups=[cells[sig] for sig,t in targets]
            forced={p for group,cap in zip(groups,caps) if cap==1 for p in combinations(sorted(group),2)}
            if len(forced)>4 or any(not set(p)&K or set(p)&protected for p in forced):continue
            rows.append(dict(parent_row=i,**{key:old[key] for key in KEYS},preD=sorted(R),
                atom_inputs=[sorted(x) for x in groups],forced_pairs=[list(p) for p in sorted(forced)],
                capacity=[min(len(x),cap) for x,cap in zip(groups,caps)]))
    for x,y in parent['binary_profile_pairs']:
        pairs=[]
        for i,l in enumerate(rows):
            if l['parent_row']!=x:continue
            for j,r in enumerate(rows):
                if r['parent_row']!=y or (x==y and i>j):continue
                if l['preD']!=sorted(E) and r['preD']!=sorted(E):continue
                if any(l['capacity'][h]+r['capacity'][h]<cap for h,cap in enumerate(caps)):continue
                if len({tuple(p) for row in (l,r) for p in row['forced_pairs']})>4:continue
                pairs.append([i,j])
        records.append(dict(original_third_rows=[x,y],fourth_field_pairs=pairs))
    return rows,records
def main():
    parents=json.loads((ROOT/'small_first_third_inventory.json').read_text())['records'];records=[];counts=[]
    allS=[A|set(X) for X in combinations(sorted(O),8)]
    candidates=[set(X) for size in range(1,4) for X in combinations(sorted(O),size) if len(set(X)-K)<=1]
    for D in ({1},{5},{1,2},{1,5},{1,2,5}):
        known=(B,C,D);parent=next(z for z in parents if z['joint_id']=='b1_in_c1' and z['D']==sorted(D))
        assert {tuple(x) for x in parent['allowed_preC_fibers']}=={tuple(sorted(X)) for X in known}
        orbitcells=[{q for q in O if tuple(int(q in X) for X in (K,*known))==sig} for sig in product((0,1),repeat=4)]
        orbits={}
        for E in candidates:
            if any(not inc(E,X) for X in known):continue
            forms=[S for S in allS if all(len(S&X)==1 for X in (*known,E))]
            if not forms or rank([[1,*[int(q in X) for X in (*known,E)]] for q in sorted(O)])!=5:continue
            sig=tuple(len(E&cell) for cell in orbitcells)
            if sig in orbits:orbits[sig]['labelled_E']+=1;continue
            assert E==set().union(*(set(sorted(cell)[:take]) for cell,take in zip(orbitcells,sig)))
            bools=fibers(D,E);allowed=[set(z['R']) for z in bools if z['covered_by_K'] and z['incomparable_with_distinct_known']]
            mandatory=set.intersection(*forms);rows,pairs=fields(D,E,allowed,parent,mandatory)
            orbits[sig]=dict(D=sorted(D),E=sorted(E),cell_signature=list(sig),labelled_E=1,
                orbit_size=math.prod(math.comb(len(cell),take) for cell,take in zip(orbitcells,sig)),
                feasible_nine_sets=len(forms),mandatory_through_seven=sorted(mandatory),mandatory_core_isolation_depth=7,
                preD_clique_depth=2,target_atoms=[dict(membership=list(s),targets=t) for s,t in atoms(D)],
                all_Boolean_one_count_fibers=bools,allowed_preD_fibers=[sorted(X) for X in allowed],
                additional_Boolean_fibers=[z['R'] for z in bools if set(z['R']) not in known and set(z['R'])!=E],
                additional_covered_fibers=[sorted(X) for X in allowed if X not in known and X!=E],rows=rows,pairs=pairs)
        for i,z in enumerate(orbits.values(),1):
            assert z['labelled_E']==z['orbit_size'];z['id']=parent['id']+'_fourth'+str(i);records.append(z)
        counts.append(dict(D=sorted(D),geometric_orbits=len(orbits),labelled_E=sum(z['labelled_E'] for z in orbits.values()),
            binary_field_pairs=sum(len(p['fourth_field_pairs']) for z in orbits.values() for p in z['pairs'])))
    names=[Path(__file__).name,'small_first_third_inventory.json','small_first_third_audit.json','SMALL_FIRST_THIRD_ADMISSION.md',
        'B1_C4_FOURTH_SPACE.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json',
        'LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md']
    result=dict(status='necessary_B1_C4_D_fourth_inventory',parameter=[13,9,1],B=[0],C=[4],
        counts=counts,records=records,source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete necessary five-branch fourth geometry, all Boolean companions and exact overlapping atom fields. No common E assumption, automaton existence, whole D/joint exclusion or F value.')
    (ROOT/'b1_c4_fourth_inventory.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps([dict(D=z['D'],E=z['E'],labels=z['labelled_E'],forms=z['feasible_nine_sets'],
        core=z['mandatory_through_seven'],companions=z['additional_Boolean_fibers'],covered=z['additional_covered_fibers'],
        supplying_rows=sum(r['preD']==z['E'] for r in z['rows']),pairs=sum(len(p['fourth_field_pairs']) for p in z['pairs'])) for z in records]))
if __name__=='__main__':main()
