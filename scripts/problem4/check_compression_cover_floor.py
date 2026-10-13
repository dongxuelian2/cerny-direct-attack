"""Independent known-bound cover cut, labelled admission and finite controls."""
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import hashlib,json,random
from alphabet_check import bfs,pair_distances,strong
ROOT=Path(__file__).resolve().parent

def binom_bound(k):return (k+2)*(k+1)//2
def covers(cover,edges):return all(x in cover or y in cover for x,y in edges)

def labelled_joint_controls():
    data=json.loads((ROOT/'compression_cover_floor_inventory.json').read_text(encoding='utf-8'))
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    H={0,1,2};O=set(range(13))-{3}
    cases={(len(z['B']),len(set(z['B'])-H)):z['B_case'] for z in joint['records']}
    index={(z['B_case'],tuple(z['cell_signature'])):z for z in joint['records']}
    counts=Counter();excluded=Counter();labels=0
    for sizeB in (1,2,3):
        for bb in combinations(sorted(O),sizeB):
            B=set(bb)
            if len(B-H)>1:continue
            case=cases[sizeB,len(B-H)];cells=[H&B,H-B,(O-H)&B,(O-H)-B]
            for sizeC in range(1,4 if sizeB==1 else 5):
                for cc in combinations(sorted(O),sizeC):
                    C=set(cc)
                    if B<=C or C<=B or len(B|C)>5 or len(C-H)>1:continue
                    record=index[case,tuple(len(C&cell) for cell in cells)]
                    protected={3}|(B if len(B)==1 else set())|(C if len(C)==1 else set())
                    remaining=H-protected
                    cut=(len(remaining)<=11 and binom_bound(len(remaining))<=5)
                    counts[record['id']]+=1;labels+=1
                    if cut:
                        excluded[record['id']]+=1
                        assert len(B)==len(C)==1 and B|C<=H
    assert labels==4806 and dict(excluded)=={'b1_in_c2':6}
    byid={z['id']:z for z in data['records']};assert len(byid)==len(counts)==43
    for z in joint['records']:
        p={3}
        if len(z['B'])==1:p|=set(z['B'])
        if len(z['C'])==1:p|=set(z['C'])
        v=byid[z['id']];remaining=set(range(3))-p
        assert v['protected_through_nine']==sorted(p) and v['remaining_P5_cover']==sorted(remaining)
        assert v['excluded_by_known_bound']==(binom_bound(len(remaining))<=5)
    assert data['excluded_joints']==['b1_in_c2']
    for h in range(1,11):
        lower=int(data['cover_size_floors'][str(h)])
        assert lower==next(k for k in range(13) if k==12 or binom_bound(k)>h)
    # Preserve the k=2,h=5 boundary rather than over-pruning it.
    assert binom_bound(1)==3<=5<binom_bound(2)
    profiles=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))['records']
    Ds=[v for v in profiles if v['joint_id']=='b1_in_c2']
    assert [v['D'] for v in Ds]==[[2],[4],[2,4]] and [len(v['binary_profile_pairs']) for v in Ds]==[14,14,14]
    return dict(original_joint_orbits=43,labelled_ordered_pairs=labels,excluded_labelled_pairs=6,
        excluded_joint='b1_in_c2',alphabet='arbitrary finite',binary_third_profiles_discharged=3,
        binary_earlier_profile_pairs_discharged=42,third_profiles=[[2],[4],[2,4]],
        cover_floors_h1_through10=[int(data['cover_size_floors'][str(h)]) for h in range(1,11)])

def check_model(rows,actual_subsets=False):
    n=len(rows[0]);distance=pair_distances(rows)
    if len(distance)!=n*(n-1)//2:return None
    tests=0;subset_tests=0
    for h in range(1,min(10,n*(n-1)//2)+1):
        edges={p for p,d in distance.items() if d<=h}
        for k in range(n-1):
            if binom_bound(k)>h:continue
            for cover in combinations(range(n),k):
                assert not covers(set(cover),edges),(rows,h,cover)
                tests+=1
    for s in range(2,n+1):
        for T in combinations(range(n),s):
            value=min(distance[p] for p in combinations(T,2))
            assert value<=binom_bound(n-s)
            if actual_subsets:
                word,_=bfs(rows,T,lambda U:len(U)<s)
                assert word is not None and len(word)==value;subset_tests+=1
    return dict(cover_controls=tests,actual_subset_BFS_controls=subset_tests,distance=distance)

def labelled_third_controls():
    data=json.loads((ROOT/'compression_cover_floor_inventory.json').read_text(encoding='utf-8'))
    source=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))['records']
    byid={v['id']:v for v in data['third_records']};assert len(byid)==len(source)==235
    O=set(range(13))-{3};H={0,1,2}
    # Bit masks, independently of the generator's set intersections.
    allS=[sum(1<<q for q in T)|(1<<3) for T in combinations(sorted(O),8)]
    labels=0;cutlabels=0;canonical_cut=[];family_checks=0
    for z in source:
        B,C,D=[set(z[k]) for k in ('B','C','D')];bm=sum(1<<q for q in B);cm=sum(1<<q for q in C)
        base=[S for S in allS if (S&bm).bit_count()==(S&cm).bit_count()==1]
        cells=[{q for q in O if (int(q in H),int(q in B),int(q in C))==key} for key in product((0,1),repeat=3)]
        options=[list(combinations(sorted(cell),take)) for cell,take in zip(cells,z['cell_signature'])]
        orbit=0;record=byid[z['id']];canonical_mask=sum(1<<q for q in D)
        for selection in product(*options):
            dm=sum(1<<q for part in selection for q in part);families=[S for S in base if (S&dm).bit_count()==1]
            assert len(families)==z['feasible_nine_sets'] and families
            intersection=(1<<13)-1
            for S in families:intersection&=S
            remaining={q for q in H if not intersection&(1<<q)}
            cut=binom_bound(len(remaining))<=4
            assert cut==record['excluded_by_known_bound']
            if dm==canonical_mask:
                assert record['mandatory_through_eight']==[q for q in range(13) if intersection&(1<<q)]
                assert record['remaining_P4_cover']==sorted(remaining)
            orbit+=1;labels+=1;cutlabels+=cut;family_checks+=len(base)
        assert orbit==z['labelled_D']
        if record['excluded_by_known_bound']:canonical_cut.append(z['id'])
    expected=['b1_out_c2_third1','b1_in_c1_third1','b1_in_c2_third1','b1_in_c2_third2','b1_in_c2_third3',
        'b1_in_c3_third1','b2_mixed_c2_third1','b2_mixed_c7_third2','b2_mixed_c9_third10','b2_in_c4_third10','b2_in_c6_third4']
    assert canonical_cut==expected==data['excluded_third_profiles'] and cutlabels==30
    return dict(original_B1_B2_third_orbits=235,complete_labelled_D_choices=labels,
        literal_nine_set_intersection_tests=family_checks,excluded_third_orbits=11,
        excluded_canonical_labelled_D_choices=cutlabels,excluded_profiles=expected,
        remaining_arbitrary_alphabet_geometries_in_this_inventory=224,
        scope='The235-orbit B1/B2 inventory, including extra Boolean-fiber shapes; B3 is not included.')

