"""Independent four paired binary seventh exclusions in E6/F7/G8.

No generator imports. Complete kernel partitions and role fields are
reconstructed; earlier independent actual-row word functions are reused.
Small coupled controls and full n13 individual ports supplement the
symbolic all-ordinary-output proof, not an extrapolated transition scan.
"""
from itertools import combinations, product, permutations
from collections import Counter, deque
from functools import lru_cache
from pathlib import Path
from math import factorial
import hashlib, json
from check_b1_e6_overlap_fifth import reason17, reason24
ROOT=Path(__file__).resolve().parent
Q=set(range(13));K={1,2};P={0,3,5,6,7,8};C={1,4}
KEYS=('preA','preB','preC','preD','preE','preF','preG')
CAPS=(1,1,2,1,1,1,1,5)

def canonical(fields):
    return tuple(tuple(sorted(tuple(sorted(b)) for b in part)) for part in fields)

@lru_cache(None)
def partitions(X,cap):
    choices=[[frozenset({q}) for q in sorted(set(X)-K)]]
    for q in sorted(set(X)&K):
        fresh=[]
        for blocks in choices:
            fresh.append([*blocks,frozenset({q})])
            for i,block in enumerate(blocks):
                if q in P or block&P:continue
                fresh.append([*blocks[:i],block|{q},*blocks[i+1:]])
        choices=fresh
    return {tuple(sorted(tuple(sorted(b)) for b in blocks))
        for blocks in choices if len(blocks)<=cap}

