"""Independent typed rows, quotient cases and singleton-first cover audit.

The universal exclusions are paper proofs. Finite quotient and geometry
domains here are audited controls, not a full automaton enumeration.
"""
from collections import Counter,deque
from itertools import combinations,combinations_with_replacement,product
from pathlib import Path
import hashlib,json
from alphabet_check import bfs,pair_distances,verify,certificate
from check_short_pair_span import exact_rank

ROOT=Path(__file__).resolve().parent

def distances(f,beta,p0):
    found={p0:''};queue=deque([p0])
    while queue:
        p=queue.popleft()
        for letter,q in (('L',beta),('F',f[p])):
            if q not in found:found[q]=found[p]+letter;queue.append(q)
    return found

def typed_rows(k,j):
    A={0};B={1};C=set(range(2,k+2));D=set(range(2,2+j))|{k+2}
    sets={'A':A,'B':B,'C':C,'D':D}
    rows=[]
    for pa,pb,pc in product('AB','ABC','ABCD'):
        groups=[sets[x] for x in (pa,pb,pc)]
        if any(groups[x]&groups[y] for x,y in combinations(range(3),2)):continue
        rows.append(pa+pb+pc)
    pairs=[]
    for pair in combinations_with_replacement(rows,2):
        if not any(v[0]=='B' for v in pair) or not any(v[1]=='C' for v in pair) or not any(v[2]=='D' for v in pair):continue
        if sum(len(sets[v[2]]) for v in pair)<k:continue
        pairs.append(pair)
    if j==0:
        assert {tuple(sorted(z)) for z in pairs}=={tuple(sorted(z)) for z in
           [('ACD','BAC'),('BCD','ABC'),('BCD','BAC')]}
        for pair in pairs:
            L=next(v for v in pair if v[1]=='C');F=next(v for v in pair if v!=L)
            assert L[2]=='D' and F[2]=='C' and F[1] in 'AB'
    else:
        expected=[] if j+2<k else [('ACB','BAD'),('BCA','ABD'),('BCA','BAD')]
        assert {tuple(sorted(z)) for z in pairs}=={tuple(sorted(z)) for z in expected}
        for pair in pairs:
            L=next(v for v in pair if v[1]=='C');F=next(v for v in pair if v!=L)
            assert L[2] in 'AB' and F[2]=='D' and F[1] in 'AB'
    return dict(k=k,intersection_size=j,binary_pairs=[list(z) for z in pairs])

def common_fiber(k,j):
    n=k+6;Q=set(range(n));A={0};O=Q-A;B={1};C=set(range(2,k+2));D=set(range(2,2+j))|{k+2}
    images=[A|set(v) for v in combinations(sorted(O),5) if all(len(set(v)&X)==1 for X in (B,C,D))]
    assert images and all(len(S-(A|B|C|D))>=2 for S in images)
    columns=[[1,int(q in B),int(q in C),int(q in D)] for q in sorted(O)]
    assert exact_rank(columns,4)==4
    allowed=[];tested=0
    for size in range(1,len(O)+1):
        for values in combinations(sorted(O),size):
            R=set(values);tested+=1
            if exact_rank([row+[int(q in R)] for q,row in zip(sorted(O),columns)],5)!=4:continue
            if not all(len(S&R)==1 for S in images):continue
            allowed.append(R)
    assert {tuple(sorted(X)) for X in allowed}=={tuple(sorted(X)) for X in (B,C,D)}
    return dict(k=k,intersection_size=j,all_outside_subsets_checked=tested,feasible_six_sets=len(images),admitted_fibers=3)

