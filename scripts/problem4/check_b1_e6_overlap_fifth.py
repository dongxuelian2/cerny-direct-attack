"""Independent complete binary E6/F17,F24 proof-word audit.

No generator imports. All kernel partitions and role normalizations
are reconstructed before complete smaller row and n13 port controls.
"""
from itertools import combinations,product,permutations
from collections import Counter
from pathlib import Path
from functools import lru_cache
from math import factorial
import hashlib,json
ROOT=Path(__file__).resolve().parent
K={1,2};P={0,3,5,6};LONG_PROTECTED={0,3,5};C={1,4}
KEYS=('preA','preB','preC','preD','preE')
def canonical(fields):return tuple(tuple(sorted(tuple(sorted(b)) for b in part)) for part in fields)
def edges(fields):return {edge for part in fields for block in part for edge in combinations(sorted(block),2)}
@lru_cache(None)
def partitions(X,cap):
    outside=set(X)-K;choices=[[frozenset({q}) for q in sorted(outside)]]
    for q in sorted(set(X)&K):
        expanded=[]
        for blocks in choices:
            expanded.append([*blocks,frozenset({q})])
            for i,block in enumerate(blocks):
                if q in P or block&P:continue
                expanded.append([*blocks[:i],block|{q},*blocks[i+1:]])
        choices=expanded
    return {tuple(sorted(tuple(sorted(b)) for b in blocks)) for blocks in choices if len(blocks)<=cap}
def kernels_and_normalization():
    inv=json.loads((ROOT/'b1_e6_overlap_fifth_inventory.json').read_text(encoding='utf-8'))
    parents=json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'))['records'];summary=[]
    for z in inv['profiles']:
        parent=next(p for p in parents if p['id']==z['id'])
        expected=[(p['original_third_rows'],p['original_fourth_rows'],xy) for p in parent['pairs'] for xy in p['fifth_field_pairs']]
        assert [(p['original_third_rows'],p['original_fourth_rows'],p['rows']) for p in z['pairs']]==expected
        for j,row in enumerate(z['rows']):
            assert row['parent_row']==j and all(row[key]==parent['rows'][j][key] for key in KEYS)
            groups=[set(row[key]) for key in KEYS];groups.append(set(range(13))-set().union(*groups))
            expectedparts={tuple(v) for v in product(*[partitions(tuple(sorted(X)),cap) for X,cap in zip(groups,[1,1,2,1,1,7])])}
            assert expectedparts=={canonical(pat['fields']) for pat in row['patterns']} and len(expectedparts)==len(row['patterns'])
            for pat in row['patterns']:assert edges(pat['fields'])=={tuple(e) for e in pat['kernel']}
        for pair in z['pairs']:
            x,y=pair['rows'];assert pair['kernel_pairs']==[list(ij) for ij in product(range(len(z['rows'][x]['patterns'])),range(len(z['rows'][y]['patterns'])))]
            fields=[z['rows'][x],z['rows'][y]]
            suppliers=[v for v in fields if v['preE']==z['F']];mergers=[v for v in fields if v['preB']==[1,4]]
            assert len(suppliers)==len(mergers)==1 and suppliers[0]!=mergers[0]
            X=suppliers[0];L=mergers[0]
            assert sorted([X['preA'],X['preB']])==[[0],[3]] and X['preC']==[5] and X['preD']==[6]
            assert L['preA'] in ([0],[3]) and L['preC'] in ([0],[3],[5])
            protected=[L[key] for key in ('preA','preC','preD','preE')]
            assert all(len(v)==1 for v in protected) and {v[0] for v in protected}==P
        v=dict(F=z['F'],original_field_pairs=len(z['pairs']),row_patterns=sum(len(r['patterns']) for r in z['rows']),
            compatible_kernel_pairs=sum(len(p['kernel_pairs']) for p in z['pairs']))
        assert v['original_field_pairs']==12 and v['row_patterns']==154 and v['compatible_kernel_pairs']==588
        summary.append(v)
    for name,digest in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    return summary
def merge(rows,pair,word,kind):
    assert pair[0]!=pair[1] and len(word)<=3
    if kind=='protected':assert set(pair)&LONG_PROTECTED
    else:assert kind=='outside_K' and not set(pair)&K
    image=set(pair)
    for ell in word:image={rows[ell][q] for q in image}
    assert len(image)==1,(rows,pair,word)
def closed_graph(rows,q):
    G={(1,4),(2,4),(1,q),(2,q)};assert len(G)==4;allkernels=set()
    for row in rows:
        assert all(not set(edge)<=set(row) for edge in G)
        ker={p for p in combinations(range(len(row)),2) if row[p[0]]==row[p[1]]}
        assert ker<=G;allkernels|=ker
        for p in combinations(range(len(row)),2):assert tuple(sorted((row[p[0]],row[p[1]]))) not in G
    assert allkernels==G
