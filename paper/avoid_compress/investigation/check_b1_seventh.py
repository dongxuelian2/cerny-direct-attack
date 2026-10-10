"""Independent literal-mask/rank and strong-core seventh admission."""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};E={6};F={7};G={8};K={1,2}
KNOWN=(B,C,D,E,F,G);KEYS=('preA','preB','preC','preD','preE','preF');FULL=(1<<13)-1;OUT=FULL^(1<<3)
def mask(X):return sum(1<<q for q in X)
def points(x):return [q for q in range(13) if x>>q&1]
def inc(x,y):return bool(x&~y) and bool(y&~x)
def rank(cols):
    work=[[int(bool(x>>q&1)) for x in cols] for q in points(OUT)];r=0
    for j in range(len(cols)):
        i=next((i for i in range(r,len(work)) if work[i][j]),None)
        if i is None:continue
        work[r],work[i]=work[i],work[r];v=pow(work[r][j],-1,100003)
        work[r]=[x*v%100003 for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j]
            if v:work[i]=[(x-v*y)%100003 for x,y in zip(work[i],work[r])]
        r+=1
    return r
def extension(H,allowed,parent,protected):
    caps=[1,1,2,1,1,1,1,5];rows=[];records=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            groups=[set(old[key]) for key in KEYS]+[R]
            if sum(map(len,groups))!=len(set().union(*groups)):continue
            groups.append(Q-set().union(*groups))
            forced={p for X,cap in zip(groups,caps) if cap==1 for p in combinations(sorted(X),2)}
            if len(forced)>4 or any(not set(p)&K or set(p)&protected for p in forced):continue
            rows.append(dict(parent_row=i,**{key:old[key] for key in KEYS},preG=sorted(R),
                forced_pairs=[list(p) for p in sorted(forced)],capacity=[min(len(X),cap) for X,cap in zip(groups,caps)]))
    for previous in parent['pairs']:
        for x,y in previous['sixth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                for j,right in enumerate(rows):
                    if (left['parent_row'],right['parent_row'])!=(x,y) or (x==y and i>j):continue
                    if left['preG']!=sorted(H) and right['preG']!=sorted(H):continue
                    if any(left['capacity'][h]+right['capacity'][h]<caps[h] for h in range(8)):continue
                    if len({tuple(p) for row in (left,right) for p in row['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=previous['original_third_rows'],original_fourth_rows=previous['original_fourth_rows'],
                original_fifth_rows=previous['original_fifth_rows'],original_sixth_rows=[x,y],seventh_field_pairs=pairs))
    return rows,records
def main():
    assert all(100003%q for q in range(2,317)) and 9**9<100003**2
    coreaudit=json.loads((ROOT/'mandatory_core_isolation_audit.json').read_text(encoding='utf-8'));assert coreaudit['status']=='pass'
    inv=json.loads((ROOT/'b1_seventh_inventory.json').read_text(encoding='utf-8'))
    parent=next(z for z in json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))['records'] if z['E']==[6] and z['F']==[7] and z['G']==[8])
    known=list(map(mask,KNOWN));k=mask(K)
    allS=[s for s in range(FULL+1) if s&(1<<3) and s.bit_count()==9];assert len(allS)==495
    candidates=[h for h in range(1,FULL+1) if not h&(1<<3) and (h&~k).bit_count()<=1];assert len(candidates)==43
    members={}
    for h in candidates:
        if any(not inc(h,x) for x in known):continue
        forms=[s for s in allS if all((s&x).bit_count()==1 for x in (*known,h))]
        if not forms or rank([OUT,*known,h])!=8:continue
        sig=tuple(sum(bool(h>>q&1) and tuple(int(bool(x>>q&1)) for x in (k,*known))==key for q in points(OUT)) for key in product((0,1),repeat=7))
        members.setdefault(sig,[]).append(h)
    assert len(members)==7 and sum(map(len,members.values()))==19
    labelled=masks=ranktests=0;summary=[];covered_companions=0
    for z in inv['records']:
        h=mask(z['H']);sig=tuple(z['cell_signature']);assert h in members[sig]
        assert len(members[sig])==z['labelled_H']==z['orbit_size']
        for actual in members[sig]:
            cols=[OUT,*known,actual];forms=[s for s in allS if all((s&x).bit_count()==1 for x in cols[1:])]
            assert len(forms)==z['feasible_nine_sets'];common=FULL
            for s in forms:common&=s
            cells={}
            for q in points(OUT):
                key=tuple(int(bool(x>>q&1)) for x in cols[1:]);cells[key]=cells.get(key,0)|(1<<q)
            bools=[]
            for r in range(1,FULL+1):
                if r&(1<<3):continue
                masks+=1
                if any(r&cell not in (0,cell) for cell in cells.values()):continue
                ranktests+=1
                if rank(cols+[r])==8 and all((s&r).bit_count()==1 for s in forms):bools.append(r)
            allowed=[r for r in bools if (r&~k).bit_count()<=1 and all(r==x or inc(r,x) for x in cols[1:])]
            assert set(allowed)==set(cols[1:])
            if actual!=h:
                mapping={}
                for key in product((0,1),repeat=7):
                    cell=[q for q in points(OUT) if tuple(int(bool(x>>q&1)) for x in (k,*known))==key]
                    source=[q for q in cell if h>>q&1]+[q for q in cell if not h>>q&1]
                    target=[q for q in cell if actual>>q&1]+[q for q in cell if not actual>>q&1];mapping.update(zip(source,target))
                assert set(bools)=={sum(1<<mapping[q] for q in v['R']) for v in z['all_Boolean_one_count_fibers']}
            else:
                assert set(bools)=={mask(v['R']) for v in z['all_Boolean_one_count_fibers']}
                for v in z['all_Boolean_one_count_fibers']:
                    coef=list(map(Fraction,v['coefficients']));r=mask(v['R'])
                    assert all(sum(t*int(bool(x>>q&1)) for t,x in zip(coef,cols))==int(bool(r>>q&1)) for q in points(OUT))
                    assert 8*coef[0]+sum(coef[1:])==1
                    assert v['covered_by_K']==((r&~k).bit_count()<=1)
                    assert v['incomparable_with_distinct_known']==all(r==x or inc(r,x) for x in cols[1:])
                assert points(common)==z['mandatory_through_four']==z['immediate_kernel_protected']
                assert z['mandatory_core_isolation_depth']==12-4-1==7
                assert {mask(v) for v in z['allowed_preG_fibers']}==set(allowed) and not z['additional_covered_fibers']
                rows,pairs=extension(set(z['H']),[set(points(r)) for r in sorted(allowed,key=points)],parent,set(points(common)))
                assert rows==z['rows'] and pairs==z['pairs']
            labelled+=1
        summary.append(dict(H=z['H'],labelled_H=z['labelled_H'],field_pairs=sum(len(p['seventh_field_pairs']) for p in z['pairs']),
            additional_Boolean_fibers=z['additional_Boolean_fibers'],additional_covered_fibers=z['additional_covered_fibers']))
    assert labelled==19 and len(summary)==7 and masks==19*4095
    assert [v['field_pairs'] for v in summary]==[1094,1094,48,48,48,1094,48]
    extras=[v for v in summary if v['additional_Boolean_fibers']]
    assert [v['H'] for v in extras]==[[2],[9],[2,9]]
    assert [v['additional_Boolean_fibers'] for v in extras]==[[[9,10,11,12]],[[2,10,11,12]],[[10,11,12]]]
    control=next(v for v in coreaudit['conditional_all_alphabet_cover_exclusions'] if v['branch']=='E6_F7_G8_H2')
    assert control['core_isolation_depth']==7 and control['remaining_P5_cover']==[1]
    kept=[z for z in inv['records'] if z['H']!=[2]]
    coverage={tuple(p['original_sixth_rows']) for z in kept for p in z['pairs'] if p['seventh_field_pairs']}
    original={tuple(xy) for p in parent['pairs'] for xy in p['sixth_field_pairs']}
    assert coverage==original and len(coverage)==365
    assert sum(z['labelled_H'] for z in kept)==18 and sum(len(p['seventh_field_pairs']) for z in kept for p in z['pairs'])==2380
    for name,digest in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    names=[Path(__file__).name,'enumerate_b1_seventh.py','b1_seventh_inventory.json','B1_SEVENTH_ENTRANCE.md',
        'b1_sixth_inventory.json','b1_sixth_audit.json','B1_SIXTH_ENTRANCE.md','B1_FIFTH_ENTRANCE.md',
        'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md']
    result=dict(status='pass',parameter=[13,9,1],branch=dict(E=[6],F=[7],G=[8]),alphabet='arbitrary finite',
        complete_geometric_orbits=7,complete_labelled_H_choices=labelled,all_subset_masks_tested=masks,
        cell_constant_augmented_rank_tests=ranktests,records=summary,common_seventh_after_cover=True,
        additional_Boolean_orbits=3,additional_covered_orbits=0,excluded_H=[2],excluded_field_pairs=1094,
        remaining_geometric_orbits=6,remaining_labelled_H=18,remaining_binary_field_pairs=2380,
        all_original_sixth_pairs_retained=365,mandatory_isolation_depth=7,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete seventh space/Boolean/field admission, common fiber after explicit cover filtering, and mandatory-core all-alphabet H2 exclusion. No whole sixth/fifth/joint exclusion, full13-state automaton scan, F value or numerical alphabet separation.')
    (ROOT/'b1_seventh_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key not in ('records','source_sha256')}))
if __name__=='__main__':main()
