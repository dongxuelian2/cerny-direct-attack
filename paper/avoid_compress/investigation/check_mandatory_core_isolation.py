"""Independent literal mandatory-core lemma and conditional cover audit.

Subset BFS and separate forward pair BFS; no generators imported.
No inference from diagnostic or bounded solver negatives.
"""
from itertools import combinations,product
from collections import deque,Counter
from pathlib import Path
import hashlib,json,random
ROOT=Path(__file__).resolve().parent
def strong(rows):
    n=len(rows[0])
    for start in range(n):
        seen={start};todo=[start]
        while todo:
            q=todo.pop()
            for row in rows:
                t=row[q]
                if t not in seen:seen.add(t);todo.append(t)
        if len(seen)!=n:return False
    return True
def pair_distances(rows):
    n=len(rows[0]);dist={}
    for pair in combinations(range(n),2):
        seen={pair};todo=deque([(pair,0)])
        while todo:
            p,d=todo.popleft();found=False
            for row in rows:
                q=tuple(sorted((row[p[0]],row[p[1]])))
                if q[0]==q[1]:dist[pair]=d+1;found=True;break
                if q not in seen:seen.add(q);todo.append((q,d+1))
            if found:break
    return dist
def apply(S,row):return frozenset(row[x] for x in S)
def core_and_compression(rows,S):
    n=len(rows[0]);S=frozenset(S);m=n-len(S);core=set(S);seen={S:0};todo=deque([S]);compression=None
    while todo:
        T=todo.popleft();d=seen[T]
        if len(T)<len(S) and compression is None:compression=d
        if d<=m:core&=set(T)
        if d>=m and compression is not None:continue
        for row in rows:
            U=apply(T,row)
            if U not in seen:seen[U]=d+1;todo.append(U)
    assert compression is not None
    reached=set(S);levels={q:0 for q in S};queue=deque(S)
    while queue:
        q=queue.popleft()
        for row in rows:
            t=row[q]
            if t not in reached:reached.add(t);levels[t]=levels[q]+1;queue.append(t)
    return core,compression,levels
def check_subset(rows,S,dist):
    n=len(rows[0]);s=len(S);m=n-s;core,c,levels=core_and_compression(rows,S)
    assert len(levels)==n and max(levels.values())<=m
    assert c==min(dist[p] for p in combinations(sorted(S),2))
    count=0
    for p,d in dist.items():
        if set(p)&core:assert d>=c-m,(rows,S,core,c,m,p,d);count+=1
    return dict(core=sorted(core),compression=c,m=m,pair_tests=count,nonvacuous=bool(core) and c>=m+2)
def exhaustive(n,k):
    transformations=list(product(range(n),repeat=n));total=qualified=subsets=checks=nonvacuous=0
    for rows in product(transformations,repeat=k):
        total+=1
        if not strong(rows):continue
        dist=pair_distances(rows)
        if len(dist)!=n*(n-1)//2:continue
        qualified+=1
        for size in range(2,n+1):
            for S in combinations(range(n),size):
                z=check_subset(rows,S,dist);subsets+=1;checks+=z['pair_tests'];nonvacuous+=z['nonvacuous']
    assert total==n**(n*k)
    return dict(n=n,alphabet_size=k,complete_ordered_row_assignments=total,strong_sync_models=qualified,
        all_size_ge_two_subsets=subsets,mandatory_incident_pair_tests=checks,nonvacuous_subset_controls=nonvacuous)
def word_image(rows,S,word):
    S=set(S)
    for letter in word:S={rows[ord(letter)-97][q] for q in S}
    return S
def frontier():
    certs=json.loads((ROOT/'frontier_certificates.json').read_text(encoding='utf-8'))['certificates'];assert len(certs)==290
    cache={};checks=nonvacuous=additional=0;control=None;improvements=[]
    for index,z in enumerate(certs):
        rows=tuple(tuple(row) for row in z['rows']);S=set(z['S']);A=set(z['A'])
        assert strong(rows) and word_image(rows,range(z['n']),z['reaching'])==S
        assert len(word_image(rows,range(z['n']),z['reset']))==1
        if rows not in cache:cache[rows]=pair_distances(rows)
        dist=cache[rows];assert len(dist)==z['n']*(z['n']-1)//2
        result=check_subset(rows,S,dist);checks+=result['pair_tests'];nonvacuous+=result['nonvacuous']
        additional+=len(set(result['core'])-A)
        if result['compression']>result['m']+2 and z['value']>result['m']+1 and A and control is None:
            x=min(A);newrows=[list(row)+[row[x]] for row in rows];mnew=z['n']+1-len(S)
            core,c,_=core_and_compression(newrows,S);d=pair_distances(newrows)
            assert not strong(newrows) and len(d)==(z['n']+1)*z['n']//2 and x in core
            assert d[(x,z['n'])]==1<c-mnew
            assert word_image(newrows,range(z['n']+1),z['reaching'])==S
            assert len(word_image(newrows,range(z['n']+1),z['reset']))==1
            control=dict(frontier_index=index,n=z['n']+1,S=sorted(S),rows=newrows,
                cloned_state=x,transient_state=z['n'],mandatory_core=sorted(core),compression=c,m=mnew,
                violating_pair=[x,z['n']],merging_distance=1,strongly_connected=False,synchronizing=True,
                actual_reachable_image=True,reaching=z['reaching'],reset=z['reset'])
        for x in result['core']:
            seen={frozenset(S):0};todo=deque(seen);score=None
            while todo:
                T=todo.popleft();depth=seen[T]
                if len(T)<len(S) or x not in T:score=depth;break
                for row in rows:
                    U=apply(T,row)
                    if U not in seen:seen[U]=depth+1;todo.append(U)
            assert score is not None
            if score<result['compression'] and len(improvements)<12:
                incident=min(d for p,d in dist.items() if x in p)
                assert score>result['m'] and incident>=result['compression']-result['m']
                improvements.append(dict(frontier_index=index,n=z['n'],s=len(S),x=x,ac_singleton=score,
                    compression=result['compression'],old_depth_guarantee=score-result['m']-1,
                    new_depth_guarantee=result['compression']-result['m']-1,actual_incident_distance=incident))
    assert control is not None
    return dict(certificates=290,distinct_row_models=len(cache),mandatory_incident_pair_tests=checks,
        nonvacuous_certificate_controls=nonvacuous,core_points_outside_original_A=additional,
        strict_guarantee_improvement_controls=improvements,strong_connectivity_boundary_control=control)
