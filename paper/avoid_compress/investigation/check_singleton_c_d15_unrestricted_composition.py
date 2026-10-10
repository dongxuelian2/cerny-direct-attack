"""Complete D15 fourth coverage, all labelled transports and whole accounting."""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};K={1,2};D={1,5};H={0,3,4}

def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inc(X,Y):return bool(X-Y) and bool(Y-X)
def transform(X,p):return sorted(p[q] for q in X)
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

def main():
    reports=['c4_d15_e6_unrestricted_audit.json','c4_d15_e26_unrestricted_audit.json','b1_c4_fourth_audit.json']
    e6,e26,parent=map(read,reports)
    for z in (e6,e26,parent):
        assert z['status']=='pass'
        for n,h in z['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert e6['unrestricted_E6_paper_excluded'] and e6['E']==[6]
    assert e26['unrestricted_E26_paper_excluded'] and e26['E']==[2,6]
    assert e6['complete_individual_rows']==7344 and e26['complete_individual_rows']==5232
    third=read('small_first_third_inventory.json');inventory=read('b1_c4_fourth_inventory.json');common=read('common_block_profiles_audit.json')
    root=next(r for r in third['records'] if r['id']=='b1_in_c1_third4')
    other=next(r for r in third['records'] if r['id']=='b1_out_c2_third4')
    swap=[4,1,2,3,0,5,6,7,8,9,10,11,12]
    assert root['labelled_D']==other['labelled_D']==16
    for key in ('B','C','D'):assert transform(root[key],swap)==other[key]
    assert len(root['rows'])==len(other['rows'])==8 and root['binary_profile_pairs']==other['binary_profile_pairs']
    assert len(root['binary_profile_pairs'])==14
    for f,g in zip(root['rows'],other['rows']):
        for key in ('preA','preB','preC'):assert transform(f[key],swap)==g[key]
        assert f['cell_capacity']==g['cell_capacity']
        assert sorted(transform(pair,swap) for pair in f['forced_pairs'])==g['forced_pairs']
    profiles=[z for z in inventory['records'] if z['D']==[1,5]]
    assert [z['E'] for z in profiles]==[[2],[6],[1,2],[1,6],[2,5],[2,6],[1,2,6]]
    assert [z['labelled_E'] for z in profiles]==[1,7,1,7,1,7,7]
    assert sum(z['labelled_E'] for z in profiles)==31 and sum(len(z['rows']) for z in profiles)==96
    for z in profiles:
        assert z['additional_covered_fibers']==[]
        if z['E']==[2]:
            v=next(v for v in parent['records'] if v['D']==[1,5] and v['E']==[2])
            assert v['known_compression_cover_cut'] and v['remaining_P5_cover']==[1]
    allS=[set(S) for S in combinations(range(13),9) if 3 in S];coverage=[];labels=booleans=0
    for t in (root,other):
        B=set(t['B']);C=set(t['C'])
        assert not any(z['id']==t['id'] for z in common['profile_cuts'])
        for guard in (1,2):
            for ordinary in range(5,13):
                actualD={guard,ordinary};forms=[S for S in allS if all(len(S&X)==1 for X in (B,C,actualD))]
                assert len(forms)==112 and set.intersection(*forms)==H
                candidates=[]
                for size in range(1,4):
                    for points in combinations(sorted(Q-A),size):
                        E=set(points)
                        if len(E-K)>1 or not all(inc(E,X) for X in (B,C,actualD)):continue
                        initial=[S for S in forms if len(S&E)==1]
                        if not initial or rank([Q-A,B,C,actualD,E])!=5:continue
                        candidates.append(E)
                h=next(iter(K-{guard}));wanted=[{h},K,{h,ordinary}]
                for q in range(5,13):
                    if q!=ordinary:wanted.extend(({q},{guard,q},{h,q},K|{q}))
                assert len(candidates)==31 and {frozenset(E) for E in candidates}=={frozenset(E) for E in wanted}
                for E in candidates:
                    fresh=E-K-{ordinary};p=list(range(13))
                    if t is other:p[0],p[4]=4,0
                    if guard==2:p[1],p[2]=2,1
                    p[5]=ordinary
                    if fresh:
                        sentinel,=fresh;p[6]=sentinel
                        for q,v in zip(range(7,13),sorted(set(range(5,13))-{ordinary,sentinel})):p[q]=v
                    else:
                        for q,v in zip(range(6,13),sorted(set(range(5,13))-{ordinary})):p[q]=v
                    assert sorted(p)==list(range(13)) and set(transform(D,p))==actualD
                    z=next(z for z in profiles if set(transform(z['E'],p))==E)
                    initial=[S for S in forms if len(S&E)==1]
                    assert len(initial)==z['feasible_nine_sets'] and sorted(set.intersection(*initial))==transform(z['mandatory_through_seven'],p)
                    fields={tuple(tuple(transform(f[k],p)) for k in ('preA','preB','preC','preD')) for f in z['rows']}
                    direct=set()
                    for cols in product((A,B),(A,B,C),(A,B,C,actualD),(A,B,C,actualD,E)):
                        if all(sum(q in X for X in cols)<=1 for q in Q):direct.add(tuple(tuple(sorted(X)) for X in cols))
                    assert fields==direct and len(fields)==len(z['rows'])
                    for f in z['all_Boolean_one_count_fibers']:
                        R=set(transform(f['R'],p));co=list(map(Fraction,f['coefficients']));cols=[Q-A,B,C,actualD,E]
                        assert all(sum(c*int(q in X) for c,X in zip(co,cols))==int(q in R) for q in Q-A)
                        assert 8*co[0]+sum(co[1:])==1 and all(len(S&R)==1 for S in initial)
                        assert f['covered_by_K']==(len(R-K)<=1);booleans+=1
                    labels+=1
        coverage.append(dict(id=t['id'],B=t['B'],C=t['C'],D=t['D'],D_labels=16,complete_fourth_geometries=7,
            complete_E_labels_per_D=31,canonical_individual_fields=96,all_labelled_transports_checked=True,
            unrestricted_remaining_E=[],new_binary_parent_pairs_excluded=14))
    for name in ('c4_d15_e6_unrestricted_samples.json','c4_d15_e26_unrestricted_samples.json'):
        b=read(name)['boundary_control'];rows=[]
        for row in b['rows']:
            r=[-1]*len(row)
            for q,v in enumerate(row):r[swap[q]]=swap[v]
            rows.append(r)
        w=b['short_merge'];pair=transform(w['pair'],swap)
        assert action(pair[0],w['word'],rows)==action(pair[1],w['word'],rows)
        assert len({action(q,b['reset'],rows) for q in range(len(rows[0]))})==1
    names=[Path(__file__).name,'SINGLETON_C_D15_UNRESTRICTED_EXCLUSION.md','C4_D15_E6_UNRESTRICTED_EXCLUSION.md',
        'C4_D15_E26_UNRESTRICTED_EXCLUSION.md',*reports,'b1_c4_fourth_inventory.json','B1_C4_FOURTH_SPACE.md',
        'small_first_third_inventory.json','small_first_third_audit.json','SMALL_FIRST_THIRD_ADMISSION.md','common_block_profiles_audit.json',
        'c4_d15_e6_unrestricted_samples.json','c4_d15_e26_unrestricted_samples.json','C4_D15_E12_UNRESTRICTED_EXCLUSION.md',
        'C4_D15_E25_UNRESTRICTED_EXCLUSION.md','SATURATED_TWO_GUARD_TRAP.md','C4_D15_E16_E126_UNRESTRICTED_EXCLUSION.md',
        'COMPRESSION_COVER_FLOOR.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    report=dict(status='pass',parameter=[13,9,1],excluded_unrestricted_third_ids=[r['id'] for r in coverage],
        excluded_binary_third_ids=[r['id'] for r in coverage],newly_excluded_binary_third_types=2,
        newly_removed_previously_remaining_binary_pairs=28,whole_unrestricted_third_exclusions=2,newly_excluded_D_labels=32,
        complete_E_labels_both_roots=992,labelled_field_transports_checked=labels,Boolean_identities_checked=booleans,coverage=coverage,
        newly_removed_current_binary_fourth_pairs_both_roots=164,source_sha256={n:sha(ROOT/n) for n in names},
        scope='Two whole conditional D15 third exclusions for arbitrary alphabets, including28 remaining binary parent pairs. Other third/joint types and numerical F extrema remain unresolved.')
    assert (labels,booleans)==(992,3968)
    (ROOT/'singleton_c_d15_unrestricted_composition_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','coverage')}),flush=True)
if __name__=='__main__':main()
