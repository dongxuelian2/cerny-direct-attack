"""Independent paired-G seventh spaces, overlapping atoms and extension completeness."""
from itertools import combinations,product,permutations
from fractions import Fraction
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};E={6};F={2,7};G=None;K={1,2}
KNOWN=();KEYS=('preA','preB','preC','preD','preE','preF')
FULL=8191;OUT=FULL^(1<<3);P={0,3,5,6,8}

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

def output_atoms(G):
    fields=(A,B,C,D,E,F,G);groups=[];seen=set()
    for t in range(13):
        signature=tuple(t in X for X in fields)
        if signature in seen:continue
        seen.add(signature);groups.append([q for q in range(13) if tuple(q in X for X in fields)==signature])
    return groups

def atom_input(fields,targets):
    groups=[[] for _ in targets]
    for q in range(13):
        wanted=tuple(q in X for X in fields)
        found=[j for j,out in enumerate(targets) if tuple(out[0] in X for X in (A,B,C,D,E,F,G))==wanted]
        if not found:return None
        assert len(found)==1;groups[found[0]].append(q)
    return groups

def admissible(groups,targets,protected):
    forced={p for inputs,outputs in zip(groups,targets) if len(outputs)==1 for p in combinations(inputs,2)}
    if len(forced)>4 or any(not set(p)&K or set(p)&protected for p in forced):return None
    return forced

