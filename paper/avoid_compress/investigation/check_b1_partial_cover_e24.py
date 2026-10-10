"""Independent full normalized rows and closed-graph E24 word proof.

No generator is imported. Common independent partition utilities are
reused; the actual row enumeration and every proof witness are separate.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations,permutations,product
from math import factorial
import hashlib,json
from check_b1_partial_cover_fourth import independent_partitions,canonical,kernel
ROOT=Path(__file__).resolve().parent
K={1,2};PROTECTED={0,3,5};C={1,4};E={2,4}

def kernel_controls():
    data=json.loads((ROOT/'b1_partial_cover_e24_inventory.json').read_text(encoding='utf-8'))
    old=next(v for v in json.loads((ROOT/'b1_partial_cover_fourth_inventory.json').read_text(encoding='utf-8'))['records'] if v['E']==[2,4])
    assert [(p['original_third_rows'],p['rows']) for p in data['pairs']]==[(p['original_rows'],xy) for p in old['pairs'] for xy in p['fourth_field_pairs']]
    for row in data['rows']:
        inputs=[set(row[key]) for key in ('preA','preB','preC','preD')]
        inputs.append(set(range(13))-set().union(*inputs))
        expected={tuple(parts) for parts in product(*[independent_partitions(tuple(sorted(X)),cap,tuple(sorted(PROTECTED)))
            for X,cap in zip(inputs,[1,1,2,1,8])])}
        assert expected=={canonical(v['fields']) for v in row['patterns']} and len(expected)==len(row['patterns'])
        for pat in row['patterns']:assert kernel(pat['fields'])=={tuple(p) for p in pat['kernel']}
    for pair in data['pairs']:
        x,y=pair['rows'];assert pair['kernel_pairs']==[list(ij) for ij in product(range(len(data['rows'][x]['patterns'])),range(len(data['rows'][y]['patterns'])))]
    result=dict(original_field_pairs=len(data['pairs']),row_patterns=sum(len(r['patterns']) for r in data['rows']),
        compatible_kernel_pairs=sum(len(p['kernel_pairs']) for p in data['pairs']))
    assert result==dict(original_field_pairs=6,row_patterns=96,compatible_kernel_pairs=384)
    return result

def merge(rows,pair,word,kind):
    assert len(set(pair))==2 and len(word)<=3
    if kind=='protected':assert set(pair)&PROTECTED
    else:assert kind=='outside' and not set(pair)&K
    image=set(pair)
    for letter in word:image={rows[letter][q] for q in image}
    assert len(image)==1,(rows,pair,word)

def closed_graph(rows,q):
    G={(1,4),(2,4),tuple(sorted((1,q))),tuple(sorted((2,q)))}
    assert len(G)==4
    immediate={}
    for row in rows:
        im={row[x] for x in range(len(row))}
        assert all(not {x,y}<=im for x,y in G)
        immediate[tuple(row)]={p for p in combinations(range(len(row)),2) if row[p[0]]==row[p[1]]}
        assert immediate[tuple(row)]<=G
        # Direct literal inverse check, independent of the image argument.
        for pair in combinations(range(len(row)),2):
            out=tuple(sorted((row[pair[0]],row[pair[1]])))
            assert out not in G
    assert set().union(*immediate.values())==G

def initial_count_control(L,F,q):
    pre={x for x in range(len(F)) if F[x] in E}
    pre2={x for x in range(len(F)) if F[F[x]] in E}
    assert pre=={q} and pre2=={1} and L[2]==L[q]
    feasible=0
    for values in product((0,1),repeat=4):
        x1,x2,x4,xq=values
        if x1+x4==x2+x4==1 and xq==x1==1 and x2+xq<=1:feasible+=1
    assert feasible==0

def reason(L,F,u,J):
    delta=L[u];gamma=F[5];T={2}|set(J);rows=(L,F)
    if delta==gamma:
        absent=next(x for x in C if x!=delta)
        assert absent not in set(L)|set(F);return 'missing_C_target'
    if gamma==4:
        pre2=next((x for x in (1,*J) if F[x]==2),None)
        if pre2 is not None:
            merge(rows,(5,pre2),(1,1),'protected');return 'gamma4_protected_FF'
        assert {F[x] for x in J}==set(J)
        q=next(x for x in J if F[x]==F[1])
        assert delta==1
        preq=next((x for x in T if L[x]==q),None)
        if preq is not None:
            merge(rows,(u,preq),(0,1),'protected');return 'gamma4_protected_LF'
        assert {L[x] for x in J}==T-{q}
        r=next(x for x in J if L[x]==L[2])
        if r!=q:
            x=next(x for x in J if L[x]==2);y=next(x for x in J if L[x]==r)
            merge(rows,(x,y),(0,0),'outside');return 'gamma4_outside_LL'
        closed_graph(rows,q);return 'gamma4_closed_four_cycle'
    assert gamma==1 and delta==4
    pre2=next((x for x in T if L[x]==2),None)
    if pre2 is not None:
        merge(rows,(u,pre2),(0,1),'protected');return 'gamma1_protected_LF'
    assert {L[x] for x in J}==set(J)
    q=next(x for x in J if L[x]==L[2])
    outside_image={F[x] for x in J};assert len(outside_image)==len(J)
    z=next(iter(T-outside_image))
    if z not in (2,q):
        x=next(x for x in J if F[x]==2);y=next(x for x in J if F[x]==q)
        merge(rows,(x,y),(1,0),'outside');return 'gamma1_outside_FL'
    if z==2:
        if F[1]!=2:
            assert 2 not in set(L)|set(F);return 'gamma1_missing_incoming2'
        r=next(x for x in J if F[x]==q);x=next(x for x in J if F[x]==r)
        merge(rows,(5,x),(1,1,0),'protected');return 'gamma1_protected_FFL_z2'
    assert z==q
    if F[1]==q:
        r=next(x for x in J if F[x]==2)
        if r!=q:
            x=next(x for x in J if F[x]==r)
            merge(rows,(5,x),(1,1,0),'protected');return 'gamma1_protected_FFL_unique'
        initial_count_control(L,F,q);return 'gamma1_initial_one_count_incompatible'
    r=next(x for x in J if F[x]==F[1])
    if r!=q:
        x=next(x for x in J if F[x]==r)
        merge(rows,(5,x),(1,1),'protected');return 'gamma1_protected_FF_extra'
    closed_graph(rows,q);return 'gamma1_closed_four_cycle'

def ordinary_maps(inputs,guard,targets):
    for outputs in permutations(targets):yield dict(zip(inputs,outputs))
    for q in inputs:
        if q==guard:continue
        blocks=[(guard,q)]+[(x,) for x in inputs if x not in (guard,q)]
        for outputs in permutations(targets,len(blocks)):
            yield {x:t for block,t in zip(blocks,outputs) for x in block}

def rows(n):
    J=tuple(range(6,n));T=(2,*J);I=(1,*J)
    left=[];right=[]
    for ordinary,p,swap,delta in product(ordinary_maps(T,2,T),(0,3),(False,True),(1,4)):
        L=[-1]*n;L[1]=L[4]=0;L[3 if p==0 else 0]=3;u=5 if swap else p;v=p if swap else 5
        L[u]=delta;L[v]=5
        for x,t in ordinary.items():L[x]=t
        assert all(x>=0 for x in L);left.append((L,u))
    for ordinary,swap,gamma in product(ordinary_maps(I,1,T),(False,True),(1,4)):
        F=[-1]*n;F[0]=3 if swap else 0;F[3]=0 if swap else 3;F[2]=F[4]=5;F[5]=gamma
        for x,t in ordinary.items():F[x]=t
        assert all(x>=0 for x in F);right.append(F)
    return left,right,J

def literal_controls(n):
    left,right,J=rows(n);hist=Counter()
    for (L,u),F in product(left,right):hist[reason(L,F,u,J)]+=1
    total=sum(hist.values());k=n-5
    assert total==32*k*k*factorial(k)**2
    assert hist['missing_C_target']*2==total
    assert hist['gamma1_closed_four_cycle']>0 and hist['gamma4_closed_four_cycle']>0
    assert hist['gamma1_initial_one_count_incompatible']>0
    return dict(n=n,complete_normalized_row_pairs=total,proof_cases=dict(sorted(hist.items())),
        scope='Complete over-approximate local templates, including harmless SC-impossible protected variants; no smaller-n equality claim.')

def literal_kernel(row):
    groups={}
    for q,t in enumerate(row):groups.setdefault(t,[]).append(q)
    return {p for group in groups.values() for p in combinations(group,2)}

def ports():
    J=tuple(range(6,13));T=(2,*J);totals=Counter()
    for q in J:
        G={(1,4),(2,4),tuple(sorted((1,q))),tuple(sorted((2,q)))}
        for gamma in (1,4):
            delta=next(x for x in C if x!=gamma)
            l_targets=J if gamma==1 else tuple(x for x in T if x!=q)
            f_targets=tuple(x for x in T if x!=q) if gamma==1 else J
            for outputs in permutations(l_targets):
                for p,swap in product((0,3),(False,True)):
                    L=[-1]*13;L[1]=L[4]=0;L[3 if p==0 else 0]=3;u=5 if swap else p;v=p if swap else 5
                    L[u]=delta;L[v]=5
                    for x,t in zip(J,outputs):L[x]=t
                    L[2]=L[q]
                    assert literal_kernel(L)=={(1,4),tuple(sorted((2,q)))}
                    image=set(L);assert all(not set(edge)<=image for edge in G)
                    totals[f'gamma{gamma}_L_letters']+=1
            for outputs in permutations(f_targets):
                for swap in (False,True):
                    F=[-1]*13;F[0]=3 if swap else 0;F[3]=0 if swap else 3;F[2]=F[4]=5;F[5]=gamma
                    for x,t in zip(J,outputs):F[x]=t
                    F[1]=F[q]
                    assert literal_kernel(F)=={(2,4),tuple(sorted((1,q)))}
                    image=set(F);assert all(not set(edge)<=image for edge in G)
                    totals[f'gamma{gamma}_F_letters']+=1
    assert totals==Counter(gamma1_L_letters=141120,gamma4_L_letters=141120,
        gamma1_F_letters=70560,gamma4_F_letters=70560)
    initial_sets=0
    for q in J:
        for S in combinations(range(13),9):
            X=set(S)
            if not PROTECTED<=X or len(X&C)!=1 or len(X&E)!=1:continue
            initial_sets+=1
            assert not (q in X and 1 in X and len({2,q}&X)<=1)
    assert initial_sets==392
    return dict(all_hard_branch_full_letter_systems=dict(totals),full_letter_assignments=sum(totals.values()),
        all_seven_extra_kernel_labels_checked=True,initial_nine_set_controls=initial_sets,
        scope='Every individual full n13 hard-branch letter, including all ordinary permutations; graph proof covers arbitrary coupled letters, not n13 row-pair enumeration.')

def main():
    kernels=kernel_controls();literal=[]
    for n in (7,8,9):
        z=literal_controls(n);literal.append(z);print(json.dumps(dict(n=n,pairs=z['complete_normalized_row_pairs'])),flush=True)
    port_controls=ports()
    names=[Path(__file__).name,'enumerate_b1_partial_cover_e24.py','b1_partial_cover_e24_inventory.json',
        'B1_PARTIAL_COVER_E24_EXCLUSION.md','B1_PARTIAL_COVER_FOURTH.md',
        'b1_partial_cover_fourth_inventory.json','check_b1_partial_cover_fourth.py',
        'ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md',
        'LOCAL_EQUALITY_FLAG.md','CODIMENSION_FOUR_P5_DICHOTOMY.md']
    result=dict(status='pass',parameter=[13,9,1],binary_only=True,E=[2,4],kernel_controls=kernels,
        complete_literal_controls=literal,complete_n13_hard_branch_controls=port_controls,
        removed_fourth_field_pairs=6,remaining_binary_fourth_geometries=3,
        remaining_binary_labelled_E_choices=21,remaining_binary_fourth_field_pairs=88,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete conditional binary E24 exclusion via short protected/outside witnesses, an actual one-count obstruction and a backward-closed four-cycle. No whole third/joint exclusion, F value or numerical alphabet separation.')
    (ROOT/'b1_partial_cover_e24_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',kernel_controls=kernels,literal_pairs=[z['complete_normalized_row_pairs'] for z in literal],
        n13_full_letter_controls=port_controls['full_letter_assignments'],remaining_fourth_pairs=88)),flush=True)

if __name__=='__main__':main()
