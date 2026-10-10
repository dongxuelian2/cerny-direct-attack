"""All guarded labels/Boolean companions and exact fourth accounting."""
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};K={1,2};H={0,3,4};D={1,5}

def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transform(X,p):return sorted(p[q] for q in X)
def action(q,w,rows):
    for ch in w:q=rows[ord(ch)-97][q]
    return q

def main():
    reports=['c4_d15_guarded_unrestricted_audit.json','b1_c4_fourth_audit.json']
    proof,parent=map(read,reports)
    for z in (proof,parent):
        assert z['status']=='pass'
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert proof['unrestricted_paper_excluded'] and proof['complete_individual_fields_per_E']==12
    assert proof['complete_binary_ordered_alphabets_through_n8']==146432
    assert proof['complete_distinct_ternary_supplier_sets_at_n7']==454656
    third=read('small_first_third_inventory.json');inventory=read('b1_c4_fourth_inventory.json')
    root=next(r for r in third['records'] if r['id']=='b1_in_c1_third4')
    other=next(r for r in third['records'] if r['id']=='b1_out_c2_third4')
    swap=[4,1,2,3,0,5,6,7,8,9,10,11,12]
    assert root['labelled_D']==other['labelled_D']==16
    for key in ('B','C','D'):assert transform(root[key],swap)==other[key]
    assert root['binary_profile_pairs']==other['binary_profile_pairs'] and len(root['binary_profile_pairs'])==14
    assert len(root['rows'])==len(other['rows'])==8
    for f,g in zip(root['rows'],other['rows']):
        for key in ('preA','preB','preC'):assert transform(f[key],swap)==g[key]
        assert f['cell_capacity']==g['cell_capacity']
        assert sorted(transform(pair,swap) for pair in f['forced_pairs'])==g['forced_pairs']
    allS=[set(S) for S in combinations(range(13),9) if 3 in S];labels=booleans=0;coverage=[]
    for E in ({1,6},{1,2,6}):
        z=next(z for z in inventory['records'] if z['D']==sorted(D) and z['E']==sorted(E))
        assert z['labelled_E']==7 and z['additional_covered_fibers']==[] and z['mandatory_through_seven']==sorted(H)
        assert sum(len(p['fourth_field_pairs']) for p in z['pairs'])==9
        for t in (root,other):
            for guard in (1,2):
                for ordinary in range(5,13):
                    for sentinel in range(5,13):
                        if sentinel==ordinary:continue
                        p=list(range(13))
                        if t is other:p[0],p[4]=4,0
                        if guard==2:p[1],p[2]=2,1
                        p[5],p[6]=ordinary,sentinel
                        for q,v in zip(range(7,13),sorted(set(range(5,13))-{ordinary,sentinel})):p[q]=v
                        assert sorted(p)==list(range(13))
                        B=set(t['B']);C=set(t['C']);actualD={guard,ordinary};actualE=set(transform(E,p))
                        assert actualE==({guard,sentinel} if len(E)==2 else K|{sentinel})
                        assert transform(root['B'],p)==t['B'] and transform(root['C'],p)==t['C'] and set(transform(D,p))==actualD
                        initial=[S for S in allS if all(len(S&X)==1 for X in (B,C,actualD,actualE))]
                        assert len(initial)==z['feasible_nine_sets']==(56 if len(E)==2 else 36) and set.intersection(*initial)==H
                        fields={tuple(tuple(transform(f[k],p)) for k in ('preA','preB','preC','preD')) for f in z['rows']}
                        direct=set()
                        for cols in product((A,B),(A,B,C),(A,B,C,actualD),(A,B,C,actualD,actualE)):
                            if all(sum(q in X for X in cols)<=1 for q in Q):direct.add(tuple(tuple(sorted(X)) for X in cols))
                        assert fields==direct and len(fields)==12
                        for f in z['all_Boolean_one_count_fibers']:
                            R=set(transform(f['R'],p));co=list(map(Fraction,f['coefficients']));cols=[Q-A,B,C,actualD,actualE]
                            assert all(sum(c*int(q in X) for c,X in zip(co,cols))==int(q in R) for q in Q-A)
                            assert 8*co[0]+sum(co[1:])==1 and all(len(S&R)==1 for S in initial)
                            assert f['covered_by_K']==(len(R-K)<=1);booleans+=1
                        labels+=1
            coverage.append(dict(id=t['id'],B=t['B'],C=t['C'],D=t['D'],E=sorted(E),D_labels=16,E_labels_per_D=7,
                labelled_extensions=112,complete_individual_fields=12,normalized_binary_fourth_pairs_excluded=9,whole_third_excluded=False))
    remaining=[r for r in inventory['records'] if r['D']==[1,5] and r['E'] not in ([1,2],[2,5],[1,6],[1,2,6])
        and not next(q for q in parent['records'] if q['D']==r['D'] and q['E']==r['E'])['all_alphabet_excluded']]
    assert [r['E'] for r in remaining]==[[6],[2,6]]
    assert (len(remaining),sum(r['labelled_E'] for r in remaining))==(2,14)
    assert sum(len(q['fourth_field_pairs']) for r in remaining for q in r['pairs'])==82
    parents={tuple(q['original_third_rows']) for r in remaining for q in r['pairs'] if q['fourth_field_pairs']}
    assert parents==set(map(tuple,root['binary_profile_pairs']))
    for b in read('c4_d15_guarded_unrestricted_samples.json')['boundary_controls'].values():
        rows=[]
        for row in b['rows']:
            r=[-1]*len(row)
            for q,v in enumerate(row):r[swap[q]]=swap[v]
            rows.append(r)
        w=b['short_merge'];pair=transform(w['pair'],swap)
        assert action(pair[0],w['word'],rows)==action(pair[1],w['word'],rows)
        assert len({action(q,b['reset'],rows) for q in range(len(rows[0]))})==1
    names=[Path(__file__).name,'SINGLETON_C_D15_GUARDED_EXCLUSION.md','C4_D15_E16_E126_UNRESTRICTED_EXCLUSION.md',
        *reports,'b1_c4_fourth_inventory.json','B1_C4_FOURTH_SPACE.md','small_first_third_inventory.json','small_first_third_audit.json',
        'SMALL_FIRST_THIRD_ADMISSION.md','c4_d15_guarded_unrestricted_samples.json','C4_D15_E12_UNRESTRICTED_EXCLUSION.md',
        'C4_D15_E25_UNRESTRICTED_EXCLUSION.md','SATURATED_TWO_GUARD_TRAP.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],excluded_root_extensions=coverage,complete_root_extension_cuts=4,
        normalized_binary_fourth_pairs_excluded=36,labelled_field_transports_checked=labels,Boolean_identities_checked=booleans,
        remaining_C4_D15_E=[r['E'] for r in remaining],remaining_C4_D15_geometries=2,remaining_C4_D15_E_labels=14,
        remaining_C4_D15_binary_pairs=82,whole_third_types_removed=0,binary_parent_pairs_removed=0,
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Four normalized arbitrary-alphabet E16/E126 fourth cuts only. All D15 parent profiles still admitted via E6/E26. Broader third/joint counts and numerical F unchanged.')
    assert (labels,booleans)==(448,1792)
    (ROOT/'singleton_c_d15_guarded_transport_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','excluded_root_extensions')}),flush=True)
if __name__=='__main__':main()
