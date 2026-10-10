"""All labels, exact fields, Boolean identities and residual parents."""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};K={1,2};D={5};J={0,3,4,5}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transform(X,p):return sorted(p[q] for q in X)
def main():
    reports=['c4_d5_e12_e126_unrestricted_audit.json','letter_image_short_pair_cover_audit.json','b1_c4_fourth_audit.json']
    proof,generic,parent=map(read,reports)
    for z in (proof,generic,parent):
        assert z['status']=='pass'
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert proof['excluded_E']==[[1,2],[1,2,6]]
    third=read('small_first_third_inventory.json');inventory=read('b1_c4_fourth_inventory.json')
    root=next(z for z in third['records'] if z['id']=='b1_in_c1_third2')
    other=next(z for z in third['records'] if z['id']=='b1_out_c2_third2')
    swap=[4,1,2,3,0,5,6,7,8,9,10,11,12]
    assert root['labelled_D']==other['labelled_D']==8
    assert root['binary_profile_pairs']==other['binary_profile_pairs'] and len(root['binary_profile_pairs'])==14
    for key in ('B','C','D'):assert transform(root[key],swap)==other[key]
    for f,g in zip(root['rows'],other['rows']):
        for key in ('preA','preB','preC'):assert transform(f[key],swap)==g[key]
        assert f['cell_capacity']==g['cell_capacity']
        assert sorted(transform(pair,swap) for pair in f['forced_pairs'])==g['forced_pairs']
    profiles=[z for z in inventory['records'] if z['D']==[5] and z['E'] in proof['excluded_E']]
    assert [z['labelled_E'] for z in profiles]==[1,7]
    assert all(z['additional_covered_fibers']==[] and len(z['rows'])==16 for z in profiles)
    assert all(sum(len(p['fourth_field_pairs']) for p in z['pairs'])==41 for z in profiles)
    allS=[set(S) for S in combinations(range(13),9) if 3 in S];labels=identities=0;coverage=[]
    for t in (root,other):
        checked=0
        for d in range(5,13):
            for actualE in [K]+[K|{e} for e in range(5,13) if e!=d]:
                p=list(range(13))
                if t is other:p[0],p[4]=4,0
                p[5]=d
                if len(actualE)==3:
                    p[6]=next(iter(actualE-K));positions=range(7,13)
                    remaining=sorted(set(range(5,13))-{p[5],p[6]});canonicalE=[1,2,6]
                else:
                    positions=range(6,13);remaining=sorted(set(range(5,13))-{d});canonicalE=[1,2]
                for q,v in zip(positions,remaining):p[q]=v
                assert sorted(p)==list(range(13))
                z=next(z for z in profiles if z['E']==canonicalE)
                B=set(t['B']);C=set(t['C']);actualD={d};protected={0,3,4,d}
                initial=[S for S in allS if all(len(S&X)==1 for X in (B,C,actualD,actualE))]
                assert len(initial)==z['feasible_nine_sets']==(70 if len(actualE)==2 else 45)
                assert set.intersection(*initial)==protected
                fields={tuple(tuple(transform(f[k],p)) for k in ('preA','preB','preC','preD')) for f in z['rows']}
                direct=set()
                for cols in product((A,B),(A,B,C),(A,B,C,actualD),(A,B,C,actualD,actualE)):
                    if all(sum(q in X for X in cols)<=1 for q in Q):direct.add(tuple(tuple(sorted(X)) for X in cols))
                assert fields==direct and len(fields)==16
                assert sum(set(f[3])==actualE for f in fields)==8
                assert sum(set(f[2])==actualD and set(f[3])==actualE for f in fields)==4
                for f in z['all_Boolean_one_count_fibers']:
                    R=set(transform(f['R'],p));co=list(map(Fraction,f['coefficients']));cols=[Q-A,B,C,actualD,actualE]
                    assert all(sum(c*int(q in X) for c,X in zip(co,cols))==int(q in R) for q in Q-A)
                    assert 8*co[0]+sum(co[1:])==1 and all(len(S&R)==1 for S in initial)
                    identities+=1
                if len(actualE)==2:
                    assert actualE==K and {d}<=protected
                else:
                    assert len(list(combinations(sorted(actualE),2)))==3
                labels+=1;checked+=1
        coverage.append(dict(id=t['id'],D_labels=8,E_labels_per_D=8,labelled_extensions=checked,
                             normalized_fourth_pairs_excluded=82,whole_third_excluded=False))
    remaining=[z for z in inventory['records'] if z['D']==[5] and z['E'] in ([6],[1,6])]
    assert (len(remaining),sum(z['labelled_E'] for z in remaining),sum(len(p['fourth_field_pairs']) for z in remaining for p in z['pairs']))==(2,21,82)
    residual={tuple(p['original_third_rows']) for z in remaining for p in z['pairs'] if p['fourth_field_pairs']}
    assert residual==set(map(tuple,root['binary_profile_pairs']))
    names=[Path(__file__).name,'C4_D5_E12_E126_UNRESTRICTED_EXCLUSION.md',*reports,
           'b1_c4_fourth_inventory.json','B1_C4_FOURTH_SPACE.md','small_first_third_inventory.json',
           'small_first_third_audit.json','SMALL_FIRST_THIRD_ADMISSION.md',
           'MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json',
           'TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md','two_cover_unique_immediate_pair_audit.json',
           'LETTER_IMAGE_SHORT_PAIR_COVER.md','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    result=dict(status='pass',parameter=[13,9,1],coverage=coverage,
                labelled_extensions_checked=labels,Boolean_identities_checked=identities,
                new_normalized_unrestricted_fourth_cuts_both_roots=4,
                newly_removed_current_binary_fourth_pairs_both_roots=164,
                remaining_C4_D5_E=[z['E'] for z in remaining],remaining_C4_geometries=2,
                remaining_C4_E_labels=21,remaining_C4_binary_pairs=82,
                whole_third_types_removed=0,binary_parent_pairs_removed=0,
                source_sha256={n:sha(ROOT/n) for n in names},
                scope='Two complete E geometries excluded at both singleton-C/D5 roots; E6/E16 and all F extrema unresolved.')
    assert (labels,identities)==(128,512)
    (ROOT/'singleton_c_d5_e12_e126_transport_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','coverage')}),flush=True)
if __name__=='__main__':main()
