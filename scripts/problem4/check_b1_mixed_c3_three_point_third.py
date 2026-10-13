"""Complete split kernels, universal graphs/count forms and small row controls.

The n=13 theorem is symbolic. No full thirteen-state transition-table
scan or extrapolation from the small controls is asserted.
"""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import hashlib,json
from alphabet_check import pair_distances,strong
ROOT=Path(__file__).resolve().parent
H={0,1,2};C={0,1,5};D={0,2,6};V={1,5};CT={tuple(p) for p in combinations(sorted(C),2)}

def partitions(values):
    work=[()]
    for q in values:
        after=[]
        for blocks in work:
            after.append(blocks+((q,),))
            for j in range(len(blocks)):
                after.append(blocks[:j]+(blocks[j]+(q,),)+blocks[j+1:])
        work=after
    return work

def pairs(blocks):return {tuple(p) for block in blocks for p in combinations(block,2)}

def cores():
    answer=[];maps=set()
    for values in product(sorted(C),repeat=3):
        g=dict(zip(sorted(D),values));K={p for p in combinations(sorted(D),2) if g[p[0]]==g[p[1]]}
        if len(CT|K)>4:continue
        for delta in sorted(C):
            if {delta}|set(values)==C:
                answer.append((delta,g,frozenset(K)));maps.add(values)
    assert len(maps)==24 and len(answer)==36
    return answer

def split_patterns(RR,J,KD):
    L=[v for v in partitions(sorted(RR)) if len(CT|pairs(v))<=4 and all(set(p)&H for p in pairs(v))]
    F=[v for v in partitions(sorted(V|J)) if len(CT|set(KD)|pairs(v))<=4 and all(set(p)&H for p in pairs(v))]
    return [(lb,fb) for lb in L for fb in F if len(CT|set(KD)|pairs(lb)|pairs(fb))<=4]

def kernel_audit():
    RR={2}|set(range(6,13));J=set(range(7,13))
    rawL=partitions(sorted(RR));rawF=partitions(sorted(V|J));rawD=partitions(sorted(D))
    assert (len(rawL),len(rawF),len(rawD))==(4140,4140,5)
    reports=[];lset=set();fset=set()
    for KD in (frozenset(),frozenset({(0,2)}),frozenset({(0,6)}),frozenset({(2,6)})):
        patterns=split_patterns(RR,J,KD)
        assert len(patterns)==(22 if not KD else 4 if KD==frozenset({(2,6)}) else 2)
        lset.update(lb for lb,fb in patterns);fset.update(fb for lb,fb in patterns)
        reports.append(dict(D_kernel=[list(v) for v in sorted(KD)],split_patterns=len(patterns)))
    assert len(lset)==len(fset)==8 and sum(v['split_patterns'] for v in reports)==30
    hist=Counter()
    for name,blocks_set in (('L',lset),('F',fset)):
        for blocks in sorted(blocks_set):
            off={j for j,block in enumerate(blocks) if set(block)-H}
            assert (len(blocks),len(off)) in ((8,7),(7,7))
            for values in permutations(sorted(RR),len(blocks)):
                inverse={v:blocks[j] for j,v in enumerate(values)}
                assert any(v in inverse and set(inverse[v])-H for v in (2,6))
                bad=all(v in inverse and set(inverse[v])-H for v in (2,6))
                hist[name+('_outside_D_pullback' if bad else '_D_cover_admitted')]+=1
    assert sum(hist.values())==645120
    retained=[(delta,g,K) for delta,g,K in cores() if delta in V and g[6] in V and g[2]==0]
    assert len(retained)==8
    return dict(L_abstract_kernels=4140,F_R_abstract_kernels=4140,F_D_abstract_kernels=5,
        F_D_core_maps=24,delta_F_core_maps=36,split_kernel_patterns=30,split_reports=reports,
        L_complete_output_assignments=322560,F_complete_output_assignments=322560,
        output_histogram=dict(sorted(hist.items())),surviving_eight_cores=len(retained))

def protected(L,F,delta,mode):
    if mode==0:L[3]=3;L[4]=delta;F[3]=4;F[4]=3
    elif mode==1:L[3]=delta;L[4]=3;F[3]=3;F[4]=4
    else:L[3]=delta;L[4]=3;F[3]=4;F[4]=3

