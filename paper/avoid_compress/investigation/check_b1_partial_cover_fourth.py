"""Independent K-cover kernel and common-E admission checker.

No generator is imported. Literal masks, an independent partition order
and bounded-integer exact modular ranks replace the generator routines.
"""
from itertools import combinations,product
from collections import deque
from functools import lru_cache
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};K={1,2}
FULL=(1<<13)-1;OUT=FULL^(1<<3)
def mask(X):return sum(1<<q for q in X)
def points(v):return [q for q in range(13) if v>>q&1]
def incomparable(x,y):return bool(x&~y) and bool(y&~x)
def canonical(fields):return tuple(tuple(sorted(tuple(sorted(block)) for block in field)) for field in fields)
def kernel(fields):return {p for field in fields for block in field for p in combinations(sorted(block),2)}

@lru_cache(None)
def independent_partitions(X,cap,protected):
    X=set(X); protected=set(protected)
    blocks=[frozenset({q}) for q in sorted(X-K)]
    candidates=[blocks]
    for q in sorted(X&K):
        expanded=[]
        for fields in candidates:
            expanded.append([*fields,frozenset({q})])
            for i,block in enumerate(fields):
                if any({q,r}&protected for r in block):continue
                expanded.append([*fields[:i],block|{q},*fields[i+1:]])
        candidates=expanded
    return {tuple(sorted(tuple(sorted(block)) for block in fields)) for fields in candidates if len(fields)<=cap}

def rank1009(columns):
    work=[[int(bool(c>>q&1)) for c in columns] for q in points(OUT)];r=0
    for j in range(len(columns)):
        i=next((i for i in range(r,len(work)) if work[i][j]),None)
        if i is None:continue
        work[r],work[i]=work[i],work[r];scale=pow(work[r][j],-1,1009)
        work[r]=[x*scale%1009 for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j]
            if v:work[i]=[(x-v*y)%1009 for x,y in zip(work[i],work[r])]
        r+=1
    return r

def kernel_controls():
    inventory=json.loads((ROOT/'b1_partial_cover_inventory.json').read_text(encoding='utf-8'))
    original=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))['records']
    counts=[]
    for profile in inventory['profiles']:
        old=next(v for v in original if v['id']==profile['id'])
        assert [v['rows'] for v in profile['pairs']]==old['binary_profile_pairs']
        protected=A|B|(set(profile['D']) if len(profile['D'])==1 else set())
        for row,oldrow in zip(profile['rows'],old['rows']):
            assert all(row[key]==oldrow[key] for key in ('preA','preB','preC'))
            inputs=[set(row[key]) for key in ('preA','preB','preC')]
            inputs.append(Q-set().union(*inputs))
            possible=[independent_partitions(tuple(sorted(X)),cap,tuple(sorted(protected))) for X,cap in zip(inputs,[1,1,2,9])]
            independent={tuple(fields) for fields in product(*possible)}
            supplied={canonical(v['fields']) for v in row['patterns']}
            assert independent==supplied and len(supplied)==len(row['patterns'])
            for pattern in row['patterns']:assert kernel(pattern['fields'])=={tuple(p) for p in pattern['kernel']}
        for pair in profile['pairs']:
            x,y=pair['rows']
            assert pair['kernel_pairs']==[list(ij) for ij in product(range(len(profile['rows'][x]['patterns'])),range(len(profile['rows'][y]['patterns'])))]
        counts.append(dict(D=profile['D'],original_pairs=len(profile['pairs']),
            row_patterns=sum(len(v['patterns']) for v in profile['rows']),kernel_pairs=sum(len(v['kernel_pairs']) for v in profile['pairs'])))
    assert sum(v['row_patterns'] for v in counts)==646 and sum(v['kernel_pairs'] for v in counts)==6555
    return counts

