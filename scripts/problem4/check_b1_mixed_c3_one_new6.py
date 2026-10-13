"""Complete kernel/core cover and independent small literal row controls.

The thirteen-state exclusions use the accompanying symbolic proof. Small
row families are controls; they are never extrapolated to an F value.
"""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib, json
from alphabet_check import pair_distances, strong

ROOT=Path(__file__).resolve().parent
C={0,1,5}; H={0,1,2}; R={2}|set(range(6,13)); Q=set(range(13))
US=({0},{0,1})

def partitions(values):
    work=[()]
    for q in values:
        following=[]
        for blocks in work:
            following.append(blocks+((q,),))
            for j in range(len(blocks)):
                following.append(blocks[:j]+(blocks[j]+(q,),)+blocks[j+1:])
        work=following
    return work

def pairs(blocks):
    return {tuple(v) for block in blocks for v in combinations(block,2)}

def base(q):
    return {tuple(v) for v in combinations(sorted(C),2)}|{(2,q)}

def admitted(U,q,RR):
    inputs=(C-U)|(RR-{6}); K=base(q)
    return [blocks for blocks in partitions(sorted(inputs))
            if len(blocks)<=len(RR) and pairs(blocks)<=K]

def kernels():
    rawL=partitions(sorted(R)); reports=[]; targets=Counter()
    for q in (6,7):
        E={2,q}; keptL=[v for v in rawL if pairs(v)=={(2,q)}]
        assert len(keptL)==1 and len(keptL[0])==7
        assert all(set(block)-H for block in keptL[0])
        for U in US:
            inputs=(C-U)|(R-{6}); raw=partitions(sorted(inputs)); kept=admitted(U,q,R)
            assert len(kept)==((1 if q==6 else 3) if len(U)==1 else (1 if q==6 else 2))
            hist=Counter()
            for blocks in kept:
                off={j for j,block in enumerate(blocks) if set(block)-H}
                assert (len(blocks),len(off)) in ((8,7),(7,7))
                for values in permutations(sorted(R),len(blocks)):
                    inv={target:blocks[j] for j,target in enumerate(values)}
                    if E<=set(inv) and all(set(inv[v])-H for v in E):
                        reason='outside_FL'
                    else:
                        reason='admitted_no_outside_FL'
                        if q==7:
                            assert 6 in inv and set(inv[6])-H
                        else:
                            assert next(values[j] for j in range(len(blocks)) if j not in off) in E
                    hist[reason]+=1;targets[reason]+=1
            reports.append(dict(U=sorted(U),extra_partner=q,abstract_kernels=len(raw),
                admitted_kernels=len(kept),block_counts=sorted(map(len,kept)),
                complete_output_assignments=sum(hist.values()),outcomes=dict(sorted(hist.items()))))
    assert len(rawL)==4140 and sum(v['abstract_kernels'] for v in reports)==50574
    assert sum(targets.values())==282240
    # All L-output injections: every used R target has a non-H predecessor.
    lh=Counter()
    for q in (6,7):
        for values in permutations(sorted(R),7):
            missing=next(iter(R-set(values)))
            lh['outside_LL' if missing not in {2,q} else 'missing_E']+=1
    assert sum(lh.values())==80640
    return dict(L_abstract_kernels=4140,F_abstract_kernels=50574,
        complete_F_output_assignments=282240,complete_L_output_assignments=80640,
        F_reports=reports,L_outcomes=dict(sorted(lh.items())))

def core_maps(U):
    D=U|{6}; kept=[]
    for delta,values in product(sorted(C),product(sorted(C),repeat=len(D))):
        g=dict(zip(sorted(D),values))
        if not {tuple(v) for v in combinations(sorted(D),2) if g[v[0]]==g[v[1]]}<=base(6):continue
        if {delta}|set(g.values())!=C:continue
        kept.append((delta,g))
    assert len(kept)==(6 if len(U)==1 else 24)
    return kept