def seeded():
    rng=random.Random(20261009);proposed=qualified=subsets=checks=0
    for _ in range(500):
        n=rng.randrange(4,10);k=rng.randrange(2,5);rows=tuple(tuple(rng.randrange(n) for _ in range(n)) for _ in range(k));proposed+=1
        if not strong(rows):continue
        dist=pair_distances(rows)
        if len(dist)!=n*(n-1)//2:continue
        qualified+=1
        for size in range(2,n+1):
            for S in combinations(range(n),size):
                z=check_subset(rows,S,dist);subsets+=1;checks+=z['pair_tests']
    return dict(seed=20261009,proposed_models=proposed,strong_sync_models=qualified,
        all_subsets_checked=subsets,mandatory_incident_pair_tests=checks,n_range=[4,9],alphabet_range=[2,4])
def applications():
    # Literal one-count families; their mandatory guard point2 is now
    # isolated in P7, so K12 strips to {1} on P5 for every alphabet.
    A={3};B={0};C={1,4};D={5};E={6};F={7};G={8};tests=[]
    for name,known,depth in (
        ('E6_F2',(B,C,D,E,{2}),6),
        ('E6_F7_G2',(B,C,D,E,F,{2}),5),
        ('E6_F7_G8_H2',(B,C,D,E,F,G,{2}),4)):
        forms=[set(S) for S in combinations(range(13),9) if A<=set(S) and all(len(set(S)&X)==1 for X in known)]
        assert forms;mandatory=set.intersection(*forms);assert 2 in mandatory and depth>=4
        remaining={1,2}-mandatory;assert len(remaining)<=1 and 13-len(remaining)>=2
        assert (len(remaining)+2)*(len(remaining)+1)//2<=5
        tests.append(dict(branch=name,one_count_depth=depth,nine_set_family=len(forms),mandatory=sorted(mandatory),
            core_isolation_depth=7,remaining_P5_cover=sorted(remaining),excluded_for_arbitrary_finite_alphabet=True))
    primary=json.loads((ROOT/'compression_cover_primary_source.json').read_text(encoding='utf-8'))
    assert primary['theorem']==1 and primary['arbitrary_finite_alphabet'] and not primary['subset_reachability_required']
    return tests
def main():
    finite=[]
    for n,k in ((2,2),(3,2),(4,2),(3,3)):
        z=exhaustive(n,k);finite.append(z);print(json.dumps(z),flush=True)
    front=frontier();randoms=seeded();cuts=applications()
    names=[Path(__file__).name,'MANDATORY_CORE_ISOLATION.md','frontier_certificates.json',
        'ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md','COMPRESSION_COVER_FLOOR.md',
        'compression_cover_primary_source.json','CODIMENSION_FOUR_P5_DICHOTOMY.md',
        'B1_FIFTH_ENTRANCE.md','B1_SIXTH_ENTRANCE.md']
    result=dict(status='pass',lemma='d(x,q)>=c(S)-(n-|S|) for x mandatory through n-|S|',
        alphabet='arbitrary finite',subset_size_range='2<=|S|<=n',requires_strong_connectivity=True,
        requires_synchronization=True,requires_actual_image_for_lemma=False,
        complete_small_row_domains=finite,frontier_controls=front,seeded_larger_controls=randoms,
        conditional_all_alphabet_cover_exclusions=cuts,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Symbolic mandatory-core isolation with complete small controls, all290 frontier examples and three conditional all-alphabet cover exclusions. No new extremal F value, full13-state automaton scan or numerical alphabet separation.')
    (ROOT/'mandatory_core_isolation_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',frontier=front,seeded=randoms,conditional_cuts=cuts)),flush=True)
if __name__=='__main__':main()
