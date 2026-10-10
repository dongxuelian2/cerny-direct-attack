"""Independent literal fourth geometry, all companions and complete fields."""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={4};K={1,2};FULL=8191;OUT=FULL^(1<<3)
KEYS=('preA','preB','preC')
def mask(X):return sum(1<<q for q in X)
def points(x):return [q for q in range(13) if x>>q&1]
def inc(x,y):return bool(x&~y) and bool(y&~x)
def rank(cols):
    a=[[int(bool(x>>q&1)) for x in cols] for q in points(OUT)];i=0
    for j in range(len(cols)):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];v=pow(a[i][j],-1,10007);a[i]=[x*v%10007 for x in a[i]]
        for k in range(i+1,len(a)):
            v=a[k][j]
            if v:a[k]=[(x-v*y)%10007 for x,y in zip(a[k],a[i])]
        i+=1
    return i
def output_atoms(D):
    known=(A,B,C,D);result=[];seen=set()
    for q in range(13):
        sig=tuple(q in X for X in known)
        if sig not in seen:
            seen.add(sig);result.append([t for t in range(13) if tuple(t in X for X in known)==sig])
    return result
def inputs(fields,targets,D):
    result=[[] for _ in targets]
    for q in range(13):
        sig=tuple(q in X for X in fields)
        found=[i for i,t in enumerate(targets) if tuple(t[0] in X for X in (A,B,C,D))==sig]
        if not found:return None
        assert len(found)==1;result[found[0]].append(q)
    return result
def admissible(groups,targets,protected):
    forced={p for source,target in zip(groups,targets) if len(target)==1 for p in combinations(source,2)}
    if len(forced)>4 or any(not set(p)&K or set(p)&protected for p in forced):return None
    return forced
def extension(D,E,allowed,parent,protected):
    targets=output_atoms(D);caps=list(map(len,targets));rows=[];pairs=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            cols=[set(old[k]) for k in KEYS]+[R];groups=inputs(cols,targets,D)
            if groups is None:continue
            forced=admissible(groups,targets,protected)
            if forced is None:continue
            rows.append(dict(parent_row=i,**{k:old[k] for k in KEYS},preD=sorted(R),atom_inputs=groups,
                forced_pairs=[list(p) for p in sorted(forced)],capacity=[min(len(x),cap) for x,cap in zip(groups,caps)]))
    for x,y in parent['binary_profile_pairs']:
        found=[]
        for i,l in enumerate(rows):
            for j,r in enumerate(rows):
                if (l['parent_row'],r['parent_row'])!=(x,y) or (x==y and i>j):continue
                if l['preD']!=sorted(E) and r['preD']!=sorted(E):continue
                if any(l['capacity'][h]+r['capacity'][h]<cap for h,cap in enumerate(caps)):continue
                if len({tuple(p) for row in (l,r) for p in row['forced_pairs']})>4:continue
                found.append([i,j])
        pairs.append(dict(original_third_rows=[x,y],fourth_field_pairs=found))
    return rows,pairs
def tuple_control(D,R,protected,parent):
    targets=output_atoms(D);tested=raw=kept=0;matches=set()
    for old in product([A,B],[A,B,C],[A,B,C,D]):
        tested+=1;groups=inputs([*old,R],targets,D)
        if groups is None:continue
        raw+=1
        if admissible(groups,targets,protected) is not None:
            kept+=1;matches.add(tuple(tuple(sorted(X)) for X in old))
    assert tested==24
    represented=set()
    for old in parent['rows']:
        groups=inputs([*(set(old[k]) for k in KEYS),R],targets,D)
        if groups is not None and admissible(groups,targets,protected) is not None:
            represented.add(tuple(tuple(old[k]) for k in KEYS))
    assert matches==represented
    return dict(R=sorted(R),individual_field_tuples=tested,raw_compatible_tuples=raw,admissible_tuples=kept)
