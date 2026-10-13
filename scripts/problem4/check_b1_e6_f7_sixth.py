"""Independent five binary sixth exclusions in E6/F7.

Kernel injections, complete individual G2 letters, and complete
normalized nonsingleton rows. Reuses an earlier independent literal
word auditor; imports no generator. New protected6/7 assignments,
actual preimages, capacities and word depths are checked separately.
"""
from itertools import combinations,product,permutations
from collections import Counter
from functools import lru_cache
from pathlib import Path
from math import factorial
import hashlib,json
from check_b1_e6_overlap_fifth import reason17,reason24
ROOT=Path(__file__).resolve().parent
Q=set(range(13));K={1,2};P={0,3,5,6,7};C={1,4};KEYS=('preA','preB','preC','preD','preE','preF')
def canonical(fields):return tuple(tuple(sorted(tuple(sorted(b)) for b in part)) for part in fields)
def edges(fields):return {e for part in fields for block in part for e in combinations(sorted(block),2)}
@lru_cache(None)
def partitions(X,cap,protected):
    choices=[[frozenset({q}) for q in sorted(set(X)-K)]];protected=set(protected)
    for q in sorted(set(X)&K):
        fresh=[]
        for blocks in choices:
            fresh.append([*blocks,frozenset({q})])
            for i,block in enumerate(blocks):
                if q in protected or block&protected:continue
                fresh.append([*blocks[:i],block|{q},*blocks[i+1:]])
        choices=fresh
    return {tuple(sorted(tuple(sorted(b)) for b in blocks)) for blocks in choices if len(blocks)<=cap}
def kernel_controls():
    inv=json.loads((ROOT/'b1_e6_f7_sixth_kernel_inventory.json').read_text(encoding='utf-8'))
    parents=json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))['records'];summary=[]
    for z in inv['profiles']:
        parent=next(v for v in parents if v['id']==z['id'])
        assert [(v['original_third_rows'],v['original_fourth_rows'],v['original_fifth_rows'],v['rows']) for v in z['pairs']]==[
            (v['original_third_rows'],v['original_fourth_rows'],v['original_fifth_rows'],xy) for v in parent['pairs'] for xy in v['sixth_field_pairs']]
        for j,row in enumerate(z['rows']):
            assert row['parent_row']==j and all(row[key]==parent['rows'][j][key] for key in KEYS)
            groups=[set(row[key]) for key in KEYS];groups.append(Q-set().union(*groups))
            expected={tuple(parts) for parts in product(*[partitions(tuple(sorted(X)),cap,tuple(z['protected']))
                for X,cap in zip(groups,[1,1,2,1,1,1,6])])}
            assert expected=={canonical(v['fields']) for v in row['patterns']} and len(expected)==len(row['patterns'])
            for pat in row['patterns']:assert edges(pat['fields'])=={tuple(e) for e in pat['kernel']}
        for pair in z['pairs']:
            x,y=pair['rows'];assert pair['kernel_pairs']==[list(ij) for ij in product(range(len(z['rows'][x]['patterns'])),range(len(z['rows'][y]['patterns'])))]
            if z['G']==[2]:continue
            fields=[z['rows'][x],z['rows'][y]];X=[v for v in fields if v['preF']==z['G']];L=[v for v in fields if v['preB']==[1,4]]
            assert len(X)==len(L)==1 and X[0]!=L[0];X=X[0];L=L[0]
            assert sorted([X['preA'],X['preB']])==[[0],[3]]
            assert X['preC']==[5] and X['preD']==[6] and X['preE']==[7]
            assert L['preA'] in ([0],[3]) and L['preC'] in ([0],[3],[5])
            singleton=[L[key] for key in ('preA','preC','preD','preE','preF')]
            assert all(len(t)==1 for t in singleton) and {t[0] for t in singleton}==P
        summary.append(dict(G=z['G'],original_field_pairs=len(z['pairs']),row_patterns=sum(len(r['patterns']) for r in z['rows']),
            compatible_kernel_pairs=sum(len(p['kernel_pairs']) for p in z['pairs'])))
    assert [v['original_field_pairs'] for v in summary]==[365,24,24,24,24]
    assert [v['row_patterns'] for v in summary]==[90,242,252,252,242]
    assert [v['compatible_kernel_pairs'] for v in summary]==[686,144,864,864,144]
    for name,digest in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    return inv,summary