def star(v,T):return {tuple(sorted((v,t))) for t in T if v!=t}

def graph(kind,n=13):
    J=set(range(7,n));W={5,6}|J
    if kind=='join':return {tuple(p) for p in combinations(sorted(H),2)}|set().union(*(star(v,W) for v in H))
    G=CT|{tuple(p) for p in combinations(sorted(D),2)}|star(2,{6}|J)
    if kind=='singular_15':G|=star(2,V)
    else:assert kind=='bijective_15'
    return G

def universal_graph(kind,delta,g,KD,mode,q=None):
    Q=set(range(13));RR={2}|set(range(6,13));J=set(range(7,13));G=graph(kind)
    lp=[-1]*13;fp=[-1]*13;protected(lp,fp,delta,mode)
    L={v:{lp[v]} for v in (3,4)};F={v:{fp[v]} for v in (3,4)}
    L.update({v:{4} for v in C});F.update({v:{target} for v,target in g.items()})
    if kind=='bijective_15':
        L[2]={2};L.update({v:RR-{2} for v in RR-{2}});LK=CT
    else:L.update({v:RR-{2} for v in RR});LK=CT|{(2,q)}
    if kind=='join':
        F[1]={2};F[5]=RR-{2};F.update({v:RR-{2} for v in J});FK=set(KD)
    else:
        F.update({v:(set(J) if kind=='bijective_15' else RR-{2}) for v in V})
        F.update({v:RR-{2} for v in J});FK=set(KD)|{(1,5)}
    assert set(L)==set(F)==Q and LK|FK<=G and (3,4) not in G
    count=0
    for row in (L,F):
        for a,b in combinations(sorted(Q),2):
            if (a,b) not in G:
                assert not any(tuple(sorted((c,d))) in G for c in row[a] for d in row[b] if c!=d),(kind,a,b)
            count+=1
    return count

def graph_audit():
    hist=Counter();checks=0
    for delta,g,KD in cores():
        if delta not in V or g[6] not in V or g[2]!=0:continue
        for mode in range(3):
            if g[0] in V:
                checks+=universal_graph('bijective_15',delta,g,KD,mode);hist['bijective_15']+=1
            if not KD:
                for q in range(6,13):
                    checks+=universal_graph('singular_15',delta,g,KD,mode,q);hist['singular_15']+=1
                    if delta==g[6]==5:
                        checks+=universal_graph('join',delta,g,KD,mode,q);hist['join']+=1
    assert sum(hist.values())==123
    return dict(complete_graph_configurations=123,set_valued_backward_checks=checks,histogram=dict(sorted(hist.items())))

def feasible_sets(n):
    Q=set(range(n));s=n-4
    result=[Q-set(omit) for omit in combinations(sorted(Q-{3,4}),4)
        if len((Q-set(omit))&C)==len((Q-set(omit))&D)==1]
    assert all(len(T)==s for T in result) and len(result)==1+4*(n-7)
    return result

def good(T,s):return len(T)==s and {3,4}<=T and len(T&C)==len(T&D)==1

def F_count_failure(F,T,depth=5):
    s=len(T)
    for i in range(depth+1):
        if not good(T,s):return i
        T={F[v] for v in T}
    return None

def any_prefix_failure(L,F,T,depth=5):
    s=len(T);todo=[(T,0)];seen={frozenset(T)}
    for current,d in todo:
        if not good(current,s):return True
        if d==depth:continue
        for row in (L,F):
            image={row[v] for v in current};key=frozenset(image)
            if key not in seen:seen.add(key);todo.append((image,d+1))
    return False