def quotients(k,j):
    U=set(range(j));V=set(range(j,k));raw=reachable=compatible=Vcases=Ucases=0
    maps=product(range(k),repeat=k if j==0 else j+1)
    for values in maps:
        f=tuple(values) if j==0 else tuple(values[p] if p in U else values[-1] for p in range(k))
        for beta,p0 in product(range(k),repeat=2):
            raw+=1; paths=distances(f,beta,p0)
            if len(paths)!=k:continue
            reachable+=1;assert max(map(len,paths.values()))<=k-1
            # The C projections are literally all unit vertices of dimension k-1.
            # The paper equality flag supplies the matching upper dimension.
            if j==0:
                compatible+=1
                rest={k,k+1,k+2,k+3,k+4};family={p:frozenset(rest|{p}) for p in range(k)}
                assert all(len(family[p])==6 for p in range(k))
                assert all(family[beta] in family.values() and family[f[p]] in family.values() for p in range(k))
                continue
            if len({p0 in U,beta in U,f[p0] in U})!=1:continue
            compatible+=1
            if p0 in V:
                Vcases+=1
                assert beta in V and values[-1] in V
                assert all(f[p] in V for p in V)
                raise AssertionError('A closed V quotient cannot reach all C states')
            Ucases+=1
            assert beta in U
            endpoint=min(V,key=lambda p:(len(paths[p]),paths[p]));word=paths[endpoint]
            assert word and word[-1]=='F' and len(word)<=k-1
            point=p0;new_point=k;rest={k+1,k+2,k+3,k+4,k+5}
            D=U|{new_point}
            for letter in word:
                assert point in U and len((rest|{point})&D)==1
                point=beta if letter=='L' else f[point]
            assert point in V and not (rest|{point})&D
    assert Vcases==0
    return dict(k=k,intersection_size=j,quotient_assignments=raw,all_vertices_reachable=reachable,
                first_outside_equality_compatible=compatible,U_branch_cases=Ucases,V_branch_cases=Vcases)

def witness_controls():
    data=json.loads((ROOT/'third_entrance_control_witnesses.json').read_text(encoding='utf-8'))
    records=[];boundary=None
    for z in data['witnesses']:
        rows=z['rows'];a=z['A'][0];A={a};s=z['s'];n=z['n'];S=set(z['S'])
        checked=certificate(rows,S,1);assert checked is not None and verify(checked) and checked['value']==n-1
        original,_=bfs(rows,S,lambda T:len(T)<s or a not in T)
        assert len(original)==n-1
        first={frozenset(q for q,v in enumerate(row) if v==a) for row in rows}-{frozenset(A)}
        assert len(first)==1;B=set(next(iter(first)))
        if len(B)!=1:continue
        b=next(iter(B));second={frozenset(q for q,v in enumerate(row) if v in B) for row in rows}-{frozenset(A),frozenset(B)}
        assert len(second)==1;C=set(next(iter(second)))
        word,_=bfs(rows,S,lambda T:len(T)<s or not (A|B)<=T)
        assert len(word)==n-2
        dist=pair_distances(rows)
        assert min(d for pair,d in dist.items() if b in pair)>=s-2
        preC=[{q for q,v in enumerate(row) if v in C} for row in rows]
        fresh=[D for D in preC if D not in (A,B,C)]
        assert fresh
        covered=all(x in C or y in C for (x,y),d in dist.items() if d<=3)
        if s>=6 and len(C)>=3:
            assert not covered
            for D in fresh:
                if len(D-C)==1:
                    suppliers=[row for row in rows if {q for q,v in enumerate(row) if v in B}==C]
                    assert len(suppliers)==1
                    L=suppliers[0]
                    assert any(L[x]==L[y] for x,y in combinations(sorted(set(range(n))-C),2))
                else:
                    if (n,s)==(12,6):boundary=dict(n=n,s=s,B=sorted(B),C=sorted(C),D=sorted(D),
                       new_third_points=len(D-C),cover_P3=covered,scope='Actual binary equality witness with two new third points; no one-new-point quotient assumption is imposed')
        records.append(dict(n=n,s=s,B=sorted(B),C=sorted(C),two_protected_delay=len(word),second_covers_P3=covered))
    assert boundary is not None
    return records,boundary