def initial_count(L,X,q):
    assert {x for x in range(len(X)) if X[x] in (2,4)}=={q}
    assert {x for x in range(len(X)) if X[X[x]] in (2,4)}=={1} and L[2]==L[q]
    feasible=[]
    for x1,x2,x4,xq in product((0,1),repeat=4):
        if x1+x4==x2+x4==1 and xq==x1==1 and x2+xq<=1:feasible.append((x1,x2,x4,xq))
    assert not feasible
def reason17(L,X,u,J,j):
    T={2}|set(J);outside=(4,*[x for x in J if x!=j]);gamma=X[5];delta=L[u];rows=(L,X)
    if gamma==delta:
        assert 5-gamma not in set(L)|set(X);return 'missing_C_target'
    if gamma==1:
        pre=next((x for x in (2,*outside) if X[x]==j),None)
        if pre is not None:merge(rows,(5,pre),(1,1),'protected');return 'gamma1_protected_XX'
        assert {X[x] for x in outside}==T-{j}
        r=next(x for x in outside if X[x]==X[2])
        if r!=4:
            x=next(x for x in outside if X[x]==2);y=next(x for x in outside if X[x]==r)
            merge(rows,(x,y),(1,1),'outside_K');return 'gamma1_outside_XX'
        pre=next((x for x in T if L[x]==2),None)
        if pre is not None:merge(rows,(u,pre),(0,1),'protected');return 'gamma1_protected_LX'
        assert {L[x] for x in J}==set(J)
        q=next(x for x in J if L[x]==L[2])
        if q!=j:
            x=next(x for x in outside if X[x]==2);y=next(x for x in outside if X[x]==q)
            merge(rows,(x,y),(1,0),'outside_K');return 'gamma1_outside_XL'
        closed_graph(rows,j);return 'gamma1_closed_four_cycle'
    assert gamma==4 and delta==1
    pre=next((x for x in T if L[x]==j),None)
    if pre is not None:merge(rows,(u,pre),(0,1),'protected');return 'gamma4_protected_LX'
    assert {L[x] for x in J}==T-{j}
    q=next(x for x in J if L[x]==L[2])
    if q!=j:
        x=next(x for x in J if L[x]==2);y=next(x for x in J if L[x]==q)
        merge(rows,(x,y),(0,0),'outside_K');return 'gamma4_outside_LL'
    outside_image={X[x] for x in outside};z=next(iter(T-outside_image))
    if z not in (2,j):
        x=next(x for x in outside if X[x]==2);y=next(x for x in outside if X[x]==j)
        merge(rows,(x,y),(1,0),'outside_K');return 'gamma4_outside_XL'
    if z==j:
        if X[2]!=j:assert j not in set(L)|set(X);return 'gamma4_missing_incoming_j'
        r=next(x for x in outside if X[x]==2);x=5 if r==4 else next(x for x in outside if X[x]==r)
        merge(rows,(r,x),(1,1,0),'outside_K');return 'gamma4_outside_XXL_zj'
    assert z==2 and outside_image==set(J)
    if X[2]==2:
        r=next(x for x in outside if X[x]==j)
        if r==4:merge(rows,(2,5),(1,1,0),'protected');return 'gamma4_protected_XXL_unique'
        x=next(x for x in J if L[x]==2);y=next(x for x in J if L[x]==r)
        merge(rows,(x,y),(0,1,0),'outside_K');return 'gamma4_outside_LXL_unique'
    r=next(x for x in outside if X[x]==X[2])
    if r!=4:
        x=next(x for x in J if L[x]==2);y=next(x for x in J if L[x]==r)
        merge(rows,(x,y),(0,1),'outside_K');return 'gamma4_outside_LX_extra'
    closed_graph(rows,j);return 'gamma4_closed_four_cycle'