def independent_G2_letters(row):
    U=P|{2};groups=[set(row[key]) for key in KEYS];groups.append(Q-set().union(*groups))
    targets=({3},{0},{1,4},{5},{6},{7},{2,8,9,10,11,12})
    for kernel in [None]+[(1,q) for q in sorted(Q-U-{1})]:
        if kernel and not any(set(kernel)<=X for X in groups):continue
        options=[];possible=True
        for X,Y in zip(groups,targets):
            blocks=[(q,) for q in sorted(X) if not kernel or q not in kernel]
            if kernel and set(kernel)<=X:blocks.append(kernel)
            blocks.sort()
            if len(blocks)>len(Y):possible=False;break
            options.append([(blocks,out) for out in permutations(sorted(Y),len(blocks))])
        if not possible:continue
        for parts in product(*options):
            word=[-1]*13
            for blocks,outputs in parts:
                for block,t in zip(blocks,outputs):
                    for q in block:word[q]=t
            assert all(t>=0 for t in word);yield word,kernel
def G2_controls(inv):
    z=next(v for v in inv['profiles'] if v['G']==[2]);counts=Counter();total=0;nonempty=0
    for i,row in enumerate(z['rows']):
        actual=dict(full_letters=0,permutations=0,C_kernel=0,external_kernel=0);aggregate=0
        for word,kernel in independent_G2_letters(row):
            actual['full_letters']+=1;actual['permutations']+=kernel is None;actual['C_kernel']+=kernel==(1,4)
            actual['external_kernel']+=kernel is not None and kernel!=(1,4)
            aggregate=(aggregate+int.from_bytes(hashlib.sha256(bytes(word)).digest(),'big'))%(1<<256)
            ker={e for e in combinations(range(13),2) if word[e[0]]==word[e[1]]}
            assert ker==(set() if kernel is None else {kernel})
            assert len({word[q] for q in Q-{1}})==12 and len(set(word))>=12
            preC={q for q in Q if word[q] in C};assert preC in ({3},{0},C,{5})
            invG={e for e in combinations(range(13),2) if set((word[e[0]],word[e[1]]))==C};assert invG<={(1,4)}
            if set(row['preB'])==C:
                assert kernel==(1,4) and len(preC)==1;counts['C_merger_role']+=1
            if kernel is not None and kernel!=(1,4):
                assert len(preC)==1 and kernel[1] in range(8,13);counts['external_kernel_role']+=1
            if len(preC)==1:
                u=next(iter(preC));assert u in {0,3,5}
                if word[u]==1:
                    assert 4 not in word
                    for q in range(8,13):
                        assert q in word;x=next(x for x,t in enumerate(word) if t==q)
                        assert x!=u and {word[u],word[x]}=={1,q}
                        merger=list(range(13));merger[1]=q
                        assert merger[word[u]]==merger[word[x]];counts['protected_two_step_witnesses']+=1
        reconstructed=dict(row=i,**actual,unordered_row_hash_sum=f'{aggregate:064x}')
        assert reconstructed==z['G2_individual_letter_controls'][i];total+=actual['full_letters'];nonempty+=actual['full_letters']>0
    assert total==129600 and counts['C_merger_role']>0 and counts['external_kernel_role']>0
    return dict(complete_individual_letters=total,all_known_preimage_rows=len(z['rows']),rows_with_actual_letters=nonempty,
        role_and_word_controls=dict(counts),correct_singleton2_isolation_depth=1,
        uses_singleton_P2_cover=False,scope='Every individual n13 letter, no coupled transition-pair enumeration. Binary role and protected two-step contradiction are symbolic.')
def ordinary_maps(inputs,guard,targets):
    for out in permutations(targets):yield dict(zip(inputs,out)),None
    for q in inputs:
        if q==guard:continue
        blocks=[(guard,q)]+[(x,) for x in inputs if x not in (guard,q)]
        for out in permutations(targets,len(blocks)):yield {x:t for block,t in zip(blocks,out) for x in block},q
def left_rows(n):
    T=(2,*range(8,n))
    for ordinary,q in ordinary_maps(T,2,T):
        for preA in (0,3):
            for u in sorted(P-{preA,6,7}):
                for preD,preE,preF in permutations(sorted(P-{preA,u})):
                    for delta in (1,4):
                        L=[-1]*n;L[1]=L[4]=0;L[preA]=3;L[u]=delta;L[preD]=5;L[preE]=6;L[preF]=7
                        for x,t in ordinary.items():L[x]=t
                        assert all(t>=0 for t in L);yield L,u,q