def count_audit():
    RR={2}|set(range(6,13));J=set(range(7,13));sets=feasible_sets(13)
    rows=subsets=zero_rows=0;hist=Counter()
    for values in permutations(sorted({6}|J)):
        mapping=dict(zip([5]+sorted(J),values));r=mapping[5]
        for alpha in ((0,1,5) if r in J else (5,)):
            F=list(range(13));F[0]=alpha;F[1]=2;F[2]=0;F[6]=1
            for v,target in mapping.items():F[v]=target
            for T in sets:
                failure=F_count_failure(F,T,5);assert failure is not None
                if r==6:
                    image=T.copy();total=0
                    for i in range(5):total+=len(image&D);image={F[v] for v in image}
                    assert total in (3,6)
                hist['first_failure_'+str(failure)]+=1;subsets+=1
            rows+=1
        if r in J:
            # Separate zero-reachability obstruction for the 15 F kernel.
            for gamma in V:
                F=list(range(13));F[0]=F[2]=0;F[6]=gamma;F[1]=r
                for v,target in mapping.items():F[v]=target
                T0={3,4,0}|J;image={F[v] for v in T0}
                assert len(image)==9 and image&D=={0,6};zero_rows+=1
    assert (rows,subsets,zero_rows)==(13680,342000,8640)
    return dict(parameterized_F_count_rows=rows,complete_nine_set_controls=subsets,
        five_cycle_rows=720,zero_reachability_F_rows=zero_rows,count_failure_histogram=dict(sorted(hist.items())),
        scope='All ordinary permutations in the parameterized F-only form/count lemmas; protected a,b permutation is irrelevant because both are in every set')

def off_pre(row,target):return next(v for v,t in enumerate(row) if t==target and v not in H)

def word_pair(L,F,pair,word,protected_pair=False):
    a,b=pair;assert a!=b
    if protected_pair:assert set(pair)&{3,4}
    else:assert not set(pair)&H
    for ch in word:
        row=L if ch=='L' else F;a,b=row[a],row[b]
    assert a==b,(pair,word)

def literal_graph(G,L,F):
    assert (3,4) not in G
    for row in (L,F):
        for a,b in combinations(range(len(L)),2):
            if row[a]==row[b]:assert (a,b) in G
            elif tuple(sorted((row[a],row[b]))) in G:assert (a,b) in G

