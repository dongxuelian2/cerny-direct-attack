"""Independent admission, graph and word-witness audit for B=0,C=12."""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
A={3};B={0};C={1,2};G={(1,2)}

def canonical(fields):return tuple(tuple(sorted(tuple(sorted(b)) for b in f)) for f in fields)
def kernel(fields):return {tuple(z) for f in fields for b in f for z in combinations(sorted(b),2)}

def literal_partitions(X):
    order=sorted(X)
    def visit(k,bs):
        if k==len(order):yield bs;return
        q=order[k]
        for j in range(len(bs)):
            new=[b.copy() for b in bs];new[j].add(q);yield from visit(k+1,new)
        yield from visit(k+1,[*bs,{q}])
    yield from visit(0,[])

def independent_patterns(n,row):
    inputs=[set(row[k]) for k in ('preA','preB','preC')];inputs.append(set(range(n))-set().union(*inputs))
    fs=[]
    for X,cap in zip(inputs,[1,1,2,n-4]):
        choices=[]
        for p in literal_partitions(X):
            if len(p)>cap:continue
            K=kernel([p])
            if any(not set(z)&C or set(z)&(A|B) for z in K):continue
            choices.append(p)
        fs.append(choices)
    return {canonical(fields) for fields in product(*fs)}

def closed_graph(row,pattern):
    assert kernel(pattern)<=G
    for p in combinations(row['preC'],2):assert tuple(p) in G

def kernel_audit():
    data=json.loads((ROOT/'b1_c2_h_cover_inventory.json').read_text(encoding='utf-8'))
    original=json.loads((ROOT/'small_first_third_inventory.json').read_text(encoding='utf-8'))
    counts=[]
    for z in data['profiles']:
        source=next(v for v in original['records'] if v['id']==z['id'])
        assert [v['rows'] for v in z['pairs']]==source['binary_profile_pairs']
        for row in z['rows']:
            computed=independent_patterns(13,row)
            actual={canonical(v['fields']) for v in row['patterns']}
            assert len(actual)==len(row['patterns']) and actual==computed
        hist=Counter();graphchecks=0
        for pair in z['pairs']:
            left,right=[z['rows'][i] for i in pair['rows']]
            assert pair['kernel_pairs']==[list(ij) for ij in product(range(len(left['patterns'])),range(len(right['patterns'])))]
            for i,j in pair['kernel_pairs']:
                pl=left['patterns'][i]['fields'];pr=right['patterns'][j]['fields']
                if z['D']==[1,4]:hist['overlapping_D']+=1;continue
                both=set(left['preB'])==set(right['preB'])==C
                nonsupplier=(left if set(left['preB'])!=C else right)
                if kernel(pl)|kernel(pr)<=G:
                    closed_graph(left,pl);closed_graph(right,pr);hist['closed_G']+=1;graphchecks+=2
                else:
                    assert set(nonsupplier['preC'])=={4};hist['singleton_C_outputs']+=1
        counts.append(dict(D=z['D'],original_pairs=len(z['pairs']),row_patterns=sum(len(v['patterns']) for v in z['rows']),
            kernel_pairs=sum(len(v['kernel_pairs']) for v in z['pairs']),classification=dict(hist),universal_closed_graph_rows=graphchecks))
    assert [(z['row_patterns'],z['kernel_pairs']) for z in counts]==[(170,497),(42,54)]
    return counts

def rows_for(n,pattern):
    targets=[sorted(A),sorted(B),sorted(C),list(range(4,n))]
    for labels in product(*(permutations(T,len(fs)) for T,fs in zip(targets,pattern))):
        row=[-1]*n
        for fs,outputs in zip(pattern,labels):
            for block,t in zip(fs,outputs):
                for q in block:row[q]=t
        assert all(t>=0 for t in row);yield tuple(row)

def outside_pre(row,target):
    q=next((q for q,z in enumerate(row) if z==target and q not in C),None)
    assert q is not None,(row,target);return q

def merge_word(rows,pair,word):
    assert len(set(pair))==2 and not set(pair)&C and len(word)<=5
    V=set(pair)
    for k in word:V={rows[k][q] for q in V}
    assert len(V)==1,(rows,pair,word)

def closed_literal(rows):
    n=len(rows[0])
    for row in rows:
        for p in combinations(range(n),2):
            out={row[q] for q in p}
            if len(out)==1 or out<=C:assert p==(1,2)