def right_rows(n,G):
    J=tuple(range(8,n));T=(2,*J);I=tuple(sorted(set(range(n))-P-set(G)))
    if G in ([1,2],[1,2,8]):systems=((dict(zip(I,out)),None) for out in permutations(T,len(I)))
    else:systems=ordinary_maps(I,2 if G==[1,8] else 1,T)
    for (ordinary,q),swap,gamma in product(systems,(False,True),(1,4)):
        X=[-1]*n;X[0]=3 if swap else 0;X[3]=0 if swap else 3;X[5]=gamma;X[6]=5;X[7]=6
        for x in G:X[x]=7
        for x,t in ordinary.items():X[x]=t
        assert all(t>=0 for t in X);yield X
def merge(rows,pair,word,kind):
    assert pair[0]!=pair[1] and len(word)==2
    if kind=='protected':assert set(pair)&{0,3,5}
    else:assert kind=='outside_K' and not set(pair)&K
    image=set(pair)
    for ell in word:image={rows[ell][q] for q in image}
    assert len(image)==1
def short_reason(L,X,u,q,G,J):
    gamma=X[5];delta=L[u];rows=(L,X);I=tuple(sorted(set(range(len(X)))-P-set(G)))
    if gamma==delta:assert 5-gamma not in set(L)|set(X);return 'missing_C_target'
    if gamma==1:
        t=next(t for t in G if t!=1 and t in {X[x] for x in I});x=next(x for x in I if X[x]==t)
        merge(rows,(5,x),(1,1),'protected');return 'protected_XX'
    assert gamma==4 and delta==1
    if len(G)==3:
        t=next(t for t in (2,8) if t in {L[x] for x in (2,*J)});x=next(x for x in (2,*J) if L[x]==t)
        merge(rows,(u,x),(0,1),'protected');return 'protected_LX_G128'
    if 2 in {L[x] for x in (2,*J)}:
        x=next(x for x in (2,*J) if L[x]==2);merge(rows,(u,x),(0,1),'protected');return 'protected_LX_G12'
    assert q is not None and L[2]==L[q]
    x=next(x for x in I if X[x]==2);y=next(x for x in I if X[x]==q)
    merge(rows,(x,y),(1,0),'outside_K');return 'outside_XL_extra_kernel'
def literal_controls(n,G):
    left=list(left_rows(n));right=list(right_rows(n,G));hist=Counter();J=tuple(range(8,n))
    for (L,u,q),X in product(left,right):
        if G==[1,8]:reason=reason17(L,X,u,J,8)
        elif G==[2,4]:reason=reason24(L,X,u,J)
        else:reason=short_reason(L,X,u,q,G,J)
        hist[reason]+=1
    k=n-7;total=sum(hist.values());expected=192*k*factorial(k)**2
    if G in ([1,8],[2,4]):expected*=k;assert hist['gamma1_closed_four_cycle']>0 and hist['gamma4_closed_four_cycle']>0
    if G==[2,4]:assert hist['gamma1_initial_one_count_incompatible']>0
    assert total==expected and hist['missing_C_target']*2==total
    return dict(n=n,G=G,complete_normalized_row_pairs=total,proof_cases=dict(sorted(hist.items())))
def short_ports():
    T=(2,*range(8,13));counts=Counter()
    for out in permutations(T):
        inverse=dict(zip(out,(4,*range(8,13))));assert set(inverse)==set(T) and not set(inverse.values())&K;counts['G12_X_systems']+=1
    for out in permutations(T,5):
        inverse=dict(zip(out,(4,*range(9,13))));assert len(inverse)==5 and any(t in inverse for t in (2,8));counts['G128_X_systems']+=1
    for ordinary,q in ordinary_maps(T,2,T):
        assert len(set(ordinary.values()))>=5 and any(t in ordinary.values() for t in (2,8));counts['ordinary_L_systems']+=1
        if 2 not in ordinary.values():assert q is not None and ordinary[2]==ordinary[q];counts['L_systems_omitting2']+=1
    assert counts==Counter(G12_X_systems=720,G128_X_systems=720,ordinary_L_systems=4320,L_systems_omitting2=600)
    return dict(counts)
