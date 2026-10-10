"""All singleton-prefix labels, last fresh fibers and whole-joint accounting."""
from pathlib import Path
from itertools import combinations,permutations,product
import json,hashlib
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};H={0,1,2}
IDS=['b1_out_c1_third1','b1_out_c2_third2','b1_in_c1_third2']
def read(n):return json.loads((ROOT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transform(X,p):return sorted(p[q] for q in X)
def main():
    reports=['singleton_core_span_audit.json','two_cover_protected_kernel_graph_audit.json',
             'two_cover_protected_kernel_application_audit.json','two_cover_third_exact_kernel_audit.json',
             'small_first_third_audit.json','b1_c4_fourth_audit.json']
    for n in reports:
        z=read(n);assert z['status']=='pass'
        for f,h in z['source_sha256'].items():assert sha(ROOT/f)==h,f
    third=read('small_first_third_inventory.json')['records'];allS=[set(S) for S in combinations(range(13),9) if 3 in S]
    dlabels=prefixes=last=guards=pairs=0;coverage=[]
    for name in IDS:
        z=next(z for z in third if z['id']==name);B=set(z['B']);C=set(z['C']);D=set(z['D'])
        assert len(B)==len(C)==len(D)==1 and not (A&B or A&C or A&D or B&C or B&D or C&D)
        assert set(map(tuple,z['allowed_preC_fibers']))==set(map(tuple,(z['B'],z['C'],z['D'])))
        assert len(z['rows'])==8 and len(z['binary_profile_pairs'])==14
        labels=H if name==IDS[0] else set(range(5,13));assert len(labels)==z['labelled_D']
        labelcount=0
        for d in sorted(labels):
            p=list(range(13));original=next(iter(D));p[original],p[d]=d,original
            actualD={d};core=A|B|C|actualD;K=H-core
            assert len(core)==4 and len(K)==2
            forms=[S for S in allS if all(len(S&X)==1 for X in (B,C,actualD))]
            assert set.intersection(*forms)==core
            native={tuple(tuple(transform(f[k],p)) for k in ('preA','preB','preC')) for f in z['rows']}
            direct=set()
            for cols in product((A,B),(A,B,C),(A,B,C,actualD)):
                if all(sum(q in X for X in cols)<=1 for q in Q):direct.add(tuple(tuple(sorted(X)) for X in cols))
            assert native==direct and len(native)==8
            ordinary=sorted(Q-core-K);assert len(ordinary)==7
            # All early singleton choices; pairs die by the uniform obstruction,
            # guards die by the known one-cover floor, independently of labels.
            guards+=2*(1+7+7*6)
            pairs+=15+7*13+7*6*11
            for e,f,g in permutations(ordinary,3):
                C7=core|{e,f,g};assert len(C7)==7 and not C7&K
                outside=Q-C7
                fresh=[{q} for q in sorted(outside)]+[set(pair) for pair in combinations(sorted(outside),2) if set(pair)&K]
                assert len(fresh)==15 and sum(len(R)==1 for R in fresh)==6
                for R in fresh:
                    assert not R&C7
                    if len(R)==1:
                        C8=C7|R;assert len(C8)==8
                        assert len([S for S in allS if C8<=S])==5
                    else:
                        assert len(R)==2 and R&K
                        initial=[S for S in allS if C7<=S and len(S&R)==1]
                        assert len(initial)==8
                        for pstate in sorted(Q-C7-R):
                            saturated=[S for S in initial if pstate in S]
                            assert len(saturated)==2
                    last+=1
                prefixes+=1
            labelcount+=1;dlabels+=1
        coverage.append(dict(id=name,B=z['B'],C=z['C'],D=z['D'],D_labels=labelcount,
                             whole_unrestricted_third_excluded=True,whole_binary_third_excluded=True,
                             original_binary_pairs=14))
    assert (dlabels,prefixes,last,guards,pairs)==(19,3990,59850,1900,10792)
    known=set(read('two_cover_protected_kernel_application_audit.json')['all_inventory_unrestricted_excluded_ids'])
    known|=set(read('two_cover_third_exact_kernel_audit.json')['all_inventory_unrestricted_excluded_ids'])|set(IDS)
    wholejoints=[]
    for joint in ['b1_in_c1','b1_out_c2']:
        records=[z for z in third if z['joint_id']==joint];assert len(records)==5
        assert [z['D'] for z in records]==[[1],[5],[1,2],[1,5],[1,2,5]]
        for z in records:
            B,C,D=map(set,(z['B'],z['C'],z['D']))
            forms=[S for S in allS if all(len(S&X)==1 for X in (B,C,D))];K=H-set.intersection(*forms)
            assert len(K)<=1 or z['id'] in known
        wholejoints.append(dict(id=joint,complete_third_geometries=5,all_excluded=True))
    historical=read('two_cover_third_unique_kernel_audit.json')['records']
    assert {z['id'] for z in historical}<=known
    names=[Path(__file__).name,'SINGLETON_THIRD_CHAIN_UNRESTRICTED_EXCLUSION.md',*reports,
           'small_first_third_inventory.json','two_cover_third_unique_kernel_audit.json',
           'TWO_COVER_PROTECTED_KERNEL_OBSTRUCTION.md','EXACT_ATOM_KERNEL_COMPATIBILITY.md',
           'B1_C4_FOURTH_SPACE.md','SMALL_FIRST_THIRD_ADMISSION.md','LOCAL_EQUALITY_FLAG.md',
           'MANDATORY_CORE_ISOLATION.md','COMPRESSION_COVER_FLOOR.md',
           'ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md']
    result=dict(status='pass',parameter=[13,9,1],excluded_unrestricted_third_ids=IDS,excluded_binary_third_ids=IDS,
                excluded_unrestricted_joint_ids=[z['id'] for z in wholejoints],excluded_binary_joint_ids=[z['id'] for z in wholejoints],
                coverage=coverage,joint_coverage=wholejoints,D_labels_checked=dlabels,
                singleton_prefixes_checked=prefixes,last_fresh_fibers_checked=last,
                early_guard_singletons_excluded=guards,early_pair_fibers_excluded=pairs,
                all_43_historical_two_cover_geometries_excluded=True,
                source_sha256={n:sha(ROOT/n) for n in names},
                scope='Three complete singleton third cuts, two whole joints and the complete historical two-cover third region. Three-cover branches and numerical F unresolved.')
    (ROOT/'singleton_third_chain_composition_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','coverage','joint_coverage')}),flush=True)
if __name__=='__main__':main()