def verify_reason(L,F,delta,g,KD):
    n=len(L);RR={2}|set(range(6,n));J=set(range(7,n));p=next(v for v in (3,4) if L[v]==delta)
    KL={z for z in combinations(sorted(RR),2) if L[z[0]]==L[z[1]]}
    KF={z for z in combinations(sorted(V|J),2) if F[z[0]]==F[z[1]]}
    mu=next(iter(RR-set(L))) if KL else None
    nu=next(iter(RR-set(F))) if KF else None
    if KL and mu not in set(next(iter(KL))):
        a,b=next(iter(KL));word_pair(L,F,(off_pre(L,a),off_pre(L,b)),'LL');return 'outside_LL'
    if (not KL and L[2] not in (2,6)) or (KL and mu not in (2,6)):
        word_pair(L,F,(off_pre(L,2),off_pre(L,6)),'LFL');return 'outside_LFL_D_cover'
    if (not KF and F[1] not in (2,6)) or (KF and nu not in (2,6)):
        word_pair(L,F,(off_pre(F,2),off_pre(F,6)),'FFL');return 'outside_FFL_D_cover'
    if delta==0:
        d=next(v for v in (2,6) if any(t==v and i not in H for i,t in enumerate(L)))
        word_pair(L,F,(p,off_pre(L,d)),'LFL');return 'outside_LFL_delta'
    if g[6]==0:
        d=next(v for v in (2,6) if any(t==v and i not in H for i,t in enumerate(F)))
        word_pair(L,F,(6,off_pre(F,d)),'FFL');return 'outside_FFL_gamma'
    if g[2]!=0:
        assert 0 not in L and [v for v,t in enumerate(F) if t==0]==[0]
        return 'zero_only_self_incoming'
    if KF:
        extra=KF-CT
        if extra:
            q=next(iter(extra))[1];assert q in J and not KL and not KD
            if delta==1:
                word_pair(L,F,(p,L.index(q)),'LF',True);return 'protected_LF_extra'
            if g[6]==1:
                word_pair(L,F,(6,off_pre(F,q)),'FF');return 'outside_F2_extra'
            assert delta==g[6]==5 and g[0]==1
        if nu==6:
            if F[5]==2:word_pair(L,F,(5,6),'FFFL')
            else:
                x=off_pre(F,2);assert x in J;word_pair(L,F,(x,off_pre(F,x)),'FFFL')
            return 'outside_F3L_singular'
        assert nu==2
        if (not KL and L[2]==6) or (KL and mu==6):
            target=next(v for v in {delta}|J if F[v]==6 and any(t==v and i not in H for i,t in enumerate(L)))
            word_pair(L,F,(off_pre(L,2),off_pre(L,target)),'LFFL');return 'outside_LF2L_singular'
        if extra:
            assert all(L[v] not in H and F[v] not in H for v in range(n) if v not in H)
            return 'H_no_external_predecessor'
        assert KF=={(1,5)}
        if not KL and F[1]==6:
            word_pair(L,F,(2,p),'LFFL',True);return 'protected_LF2L_r6'
        if g[0]==0:
            assert not KL and F[1] in J
            T0={3,4,0}|J;assert {F[v] for v in T0}&D=={0,6}
            if strong([L,F]):assert all(any_prefix_failure(L,F,T,5) for T in feasible_sets(n))
            return 'zero_unreachable_from_safe_prefix'
        kind='singular_15' if KL else 'bijective_15'
        literal_graph(graph(kind,n),L,F);return 'backward_'+kind
    e=F[1]
    if e==6:
        if F[5]==2:word_pair(L,F,(5,6),'FFFL')
        else:
            x=off_pre(F,2);assert x in J;word_pair(L,F,(x,off_pre(F,x)),'FFFL')
        return 'outside_F3L_bijective'
    assert e==2
    if (not KL and L[2]==6) or (KL and mu==6):
        x=off_pre(F,6);target=delta if x==5 else x
        word_pair(L,F,(off_pre(L,2),off_pre(L,target)),'LFFL');return 'outside_LF2L_bijective'
    if not KL:
        if delta==1:
            word_pair(L,F,(2,p),'LFFL',True);return 'protected_LF2L_delta1'
        if F[5]==6:
            word_pair(L,F,(2,p),'LFFL',True);return 'protected_LF2L_r6'
    if g[6]==1:
        assert all(F_count_failure(F,T,5) is not None for T in feasible_sets(n))
        if F[5]==6:
            assert KL and not KD and g[0]==5 and all(F[v] in J for v in J)
            return 'five_cycle_count_obstruction'
        return 'F_count_form_chain'
    assert g[6]==5
    if not KL:
        assert delta==5 and all(L[v] not in H and F[v] not in H for v in range(n) if v not in H)
        return 'H_no_external_predecessor'
    if delta==1:
        x=off_pre(F,6)
        if x==5:word_pair(L,F,(p,off_pre(L,6)),'LFFFL');return 'outside_LF3L_swap'
        word_pair(L,F,(p,off_pre(L,x)),'LFFL');return 'outside_LF2L_delta1'
    literal_graph(graph('join',n),L,F);return 'backward_join'

def forward_distances(L,F):
    n=len(L);pp=list(combinations(range(n),2));trans=[[-2]*(n*n) for _ in (0,1)]
    for j,row in enumerate((L,F)):
        for a,b in pp:
            c,d=row[a],row[b];trans[j][a*n+b]=-1 if c==d else min(c,d)*n+max(c,d)
    result={}
    for a,b in pp:
        start=a*n+b;todo=[start];depth=[0];seen=1<<start;pos=0;found=False
        while pos<len(todo) and not found:
            state=todo[pos];step=depth[pos]+1;pos+=1
            for j in (0,1):
                target=trans[j][state]
                if target==-1:result[a,b]=step;found=True;break
                bit=1<<target
                if not seen&bit:seen|=bit;todo.append(target);depth.append(step)
    return result