def overlap_ports(G):
    J=tuple(range(8,13));T=(2,*J);counts=Counter()
    for q in J:
        graph={(1,4),(2,4),(1,q),(2,q)}
        for gamma in (1,4):
            l_targets=J if gamma==1 else tuple(x for x in T if x!=q)
            x_targets=tuple(x for x in T if x!=q) if gamma==1 else J
            for out in permutations(l_targets):
                for preA in (0,3):
                    for u in sorted(P-{preA,6,7}):
                        for preD,preE,preF in permutations(sorted(P-{preA,u})):
                            L=[-1]*13;L[1]=L[4]=0;L[preA]=3;L[u]=5-gamma;L[preD]=5;L[preE]=6;L[preF]=7
                            for x,t in zip(J,out):L[x]=t
                            L[2]=L[q]
                            ker={e for e in combinations(range(13),2) if L[e[0]]==L[e[1]]}
                            assert ker=={(1,4),(2,q)} and all(not set(e)<=set(L) for e in graph);counts[f'gamma{gamma}_L_letters']+=1
            if G==[1,8]:Gactual={1,q};I=(4,*[x for x in J if x!=q]);guard=2;partner=4
            else:Gactual={2,4};I=J;guard=1;partner=q
            for out in permutations(x_targets):
                for swap in (False,True):
                    X=[-1]*13;X[0]=3 if swap else 0;X[3]=0 if swap else 3;X[5]=gamma;X[6]=5;X[7]=6
                    for x in Gactual:X[x]=7
                    for x,t in zip(I,out):X[x]=t
                    X[guard]=X[partner]
                    ker={e for e in combinations(range(13),2) if X[e[0]]==X[e[1]]}
                    assert ker=={(1,q),(2,4)} and all(not set(e)<=set(X) for e in graph);counts[f'gamma{gamma}_X_letters']+=1
    assert counts==Counter(gamma1_L_letters=14400,gamma4_L_letters=14400,gamma1_X_letters=1200,gamma4_X_letters=1200)
    result=dict(G=G,all_hard_branch_full_letter_systems=dict(counts),full_letter_assignments=sum(counts.values()),all_five_ordinary_labels_checked=True)
    if G==[2,4]:
        initial=0
        for q in J:
            for values in combinations(range(13),9):
                S=set(values)
                if not P<=S or len(S&C)!=1 or len(S&{2,4})!=1:continue
                initial+=1;assert not (1 in S and q in S and len(S&{2,q})<=1)
        assert initial==100;result['initial_nine_set_controls']=initial
    return result
def main():
    inv,kernels=kernel_controls();single=G2_controls(inv);literal=[]
    for G in ([1,2],[1,8],[2,4],[1,2,8]):
        for n in (9,10,11):
            z=literal_controls(n,G);literal.append(z);print(json.dumps(dict(n=n,G=G,pairs=z['complete_normalized_row_pairs'])),flush=True)
    ports=short_ports();overlaps=[overlap_ports(G) for G in ([1,8],[2,4])]
    parent=json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))['records']
    kept=[z for z in parent if z['E']==[6] and z['F']==[7] and z['G'] in ([8],[2,8])]
    assert len(kept)==2 and sum(z['labelled_G'] for z in kept)==10
    assert sum(len(p['sixth_field_pairs']) for z in kept for p in z['pairs'])==730
    assert len({tuple(p['original_fifth_rows']) for z in kept for p in z['pairs'] if p['sixth_field_pairs']})==122
    names=[Path(__file__).name,'enumerate_b1_e6_f7_sixth.py','b1_e6_f7_sixth_kernel_inventory.json',
        'PROOF.md#problem4-b1-e6-f7-g2-exclusion','PROOF.md#problem4-b1-e6-f7-paired-sixth-exclusions','check_b1_e6_overlap_fifth.py',
        'b1_sixth_inventory.json','b1_sixth_audit.json','PROOF.md#problem4-b1-sixth-entrance','PROOF.md#problem4-b1-fifth-entrance',
        'PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],alphabet='binary only',E=[6],F=[7],excluded_G=[[2],[1,2],[1,8],[2,4],[1,2,8]],
        kernel_controls=kernels,complete_G2_individual_letter_controls=single,complete_literal_controls=literal,
        complete_n13_short_ports=ports,complete_n13_overlap_hard_ports=overlaps,removed_sixth_field_pairs=461,
        remaining_G=[[8],[2,8]],remaining_geometric_orbits=2,remaining_labelled_G=10,remaining_field_pairs=730,
        all_original_fifth_pairs_retained=122,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Five complete conditional binary sixth exclusions. Correct P1-only singleton2 depth, all protected6/7 inputs retained. No whole fifth/third/joint exclusion, full n13 row-pair scan, unrestricted exclusion, F value or numerical alphabet separation.')
    (ROOT/'b1_e6_f7_sixth_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',kernels=kernels,G2_letter_controls=single,short_ports=ports,
        overlap_full_letters=[z['full_letter_assignments'] for z in overlaps],remaining_pairs=730)),flush=True)
if __name__=='__main__':main()