def exhaustive(n,k):
    transformations=list(product(range(n),repeat=n));total=0;qualified=0;covers_checked=0;subset_BFS=0
    for rows in product(transformations,repeat=k):
        total+=1
        if not strong(rows):continue
        result=check_model(rows,qualified<64)
        if result is None:continue
        qualified+=1;covers_checked+=result['cover_controls'];subset_BFS+=result['actual_subset_BFS_controls']
    assert total==n**(n*k)
    return dict(n=n,alphabet_size=k,complete_ordered_row_assignments=total,strong_sync_models=qualified,
        forbidden_cover_controls=covers_checked,independent_actual_subset_BFS_controls=subset_BFS)

def frontier_controls():
    data=json.loads((ROOT/'frontier_certificates.json').read_text(encoding='utf-8'))['certificates']
    cache={};checks=0;protected=0
    for z in data:
        key=tuple(tuple(row) for row in z['rows'])
        if key not in cache:
            assert strong(key);result=check_model(key);assert result is not None;cache[key]=result
        result=cache[key];checks+=result['cover_controls']
        A=set(z['A']);m=z['n']-len(z['S'])
        incident=min(d for p,d in result['distance'].items() if set(p)&A)
        assert z['value']<=m+incident;protected+=1
    assert len(data)==290
    return dict(frontier_certificates=290,distinct_row_models=len(cache),forbidden_cover_controls=checks,
        protected_pair_bound_controls=protected,scope='All290 existing verified frontier examples; repeated row models are cached, no claim of290 distinct automata.')

def random_controls():
    rng=random.Random(20261009);total=300;qualified=0;checks=0
    for index in range(total):
        n=rng.randrange(4,10);k=rng.randrange(2,5)
        rows=tuple(tuple(rng.randrange(n) for q in range(n)) for letter in range(k))
        if not strong(rows):continue
        result=check_model(rows)
        if result is None:continue
        qualified+=1;checks+=result['cover_controls']
    return dict(seed=20261009,proposed_models=300,strong_sync_models=qualified,forbidden_cover_controls=checks,
        n_range=[4,9],alphabet_range=[2,4],scope='Seeded controls, not exhaustive beyond the separately listed domains.')

def main():
    admission=labelled_joint_controls();third=labelled_third_controls();finite=[]
    for n,k in ((2,2),(3,2),(4,2),(3,3)):
        finite.append(exhaustive(n,k));print(json.dumps(finite[-1]),flush=True)
    front=frontier_controls();randoms=random_controls()
    primary=json.loads((ROOT/'compression_cover_primary_source.json').read_text(encoding='utf-8'))
    assert primary['theorem']==1 and primary['arbitrary_finite_alphabet'] and not primary['subset_reachability_required']
    names=[Path(__file__).name,'enumerate_compression_cover_floor.py','compression_cover_floor_inventory.json',
        'compression_cover_primary_source.json','PROOF.md#problem4-compression-cover-floor','joint_fiber_orbits.json',
        'small_first_third_inventory.json','frontier_certificates.json','alphabet_check.py',
        'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber','PROOF.md#problem4-local-equality-flag','PROOF.md#problem4-codimension-four-p5-dichotomy']
    result=dict(status='pass',parameter=[13,9,1],admission=admission,third_intersection_controls=third,complete_small_row_controls=finite,
        frontier_controls=front,seeded_larger_alphabet_controls=randoms,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Known compression-theorem cover floor and complete arbitrary-alphabet whole-joint exclusion. Finite controls supplement the symbolic argument; no full13-state scan, new F value or numerical alphabet separation.')
    (ROOT/'compression_cover_floor_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',admission=admission,frontier=front,random_controls=randoms)),flush=True)

if __name__=='__main__':main()