def main():
    assert all(10007%d for d in range(2,101)) and 6**3<10007
    inv=json.loads((ROOT/'b1_c4_fourth_inventory.json').read_text())
    assert inv['B']==[0] and inv['C']==[4]
    parents=json.loads((ROOT/'small_first_third_inventory.json').read_text())['records']
    allS=[s for s in range(FULL+1) if s&(1<<3) and s.bit_count()==9]
    candidates=[e for e in range(1,FULL+1) if not e&(1<<3) and (e&~mask(K)).bit_count()<=1]
    summary=[];counts=[];labels=masks=ranktests=0
    for D in ({1},{5},{1,2},{1,5},{1,2,5}):
        known=list(map(mask,(B,C,D)));k=mask(K)
        parent=next(z for z in parents if z['joint_id']=='b1_in_c1' and z['D']==sorted(D))
        members={}
        for e in candidates:
            if any(not inc(e,x) for x in known):continue
            forms=[s for s in allS if all((s&x).bit_count()==1 for x in (*known,e))]
            if not forms or rank([OUT,*known,e])!=5:continue
            sig=tuple(sum(bool(e>>q&1) and tuple(int(bool(x>>q&1)) for x in (k,*known))==key for q in points(OUT)) for key in product((0,1),repeat=4))
            members.setdefault(sig,[]).append(e)
        profiles=[z for z in inv['records'] if z['D']==sorted(D)];assert len(members)==len(profiles)
        assert {tuple(z['cell_signature']) for z in profiles}==set(members)
        targets=output_atoms(D);before=len(summary)
        for z in profiles:
            e=mask(z['E']);sig=tuple(z['cell_signature']);assert e in members[sig]
            assert len(members[sig])==z['labelled_E']==z['orbit_size']
            assert [a['targets'] for a in z['target_atoms']]==targets
            assert all(a['membership']==[int(a['targets'][0] in X) for X in (A,B,C,D)] for a in z['target_atoms'])
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
                    if rank(cols+[r])==5 and all((s&r).bit_count()==1 for s in forms):bools.append(r)
                mapping={}
                for key in product((0,1),repeat=4):
                    cell=[q for q in points(OUT) if tuple(int(bool(x>>q&1)) for x in (k,*known))==key]
                    source=[q for q in cell if e>>q&1]+[q for q in cell if not e>>q&1]
                    target=[q for q in cell if actual>>q&1]+[q for q in cell if not actual>>q&1];mapping.update(zip(source,target))
                assert set(bools)=={sum(1<<mapping[q] for q in v['R']) for v in z['all_Boolean_one_count_fibers']}
                if actual==e:
                    assert len(z['all_Boolean_one_count_fibers'])==len({tuple(v['R']) for v in z['all_Boolean_one_count_fibers']})
                    for v in z['all_Boolean_one_count_fibers']:
                        co=list(map(Fraction,v['coefficients']));r=mask(v['R']);assert len(co)==5
                        assert all(sum(t*int(bool(x>>q&1)) for t,x in zip(co,cols))==int(bool(r>>q&1)) for q in points(OUT))
                        assert 8*co[0]+sum(co[1:])==1 and v['covered_by_K']==((r&~k).bit_count()<=1)
                        assert v['incomparable_with_distinct_known']==all(r==x or inc(r,x) for x in cols[1:])
                    allowed=[r for r in bools if (r&~k).bit_count()<=1 and all(r==x or inc(r,x) for x in cols[1:])]
                    assert {mask(X) for X in z['allowed_preD_fibers']}==set(allowed)
                    assert points(common)==z['mandatory_through_seven'] and z['mandatory_core_isolation_depth']==7
                    assert z['preD_clique_depth']==2 and common&mask(A|B)==mask(A|B)
                    rows,pairs=extension(D,set(z['E']),[set(points(r)) for r in sorted(allowed,key=points)],parent,set(points(common)))
                    assert rows==z['rows'] and pairs==z['pairs']
                labels+=1
            controls=[tuple_control(D,set(R),set(z['mandatory_through_seven']),parent) for R in z['allowed_preD_fibers'] if set(R) not in (B,C,D)]
            supply=next(t for t in controls if t['R']==z['E'])
            assert supply['admissible_tuples']==sum(r['preD']==z['E'] for r in z['rows'])
            core=set(z['mandatory_through_seven']);clique_cuts=[]
            for X,d in ((C,0),(D,1),(set(z['E']),2)):
                if len(X)>1 and X&core:clique_cuts.append(dict(clique=sorted(X),merging_depth=d,mandatory=sorted(X&core)))
            cover_cut=len(K-core)<=1
            excluded=bool(clique_cuts) or cover_cut or supply['admissible_tuples']==0
            summary.append(dict(D=z['D'],E=z['E'],labels=z['labelled_E'],forms=z['feasible_nine_sets'],
                mandatory=z['mandatory_through_seven'],additional_Boolean_fibers=z['additional_Boolean_fibers'],
                additional_covered_fibers=z['additional_covered_fibers'],individual_tuple_controls=controls,
                mandatory_clique_cuts=clique_cuts,remaining_P5_cover=sorted(K-core),known_compression_cover_cut=cover_cut,
                all_alphabet_excluded=excluded,binary_field_pairs=sum(len(p['fourth_field_pairs']) for p in z['pairs'])))
        branch=summary[before:];retained=[z for z in branch if not z['all_alphabet_excluded'] and z['binary_field_pairs']]
        original={tuple(xy) for xy in parent['binary_profile_pairs']}
        coverage={tuple(p['original_third_rows']) for z in profiles if any(z['E']==r['E'] for r in retained) for p in z['pairs'] if p['fourth_field_pairs']}
        assert coverage<=original
        counts.append(dict(D=sorted(D),geometric_orbits=len(profiles),labelled_E=sum(z['labelled_E'] for z in profiles),
            all_alphabet_excluded_E=[z['E'] for z in branch if z['all_alphabet_excluded']],
            remaining_unrestricted_E=[z['E'] for z in branch if not z['all_alphabet_excluded']],
            remaining_binary_E=[z['E'] for z in retained],remaining_binary_field_pairs=sum(z['binary_field_pairs'] for z in retained),
            original_third_pairs=len(original),remaining_original_third_pairs=len(coverage)))
    assert labels==sum(z['labelled_E'] for z in inv['records']) and masks==labels*4095
    for name,h in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
    names=[Path(__file__).name,'enumerate_b1_c4_fourth.py','b1_c4_fourth_inventory.json',
        'B1_C4_FOURTH_SPACE.md','small_first_third_inventory.json','small_first_third_audit.json',
        'SMALL_FIRST_THIRD_ADMISSION.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json',
        'LOCAL_EQUALITY_FLAG.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md']
    result=dict(status='pass',parameter=[13,9,1],B=[0],C=[4],geometric_orbits=len(summary),labelled_E=labels,
        all_subset_masks_tested=masks,augmented_rank_tests=ranktests,counts=counts,records=summary,
        all_companions_retained=True,complete_individual_tuple_controls_per_fiber=24,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Independent complete five-branch fourth geometry, exact overlapping atoms, Boolean companions, individual24-tuple controls, mandatory-clique/known-cover cuts and binary incoming capacity. All parent third types remain; no whole D/joint, F value or numerical alphabet separation.')
    (ROOT/'b1_c4_fourth_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ('status','geometric_orbits','labelled_E','all_subset_masks_tested','augmented_rank_tests','counts')}))
if __name__=='__main__':main()
