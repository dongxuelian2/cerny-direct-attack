"""Complete D12 fourth coverage, all labelled transports and old pair accounting."""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
import hashlib,json
from check_singleton_c_d125_unrestricted_composition import rank
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};K={1,2};D=K;H={0,3,4}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inc(X,Y):return bool(X-Y) and bool(Y-X)
def transform(X,p):return sorted(p[q] for q in X)
def action(q,w,rows):
    for ch in w:q=rows[ord(ch)-97][q]
    return q
def main():
    reports=['c4_d12_unrestricted_audit.json','b1_c4_fourth_audit.json','common_block_profiles_audit.json']
    proof,parent,common=map(read,reports)
    for z in (proof,parent,common):
        assert z['status']=='pass'
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert proof['unrestricted_excluded_E']==[[5],[1,5]] and proof['wide_initial_family_size']==70
    assert proof['complete_individual_rows']==7328 and proof['complete_binary_ordered_alphabets_through_n8']==135616
    assert proof['seeded_larger_alphabets']==48000
    third=read('small_first_third_inventory.json');inventory=read('b1_c4_fourth_inventory.json')
    root=next(r for r in third['records'] if r['id']=='b1_in_c1_third3')
    other=next(r for r in third['records'] if r['id']=='b1_out_c2_third3')
    swap=[4,1,2,3,0,5,6,7,8,9,10,11,12]
    assert root['labelled_D']==other['labelled_D']==1
    for key in ('B','C','D'):assert transform(root[key],swap)==other[key]
    assert len(root['rows'])==len(other['rows'])==8 and root['binary_profile_pairs']==other['binary_profile_pairs']
    assert {tuple(transform(X,swap)) for X in root['allowed_preC_fibers']}==set(map(tuple,other['allowed_preC_fibers']))
    for f,g in zip(root['rows'],other['rows']):
        for key in ('preA','preB','preC'):assert transform(f[key],swap)==g[key]
        assert f['cell_capacity']==g['cell_capacity']
        assert sorted(transform(pair,swap) for pair in f['forced_pairs'])==g['forced_pairs']
    profiles=[z for z in inventory['records'] if z['D']==[1,2]]
    assert [z['E'] for z in profiles]==[[5],[1,5]] and [z['labelled_E'] for z in profiles]==[8,16]
    allS=[set(S) for S in combinations(range(13),9) if 3 in S];coverage=[];label_checks=0;boolean_checks=0
    for t in (root,other):
        B=set(t['B']);C=set(t['C']);forms=[S for S in allS if all(len(S&X)==1 for X in (B,C,D))]
        assert len(forms)==t['feasible_nine_sets']==112 and set.intersection(*forms)==H
        candidates=[]
        for size in range(1,4):
            for points in combinations(sorted(Q-A),size):
                E=set(points)
                if len(E-K)>1 or not all(inc(E,X) for X in (B,C,D)):continue
                initial=[S for S in forms if len(S&E)==1]
                if not initial or rank([Q-A,B,C,D,E])!=5:continue
                candidates.append(sorted(E))
        assert set(map(tuple,candidates))=={tuple(sorted(set(G)|{q})) for G in ((),(1,),(2,)) for q in range(5,13)}
        assert len(candidates)==24
        for E_list in candidates:
            E=set(E_list);z=profiles[0 if len(E)==1 else 1]
            p=list(range(13))
            if t is other:p[0],p[4]=4,0
            if E&K=={2}:p[1],p[2]=2,1
            q=next(iter(E-K));p[5],p[q]=q,5
            assert sorted(p)==list(range(13)) and transform(z['E'],p)==E_list
            assert transform(root['B'],p)==t['B'] and transform(root['C'],p)==t['C']
            assert transform(D,p)==[1,2]
            initial=[S for S in forms if len(S&E)==1]
            assert len(initial)==z['feasible_nine_sets']==(70 if len(E)==1 else 56)
            assert sorted(set.intersection(*initial))==transform(z['mandatory_through_seven'],p)
            assert z['additional_covered_fibers']==[]
            actual={tuple(tuple(transform(f[k],p)) for k in ('preA','preB','preC','preD')) for f in z['rows']}
            direct=set()
            for cols in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
                if all(sum(q in X for X in cols)<=1 for q in Q):direct.add(tuple(tuple(sorted(X)) for X in cols))
            assert actual==direct and len(direct)==(16 if len(E)==1 else 12)
            for f in z['all_Boolean_one_count_fibers']:
                R=set(transform(f['R'],p));co=list(map(Fraction,f['coefficients']));cols=[Q-A,B,C,D,E]
                assert all(sum(c*int(q in X) for c,X in zip(co,cols))==int(q in R) for q in Q-A)
                assert 8*co[0]+sum(co[1:])==1 and all(len(S&R)==1 for S in initial)
                assert f['covered_by_K']==(len(R-K)<=1);boolean_checks+=1
            label_checks+=1
        cut=next(z for z in common['profile_cuts'] if z['id']==t['id'])
        assert len(cut['removed_parent_pairs'])==5 and len(cut['remaining_parent_pairs'])==9
        assert set(map(tuple,cut['removed_parent_pairs']))|set(map(tuple,cut['remaining_parent_pairs']))==set(map(tuple,t['binary_profile_pairs']))
        coverage.append(dict(id=t['id'],B=t['B'],C=t['C'],D=t['D'],D_labels=1,
            complete_fourth_geometries=2,complete_E_labels=24,complete_canonical_individual_fields=28,
            all_labelled_field_transports_checked=True,unrestricted_remaining_E=[],new_binary_pairs_excluded=9))
    controls=read('c4_d12_unrestricted_samples.json')['boundary_controls'];literal_controls=[]
    for key,s in controls.items():
        rows=[]
        for row in s['rows']:
            mapped=[-1]*len(row)
            for q,v in enumerate(row):mapped[swap[q]]=swap[v]
            rows.append(mapped)
        w=s['short_merge'];pair=transform(w['pair'],swap)
        assert action(pair[0],w['word'],rows)==action(pair[1],w['word'],rows)
        assert len({action(q,s['reset'],rows) for q in range(len(rows[0]))})==1
        literal_controls.append(dict(E=key,n=s['n'],word=w['word'],kind=w['kind']))
    names=[Path(__file__).name,'SINGLETON_C_D12_UNRESTRICTED_EXCLUSION.md','C4_D12_UNRESTRICTED_EXCLUSION.md',
        *reports,'b1_c4_fourth_inventory.json','B1_C4_FOURTH_SPACE.md','small_first_third_inventory.json',
        'small_first_third_audit.json','SMALL_FIRST_THIRD_ADMISSION.md','c4_d12_unrestricted_samples.json',
        'check_singleton_c_d125_unrestricted_composition.py','MANDATORY_CORE_ISOLATION.md',
        'mandatory_core_isolation_audit.json','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],excluded_unrestricted_third_ids=[r['id'] for r in coverage],
        excluded_binary_third_ids=[r['id'] for r in coverage],newly_excluded_binary_third_types=2,
        newly_removed_previously_remaining_binary_pairs=18,whole_unrestricted_third_exclusions=2,
        newly_excluded_D_labels=2,complete_E_labels_both_roots=48,
        labelled_field_transports_checked=label_checks,Boolean_identities_checked=boolean_checks,
        coverage=coverage,literal_conjugated_controls=literal_controls,
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Two whole conditional D12 third exclusions for arbitrary alphabets, including eighteen remaining binary parent pairs. Other third/joint types and numerical F extrema remain unresolved.')
    (ROOT/'singleton_c_d12_unrestricted_composition_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','coverage')}),flush=True)
if __name__=='__main__':main()