def kernels_and_roles():
    inv=json.loads((ROOT/'b1_e6_f7_g8_seventh_kernel_inventory.json').read_text(encoding='utf-8'))
    parent=json.loads((ROOT/'b1_seventh_inventory.json').read_text(encoding='utf-8'))['records']
    summary=[]
    for z in inv['profiles']:
        source=next(v for v in parent if v['id']==z['id'])
        assert z['protected']==sorted(P)==source['mandatory_through_four']
        expected=[(p['original_third_rows'],p['original_fourth_rows'],
            p['original_fifth_rows'],p['original_sixth_rows'],xy)
            for p in source['pairs'] for xy in p['seventh_field_pairs']]
        assert [(p['original_third_rows'],p['original_fourth_rows'],
            p['original_fifth_rows'],p['original_sixth_rows'],p['rows']) for p in z['pairs']]==expected
        for i,row in enumerate(z['rows']):
            assert row['parent_row']==i and all(row[key]==source['rows'][i][key] for key in KEYS)
            groups=[set(row[key]) for key in KEYS]
            groups.append(Q-set().union(*groups))
            expected={tuple(parts) for parts in product(*[partitions(tuple(sorted(X)),cap)
                for X,cap in zip(groups,CAPS)])}
            assert expected=={canonical(v['fields']) for v in row['patterns']}
            assert len(expected)==len(row['patterns'])
            for pat in row['patterns']:
                kernel={e for part in pat['fields'] for block in part for e in combinations(sorted(block),2)}
                assert kernel=={tuple(e) for e in pat['kernel']}
                assert all(set(e)&K and not set(e)&P for e in kernel)
        for pair in z['pairs']:
            x,y=pair['rows']
            assert pair['kernel_pairs']==[list(ij) for ij in product(
                range(len(z['rows'][x]['patterns'])),range(len(z['rows'][y]['patterns'])))]
            rows=(z['rows'][x],z['rows'][y])
            X=[v for v in rows if v['preG']==z['H']]
            L=[v for v in rows if v['preB']==[1,4]]
            assert len(X)==len(L)==1 and X[0]!=L[0]
            X=X[0];L=L[0]
            assert sorted((X['preA'],X['preB']))==[[0],[3]]
            assert [X[key] for key in ('preC','preD','preE','preF')]==[[5],[6],[7],[8]]
            assert L['preA'] in ([0],[3]) and L['preC'] in ([0],[3],[5])
            singleton=[L[key] for key in ('preA','preC','preD','preE','preF','preG')]
            assert all(len(t)==1 for t in singleton) and {t[0] for t in singleton}==P
        item=dict(H=z['H'],original_field_pairs=len(z['pairs']),
            row_patterns=sum(len(r['patterns']) for r in z['rows']),
            compatible_kernel_pairs=sum(len(p['kernel_pairs']) for p in z['pairs']))
        assert item['original_field_pairs']==48;summary.append(item)
    for name,digest in inv['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    return summary

def ordinary_maps(inputs,guard,targets):
    for out in permutations(targets):yield dict(zip(inputs,out)),None
    for q in inputs:
        if q==guard:continue
        blocks=[(guard,q)]+[(x,) for x in inputs if x not in (guard,q)]
        for out in permutations(targets,len(blocks)):
            yield {x:t for block,t in zip(blocks,out) for x in block},q

def left_rows(n):
    T=(2,*range(9,n))
    for ordinary,q in ordinary_maps(T,2,T):
        for preA in (0,3):
            for u in sorted({0,3,5}-{preA}):
                for predecessors in permutations(sorted(P-{preA,u})):
                    for delta in (1,4):
                        L=[-1]*n;L[1]=L[4]=0;L[preA]=3;L[u]=delta
                        for x,t in zip(predecessors,(5,6,7,8)):L[x]=t
                        for x,t in ordinary.items():L[x]=t
                        assert all(t>=0 for t in L);yield L,u,q

def right_rows(n,H):
    J=tuple(range(9,n));T=(2,*J);I=tuple(sorted(set(range(n))-P-set(H)))
    if H in ([1,2],[1,2,9]):
        systems=((dict(zip(I,out)),None) for out in permutations(T,len(I)))
    else:systems=ordinary_maps(I,2 if H==[1,9] else 1,T)
    for (ordinary,q),swap,gamma in product(systems,(False,True),(1,4)):
        X=[-1]*n;X[0]=3 if swap else 0;X[3]=0 if swap else 3
        X[5]=gamma;X[6]=5;X[7]=6;X[8]=7
        for x in H:X[x]=8
        for x,t in ordinary.items():X[x]=t
        assert all(t>=0 for t in X);yield X

def merge(rows,pair,word,kind):
    assert pair[0]!=pair[1] and len(word)==2
    if kind=='protected':assert set(pair)&P
    else:assert kind=='outside_K' and not set(pair)&K
    image=set(pair)
    for ell in word:image={rows[ell][q] for q in image}
    assert len(image)==1

def short_reason(L,X,u,q,H,J):
    gamma=X[5];delta=L[u];rows=(L,X)
    I=tuple(sorted(set(range(len(X)))-P-set(H)))
    if gamma==delta:
        assert 5-gamma not in set(L)|set(X);return 'missing_C_target'
    if gamma==1:
        t=next(t for t in H if t!=1 and t in {X[x] for x in I})
        x=next(x for x in I if X[x]==t)
        merge(rows,(5,x),(1,1),'protected');return 'protected_XX'
    assert gamma==4 and delta==1
    if len(H)==3:
        t=next(t for t in (2,9) if t in {L[x] for x in (2,*J)})
        x=next(x for x in (2,*J) if L[x]==t)
        merge(rows,(u,x),(0,1),'protected');return 'protected_LX_H129'
    if 2 in {L[x] for x in (2,*J)}:
        x=next(x for x in (2,*J) if L[x]==2)
        merge(rows,(u,x),(0,1),'protected');return 'protected_LX_H12'
    assert q is not None and L[2]==L[q]
    x=next(x for x in I if X[x]==2);y=next(x for x in I if X[x]==q)
    merge(rows,(x,y),(1,0),'outside_K');return 'outside_XL_extra_kernel'

def independent_pair_distances(rows):
    # Forward BFS from each pair, independent of any alleged proof word.
    result={}
    for initial in combinations(range(len(rows[0])),2):
        queue=deque([(initial,0)]);seen={initial}
        while queue:
            state,d=queue.popleft()
            if state[0]==state[1]:result[initial]=d;break
            for row in rows:
                nxt=tuple(sorted((row[state[0]],row[state[1]])))
                if nxt not in seen:seen.add(nxt);queue.append((nxt,d+1))
        else:result[initial]=None
    return result

def independent_contradiction(L,X,reason):
    rows=(L,X);n=len(L)
    distances=independent_pair_distances(rows)
    sync=all(v is not None for v in distances.values())
    protected=any(v is not None and v<=7 and set(e)&P for e,v in distances.items())
    uncovered=any(v is not None and v<=5 and not set(e)&K for e,v in distances.items())
    sc=True
    for start in range(n):
        reached={start};todo=[start]
        for q in todo:
            for row in rows:
                t=row[q]
                if t not in reached:reached.add(t);todo.append(t)
        sc &= len(reached)==n
    if reason=='gamma1_initial_one_count_incompatible':
        q=next(q for q in range(9,n) if L[q]==L[2])
        assert {i for i in range(n) if X[i] in (2,4)}=={q}
        assert {i for i in range(n) if X[X[i]] in (2,4)}=={1}
        for x1,x2,x4,xq in product((0,1),repeat=4):
            assert not (x1+x4==x2+x4==1 and xq==x1==1 and x2+xq<=1)
    else:assert not sc or not sync or protected or uncovered
    return dict(strongly_connected=sc,synchronizing=sync,
        protected_distance_violation=protected,uncovered_distance_violation=uncovered)

def literal_controls(n,H):
    left=list(left_rows(n));right=list(right_rows(n,H))
    hist=Counter();samples={};J=tuple(range(9,n))
    for (L,u,q),X in product(left,right):
        if H==[1,9]:reason=reason17(L,X,u,J,9)
        elif H==[2,4]:reason=reason24(L,X,u,J)
        else:reason=short_reason(L,X,u,q,H,J)
        hist[reason]+=1
        if reason not in samples:samples[reason]=independent_contradiction(L,X,reason)
    k=n-8;total=sum(hist.values());expected=768*k*factorial(k)**2
    if H in ([1,9],[2,4]):
        expected*=k
        assert hist['gamma1_closed_four_cycle'] and hist['gamma4_closed_four_cycle']
    if H==[2,4]:assert hist['gamma1_initial_one_count_incompatible']
    assert total==expected and hist['missing_C_target']*2==total
    return dict(n=n,H=H,complete_normalized_row_pairs=total,
        proof_cases=dict(sorted(hist.items())),independent_forward_BFS_case_controls=samples)

def short_ports():
    J=tuple(range(9,13));T=(2,*J);counts=Counter()
    for out in permutations(T):
        inverse=dict(zip(out,(4,*J)))
        assert set(inverse)==set(T) and not set(inverse.values())&K
        counts['H12_X_systems']+=1
    for out in permutations(T,4):
        inverse=dict(zip(out,(4,*range(10,13))))
        assert len(inverse)==4 and any(t in inverse for t in (2,9))
        counts['H129_X_systems']+=1
    for ordinary,q in ordinary_maps(T,2,T):
        assert len(set(ordinary.values()))>=4 and any(t in ordinary.values() for t in (2,9))
        counts['ordinary_L_systems']+=1
        if 2 not in ordinary.values():
            assert q is not None and ordinary[2]==ordinary[q]
            counts['L_systems_omitting2']+=1
    assert counts==Counter(H12_X_systems=120,H129_X_systems=120,
        ordinary_L_systems=600,L_systems_omitting2=96)
    return dict(counts)

def overlap_ports(H):
    J=tuple(range(9,13));T=(2,*J);counts=Counter()
    for q in J:
        graph={(1,4),(2,4),(1,q),(2,q)}
        for gamma in (1,4):
            l_targets=J if gamma==1 else tuple(x for x in T if x!=q)
            x_targets=tuple(x for x in T if x!=q) if gamma==1 else J
            for out in permutations(l_targets):
                for preA in (0,3):
                    for u in sorted({0,3,5}-{preA}):
                        for predecessors in permutations(sorted(P-{preA,u})):
                            L=[-1]*13;L[1]=L[4]=0;L[preA]=3;L[u]=5-gamma
                            for x,t in zip(predecessors,(5,6,7,8)):L[x]=t
                            for x,t in zip(J,out):L[x]=t
                            L[2]=L[q]
                            kernel={e for e in combinations(range(13),2) if L[e[0]]==L[e[1]]}
                            assert kernel=={(1,4),(2,q)}
                            assert all(not set(e)<=set(L) for e in graph)
                            counts[f'gamma{gamma}_L_letters']+=1
            if H==[1,9]:
                Hactual={1,q};I=(4,*[x for x in J if x!=q]);guard=2;partner=4
            else:Hactual={2,4};I=J;guard=1;partner=q
            for out in permutations(x_targets):
                for swap in (False,True):
                    X=[-1]*13;X[0]=3 if swap else 0;X[3]=0 if swap else 3
                    X[5]=gamma;X[6]=5;X[7]=6;X[8]=7
                    for x in Hactual:X[x]=8
                    for x,t in zip(I,out):X[x]=t
                    X[guard]=X[partner]
                    kernel={e for e in combinations(range(13),2) if X[e[0]]==X[e[1]]}
                    assert kernel=={(1,q),(2,4)}
                    assert all(not set(e)<=set(X) for e in graph)
                    counts[f'gamma{gamma}_X_letters']+=1
    assert counts==Counter(gamma1_L_letters=9216,gamma4_L_letters=9216,
        gamma1_X_letters=192,gamma4_X_letters=192)
    result=dict(H=H,all_hard_branch_full_letter_systems=dict(counts),
        full_letter_assignments=sum(counts.values()),all_four_ordinary_labels_checked=True)
    if H==[2,4]:
        initial=0
        for q in J:
            for values in combinations(range(13),9):
                S=set(values)
                if not P<=S or len(S&C)!=1 or len(S&{2,4})!=1:continue
                initial+=1;assert not (1 in S and q in S and len(S&{2,q})<=1)
        assert initial==40;result['initial_nine_set_controls']=initial
    return result

def main():
    kernels=kernels_and_roles();literal=[]
    for H in ([1,2],[1,9],[2,4],[1,2,9]):
        for n in (10,11):
            item=literal_controls(n,H);literal.append(item)
            print(json.dumps(dict(n=n,H=H,pairs=item['complete_normalized_row_pairs'])),flush=True)
    ports=short_ports();overlaps=[overlap_ports(H) for H in ([1,9],[2,4])]
    inv=json.loads((ROOT/'b1_seventh_inventory.json').read_text(encoding='utf-8'))['records']
    kept=[z for z in inv if z['H'] in ([9],[2,9])]
    assert len(kept)==2 and sum(z['labelled_H'] for z in kept)==8
    assert sum(len(p['seventh_field_pairs']) for z in kept for p in z['pairs'])==2188
    sixth_coverage={tuple(p['original_sixth_rows']) for z in kept for p in z['pairs'] if p['seventh_field_pairs']}
    original={tuple(p['original_sixth_rows']) for z in inv for p in z['pairs'] if p['seventh_field_pairs']}
    assert sixth_coverage==original and len(sixth_coverage)==365
    names=[Path(__file__).name,'enumerate_b1_e6_f7_g8_seventh.py',
        'b1_e6_f7_g8_seventh_kernel_inventory.json','B1_E6_F7_G8_PAIRED_SEVENTH_EXCLUSIONS.md',
        'check_b1_e6_overlap_fifth.py','b1_seventh_inventory.json','b1_seventh_audit.json',
        'B1_SEVENTH_ENTRANCE.md','MANDATORY_CORE_ISOLATION.md','mandatory_core_isolation_audit.json',
        'ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
    result=dict(status='pass',parameter=[13,9,1],branch=dict(E=[6],F=[7],G=[8]),
        alphabet='binary only',excluded_H=[[1,2],[1,9],[2,4],[1,2,9]],
        mandatory_core_isolation_depth=7,kernel_controls=kernels,
        complete_literal_controls=literal,complete_n13_short_ports=ports,
        complete_n13_overlap_hard_ports=overlaps,removed_seventh_field_pairs=192,
        remaining_H=[[9],[2,9]],remaining_geometric_orbits=2,remaining_labelled_H=8,
        remaining_field_pairs=2188,all_original_sixth_pairs_retained=365,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Four conditional binary seventh exclusions; every protected8 assignment and actual one-count exception retained. Independent finite controls supplement the symbolic proof. No full n13 coupled-row scan, entire G8/fifth/third/joint exclusion, unrestricted paired exclusion, exact F value or numerical alphabet separation.')
    (ROOT/'b1_e6_f7_g8_seventh_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',kernels=kernels,
        complete_literal_pairs=sum(v['complete_normalized_row_pairs'] for v in literal),
        n13_full_hard_letters=[v['full_letter_assignments'] for v in overlaps],
        remaining_binary_field_pairs=2188)),flush=True)
if __name__=='__main__':main()