def reason24(L,X,u,J):
    T={2}|set(J);gamma=X[5];delta=L[u];rows=(L,X)
    if gamma==delta:assert 5-gamma not in set(L)|set(X);return 'missing_C_target'
    if gamma==4:
        pre=next((x for x in (1,*J) if X[x]==2),None)
        if pre is not None:merge(rows,(5,pre),(1,1),'protected');return 'gamma4_protected_XX'
        assert {X[x] for x in J}==set(J)
        q=next(x for x in J if X[x]==X[1])
        pre=next((x for x in T if L[x]==q),None)
        if pre is not None:merge(rows,(u,pre),(0,1),'protected');return 'gamma4_protected_LX'
        assert {L[x] for x in J}==T-{q}
        r=next(x for x in J if L[x]==L[2])
        if r!=q:
            x=next(x for x in J if L[x]==2);y=next(x for x in J if L[x]==r)
            merge(rows,(x,y),(0,0),'outside_K');return 'gamma4_outside_LL'
        closed_graph(rows,q);return 'gamma4_closed_four_cycle'
    assert gamma==1 and delta==4
    pre=next((x for x in T if L[x]==2),None)
    if pre is not None:merge(rows,(u,pre),(0,1),'protected');return 'gamma1_protected_LX'
    assert {L[x] for x in J}==set(J)
    q=next(x for x in J if L[x]==L[2]);outside_image={X[x] for x in J};z=next(iter(T-outside_image))
    if z not in (2,q):
        x=next(x for x in J if X[x]==2);y=next(x for x in J if X[x]==q)
        merge(rows,(x,y),(1,0),'outside_K');return 'gamma1_outside_XL'
    if z==2:
        if X[1]!=2:assert 2 not in set(L)|set(X);return 'gamma1_missing_incoming2'
        r=next(x for x in J if X[x]==q);x=next(x for x in J if X[x]==r)
        merge(rows,(5,x),(1,1,0),'protected');return 'gamma1_protected_XXL_z2'
    assert z==q
    if X[1]==q:
        r=next(x for x in J if X[x]==2)
        if r!=q:
            x=next(x for x in J if X[x]==r);merge(rows,(5,x),(1,1,0),'protected');return 'gamma1_protected_XXL_unique'
        initial_count(L,X,q);return 'gamma1_initial_one_count_incompatible'
    r=next(x for x in J if X[x]==X[1])
    if r!=q:
        x=next(x for x in J if X[x]==r);merge(rows,(5,x),(1,1),'protected');return 'gamma1_protected_XX_extra'
    closed_graph(rows,q);return 'gamma1_closed_four_cycle'
def ordinary_maps(inputs,guard,targets):
    for outputs in permutations(targets):yield dict(zip(inputs,outputs))
    for q in inputs:
        if q==guard:continue
        blocks=[(guard,q)]+[(x,) for x in inputs if x not in (guard,q)]
        for outputs in permutations(targets,len(blocks)):yield {x:t for b,t in zip(blocks,outputs) for x in b}
def left_rows(n):
    J=tuple(range(7,n));T=(2,*J)
    for ordinary in ordinary_maps(T,2,T):
        for preA in (0,3):
            for u in sorted(P-{preA,6}):
                for preD,preE in permutations(sorted(P-{preA,u})):
                    for delta in (1,4):
                        L=[-1]*n;L[1]=L[4]=0;L[preA]=3;L[u]=delta;L[preD]=5;L[preE]=6
                        for x,t in ordinary.items():L[x]=t
                        assert all(t>=0 for t in L);yield L,u
def right_rows(n,F):
    J=tuple(range(7,n));T=(2,*J);guard=2 if F==[1,7] else 1
    inputs=(2,4,*range(8,n)) if F==[1,7] else (1,*J)
    for ordinary,swap,gamma in product(ordinary_maps(inputs,guard,T),(False,True),(1,4)):
        X=[-1]*n;X[0]=3 if swap else 0;X[3]=0 if swap else 3;X[5]=gamma;X[6]=5
        for x in F:X[x]=6
        for x,t in ordinary.items():X[x]=t
        assert all(t>=0 for t in X);yield X
def literal_controls(n,F):
    left=list(left_rows(n));right=list(right_rows(n,F));hist=Counter();J=tuple(range(7,n))
    for (L,u),X in product(left,right):
        reason=reason17(L,X,u,J,7) if F==[1,7] else reason24(L,X,u,J);hist[reason]+=1
    k=n-6;total=sum(hist.values());assert total==64*k*k*factorial(k)**2 and hist['missing_C_target']*2==total
    assert hist['gamma1_closed_four_cycle']>0 and hist['gamma4_closed_four_cycle']>0
    if F==[2,4]:assert hist['gamma1_initial_one_count_incompatible']>0
    return dict(n=n,F=F,complete_normalized_row_pairs=total,proof_cases=dict(sorted(hist.items())))