def literal_family(n):
    RR={2}|set(range(6,n));J=set(range(7,n));total=0;hist=Counter();proof=Counter()
    cache={K:split_patterns(RR,J,K) for delta,g,K in cores()};initials=feasible_sets(n)
    for delta,g,KD in cores():
        for mode in range(3):
            for lb,fb in cache[KD]:
                for lv in permutations(sorted(RR),len(lb)):
                    L=[-1]*n;Fb=[-1]*n;protected(L,Fb,delta,mode)
                    for v in C:L[v]=4
                    for block,target in zip(lb,lv):
                        for v in block:L[v]=target
                    for fv in permutations(sorted(RR),len(fb)):
                        F=Fb.copy()
                        for v,target in g.items():F[v]=target
                        for block,target in zip(fb,fv):
                            for v in block:F[v]=target
                        assert all(0<=v<n for v in L+F)
                        proof[verify_reason(L,F,delta,g,KD)]+=1
                        dist=forward_distances(L,F)
                        if total<64:assert dist==pair_distances([L,F])
                        outside=[d for pair,d in dist.items() if not set(pair)&H and d<=5]
                        badprotected=[d for pair,d in dist.items() if set(pair)&{3,4} and d<=6]
                        if outside:outcome='outside_pair_'+str(min(outside))
                        elif badprotected:outcome='protected_pair_'+str(min(badprotected))
                        elif not strong([L,F]):outcome='not_strongly_connected'
                        elif len(dist)<n*(n-1)//2:outcome='nonsynchronizing'
                        else:
                            assert all(any_prefix_failure(L,F,T,5) for T in initials)
                            outcome='fails_required_entrance_prefix'
                        hist[outcome]+=1;total+=1
    assert total=={7:1440,8:18792,9:393984}[n]
    return dict(n=n,complete_row_assignments=total,outcomes=dict(sorted(hist.items())),
        symbolic_case_checks=dict(sorted(proof.items())),complete_initial_form_controls=len(initials),
        scope='Complete normalized small row controls under the stated pair/entrance premises; not all-n equality claims or a full n=13 scan')

def frontier():
    inventory=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    identity='b1_out_c5_third10';target=next(v for v in inventory['records'] if v['id']==identity)
    assert target['D']==[0,2,6] and len(target['binary_profile_pairs'])==3
    oldjoint={v['id'] for v in joint['records'] if len(v['B'])==3}|{'b2_mixed_c12','b1_out_c6','b1_in_c5'}
    oldthird={f'b1_out_c5_third{i}' for i in (1,2,3,4,5,7,8,9,10,11)}
    kept=[v for v in inventory['records'] if v['joint_id'] not in oldjoint and v['id'] not in oldthird and v['binary_profile_pairs']]
    assert len(kept)==164 and sum(len(v['binary_profile_pairs']) for v in kept)==915
    Ds=[v['D'] for v in kept if v['joint_id']=='b1_out_c5'];assert Ds==[[2,6]]
    return dict(additional_binary_third_profile_exclusions=[identity],b1_C3_mixed_remaining_D=Ds,
        remaining_binary_joint=26,remaining_unrestricted_joint=43,remaining_binary_typed_third_orbits=164,
        remaining_binary_profile_pairs=915,extremal_interval=[11,12])

def main():
    K=kernel_audit();graphs=graph_audit();counts=count_audit();literal=[]
    for n in (7,8,9):
        literal.append(literal_family(n));print(json.dumps(dict(control_n=n,assignments=literal[-1]['complete_row_assignments'])),flush=True)
    front=frontier()
    names=[Path(__file__).name,'PROOF.md#problem4-b1-mixed-c3-three-point-third-exclusion','PROOF.md#problem4-entry-fiber-flag',
        'PROOF.md#problem4-second-entrance-fiber','PROOF.md#problem4-third-entrance-space','PROOF.md#problem4-local-equality-flag',
        'PROOF.md#problem4-codimension-four-p5-dichotomy','PROOF.md#problem4-singleton-three-kernel-exclusion',
        'small_first_third_inventory.json','joint_fiber_orbits.json','alphabet_check.py']
    result=dict(status='pass',parameter=[13,9,1],kernels=K,universal_graphs=graphs,
        complete_count_form_controls=counts,complete_literal_small_families=literal,frontier=front,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Conditional binary D={0,2,6} symbolic exclusion with complete kernels, universal graphs, all parameterized F count rows and independent normalized small-row controls. No full thirteen-state scan, new F value or alphabet separation.')
    (ROOT/'b1_mixed_c3_three_point_third_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',split_kernels=30,graphs=123,F_count_rows=13680,
        literal_rows=[v['complete_row_assignments'] for v in literal],frontier=front)),flush=True)

if __name__=='__main__':main()
