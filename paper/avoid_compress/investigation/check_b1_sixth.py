"""Independent seventh-column/rank and literal sixth admission audit."""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};K={1,2}
FULL=(1<<13)-1;OUT=FULL^(1<<3);KEYS=('preA','preB','preC','preD','preE')
def mask(X):return sum(1<<q for q in X)
def points(x):return [q for q in range(13) if x>>q&1]
def inc(x,y):return bool(x&~y) and bool(y&~x)
def rank(cols):
    work=[[int(bool(c>>q&1)) for c in cols] for q in points(OUT)];r=0
    for j in range(len(cols)):
        i=next((i for i in range(r,len(work)) if work[i][j]),None)
        if i is None:continue
        work[r],work[i]=work[i],work[r];scale=pow(work[r][j],-1,10007)
        work[r]=[x*scale%10007 for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j]
            if v:work[i]=[(x-v*y)%10007 for x,y in zip(work[i],work[r])]
        r+=1
    return r
def extension(E,F,G,allowed,parent,mandatory):
    caps=[1,1,2,1,len(E),len(F),8-len(E)-len(F)];rows=[];records=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            groups=[set(old[key]) for key in KEYS]+[R]
            if sum(map(len,groups))!=len(set().union(*groups)):continue
            groups.append(Q-set().union(*groups))
            forced={p for X,cap in zip(groups,caps) if cap==1 for p in combinations(sorted(X),2)}
            if len(forced)>4 or any(not set(p)&K or set(p)&mandatory for p in forced):continue
            rows.append(dict(parent_row=i,**{key:old[key] for key in KEYS},preF=sorted(R),
                forced_pairs=[list(p) for p in sorted(forced)],capacity=[min(len(X),cap) for X,cap in zip(groups,caps)]))
    for previous in parent['pairs']:
        for x,y in previous['fifth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                for j,right in enumerate(rows):
                    if (left['parent_row'],right['parent_row'])!=(x,y) or (x==y and i>j):continue
                    if left['preF']!=sorted(G) and right['preF']!=sorted(G):continue
                    if any(left['capacity'][h]+right['capacity'][h]<caps[h] for h in range(7)):continue
                    if len({tuple(p) for row in (left,right) for p in row['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=previous['original_third_rows'],original_fourth_rows=previous['original_fourth_rows'],
                original_fifth_rows=[x,y],sixth_field_pairs=pairs))
    return rows,records
def disjoint_control(E,F,G):
    choices=[(A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E),(A,B,C,D,E,F)]
    tested=0;admitted=[]
    for fields in product(*choices):
        tested+=1;groups=[*fields,G]
        if sum(map(len,groups))==len(set().union(*groups)):admitted.append(groups)
    assert tested==720 and not admitted
    return dict(E=sorted(E),F=sorted(F),G=sorted(G),individual_preimage_tuples=tested,disjoint_tuples=0)
def main():
    assert all(10007%q for q in range(2,101)) and 8**8<10007**2
    inv=json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))
    parents=json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'))['records']
    allS=[s for s in range(FULL+1) if s&(1<<3) and s.bit_count()==9];assert len(allS)==495
    k=mask(K);candidates=[r for r in range(1,FULL+1) if not r&(1<<3) and (r&~k).bit_count()<=1];assert len(candidates)==43
    labelled=0;masks=0;ranktests=0;summary=[];exclusions=[];paircounts=[]
    for E,F in (({6},{7}),({6},{2,7}),({2,6},{7})):
        parent=next(z for z in parents if set(z['E'])==E and set(z['F'])==F)
        known=list(map(mask,(B,C,D,E,F)));members={}
        for g in candidates:
            if any(not inc(g,x) for x in known):continue
            forms=[s for s in allS if all((s&x).bit_count()==1 for x in (*known,g))]
            if not forms or rank([OUT,*known,g])!=7:continue
            sig=tuple(sum(bool(g>>q&1) and tuple(int(bool(x>>q&1)) for x in (k,*known))==key for q in points(OUT))
                for key in product((0,1),repeat=6))
            members.setdefault(sig,[]).append(g)
        assert len(members)==7 and sum(map(len,members.values()))==23
        records=[z for z in inv['records'] if set(z['E'])==E and set(z['F'])==F];assert len(records)==7
        for z in records:
            g=mask(z['G']);sig=tuple(z['cell_signature']);assert g in members[sig]
            assert len(members[sig])==z['labelled_G']==z['orbit_size']
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
                    if rank(cols+[r])==7 and all((s&r).bit_count()==1 for s in forms):bools.append(r)
                if actual!=g:
                    mapping={}
                    for key in product((0,1),repeat=6):
                        cell=[q for q in points(OUT) if tuple(int(bool(x>>q&1)) for x in (k,*known))==key]
                        source=[q for q in cell if g>>q&1]+[q for q in cell if not g>>q&1]
                        target=[q for q in cell if actual>>q&1]+[q for q in cell if not actual>>q&1]
                        mapping.update(zip(source,target))
                    assert set(bools)=={sum(1<<mapping[q] for q in v['R']) for v in z['all_Boolean_one_count_fibers']}
                else:
                    assert set(bools)=={mask(v['R']) for v in z['all_Boolean_one_count_fibers']}
                    for v in z['all_Boolean_one_count_fibers']:
                        coef=list(map(Fraction,v['coefficients']));r=mask(v['R'])
                        assert all(sum(t*int(bool(x>>q&1)) for t,x in zip(coef,cols))==int(bool(r>>q&1)) for q in points(OUT))
                        assert 8*coef[0]+sum(coef[1:])==1
                        assert v['covered_by_K']==((r&~k).bit_count()<=1)
                        assert v['incomparable_with_distinct_known']==all(r==x or inc(r,x) for x in cols[1:])
                    allowed=[r for r in bools if (r&~k).bit_count()<=1 and all(r==x or inc(r,x) for x in cols[1:])]
                    assert set(allowed)=={mask(v) for v in z['allowed_preF_fibers']}
                    assert points(common)==z['mandatory_through_five'] and points(k&~common)==z['remaining_P1_cover']
                    rows,pairs=extension(E,F,set(z['G']),[set(points(r)) for r in sorted(allowed,key=points)],parent,set(points(common)))
                    assert rows==z['rows'] and pairs==z['pairs']
                labelled+=1
            count=sum(len(p['sixth_field_pairs']) for p in z['pairs'])
            if E=={6} and F=={2,7} and z['G'] in ([1,2],[1,7],[2,4],[1,2,8]):
                assert count==0;exclusions.append(disjoint_control(E,F,set(z['G'])))
            if E=={2,6} and F=={7} and z['G'] in ([1,2],[1,6],[2,4],[1,2,8]):
                assert count==0;exclusions.append(disjoint_control(E,F,set(z['G'])))
            summary.append(dict(E=z['E'],F=z['F'],G=z['G'],labelled_G=z['labelled_G'],binary_field_pairs=count,
                additional_Boolean_fibers=z['additional_Boolean_fibers'],additional_covered_fibers=z['additional_covered_fibers']))
        coverage={tuple(p['original_fifth_rows']) for z in records for p in z['pairs'] if p['sixth_field_pairs']}
        original={tuple(xy) for p in parent['pairs'] for xy in p['fifth_field_pairs']}
        assert coverage==original and len(coverage)==122
        paircounts.append(dict(E=sorted(E),F=sorted(F),sixth_field_pairs=sum(v['binary_field_pairs'] for v in summary if v['E']==sorted(E) and v['F']==sorted(F)),
            all_original_fifth_pairs_retained=len(coverage)))
    assert labelled==69 and len(summary)==21 and len(exclusions)==8
    assert [v['sixth_field_pairs'] for v in paircounts]==[1191,470,443]
    for name,digest in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    names=[Path(__file__).name,'enumerate_b1_sixth.py','b1_sixth_inventory.json','B1_SIXTH_ENTRANCE.md',
        'b1_fifth_inventory.json','b1_fifth_audit.json','B1_FIFTH_ENTRANCE.md','B1_PARTIAL_COVER_FOURTH.md',
        'LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md']
    result=dict(status='pass',parameter=[13,9,1],selected_branches=[dict(E=v['E'],F=v['F']) for v in paircounts],
        complete_geometric_orbits=21,complete_labelled_G_choices=labelled,all_subset_masks_tested=masks,
        cell_constant_augmented_rank_tests=ranktests,records=summary,arbitrary_alphabet_crossed_fiber_exclusions=exclusions,
        binary_field_admission=paircounts,singleton2_isolation_depth=1,uses_singleton_P2_cover_argument=False,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete selected sixth geometry/Boolean/field admission and eight all-alphabet crossed-fiber cuts. No whole fifth/third/joint exclusion, full transition scan, F value or numerical alphabet separation.')
    (ROOT/'b1_sixth_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key not in ('records','source_sha256','arbitrary_alphabet_crossed_fiber_exclusions')}))
if __name__=='__main__':main()