def full_ports(F):
    J=tuple(range(7,13));T=(2,*J);counts=Counter()
    for q in J:
        for gamma in (1,4):
            delta=5-gamma
            if F==[1,7]:
                l_targets=J if gamma==1 else tuple(x for x in T if x!=q)
                x_targets=tuple(x for x in T if x!=q) if gamma==1 else J
                Xinputs=(4,*[x for x in J if x!=q]);xguard=2;xpartner=4;Factual={1,q}
            else:
                l_targets=J if gamma==1 else tuple(x for x in T if x!=q)
                x_targets=tuple(x for x in T if x!=q) if gamma==1 else J
                Xinputs=J;xguard=1;xpartner=q;Factual={2,4}
            G={(1,4),(2,4),(1,q),(2,q)}
            for outputs in permutations(l_targets):
                for preA in (0,3):
                    for u in sorted(P-{preA,6}):
                        for preD,preE in permutations(sorted(P-{preA,u})):
                            L=[-1]*13;L[1]=L[4]=0;L[preA]=3;L[u]=delta;L[preD]=5;L[preE]=6
                            for x,t in zip(J,outputs):L[x]=t
                            L[2]=L[q]
                            ker={p for p in combinations(range(13),2) if L[p[0]]==L[p[1]]}
                            assert ker=={(1,4),(2,q)} and all(not set(edge)<=set(L) for edge in G)
                            counts[f'gamma{gamma}_L_letters']+=1
            for outputs in permutations(x_targets):
                for swap in (False,True):
                    X=[-1]*13;X[0]=3 if swap else 0;X[3]=0 if swap else 3;X[5]=gamma;X[6]=5
                    for x in Factual:X[x]=6
                    for x,t in zip(Xinputs,outputs):X[x]=t
                    X[xguard]=X[xpartner]
                    ker={p for p in combinations(range(13),2) if X[p[0]]==X[p[1]]}
                    required={(1,q),(2,4)}
                    assert ker==required and all(not set(edge)<=set(X) for edge in G)
                    counts[f'gamma{gamma}_X_letters']+=1
    assert counts==Counter(gamma1_L_letters=34560,gamma4_L_letters=34560,gamma1_X_letters=8640,gamma4_X_letters=8640)
    result=dict(F=F,all_hard_branch_full_letter_systems=dict(counts),full_letter_assignments=sum(counts.values()),
        all_six_ordinary_labels_checked=True)
    if F==[2,4]:
        total=0
        for q in J:
            for values in combinations(range(13),9):
                S=set(values)
                if not P<=S or len(S&C)!=1 or len(S&{2,4})!=1:continue
                total+=1;assert not (q in S and 1 in S and len(S&{2,q})<=1)
        assert total==210;result['initial_nine_set_controls']=total
    return result
def main():
    kernels=kernels_and_normalization();literal=[];ports=[]
    for F in ([1,7],[2,4]):
        for n in (8,9,10):
            z=literal_controls(n,F);literal.append(z);print(json.dumps(dict(n=n,F=F,pairs=z['complete_normalized_row_pairs'])),flush=True)
        ports.append(full_ports(F))
    inv=json.loads((ROOT/'b1_fifth_inventory.json').read_text(encoding='utf-8'))['records']
    kept=[z for z in inv if z['E']==[6] and z['F'] in ([7],[2,7])]
    assert len(kept)==2 and sum(z['labelled_F'] for z in kept)==12
    assert sum(len(p['fifth_field_pairs']) for z in kept for p in z['pairs'])==244
    assert len({tuple(p['original_third_rows']) for z in kept for p in z['pairs'] if p['fifth_field_pairs']})==14
    names=[Path(__file__).name,'enumerate_b1_e6_overlap_fifth.py','b1_e6_overlap_fifth_inventory.json',
        'PROOF.md#problem4-b1-e6-f17-exclusion','PROOF.md#problem4-b1-e6-f24-exclusion','b1_fifth_inventory.json','b1_fifth_audit.json',
        'PROOF.md#problem4-b1-fifth-entrance','PROOF.md#problem4-b1-partial-cover-fourth','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],alphabet='binary only',E=[6],excluded_F=[[1,7],[2,4]],
        kernel_controls=kernels,complete_literal_controls=literal,complete_n13_hard_branch_controls=ports,
        removed_fifth_field_pairs=24,remaining_binary_E6_fifth_geometry=[[7],[2,7]],remaining_labelled_F=12,
        remaining_field_pairs=244,all_original_third_pairs_retained=14,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete conditional binary overlap-fifth exclusions. Actual one-count and closed-cycle cases retained. No whole E6/third/joint exclusion, full n13 row-pair scan, F value or numerical alphabet separation.')
    (ROOT/'b1_e6_overlap_fifth_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',kernels=kernels,literal_pairs=[v['complete_normalized_row_pairs'] for v in literal],
        n13_full_letter_controls=[v['full_letter_assignments'] for v in ports],remaining_E6_pairs=244)),flush=True)
if __name__=='__main__':main()