def classify(U,delta,g,e,mu,r):
    V=C-U
    if e==2:
        if mu==2:return 'two_only_self_incoming'
        if r!=6:return 'outside_LFL_E'
        if delta in V:return 'outside_LFL_D'
        if g[6] in U:return 'outside_FFL_D'
        return 'outside_LF2L_U0' if len(U)==1 else 'backward_graph_e2'
    assert e==6
    if r!=2:return 'outside_FFL_E'
    if (delta in U and mu==2) or (delta in V and mu==6):return 'outside_LFL_D'
    if g[6] in V:return 'outside_FFL_D'
    if len(U)==1:return 'backward_graph_e6_U0'
    gamma=g[6];h=next(iter(U-{gamma}))
    if g[gamma]==h:return 'outside_F3L'
    assert g[gamma]==5
    if g[h]==5:
        assert delta==h
        return 'backward_graph_e6_constant'
    assert g[h]==h
    if delta==gamma:return 'h_only_self_incoming'
    if delta==h:return 'outside_LF2L_h'
    assert delta==5
    return 'backward_graph_e6_extra'

def graph_for(U,g,reason):
    G=base(6)
    if reason=='backward_graph_e6_U0':return G|{(0,6),(1,2),(2,5)}
    G|={tuple(v) for v in combinations(sorted(U|{6}),2)}|{(2,5)}
    if reason=='backward_graph_e6_extra':G.add(tuple(sorted((2,next(iter(U-{g[6]}))))))
    return G

def protected(L,F,delta,mode):
    if mode==0:L[3]=3;L[4]=delta;F[3]=4;F[4]=3
    elif mode==1:L[3]=delta;L[4]=3;F[3]=3;F[4]=4
    else:L[3]=delta;L[4]=3;F[3]=4;F[4]=3

def universal_graph(U,delta,g,e,mu,r,reason,mode):
    G=graph_for(U,g,reason);L={q:R-{mu} for q in R};F={q:set(range(7,13)) for q in range(7,13)}
    lp=[-1]*13;fp=[-1]*13;protected(lp,fp,delta,mode)
    L.update({q:{lp[q]} for q in (3,4)});F.update({q:{fp[q]} for q in (3,4)})
    L.update({q:{4} for q in C});F.update({q:{v} for q,v in g.items()})
    F.update({q:{r} for q in C-U});F[2]={e}
    assert set(L)==set(F)==Q and (3,4) not in G
    assert base(6)<=G
    checks=0
    for row in (L,F):
        for x,y in combinations(sorted(Q),2):
            if (x,y) not in G:
                assert not any(tuple(sorted((u,v))) in G for u in row[x] for v in row[y] if u!=v),(reason,x,y)
            checks+=1
    return checks

def core_audit():
    reports=[];closures=0;canonical_total=0
    for U in US:
        hist=Counter();can=Counter()
        for delta,g in core_maps(U):
            for e,mu,external in product((2,6),(2,6),(False,True)):
                r=7 if external else (6 if e==2 else 2)
                reason=classify(U,delta,g,e,mu,r);hist[reason]+=1
                critical=not external and g[6] not in (U if e==2 else C-U)
                critical&=(mu==6 and delta in U) if e==2 else (mu==(6 if delta in U else 2))
                if critical:
                    can[reason]+=1;canonical_total+=1
                    if reason.startswith('backward_graph'):
                        for mode in range(3):closures+=universal_graph(U,delta,g,e,mu,r,reason,mode)
        assert sum(hist.values())==len(core_maps(U))*8
        reports.append(dict(U=sorted(U),port_configurations=sum(hist.values()),histogram=dict(sorted(hist.items())),
            critical_cases=sum(can.values()),critical_histogram=dict(sorted(can.items()))))
    assert canonical_total==26
    return dict(port_configurations=240,critical_core_cases=26,reports=reports,
        universal_set_valued_backward_checks=closures)