def frontier_consequences():
    inventory=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    index={z['id']:z for z in joint['records']}
    assert index['b1_out_c6']['B']==[4] and index['b1_out_c6']['C']==[0,1,2]
    assert index['b1_in_c5']['B']==[0] and index['b1_in_c5']['C']==[1,2,4]
    for name in ('b1_out_c6','b1_in_c5'):
        records=[z for z in inventory['records'] if z['joint_id']==name]
        assert len(records)==3 and all(len(set(z['D'])-set(z['C']))==1 for z in records)
    focused=next(z for z in inventory['records'] if z['joint_id']=='b1_out_c5' and z['D']==[2])
    assert len(focused['binary_profile_pairs'])==3
    C=set(focused['C']);H={0,1,2};D={2};Q=set(range(13))
    candidates=[(x,y) for x,y in combinations(sorted(Q-C),2) if {x,y}&H]
    assert len(candidates)==9 and all(2 in pair for pair in candidates)
    for pair in focused['binary_profile_pairs']:
        rows=[focused['rows'][i] for i in pair]
        L=next(row for row in rows if row['preB']==[0,1,5])
        assert set(L['preC'])==D
    exclusions={z['id'] for z in joint['records'] if len(z['B'])==3}|{
        'b2_mixed_c12','b1_out_c6','b1_in_c5'}
    assert len(exclusions)==17
    geometric=[z for z in inventory['records'] if z['joint_id'] not in exclusions]
    typed=[z for z in geometric if z['binary_profile_pairs'] and z['id']!=focused['id']]
    assert len(geometric)==221 and len(typed)==173
    assert sum(len(z['binary_profile_pairs']) for z in typed)==942
    return dict(additional_binary_joint_exclusions=['b1_out_c6','b1_in_c5'],
        additional_binary_third_profile_exclusions=[focused['id']],remaining_binary_joint=26,
        remaining_unrestricted_joint=43,remaining_geometric_small_first_third_orbits=221,
        remaining_binary_typed_third_orbits=173,remaining_binary_profile_pairs=942)

def main():
    rows=[];geometry=[];quotient=[]
    for k in (3,4,5):
        for j in range(k):
            rows.append(typed_rows(k,j));geometry.append(common_fiber(k,j));quotient.append(quotients(k,j))
    witnesses,boundary=witness_controls();frontier=frontier_consequences()
    sources=[Path(__file__).name,'BINARY_SINGLETON_FIRST_SECOND_COVER.md','ENTRY_FIBER_FLAG.md',
        'SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md','LOCAL_EQUALITY_FLAG.md',
        'check_short_pair_span.py','alphabet_check.py','third_entrance_control_witnesses.json',
        'joint_fiber_orbits.json','small_first_third_inventory.json',
        'CODIMENSION_FOUR_P5_DICHOTOMY.md','SINGLETON_THREE_KERNEL_EXCLUSION.md']
    result=dict(status='pass',general_scope='binary, singleton equality n-1, s>=6, |B|=1, |C|>=3',
        proof='BINARY_SINGLETON_FIRST_SECOND_COVER.md',row_type_cases=rows,common_fiber_geometric_cases=geometry,
        quotient_cases=quotient,finite_quotient_assignments=sum(z['quotient_assignments'] for z in quotient),
        singleton_first_witness_controls=witnesses,boundary_control=boundary,frontier=frontier,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
        limits='Universal result uses the symbolic quotient/affine proof. Finite quotient controls cover k=3,4,5 only and are not completed-transition-table enumeration. s=5, larger alphabets and arbitrary multi-new-point D are not asserted. No new F value or alphabet separation.')
    (ROOT/'singleton_first_second_cover_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',finite_k=[3,4,5],type_geometric_cases=len(rows),
        quotient_assignments=result['finite_quotient_assignments'],known_singleton_first_controls=len(witnesses),frontier=frontier)))

if __name__=='__main__':main()