def field_controls(E,parent):
    # All four output fields are disjoint. Check preimage disjointness
    # directly, rather than using the generator's sixteen-cell incidence.
    cap=[1,1,2,1,8];provided=[]
    for old_id,row in enumerate(parent['rows']):
        for preD in (A,B,C,D,E):
            inputs=[set(row[key]) for key in ('preA','preB','preC')]+[preD]
            if any(inputs[i]&inputs[j] for i,j in combinations(range(4),2)):continue
            inputs.append(Q-set().union(*inputs))
            forced={p for X,limit in zip(inputs,cap) if limit==1 for p in combinations(sorted(X),2)}
            if any(not set(p)&K or set(p)&(A|B|D) for p in forced) or len(forced)>4:continue
            provided.append(dict(old_row=old_id,preA=row['preA'],preB=row['preB'],preC=row['preC'],
                preD=sorted(preD),forced=forced,capacity=[min(len(X),limit) for X,limit in zip(inputs,cap)]))
    pairs=[]
    for x,y in parent['binary_profile_pairs']:
        current=[]
        for i,left in enumerate(provided):
            if left['old_row']!=x:continue
            for j,right in enumerate(provided):
                if right['old_row']!=y or (x==y and i>j):continue
                if set(left['preD'])!=E and set(right['preD'])!=E:continue
                if any(left['capacity'][h]+right['capacity'][h]<cap[h] for h in range(5)):continue
                if len(left['forced']|right['forced'])>4:continue
                current.append([i,j])
        pairs.append(dict(original_rows=[x,y],fourth_field_pairs=current))
    return provided,pairs

def letter_control():
    row=list(range(13));row[0]=1;row[1]=row[4]=0;row[2]=row[6]=6
    assert {q for q in Q if row[q]==3}==A and {q for q in Q if row[q]==0}==C
    assert {q for q in Q if row[q] in C}==B and {q for q in Q if row[q]==5}==D
    immediate={p for p in combinations(range(13),2) if row[p[0]]==row[p[1]]}
    assert immediate=={(1,4),(2,6)}
    reverse={p:[] for p in combinations(range(13),2)}
    for p in reverse:
        t=tuple(sorted((row[p[0]],row[p[1]])))
        if t[0]!=t[1]:reverse[t].append(p)
    reached=set(immediate);todo=deque(reached)
    while todo:
        for p in reverse[todo.popleft()]:
            if p not in reached:reached.add(p);todo.append(p)
    assert reached==immediate and all(set(p)&K and not set(p)&(A|B|D) for p in reached)
    assert any(not set(p)&C for p in reached)
    return dict(row=row,all_single_letter_mergeable_pairs=[list(p) for p in sorted(reached)],
        outside_C_injectivity_fails=True,scope='One full letter only; not a strongly connected synchronizing witness or an F lower bound.')