def pre_nonH(row,target):
    return next(q for q,v in enumerate(row) if v==target and q not in H)

def word_pair(L,F,pair,word):
    x,y=pair;assert x!=y and x not in H and y not in H
    for letter in word:
        row=L if letter=='L' else F;x,y=row[x],row[y]
    assert x==y,(pair,word)

def verify_reason(U,delta,g,L,F,q):
    RR={2}|set(range(6,len(L)));E={2,q};mu=next(iter(RR-set(L)))
    if mu not in E:
        word_pair(L,F,(pre_nonH(L,2),pre_nonH(L,q)),'LL');return 'outside_LL'
    if all(any(v==t and i not in H for i,v in enumerate(F)) for t in E):
        word_pair(L,F,(pre_nonH(F,2),pre_nonH(F,q)),'FL');return 'outside_FL'
    if q!=6:
        if delta in U:
            word_pair(L,F,(pre_nonH(L,delta),pre_nonH(L,6)),'LFL');return 'outside_LFL_D'
        if g[6] in U:
            word_pair(L,F,(6,pre_nonH(F,6)),'FFL');return 'outside_FFL_D'
        assert all(L[v] not in U and F[v] not in U for v in range(len(L)) if v not in U)
        return 'U_has_no_external_predecessor'
    e=F[2];r=F[next(iter(C-U))];reason=classify(U,delta,g,e,mu,r)
    if reason=='two_only_self_incoming':
        assert all(v!=2 for v in L) and [i for i,v in enumerate(F) if v==2]==[2]
    elif reason=='h_only_self_incoming':
        h=next(iter(U-{g[6]}));assert all(v!=h for v in L) and [i for i,v in enumerate(F) if v==h]==[h]
    elif reason.startswith('backward_graph'):
        G=graph_for(U,g,reason)
        for row in (L,F):
            for x,y in combinations(range(len(row)),2):
                if row[x]==row[y]:assert (x,y) in G
                elif tuple(sorted((row[x],row[y]))) in G:assert (x,y) in G
    elif reason=='outside_LFL_E':
        x=next(i for i,v in enumerate(F) if v==6)
        word_pair(L,F,(pre_nonH(L,2),pre_nonH(L,x)),'LFL')
    elif reason=='outside_LFL_D':
        target=6 if delta in U else 2
        word_pair(L,F,(pre_nonH(L,delta),pre_nonH(L,target)),'LFL')
    elif reason=='outside_FFL_D':word_pair(L,F,(5,6),'FFL')
    elif reason=='outside_FFL_E':
        x=next(i for i,v in enumerate(F) if v==2)
        word_pair(L,F,(x,pre_nonH(F,x)),'FFL')
    elif reason=='outside_LF2L_U0':word_pair(L,F,(pre_nonH(L,0),pre_nonH(L,2)),'LFFL')
    elif reason=='outside_LF2L_h':
        h=next(iter(U-{g[6]}));word_pair(L,F,(pre_nonH(L,h),pre_nonH(L,2)),'LFFL')
    elif reason=='outside_F3L':word_pair(L,F,(5,6),'FFFL')
    else:raise AssertionError(reason)
    return reason

