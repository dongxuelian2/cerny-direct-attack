"""Independent kernel/graph audit and complete smaller row controls."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
H={0,1,2};A={3};B={4};C={0,1,5};D={2,6};E={7}
G={tuple(z) for z in combinations(sorted(C),2)}|{(2,6)}

def canonical(field):return tuple(sorted(tuple(sorted(b)) for b in field))
def full_partitions(X):
    # Unrestricted set partitions, then literal filtering below. This does
    # not reuse the generator's H-restricted recursion.
    items=sorted(X)
    def visit(k,blocks):
        if k==len(items):yield canonical(blocks);return
        q=items[k]
        for i in range(len(blocks)):
            nextblocks=[b.copy() for b in blocks];nextblocks[i].add(q)
            yield from visit(k+1,nextblocks)
        yield from visit(k+1,[*blocks,{q}])
    yield from visit(0,[])

def Kpattern(pattern):return {tuple(z) for field in pattern for b in field for z in combinations(sorted(b),2)}
def words(n,word):
    Q=set(range(n));sets=dict(A=A,B=B,C=C,D=D,E=E)
    cells=[sets[k] for k in word];cells.append(Q-set().union(*cells));return cells

def literal_patterns(n,word):
    parts=[]
    for X,cap in zip(words(n,word),[1,1,3,2,n-7]):
        admitted=[]
        for p in full_partitions(X):
            if len(p)>cap:continue
            K=Kpattern([p])
            if len(K)>4 or any(not set(z)&H or set(z)&{3,4} for z in K):continue
            admitted.append(p)
        parts.append(admitted)
    return {tuple(z) for z in product(*parts) if len(Kpattern(z))<=4}

def classify(left,right,pl,pr):
    K=Kpattern(pl)|Kpattern(pr);extra=K-G
    if not extra:return 'closed',None,None
    assert len(extra)==1;pair=next(iter(extra))
    j=0 if pair in Kpattern(pl) else 1
    supplier,other=(left,right) if j==0 else (right,left)
    po=pr if j==0 else pl
    assert supplier['word'][3]=='E'
    assert all(any(q not in H for q in block) for row in (pl,pr) for block in row[4])
    if pair[0]==2:
        assert supplier['base_row'] in (0,2,4,6) and pair[1]>=8
        if other['word'][3]=='C' and len(po[3])==2:
            assert supplier['base_row'] in (2,6) and other['base_row'] in (1,5)
            return '2q_nonconstant_C',j,pair
        assert len(po[3])==1
        return '2q_both_constant',j,pair
    assert pair[0] in (0,1) and pair[1]>=8 and supplier['base_row'] in (1,5)
    if other['word'][3]=='D':
        assert other['base_row'] in (2,6) and len(po[3])==2
        return 'iq_D_permutation',j,pair
    assert other['base_row'] in (3,7) and len(po[3])==1
    return 'iq_both_constant',j,pair

def graph_closed(n,row,pattern):
    K=Kpattern(pattern);assert K<=G
    cells=words(n,row['word']);tests=0
    # Inverse pairs of the two complete output-cell graphs, then kernels.
    for k in (2,3):
        for p in combinations(sorted(cells[k]),2):assert p in G;tests+=1
    for p in K:assert p in G;tests+=1
    return tests

def independent_inventory(n=13,data=None):
    if data is None:data=json.loads((ROOT/'b1_mixed_c3_singleton_fourth_inventory.json').read_text(encoding='utf-8'))
    base=json.loads((ROOT/'b1_mixed_c3_fourth_inventory.json').read_text(encoding='utf-8'))['records'][0]
    assert data['n']==n and len(data['pairs'])==41
    lookup={};rowtests=0
    for row in data['rows']:
        computed=literal_patterns(n,row['word'])
        distributed={tuple(canonical(p) for p in z['fields']) for z in row['patterns']}
        assert len(distributed)==len(row['patterns']) and distributed==computed
        rowtests+=len(computed)
    hist=Counter();graphs=0;columns=0
    assert [z['rows'] for z in data['pairs']]==base['binary_fourth_profile_pairs']
    for pair in data['pairs']:
        left,right=[data['rows'][k] for k in pair['rows']];expected=[]
        for i,j in product(range(len(left['patterns'])),range(len(right['patterns']))):
            pl=left['patterns'][i]['fields'];pr=right['patterns'][j]['fields']
            if len(Kpattern(pl)|Kpattern(pr))>4:continue
            if any(len(pl[k])+len(pr[k])<cap for k,cap in enumerate([1,1,3,2,n-7])):continue
            expected.append([i,j]);case,_,_=classify(left,right,pl,pr);hist[case]+=1
            if case=='closed':
                columns+=graph_closed(n,left,pl)+graph_closed(n,right,pr);graphs+=1
        assert expected==pair['kernel_pairs']
    if n==13:
        assert rowtests==264 and sum(hist.values())==555
        assert dict(hist)==dict(closed=210,**{'2q_both_constant':210,'iq_both_constant':60,'iq_D_permutation':30,'2q_nonconstant_C':45})
    return dict(fourth_field_pairs=41,row_kernel_patterns=rowtests,compatible_kernel_pairs=sum(hist.values()),
        classification=dict(sorted(hist.items())),closed_graph_configurations=graphs,universal_graph_pair_checks=columns)

def assignments(n,pattern):
    targets=[sorted(A),sorted(B),sorted(C),sorted(D),list(range(7,n))]
    for labels in product(*(permutations(T,len(field)) for T,field in zip(targets,pattern))):
        row=[-1]*n
        for field,values in zip(pattern,labels):
            for block,t in zip(field,values):
                for q in block:row[q]=t
        assert all(t>=0 for t in row);yield tuple(row)

def off_pre(row,t):
    q=next((q for q,z in enumerate(row) if z==t and q not in H),None)
    assert q is not None,(t,row);return q

def merge_word(rows,pair,word):
    assert len(pair)==len(set(pair))==2
    assert (not set(pair)&H and len(word)<=5) or (set(pair)&{3,4} and len(word)<=6)
    V=set(pair)
    for k in word:V={rows[k][q] for q in V}
    assert len(V)==1,(pair,word,rows)

def strong(rows):
    n=len(rows[0]);seen={0};todo=[0]
    while todo:
        q=todo.pop()
        for row in rows:
            t=row[q]
            if t not in seen:seen.add(t);todo.append(t)
    if len(seen)!=n:return False
    reverse=[set() for q in range(n)]
    for row in rows:
        for q,t in enumerate(row):reverse[t].add(q)
    seen={0};todo=[0]
    while todo:
        for q in reverse[todo.pop()]-seen:seen.add(q);todo.append(q)
    return len(seen)==n

def prefix_failure(rows,T,limit):
    initial=frozenset(T);seen={initial};current={initial}
    for depth in range(1,limit+1):
        new=set()
        for V in current:
            for row in rows:
                W=frozenset(row[q] for q in V)
                if len(W)!=len(T) or not A<=W:return depth
                if depth<=10 and not B<=W:return depth
                if depth<=9 and len(W&C)!=1:return depth
                if depth<=8 and len(W&D)!=1:return depth
                if depth<=7 and not E<=W:return depth
                if W not in seen:new.add(W)
        seen|=new;current=new
    return None

def verify_reason(left,right,pl,pr,rows):
    case,j,pair=classify(left,right,pl,pr)
    if case=='closed':return 'backward_closed_G',None
    if set(rows[0])|set(rows[1])!=set(range(len(rows[0]))):return 'missing_incoming_state',None
    Z=rows[j];other=rows[1-j];i,q=pair
    if case in ('2q_both_constant','iq_both_constant'):
        cells=[words(len(Z),r['word'])[3] for r in (left,right)]
        constant=[rows[k][min(cells[k])] for k in (0,1)]
        assert sorted(constant)==[2,6]
        t=constant.index(2);T=rows[t];y=off_pre(T,2)
        if i==2:
            x=off_pre(T,q);merge_word(rows,(y,x),(t,j));return 'outside_constant_2q',None
        for m,M in enumerate(rows):
            for v in (3,4,6):
                if M[v]==i:
                    merge_word(rows,(v,off_pre(M,q)),(m,j));return 'isolated_i_predecessor',None
        m=next(m for m,M in enumerate(rows) if M[2]==i);M=rows[m]
        R={v for v,z in enumerate(M) if z==q};ordinary=R&(set(range(7,len(M)))|{3,4})
        if ordinary:
            x=off_pre(T,min(ordinary));merge_word(rows,(y,x),(t,m,j))
            return 'outside_constant_iq_ordinary',None
        assert R==C-{i} and T[6] in R,(case,left['word'],right['word'],rows,pair,m,t,R,T[6])
        merge_word(rows,(y,6),(t,m,j));return 'outside_constant_iq_Cblock',None
    if case=='iq_D_permutation':
        f=j;l=1-j;F=Z;L=other;delta=L[next(v for v in (3,4) if L[v] in C)]
        if delta==i:
            merge_word(rows,(next(v for v in (3,4) if L[v]==i),off_pre(L,q)),(l,f));return 'protected_delta_i',None
        if F[6]==i:
            merge_word(rows,(6,off_pre(F,q)),(f,f));return 'outside_F6_i',None
        assert F[2]==i and set((delta,F[2],F[6]))==C
        if L[2]==6:
            assert L[6]==2;R={v for v,z in enumerate(F) if z==q};ordinary=R&set(range(7,len(F)))
            if ordinary:x=off_pre(L,min(ordinary))
            else:
                assert R==C-{i} and delta in R;x=next(v for v in (3,4) if L[v]==delta)
            merge_word(rows,(6,x),(l,f,f));return 'outside_or_protected_D_swap',None
        assert L[2]==2 and L[6]==6;return 'D_coordinate_trap_iq',5
    assert case=='2q_nonconstant_C'
    l=j;f=1-j;L=Z;F=other
    if L[7]==2:
        merge_word(rows,(7,off_pre(L,q)),(l,l));return 'outside_L7_2',None
    assert L[7]==6
    if F[5]==2:
        merge_word(rows,(5,off_pre(F,q)),(f,l));return 'outside_F5_2',None
    assert F[5]==6;W={v for v in C if F[v]==2};assert W and W<={0,1}
    delta=L[next(v for v in (3,4) if L[v] in C)]
    assert set((delta,F[2],F[6]))==C
    if delta in W:return 'fixed_L_hole',7
    if F[6] not in W:return 'D_coordinate_trap_2q',5
    if F[2] in W and F[q]==q:
        merge_word(rows,(6,q),(f,f,l));return 'outside_F2L',None
    return 'two_J_blocks_count_chain',9

def literal_controls(n):
    # Import is only for producing smaller candidate rows. The thirteen-
    # state admission above is regenerated independently without imports.
    from enumerate_b1_mixed_c3_singleton_fourth import inventory
    data=inventory(n);admission=independent_inventory(n,data);cache={}
    for k,row in enumerate(data['rows']):
        for i,p in enumerate(row['patterns']):cache[k,i]=list(assignments(n,p['fields']))
    hist=Counter();proof=Counter();total=0;controls=0;initial=[A|B|{c,d}|(set(range(7,n))-{h}) for c,d,h in product(C,D,range(8,n))]
    for pair in data['pairs']:
        x,y=pair['rows'];left,right=data['rows'][x],data['rows'][y]
        for i,j in pair['kernel_pairs']:
            pl=left['patterns'][i]['fields'];pr=right['patterns'][j]['fields']
            for rows in product(cache[x,i],cache[y,j]):
                total+=1;reason,depth=verify_reason(left,right,pl,pr,rows);proof[reason]+=1
                if depth is None:continue
                if not strong(rows):hist['not_strong']+=1;continue
                for T in initial:
                    failure=prefix_failure(rows,T,depth)
                    assert failure is not None,(n,reason,rows,sorted(T),depth)
                    hist['entrance_prefix_'+str(failure)]+=1;controls+=1
    assert total=={9:111168,10:1272672}[n]
    return dict(n=n,row_assignments=total,proof_case_checks=dict(sorted(proof.items())),
        actual_initial_form_controls=controls,independent_prefix_outcomes=dict(sorted(hist.items())),admission=admission,
        scope='Complete smaller normalized row assignments under stated pair/count premises. No smaller-size equality or full n=13 row-scan claim.')

def thirteen_state_hole_controls():
    # Abstract actual-image forms. All F permutations are literal; L is
    # described by its two distinct hole ports. The four other block labels
    # can be permuted arbitrarily and do not affect either L image used here.
    J=set(range(7,13));hist=Counter();cores=[]
    for delta,g2,g6 in permutations(sorted(C)):
        for W in ({0},{1},{0,1}):
            if delta not in W and g6 in W:cores.append((delta,g2,g6,W))
    assert len(cores)==6
    for delta,g2,g6,W in cores:
        for q,jv in product(sorted(J-{7}),permutations(sorted(J))):
            FJ=dict(zip(sorted(J),jv))
            def Fform(form):
                c,d,h=form
                return (g2 if d==2 else g6,2 if c in W else 6,FJ[h])
            def admissible(form,depth):
                c,d,h=form
                return (depth>7 or h!=7) and (d!=2 or h==q)
            for h in sorted(J-{7}):
                T=(delta,6,h);good=True
                for k in range(1,4):
                    T=Fform(T)
                    if not admissible(T,1+k):good=False;break
                if good:assert FJ[q]==q
                hist['F_initial_hole_controls']+=1
                hist['F_initial_hole_admitted']+=good
            if FJ[q]!=q:continue
            if g2 in W:
                # Independent pair image: F^2(6)=2 and F^2(q)=q.
                F=[-1]*13;F[2]=g2;F[6]=g6
                for c in C:F[c]=2 if c in W else 6
                for x,y in FJ.items():F[x]=y
                V={6,q}
                for k in range(2):V={F[x] for x in V}
                assert V=={2,q};hist['outside_F2L_controls']+=1;continue
            for s,t in permutations(sorted(J),2):
                # Start with hole q, forced by the two D=2 images.
                V=(delta,6,q)
                F1=Fform(V);F2=Fform(F1);F3=Fform(F2);F4=Fform(F3)
                assert F2[1:]==(2,q) and F3[1:]==(2,q) and F4[1:]==(6,q)
                # The literal occupied-block calculation for either L image.
                for d,port in ((2,s),(6,t)):
                    inputs={3,4,g6 if d==2 else g2,d}|(J-{q})
                    assert len(inputs)==9 and E<=inputs and all(v in inputs for v in J-{7,q})
                    occupied_pair=bool(inputs&{2,q});occupied_six=6 in inputs
                    assert occupied_pair==(d==2) and occupied_six==(d==6)
                    assert port==(s if not occupied_six else t)
                # These holes apply at depths 4,6. The final F^2 images have
                # depths 6,8, so D count<=8 and safety of the next L suffice.
                Fs=Fform(Fform((delta,6,s)))
                Ft=Fform(Fform((delta,6,t)))
                assert Fs[1]==Ft[1]==2
                assert not (admissible((delta,6,s),4) and admissible(Fs,6)
                    and admissible((delta,6,t),6) and admissible(Ft,8))
                hist['distinct_L_port_controls']+=1
    assert hist['F_initial_hole_controls']==108000
    return dict(hist,scope='All ordinary F permutations and all distinct L hole ports at n=13. Other L block-output permutations are irrelevant to these two exact image sets; not full transition-pair enumeration.')

def main():
    kernel=independent_inventory();literal=[];holes=thirteen_state_hole_controls()
    for n in (9,10):
        literal.append(literal_controls(n));print(json.dumps(dict(n=n,row_assignments=literal[-1]['row_assignments'])),flush=True)
    names=[Path(__file__).name,'enumerate_b1_mixed_c3_singleton_fourth.py','b1_mixed_c3_singleton_fourth_inventory.json',
        'b1_mixed_c3_fourth_inventory.json','B1_MIXED_C3_SINGLETON_FOURTH_EXCLUSION.md',
        'B1_MIXED_C3_FOURTH_ENTRANCE_REDUCTION.md','ENTRY_FIBER_FLAG.md','SECOND_ENTRANCE_FIBER.md',
        'THIRD_ENTRANCE_SPACE.md','LOCAL_EQUALITY_FLAG.md','CODIMENSION_FOUR_P5_DICHOTOMY.md','SINGLETON_THREE_KERNEL_EXCLUSION.md']
    result=dict(status='pass',parameter=[13,9,1],immediate_kernel_and_graph_controls=kernel,
        complete_literal_smaller_controls=literal,complete_n13_hole_controls=holes,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete conditional binary singleton-fourth exclusion with all 41 field pairs and all ordinary permutations in the symbolic proof. No full13-state transition scan, new F value or alphabet separation.')
    (ROOT/'b1_mixed_c3_singleton_fourth_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',kernel=kernel,literal_rows=[z['row_assignments'] for z in literal])),flush=True)

if __name__=='__main__':main()
