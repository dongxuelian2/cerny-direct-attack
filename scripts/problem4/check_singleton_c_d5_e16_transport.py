"""All E16 field and Boolean transports and exact E6 residual accounting."""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};K={1,2};D={5};E={1,6}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transform(X,p):return sorted(p[q] for q in X)
def main():
    reports=['two_cover_protected_kernel_graph_audit.json','b1_c4_fourth_audit.json']
    for n in reports:
        z=read(n);assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
    inv=read('b1_c4_fourth_inventory.json');third=read('small_first_third_inventory.json')['records']
    root=next(z for z in third if z['id']=='b1_in_c1_third2');other=next(z for z in third if z['id']=='b1_out_c2_third2')
    z=next(z for z in inv['records'] if z['D']==[5] and z['E']==[1,6])
    assert z['additional_covered_fibers']==[] and z['labelled_E']==14 and len(z['rows'])==16
    assert sum(len(p['fourth_field_pairs']) for p in z['pairs'])==41
    assert len(root['binary_profile_pairs'])==len(other['binary_profile_pairs'])==14
    allS=[set(S) for S in combinations(range(13),9) if 3 in S];labels=identities=0;coverage=[]
    for t in (root,other):
        checked=0
        for d in range(5,13):
            for guard in (1,2):
                for e in range(5,13):
                    if e==d:continue
                    p=list(range(13))
                    if t is other:p[0],p[4]=4,0
                    if guard==2:p[1],p[2]=2,1
                    p[5],p[6]=d,e
                    for q,v in zip(range(7,13),sorted(set(range(5,13))-{d,e})):p[q]=v
                    assert sorted(p)==list(range(13))
                    B=set(t['B']);C=set(t['C']);actualD={d};actualE={guard,e}
                    assert set(transform(E,p))==actualE and d not in actualE
                    initial=[S for S in allS if all(len(S&X)==1 for X in (B,C,actualD,actualE))]
                    assert len(initial)==z['feasible_nine_sets']==70 and set.intersection(*initial)=={0,3,4,d}
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
                        assert 8*co[0]+sum(co[1:])==1 and all(len(S&R)==1 for S in initial);identities+=1
                    labels+=1;checked+=1
        coverage.append(dict(id=t['id'],D_labels=8,E_labels_per_D=14,labelled_extensions=checked,
                             normalized_fourth_pairs_excluded=41,whole_third_excluded=False))
    remaining=next(z for z in inv['records'] if z['D']==[5] and z['E']==[6])
    assert remaining['labelled_E']==7 and sum(len(p['fourth_field_pairs']) for p in remaining['pairs'])==41
    assert {tuple(p['original_third_rows']) for p in remaining['pairs'] if p['fourth_field_pairs']}==set(map(tuple,root['binary_profile_pairs']))
    names=[Path(__file__).name,'PROOF.md#problem4-singleton-c-d5-e16-unrestricted-exclusion','PROOF.md#problem4-two-cover-protected-kernel-obstruction',*reports,
           'b1_c4_fourth_inventory.json','PROOF.md#problem4-b1-c4-fourth-space','small_first_third_inventory.json',
           'small_first_third_audit.json','PROOF.md#problem4-small-first-third-admission','PROOF.md#problem4-mandatory-core-isolation',
           'mandatory_core_isolation_audit.json','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],coverage=coverage,labelled_extensions_checked=labels,
                Boolean_identities_checked=identities,new_unrestricted_fourth_cuts_both_roots=2,
                newly_removed_current_binary_fourth_pairs_both_roots=82,remaining_C4_D5_E=[[6]],
                remaining_C4_geometries=1,remaining_C4_E_labels=7,remaining_C4_binary_pairs=41,
                whole_third_types_removed=0,binary_parent_pairs_removed=0,
                source_sha256={n:sha(ROOT/n) for n in names},scope='Complete E16 cuts at both roots. E6, whole D5 and numerical F unresolved.')
    assert (labels,identities)==(224,896)
    (ROOT/'singleton_c_d5_e16_transport_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','coverage')}),flush=True)
if __name__=='__main__':main()