def literal_family(n,q):
    RR={2}|set(range(6,n));K=base(q);total=0;hist=Counter();proof=Counter();byU={}
    Lblocks=[{2,q}]+[{v} for v in sorted(RR-{2,q})]
    for U in US:
        local=Counter();count=0;fk=admitted(U,q,RR)
        for delta,g in core_maps(U):
            for mode in range(3):
                for lv in permutations(sorted(RR),len(Lblocks)):
                    L=[-1]*n;Fbase=[-1]*n;protected(L,Fbase,delta,mode)
                    for v in C:L[v]=4
                    for block,target in zip(Lblocks,lv):
                        for v in block:L[v]=target
                    for blocks in fk:
                        for fv in permutations(sorted(RR),len(blocks)):
                            F=Fbase.copy()
                            for v,target in g.items():F[v]=target
                            for block,target in zip(blocks,fv):
                                for v in block:F[v]=target
                            assert all(0<=v<n for v in L+F)
                            assert {p for row in (L,F) for p in combinations(range(n),2) if row[p[0]]==row[p[1]]}<=K
                            proof[verify_reason(U,delta,g,L,F,q)]+=1
                            d=pair_distances([L,F]);short=[v for p,v in d.items() if not set(p)&H and v<=5]
                            if short:reason='outside_pair_'+str(min(short))
                            elif not strong([L,F]):reason='not_strongly_connected'
                            else:
                                assert len(d)<n*(n-1)//2;reason='nonsynchronizing'
                            hist[reason]+=1;local[reason]+=1;total+=1;count+=1
        byU[str(sorted(U))]=dict(assignments=count,outcomes=dict(sorted(local.items())))
    assert total=={(7,6):360,(8,6):3240,(8,7):7128}[(n,q)]
    return dict(n=n,extra_partner=q,complete_row_assignments=total,outcomes=dict(sorted(hist.items())),
        symbolic_case_checks=dict(sorted(proof.items())),by_U=byU,
        scope='Entire small normalized row family, not an n-state F value')

def frontier():
    data=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    joint=json.loads((ROOT/'joint_fiber_orbits.json').read_text(encoding='utf-8'))
    additions=['b1_out_c5_third4','b1_out_c5_third8']
    for identity,D in zip(additions,([0,6],[0,1,6])):
        record=next(z for z in data['records'] if z['id']==identity)
        assert record['D']==D and len(record['binary_profile_pairs'])==3
    excluded_joint={z['id'] for z in joint['records'] if len(z['B'])==3}|{'b2_mixed_c12','b1_out_c6','b1_in_c5'}
    excluded_third={f'b1_out_c5_third{i}' for i in (1,2,3,4,5,7,8,9)}
    remaining=[z for z in data['records'] if z['joint_id'] not in excluded_joint and z['id'] not in excluded_third and z['binary_profile_pairs']]
    assert len(remaining)==166 and sum(len(z['binary_profile_pairs']) for z in remaining)==921
    Ds=[z['D'] for z in remaining if z['joint_id']=='b1_out_c5']
    assert Ds==[[2,6],[0,2,6],[0,1,2,6]]
    return dict(additional_binary_third_profile_exclusions=additions,b1_C3_mixed_remaining_D=Ds,
        remaining_binary_joint=26,remaining_unrestricted_joint=43,remaining_binary_typed_third_orbits=166,
        remaining_binary_profile_pairs=921,extremal_interval=[11,12])

def main():
    K=kernels();core=core_audit();literal=[literal_family(n,q) for n,q in ((7,6),(8,6),(8,7))];front=frontier()
    names=[Path(__file__).name,'PROOF.md#problem4-b1-mixed-c3-one-new6-exclusion',
        'PROOF.md#problem4-binary-singleton-first-second-cover','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-second-entrance-fiber',
        'PROOF.md#problem4-third-entrance-space','PROOF.md#problem4-local-equality-flag','PROOF.md#problem4-codimension-four-p5-dichotomy',
        'PROOF.md#problem4-singleton-three-kernel-exclusion','small_first_third_inventory.json','joint_fiber_orbits.json','alphabet_check.py']
    result=dict(status='pass',parameter=[13,9,1],kernels=K,core_cases=core,
        complete_literal_small_families=literal,frontier=front,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Two symbolic binary exclusions; complete kernels, core ports, universal graph checks and independent small normalized row controls. No full thirteen-state scan, new F value or alphabet separation.')
    (ROOT/'b1_mixed_c3_one_new6_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',F_kernel_partitions=50574,F_output_assignments=282240,L_output_assignments=80640,
        core_ports=240,critical_cores=26,literal_rows=[v['complete_row_assignments'] for v in literal],frontier=front)))

if __name__=='__main__':main()