def main():
    kernel_counts=kernel_controls()
    inventory=json.loads((ROOT/'b1_partial_cover_fourth_inventory.json').read_text(encoding='utf-8'))
    parent=next(v for v in json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))['records'] if v['id']=='b1_in_c3_third2')
    allS=[t for t in range(FULL+1) if t&(1<<3) and t.bit_count()==9]
    b,c,d,k=map(mask,(B,C,D,K))
    covered=[r for r in range(1,FULL+1) if not r&(1<<3) and r.bit_count()<=3 and (r&~k).bit_count()<=1]
    assert len(covered)==43
    members={};candidate_tests=0
    for e in covered:
        if any(not incomparable(e,x) for x in (b,c,d)):continue
        forms=[t for t in allS if all((t&x).bit_count()==1 for x in (b,c,d,e))]
        if not forms or rank1009([OUT,b,c,d,e])!=5:continue
        sig=tuple(sum(bool(e>>q&1) and tuple(int(bool(x>>q&1)) for x in (k,b,c,d))==key for q in points(OUT))
                  for key in product((0,1),repeat=4))
        members.setdefault(sig,[]).append(e)
    assert len(members)==7 and sum(len(es) for es in members.values())==31
    verified=0;families=0;kept_pairs=0;old_pairs=set();summary=[]
    for z in inventory['records']:
        sig=tuple(z['cell_signature']);assert sig in members and len(members[sig])==z['labelled_E']==z['orbit_size']
        e=mask(z['E']);assert e in members[sig]
        for labelled in members[sig]:
            forms=[t for t in allS if all((t&x).bit_count()==1 for x in (b,c,d,labelled))]
            common=FULL
            for t in forms:common&=t
            assert len(forms)==z['feasible_nine_sets'] and ((k&~common).bit_count()<=1)==z['excluded_by_known_bound']
            allowed=[]
            for r in covered:
                candidate_tests+=1
                if any(r!=x and not incomparable(r,x) for x in (b,c,d,labelled)):continue
                if rank1009([OUT,b,c,d,labelled,r])!=5:continue
                if all((t&r).bit_count()==1 for t in forms):allowed.append(r)
            assert set(allowed)=={b,c,d,labelled}
            if labelled!=e:continue
            assert points(common)==z['mandatory_through_seven'] and points(k&~common)==z['remaining_P3_cover']
            families+=len(forms)
        independent,expected_pairs=field_controls(set(z['E']),parent)
        assert len(independent)==len(z['rows'])
        for literal,row in zip(independent,z['rows']):
            assert all(literal[key]==row[key] for key in ('old_row','preA','preB','preC','preD'))
            assert literal['forced']=={tuple(p) for p in row['forced_pairs']}
        assert expected_pairs==z['pairs']
        count=sum(len(v['fourth_field_pairs']) for v in z['pairs'])
        if not z['excluded_by_known_bound']:
            kept_pairs+=count
            old_pairs.update(tuple(p['original_rows']) for p in z['pairs'] if p['fourth_field_pairs'])
        summary.append(dict(E=z['E'],labelled=z['labelled_E'],fourth_field_pairs=count,
            excluded_by_known_bound=z['excluded_by_known_bound']))
        verified+=1
    assert verified==7 and kept_pairs==106
    assert old_pairs=={tuple(p) for p in parent['binary_profile_pairs']} and len(old_pairs)==14
    assert [v['E'] for v in summary if v['excluded_by_known_bound']]==[[2]]
    control=letter_control()
    names=[Path(__file__).name,'enumerate_b1_partial_cover.py','enumerate_b1_partial_cover_fourth.py',
        'b1_partial_cover_inventory.json','b1_partial_cover_fourth_inventory.json','enumerate_small_first_third.py',
        'small_first_third_inventory.json','B1_PARTIAL_COVER_FOURTH.md','COMPRESSION_COVER_FLOOR.md',
        'ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md','LOCAL_EQUALITY_FLAG.md',
        'CODIMENSION_FOUR_P5_DICHOTOMY.md','compression_cover_primary_source.json']
    for file in ('b1_partial_cover_inventory.json','b1_partial_cover_fourth_inventory.json'):
        for name,digest in json.loads((ROOT/file).read_text(encoding='utf-8'))['source_sha256'].items():
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    result=dict(status='pass',parameter=[13,9,1],kernels=kernel_counts,
        common_fourth_geometry=dict(B=[0],C=[1,4],D=[5],arbitrary_finite_alphabet=True,
            complete_geometric_orbits=7,complete_labelled_E_choices=31,no_extra_Boolean_fibers=True,
            independent_covered_R_tests=candidate_tests,canonical_nine_family_members=families,
            excluded_fourth_fiber=[2],remaining_geometric_orbits=6,remaining_labelled_E_choices=30,
            remaining_binary_fourth_field_pairs=106,all_original_binary_pairs_retained=14,records=summary),
        adversarial_letter_control=control,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete necessary partial-cover kernel and geometry-specific common-fourth admission; one known-bound fourth cut. No full third/joint exclusion, transition-pair scan, F value or alphabet separation.')
    (ROOT/'b1_partial_cover_fourth_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key not in ('source_sha256','kernels')}))

if __name__=='__main__':main()