def reason(D,left,right,pl,pr,rows):
    n=len(rows[0]);R=set(range(4,n));J=R-{4}
    if set(rows[0])|set(rows[1])!=set(range(n)):return 'missing_incoming_state'
    if D==[1,4]:
        l=next(k for k,v in enumerate((left,right)) if set(v['preB'])==C);f=1-l;L,F=rows[l],rows[f]
        p=next(q for q in A|B if L[q] in C);delta=L[p];x=outside_pre(L,4)
        if delta==1:
            merge_word(rows,(p,x),(l,f,l));return 'protected_LFL'
        assert delta==2
        if F[4]==2:
            assert F[1]==1 and [q for q in range(n) if F[q]==1]==[1] and 1 not in L
            return 'incoming_self_loop_1'
        assert F[4]==1
        outside=next((q for q in J if F[q]==4),None)
        if outside is not None:
            merge_word(rows,(4,outside),(f,f,l));return 'outside_FFL'
        assert {F[q] for q in J}==J
        if F[2]!=4:
            r=outside_pre(F,F[2]);x=outside_pre(L,r)
            merge_word(rows,(p,x),(l,f));return 'protected_LF'
        merge_word(rows,(p,x),(l,f,f,l));return 'protected_LFFL'
    assert D==[4]
    both=set(left['preB'])==set(right['preB'])==C
    if both:
        assert kernel(pl)|kernel(pr)<=G;return 'closed_G_both_C_mergers'
    l=0 if set(left['preB'])==C else 1;f=1-l;L,F=rows[l],rows[f];other=(left,right)[f]
    if set(other['preC'])==C:
        assert kernel(pl)|kernel(pr)<=G;return 'closed_G_C_output_cell'
    assert set(other['preC'])=={4}
    delta=next(L[q] for q in range(n) if L[q] in C);beta=F[4];assert set((delta,beta))==C
    u=outside_pre(L,delta)
    collision=next((q for q in J if F[q]==F[delta]),None)
    if collision is not None:
        v=outside_pre(L,collision);merge_word(rows,(u,v),(l,f));return 'outside_LF_delta'
    if F[delta]==F[beta]:
        assert kernel(pl)|kernel(pr)<=G;return 'closed_G_only_C_pair'
    q=next(q for q in J if F[q]==F[beta]);r=F[delta]
    assert {F[q] for q in J}==R-{r}
    if q!=r:
        x=outside_pre(F,q);merge_word(rows,(4,x),(f,f));return 'outside_FF_beta'
    v=outside_pre(L,4);merge_word(rows,(u,v),(l,f,f));return 'outside_LFF_ports'

def literal_controls(n):
    from enumerate_b1_c2_h_cover import inventory
    data=inventory(n);total=0;hist=Counter();checked_closed=set()
    for z in data['profiles']:
        cache={(i,j):list(rows_for(n,p['fields'])) for i,row in enumerate(z['rows']) for j,p in enumerate(row['patterns'])}
        for pair in z['pairs']:
            x,y=pair['rows'];left,right=z['rows'][x],z['rows'][y]
            for i,j in pair['kernel_pairs']:
                pl=left['patterns'][i]['fields'];pr=right['patterns'][j]['fields']
                for rows in product(cache[x,i],cache[y,j]):
                    code=reason(z['D'],left,right,pl,pr,rows);hist[code]+=1;total+=1
                    if code.startswith('closed') and rows not in checked_closed:
                        closed_literal(rows);checked_closed.add(rows)
    k=n-4
    from math import factorial
    assert total==(44+24*k*k+24*k)*factorial(k)**2
    return dict(n=n,complete_row_assignments=total,proof_case_checks=dict(sorted(hist.items())),
        independent_literal_closed_graph_pairs=len(checked_closed),
        scope='Complete normalized rows under the outside-C/protected pair premises, not smaller-size equality claims or a full n13 scan.')

def ordinary_port_controls():
    R=tuple(range(4,13));J=set(range(5,13));Lcount=0;Fcount=0;hit4=0;no4=0
    for outputs in permutations(R):
        inv=dict(zip(outputs,R));assert set(inv)==set(R) and all(q not in C for q in inv.values());Lcount+=1
        # Every nine-input outside-C L block system is bijective onto R,
        # including systems replacing4 by an unused protected input.
        for p in (0,3):
            inputs=(p,*sorted(J));assert len(inputs)==len(set(inputs))==9
            inverse=dict(zip(outputs,inputs));assert all(q not in C for q in inverse.values())
    for outputs in permutations(R,8):
        inv=dict(zip(outputs,sorted(J)));assert len(inv)==8 and all(q not in C for q in inv.values());Fcount+=1
        if 4 in inv:assert inv[4] in J;hit4+=1
        else:
            assert set(inv)==J;no4+=1
            for q in J:assert inv[q] in J
    assert Lcount==Fcount==362880 and hit4==322560 and no4==40320
    return dict(complete_L_output_permutations=Lcount,complete_F_J_output_injections=Fcount,
        F_injections_with_outside_predecessor_of4=hit4,F_injections_permuting_J=no4,
        scope='Complete individual ordinary block-output systems at13 states. Small literal rows separately check the coupled short words; not transition-pair enumeration.')

def main():
    kernels=kernel_audit();ports=ordinary_port_controls();literal=[]
    for n in (6,7,8):
        literal.append(literal_controls(n));print(json.dumps(dict(n=n,assignments=literal[-1]['complete_row_assignments'])),flush=True)
    names=[Path(__file__).name,'enumerate_b1_c2_h_cover.py','b1_c2_h_cover_inventory.json','B1_C2_H_COVER_EXCLUSION.md',
        'small_first_third_inventory.json','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md','THIRD_ENTRANCE_SPACE.md',
        'LOCAL_EQUALITY_FLAG.md','CODIMENSION_FOUR_P5_DICHOTOMY.md']
    result=dict(status='pass',parameter=[13,9,1],kernels=kernels,complete_n13_ordinary_port_controls=ports,
        complete_literal_smaller_controls=literal,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete conditional binary joint b1_in_c4 exclusion, using C-cover and protected isolation, no C3 kernel budget. No full13-state transition scan, F value or numerical alphabet separation.')
    (ROOT/'b1_c2_h_cover_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',kernels=kernels,ports=ports,literal=[z['complete_row_assignments'] for z in literal])),flush=True)

if __name__=='__main__':main()
