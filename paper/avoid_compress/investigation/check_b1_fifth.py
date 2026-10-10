"""Independent literal-mask fifth geometry and deterministic checker.

No generator imports. Augmented integer ranks plus actual subset
families replace the coefficient-solving generator.
"""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};K={1,2}
FULL=(1<<13)-1;OUT=FULL^(1<<3)
def mask(X):return sum(1<<q for q in X)
def points(x):return [q for q in range(13) if x>>q&1]
def inc(x,y):return bool(x&~y) and bool(y&~x)
def rank(cols):
    work=[[int(bool(c>>q&1)) for c in cols] for q in points(OUT)];r=0
    for j in range(len(cols)):
        i=next((i for i in range(r,len(work)) if work[i][j]),None)
        if i is None:continue
        work[r],work[i]=work[i],work[r];v=pow(work[r][j],-1,1009)
        work[r]=[v*x%1009 for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j]
            if v:work[i]=[(x-v*y)%1009 for x,y in zip(work[i],work[r])]
        r+=1
    return r
def field_extension(E,F,allowed,parent,mandatory):
    caps=[1,1,2,1,len(E),8-len(E)];rows=[];records=[]
    for j,old in enumerate(parent['rows']):
        for preE in [A]+allowed:
            groups=[set(old[key]) for key in ('preA','preB','preC','preD')]+[preE]
            if sum(map(len,groups))!=len(set().union(*groups)):continue
            groups.append(Q-set().union(*groups))
            forced={p for X,cap in zip(groups,caps) if cap==1 for p in combinations(sorted(X),2)}
            if any(not set(p)&K or set(p)&mandatory for p in forced) or len(forced)>4:continue
            rows.append(dict(parent_row=j,preA=old['preA'],preB=old['preB'],preC=old['preC'],
                preD=old['preD'],preE=sorted(preE),forced_pairs=[list(p) for p in sorted(forced)],
                capacity=[min(len(X),cap) for X,cap in zip(groups,caps)]))
    for oldpair in parent['pairs']:
        for x,y in oldpair['fourth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                for j,right in enumerate(rows):
                    if (left['parent_row'],right['parent_row'])!=(x,y) or (x==y and i>j):continue
                    if left['preE']!=sorted(F) and right['preE']!=sorted(F):continue
                    if any(left['capacity'][h]+right['capacity'][h]<caps[h] for h in range(6)):continue
                    if len({tuple(p) for row in (left,right) for p in row['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=oldpair['original_rows'],original_fourth_rows=[x,y],fifth_field_pairs=pairs))
    return rows,records
def literal_disjoint_control(F):
    # Every alphabet, no pair capacities, no parent-row filtering.
    E={2,6};tested=0;admitted=0
    for groups in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
        tested+=1
        inputs=[*groups,F]
        if sum(map(len,inputs))==len(set().union(*inputs)):admitted+=1
    assert tested==120 and admitted==0
    return dict(F=sorted(F),all_individual_preimage_tuples=tested,disjoint_tuples=admitted)
def main():
    assert all(1009%q for q in range(2,32)) and 7**7<1009**2
    inv=json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'))
    parents=json.loads((ROOT/'b1_partial_cover_fourth_inventory.json').read_text(encoding='utf-8'))['records']
    forms=[x for x in range(FULL+1) if x&(1<<3) and x.bit_count()==9];assert len(forms)==495
    b,c,d,k=map(mask,(B,C,D,K))
    candidates=[x for x in range(1,FULL+1) if not x&(1<<3) and (x&~k).bit_count()<=1]
    assert len(candidates)==43
    summary=[];all_boolean_tests=0;column_tests=0;labelled=0
    for E in ({6},{2,6}):
        e=mask(E);parent=next(z for z in parents if set(z['E'])==E)
        members={}
        for f in candidates:
            if any(not inc(f,x) for x in (b,c,d,e)):continue
            family=[s for s in forms if all((s&x).bit_count()==1 for x in (b,c,d,e,f))]
            if not family or rank([OUT,b,c,d,e,f])!=6:continue
            sig=tuple(sum(bool(f>>q&1) and tuple(int(bool(x>>q&1)) for x in (k,b,c,d,e))==key for q in points(OUT))
                for key in product((0,1),repeat=5))
            members.setdefault(sig,[]).append(f)
        assert len(members)==7 and sum(map(len,members.values()))==27
        current=[z for z in inv['records'] if set(z['E'])==E];assert len(current)==7
        for z in current:
            f=mask(z['F']);sig=tuple(z['cell_signature'])
            assert f in members[sig] and len(members[sig])==z['labelled_F']==z['orbit_size']
            for chosen in members[sig]:
                columns=[OUT,b,c,d,e,chosen]
                family=[s for s in forms if all((s&x).bit_count()==1 for x in columns[1:])]
                common=FULL
                for s in family:common&=s
                assert len(family)==z['feasible_nine_sets']
                cell_masks={}
                for q in points(OUT):
                    key=tuple(int(bool(x>>q&1)) for x in columns[1:])
                    cell_masks[key]=cell_masks.get(key,0)|(1<<q)
                bools=[]
                for r in range(1,FULL+1):
                    if r&(1<<3):continue
                    all_boolean_tests+=1
                    # Every span column is constant on each membership cell.
                    if any(r&cell not in (0,cell) for cell in cell_masks.values()):continue
                    column_tests+=1
                    if rank(columns+[r])!=6 or any((s&r).bit_count()!=1 for s in family):continue
                    bools.append(r)
                provided=z['all_Boolean_one_count_fibers']
                if chosen!=f:
                    # Recover this labelled fiber by a literal cell permutation.
                    mapping={}
                    for key in product((0,1),repeat=5):
                        src=[q for q in points(OUT) if tuple(int(bool(x>>q&1)) for x in (k,b,c,d,e))==key]
                        fs=[q for q in src if f>>q&1];fn=[q for q in src if not f>>q&1]
                        ts=[q for q in src if chosen>>q&1];tn=[q for q in src if not chosen>>q&1]
                        mapping.update(zip(fs+fn,ts+tn))
                    expected={sum(1<<mapping[q] for q in item['R']) for item in provided}
                    assert set(bools)==expected
                else:
                    assert set(bools)=={mask(item['R']) for item in provided}
                    for item in provided:
                        coeff=list(map(Fraction,item['coefficients']));r=mask(item['R'])
                        assert all(sum(v*int(bool(x>>q&1)) for v,x in zip(coeff,columns))==int(bool(r>>q&1)) for q in points(OUT))
                        assert 8*coeff[0]+sum(coeff[1:])==1
                        assert item['covered_by_K']==((r&~k).bit_count()<=1)
                        assert item['incomparable_with_distinct_known']==all(r==x or inc(r,x) for x in columns[1:])
                    allowed=[r for r in bools if (r&~k).bit_count()<=1 and all(r==x or inc(r,x) for x in columns[1:])]
                    assert {mask(X) for X in z['allowed_preE_fibers']}==set(allowed)
                    assert points(common)==z['mandatory_through_six'] and points(k&~common)==z['remaining_P2_cover']
                    rows,pairs=field_extension(E,set(z['F']),[set(points(r)) for r in sorted(allowed,key=points)],parent,set(points(common)))
                    assert rows==z['rows'] and pairs==z['pairs']
                labelled+=1
            count=sum(len(p['fifth_field_pairs']) for p in z['pairs'])
            summary.append(dict(E=z['E'],F=z['F'],labelled_F=z['labelled_F'],binary_field_pairs=count,
                additional_Boolean_fibers=z['additional_Boolean_fibers'],additional_covered_fibers=z['additional_covered_fibers']))
    assert labelled==54 and len(summary)==14
    exclusions=[literal_disjoint_control(F) for F in ({1,2},{1,6},{2,4},{1,2,7})]
    assert [z['F'] for z in summary if z['E']==[2,6] and z['binary_field_pairs']==0]==[v['F'] for v in exclusions]
    assert sum(z['binary_field_pairs'] for z in summary if z['E']==[6])==414
    assert sum(z['binary_field_pairs'] for z in summary if z['E']==[2,6])==161
    for E in ([6],[2,6]):
        thirds={tuple(p['original_third_rows']) for z in inv['records'] if z['E']==E for p in z['pairs'] if p['fifth_field_pairs']}
        assert len(thirds)==14
    for name,digest in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    names=[Path(__file__).name,'enumerate_b1_fifth.py','b1_fifth_inventory.json','B1_FIFTH_ENTRANCE.md',
        'b1_partial_cover_fourth_inventory.json','b1_partial_cover_fourth_audit.json','B1_PARTIAL_COVER_FOURTH.md',
        'LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md',
        'CODIMENSION_FOUR_P5_DICHOTOMY.md']
    result=dict(status='pass',parameter=[13,9,1],complete_geometric_orbits=14,complete_labelled_F_choices=labelled,
        all_subset_masks_tested=all_boolean_tests,cell_constant_augmented_rank_tests=column_tests,
        records=summary,arbitrary_alphabet_crossed_fiber_exclusions=exclusions,
        remaining_E26_fifth_geometry=[[7],[1,7],[2,7]],remaining_E26_labelled_choices=18,
        binary_field_pairs=dict(E6=414,E26=161),all_original_third_pairs_retained=14,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete necessary fifth geometry and field admission, plus four all-alphabet crossed-fiber conditional exclusions. No whole E/third/joint exclusion, F value, transition-pair scan or numerical alphabet separation.')
    (ROOT/'b1_fifth_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key not in ('records','source_sha256')}))
if __name__=='__main__':main()
