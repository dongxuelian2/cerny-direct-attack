"""Independent complete fourth coverage and literal second-root transport."""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};K={1,2};D={1,2,5}
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rename(q):return 4 if q==0 else 0 if q==4 else q
def rename_set(X):return sorted(map(rename,X))
def inc(X,Y):return bool(X-Y) and bool(Y-X)
def rank(columns):
    a=[[Fraction(int(q in X)) for X in columns] for q in sorted(Q-A)];i=0
    for j in range(len(columns)):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
        for k in range(i+1,len(a)):
            v=a[k][j]
            if v:a[k]=[x-v*y for x,y in zip(a[k],a[i])]
        i+=1
    return i
def action(q,w,rows):
    for ch in w:q=rows[ord(ch)-97][q]
    return q
def conjugate(row):
    r=[-1]*len(row)
    for q,t in enumerate(row):r[rename(q)]=rename(t)
    return r

def main():
    reports=['c4_d125_e6_unrestricted_audit.json','c4_d125_guarded_unrestricted_audit.json','b1_c4_fourth_audit.json']
    e6,guarded,parent=map(read,reports)
    for z in (e6,guarded,parent):
        assert z['status']=='pass'
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert e6['unrestricted_E6_paper_excluded'] and e6['E']==[6]
    assert guarded['unrestricted_excluded_E']==[[1,6],[1,2,6]]
    assert guarded['boundary_depths']=={'E16':4,'E126':3}
    inventory=read('b1_c4_fourth_inventory.json');third=read('small_first_third_inventory.json')
    root=next(r for r in third['records'] if r['id']=='b1_in_c1_third5')
    other=next(r for r in third['records'] if r['id']=='b1_out_c2_third5')
    assert root['labelled_D']==other['labelled_D']==8
    for key in ('B','C','D'):assert rename_set(root[key])==other[key]
    assert {tuple(rename_set(X)) for X in root['allowed_preC_fibers']}==set(map(tuple,other['allowed_preC_fibers']))
    assert root['feasible_nine_sets']==other['feasible_nine_sets']==63
    assert root['binary_profile_pairs']==other['binary_profile_pairs']
    assert len(root['rows'])==len(other['rows'])==8
    for f,g in zip(root['rows'],other['rows']):
        for key in ('preA','preB','preC'):assert rename_set(f[key])==g[key]
        assert sorted(rename_set(p) for p in f['forced_pairs'])==g['forced_pairs']
        assert f['cell_capacity']==g['cell_capacity']
    profiles=[z for z in inventory['records'] if z['D']==sorted(D)]
    assert [z['E'] for z in profiles]==[[6],[1,6],[1,2,6]]
    assert [z['labelled_E'] for z in profiles]==[7,14,7]
    coverage=[];forms_all=[set(S) for S in combinations(range(13),9) if 3 in S]
    for t in (root,other):
        B=set(t['B']);C=set(t['C']);forms=[S for S in forms_all if all(len(S&X)==1 for X in (B,C,D))]
        assert len(forms)==63 and set.intersection(*forms)=={0,3,4}
        assert (set.intersection(*forms)&{0,1,2})=={0}
        candidates=[]
        for size in range(1,4):
            for points in combinations(sorted(Q-A),size):
                E=set(points)
                if len(E-K)>1 or not all(inc(E,X) for X in (B,C,D)):continue
                initial=[S for S in forms if len(S&E)==1]
                if not initial or rank([Q-A,B,C,D,E])!=5:continue
                candidates.append(sorted(E))
        canonical={tuple(E) for E in candidates}
        expected={tuple(sorted(set(G)|{q})) for G in ((),(1,),(2,),(1,2)) for q in range(6,13)}
        assert canonical==expected and len(canonical)==28
        fields=0
        for z in profiles:
            E=set(z['E']);assert z['additional_covered_fibers']==[]
            if t is other:
                actual={tuple(tuple(rename_set(f[k])) for k in ('preA','preB','preC','preD')) for f in z['rows']}
            else:actual={tuple(tuple(f[k]) for k in ('preA','preB','preC','preD')) for f in z['rows']}
            direct=set()
            for cols in product((A,B),(A,B,C),(A,B,C,D),(A,B,C,D,E)):
                if all(sum(q in X for X in cols)<=1 for q in Q):direct.add(tuple(tuple(sorted(X)) for X in cols))
            assert direct==actual and len(direct)==(16 if len(E)==1 else 12);fields+=len(direct)
            # Complete old Boolean lists transport under the state permutation.
            for f in z['all_Boolean_one_count_fibers']:
                cols=[Q-A,B,C,D,E];co=list(map(Fraction,f['coefficients']))
                R=set(rename_set(f['R'])) if t is other else set(f['R'])
                assert all(sum(c*int(q in X) for c,X in zip(co,cols))==int(q in R) for q in Q-A)
                assert 8*co[0]+sum(co[1:])==1
                initial=[S for S in forms if len(S&E)==1]
                assert all(len(S&R)==1 for S in initial)
                assert f['covered_by_K']==(len(R-K)<=1)
            count=sum(sum(set(E)==set(G)|{q} for G in ((),(1,),(2,),(1,2)) for q in range(6,13)) for E in candidates)
            assert count==28
        coverage.append(dict(id=t['id'],B=t['B'],C=t['C'],D=t['D'],D_labels=t['labelled_D'],
            complete_fourth_geometries=3,complete_E_labels=28,complete_individual_fields=fields,
            all_extra_companions_retained=True,unrestricted_remaining_E=[]))
    common=read('common_block_profiles_audit.json')
    for t in (root,other):
        z=next(z for z in common['profile_cuts'] if z['id']==t['id'])
        assert len(z['removed_parent_pairs'])==5 and len(z['remaining_parent_pairs'])==9
    # Conjugate literal constructive samples and evaluate their words again.
    sample=read('c4_d125_e6_unrestricted_samples.json')['boundary']
    controls=[sample]+list(read('c4_d125_guarded_unrestricted_samples.json')['boundary_controls'].values())
    for sample in controls:
        rows=[conjugate(row) for row in sample['rows']];w=sample['short_merge'];pair=rename_set(w['pair'])
        assert action(pair[0],w['word'],rows)==action(pair[1],w['word'],rows)
        assert len({action(q,sample['reset'],rows) for q in range(len(rows[0]))})==1
    names=[Path(__file__).name,'PROOF.md#problem4-singleton-c-d125-unrestricted-exclusion',
        'PROOF.md#problem4-c4-d125-e6-unrestricted-exclusion','PROOF.md#problem4-c4-d125-e16-e126-unrestricted-exclusion',
        'PROOF.md#problem4-universal-free-image-trap',*reports,'b1_c4_fourth_inventory.json','PROOF.md#problem4-b1-c4-fourth-space',
        'small_first_third_inventory.json','small_first_third_audit.json','PROOF.md#problem4-small-first-third-admission',
        'common_block_profiles_audit.json','c4_d125_e6_unrestricted_samples.json',
        'c4_d125_guarded_unrestricted_samples.json','PROOF.md#problem4-mandatory-core-isolation',
        'mandatory_core_isolation_audit.json','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    report=dict(status='pass',parameter=[13,9,1],excluded_unrestricted_third_ids=[r['id'] for r in coverage],
        whole_unrestricted_third_exclusions=2,additional_binary_third_exclusion='b1_out_c2_third5',
        additional_previously_remaining_binary_pairs=9,newly_excluded_unrestricted_D_labels=16,
        coverage=coverage,conjugation=[4,1,2,3,0,5,6,7,8,9,10,11,12],
        transport_boundary_controls=3,source_sha256={n:sha(ROOT/n) for n in names},
        scope='Complete two-root unrestricted D125 conditional exclusions and nine remaining binary pairs of the transported root; other third types, whole joints and numerical F remain unresolved.')
    (ROOT/'singleton_c_d125_unrestricted_composition_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','coverage')}),flush=True)
if __name__=='__main__':main()