def extension(H,allowed,parent,protected):
    targets=output_atoms(G);caps=list(map(len,targets));rows=[];records=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            fields=[set(old[k]) for k in KEYS]+[R];groups=atom_input(fields,targets)
            if groups is None:continue
            forced=admissible(groups,targets,protected)
            if forced is None:continue
            rows.append(dict(parent_row=i,**{k:old[k] for k in KEYS},preG=sorted(R),atom_inputs=groups,
                forced_pairs=[list(p) for p in sorted(forced)],capacity=[min(len(x),cap) for x,cap in zip(groups,caps)]))
    for prev in parent['pairs']:
        for x,y in prev['sixth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                for j,right in enumerate(rows):
                    if (left['parent_row'],right['parent_row'])!=(x,y) or (x==y and i>j):continue
                    if left['preG']!=sorted(H) and right['preG']!=sorted(H):continue
                    if any(left['capacity'][h]+right['capacity'][h]<cap for h,cap in enumerate(caps)):continue
                    if len({tuple(p) for r in (left,right) for p in r['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=prev['original_third_rows'],original_fourth_rows=prev['original_fourth_rows'],
                original_fifth_rows=prev['original_fifth_rows'],original_sixth_rows=[x,y],seventh_field_pairs=pairs))
    return rows,records

def full_tuple_control(R,protected,parent):
    choices=([A,B],[A,B,C],[A,B,C,D],[A,B,C,D,E],[A,B,C,D,E,F],[A,B,C,D,E,F,G])
    tested=raw=kept=0;matches=set();targets=output_atoms(G)
    for old in product(*choices):
        tested+=1;groups=atom_input([*old,R],targets)
        if groups is None:continue
        raw+=1
        if admissible(groups,targets,protected) is not None:
            kept+=1;matches.add(tuple(tuple(sorted(X)) for X in old))
    assert tested==5040
    represented={tuple(tuple(row[k]) for k in KEYS) for row in parent['rows']
        if atom_input([*(set(row[k]) for k in KEYS),R],targets) is not None
        and admissible(atom_input([*(set(row[k]) for k in KEYS),R],targets),targets,protected) is not None}
    assert matches==represented
    return dict(R=sorted(R),individual_field_tuples=tested,raw_compatible_tuples=raw,necessary_admissible_tuples=kept)

def main():
    global G,KNOWN
    assert all(100003%d for d in range(2,317)) and 9**9<100003**2
    inv=json.loads((ROOT/'b1_f27_paired_g_seventh_inventory.json').read_text())
    parents=json.loads((ROOT/'b1_sixth_inventory.json').read_text())['records']
    allS=[s for s in range(FULL+1) if s&(1<<3) and s.bit_count()==9]
    candidates=[h for h in range(1,FULL+1) if not h&(1<<3) and (h&~mask(K)).bit_count()<=1]
    summary=[];masks=ranktests=labels=0;counts=[]
    for G in ({1,8},{2,8}):
        KNOWN=(B,C,D,E,F,G);known=list(map(mask,KNOWN));k=mask(K)
        parent=next(z for z in parents if z['E']==[6] and z['F']==[2,7] and z['G']==sorted(G))
        assert parent['additional_Boolean_fibers']==[];members={}
        for h in candidates:
            if any(not inc(h,x) for x in known):continue
            forms=[s for s in allS if all((s&x).bit_count()==1 for x in (*known,h))]
            if not forms or rank([OUT,*known,h])!=8:continue
            sig=tuple(sum(bool(h>>q&1) and tuple(int(bool(x>>q&1)) for x in (k,*known))==key for q in points(OUT))
                for key in product((0,1),repeat=7));members.setdefault(sig,[]).append(h)
        profiles=[z for z in inv['records'] if z['G']==sorted(G)]
        assert len(members)==len(profiles)==8 and sum(map(len,members.values()))==20
        assert {tuple(z['cell_signature']) for z in profiles}==set(members)
        targets=output_atoms(G);assert len(targets)==9 and sum(map(len,targets))==13
        before=len(summary)
        for z in profiles:
            h=mask(z['H']);sig=tuple(z['cell_signature'])
            assert h in members[sig] and len(members[sig])==z['labelled_H']==z['orbit_size']
            assert [atom['targets'] for atom in z['target_atoms']]==targets
            for t in z['target_atoms']:
                assert t['membership']==[int(t['targets'][0] in X) for X in (A,B,C,D,E,F,G)]
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
                mapping={}
                for key in product((0,1),repeat=7):
                    cell=[q for q in points(OUT) if tuple(int(bool(x>>q&1)) for x in (k,*known))==key]
                    source=[q for q in cell if h>>q&1]+[q for q in cell if not h>>q&1]
                    target=[q for q in cell if actual>>q&1]+[q for q in cell if not actual>>q&1];mapping.update(zip(source,target))
                assert set(bools)=={sum(1<<mapping[q] for q in v['R']) for v in z['all_Boolean_one_count_fibers']}
                if actual==h:
                    for v in z['all_Boolean_one_count_fibers']:
                        co=list(map(Fraction,v['coefficients']));r=mask(v['R'])
                        assert all(sum(t*int(bool(x>>q&1)) for t,x in zip(co,cols))==int(bool(r>>q&1)) for q in points(OUT))
                        assert 8*co[0]+sum(co[1:])==1
                        assert v['covered_by_K']==((r&~k).bit_count()<=1)
                    assert points(common)==z['mandatory_through_four'] and z['mandatory_core_isolation_depth']==7
                    assert not common&mask(F|G) and common&mask({0,3,5,6})==mask({0,3,5,6})
                    assert z['preG_clique_depth']==3 and {mask(R) for R in z['allowed_preG_fibers']}==set(allowed)
                    rows,pairs=extension(set(z['H']),[set(points(r)) for r in sorted(allowed,key=points)],parent,set(points(common)))
                    assert rows==z['rows'] and pairs==z['pairs']
                labels+=1
            controls=[full_tuple_control(set(R),set(z['mandatory_through_four']),parent)
                for R in z['allowed_preG_fibers'] if set(R) not in KNOWN]
            supplying=next(t for t in controls if t['R']==z['H'])
            assert supplying['necessary_admissible_tuples']==sum(r['preG']==z['H'] for r in z['rows'])
            summary.append(dict(G=z['G'],H=z['H'],labels=z['labelled_H'],forms=z['feasible_nine_sets'],
                mandatory=z['mandatory_through_four'],additional_Boolean_fibers=z['additional_Boolean_fibers'],
                additional_covered_fibers=z['additional_covered_fibers'],complete_individual_tuple_controls=controls,
                all_alphabet_excluded=supplying['necessary_admissible_tuples']==0,
                binary_field_pairs=sum(len(p['seventh_field_pairs']) for p in z['pairs'])))
        branch=summary[before:];retained=[z for z in profiles if any(p['seventh_field_pairs'] for p in z['pairs'])]
        coverage={tuple(p['original_sixth_rows']) for z in retained for p in z['pairs'] if p['seventh_field_pairs']}
        original={tuple(xy) for p in parent['pairs'] for xy in p['sixth_field_pairs']}
        assert coverage<=original
        counts.append(dict(G=sorted(G),geometric_orbits=8,labelled_H=20,
            all_alphabet_excluded_H=[z['H'] for z in branch if z['all_alphabet_excluded']],
            binary_zero_pair_H=[z['H'] for z in branch if not z['binary_field_pairs']],
            remaining_binary_H=[z['H'] for z in branch if z['binary_field_pairs']],
            binary_field_pairs=sum(z['binary_field_pairs'] for z in branch),original_sixth_pairs=len(original),
            remaining_original_sixth_pairs=len(coverage)))
    assert labels==40 and masks==163800
    for name,digest in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    names=[Path(__file__).name,'enumerate_b1_f27_paired_g_seventh.py','b1_f27_paired_g_seventh_inventory.json',
        'B1_F27_PAIRED_G_SEVENTH.md','b1_sixth_inventory.json','b1_sixth_audit.json','B1_SIXTH_ENTRANCE.md',
        'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    result=dict(status='pass',parameter=[13,9,1],E=[6],F=[2,7],geometric_orbits=16,labelled_H=40,
        all_subset_masks_tested=masks,augmented_rank_tests=ranktests,records=summary,counts=counts,
        target_atoms=9,complete_input_field_tuples_per_fiber=5040,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete independent seventh geometry, every Boolean companion, overlapping-atom extension and5040-tuple completeness controls for each fresh/companion fiber. Some fibers excluded individually for every alphabet; binary zero-pair cuts explicitly separate. No whole G/F/E/third/joint or extremal F value.')
    (ROOT/'b1_f27_paired_g_seventh_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(dict(status='pass',orbits=16,labels=40,masks=masks,ranktests=ranktests,counts=counts)),flush=True)
if __name__=='__main__':main()
