"""Independent FULL original monoids and reversible-equivalence closure."""
import argparse
from collections import deque
import copy
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path


def digest(value):return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def sc(rows):
    n=len(rows[0]);reach=[[i==j for j in range(n)] for i in range(n)]
    for f in rows:
        for q,t in enumerate(f):reach[q][t]=True
    for k in range(n):
        for i in range(n):
            for j in range(n):reach[i][j]=reach[i][j] or (reach[i][k] and reach[k][j])
    return all(all(row) for row in reach)


def canonical_blocks(equivalence):
    n=len(equivalence);seen=set();classes=[]
    for q in range(n):
        if q in seen:continue
        C=[t for t in range(n) if equivalence[q][t]];classes.append(C);seen.update(C)
    return classes


def beta(rows):
    n=len(rows[0]);eq=[[i==j for j in range(n)] for i in range(n)]
    while True:
        before=[row[:] for row in eq]
        for f in rows:
            for i,j in combinations(range(n),2):
                if eq[i][j]:eq[f[i]][f[j]]=eq[f[j]][f[i]]=True
                if eq[f[i]][f[j]]:eq[i][j]=eq[j][i]=True
        for k in range(n):
            for i in range(n):
                for j in range(n):eq[i][j]=eq[i][j] or (eq[i][k] and eq[k][j])
        if before==eq:return canonical_blocks(eq)


def full_monoid(rows):
    n=len(rows[0]);identity=tuple(range(n));seen={identity};todo=deque([identity])
    while todo:
        w=todo.popleft()
        for f in rows:
            v=tuple(f[t] for t in w)
            if v not in seen:seen.add(v);todo.append(v)
    return seen


def verify_scope(z):
    n=z['n'];maps=[f for f in product(range(n),repeat=n) if len(set(f)) in (n-1,n)]
    stream=sha256();count=sync=maxrange=monoids=minwords=0;hist={}
    for a,b in product(maps,repeat=2):
        rows=[a,b]
        if not sc(rows):continue
        M=full_monoid(rows);r=min(len(set(w)) for w in M);monoids+=len(M)
        eq=[[any(w[i]==w[j] for w in M) for j in range(n)] for i in range(n)]
        for i,j,k in product(range(n),repeat=3):assert not (eq[i][j] and eq[j][k]) or eq[i][k]
        for f in rows:
            for i,j in combinations(range(n),2):assert not eq[i][j] or eq[f[i]][f[j]]
        P=canonical_blocks(eq);assert len(P)==r;ids={q:i for i,C in enumerate(P) for q in C}
        for w in M:
            if len(set(w))==r:
                minwords+=1
                assert all((w[i]==w[j])==(ids[i]==ids[j]) for i,j in combinations(range(n),2))
        for f in rows:
            assert all(len({ids[f[q]] for q in C})==1 for C in P)
            assert len({ids[f[C[0]]] for C in P})==r
        B=beta(rows);assert B==P
        span=max(map(len,P))-min(map(len,P));assert span<=sum(len(set(f))==n-1 for f in rows)
        count+=1;sync+=r==1;maxrange=max(maxrange,span);hist[r]=hist.get(r,0)+1
        stream.update(json.dumps([a,b,P,B,r],separators=(',',':')).encode()+b'\n')
    result=dict(n=n,all_labeled_binary_inputs=len(maps)**2,strongly_connected=count,synchronizing=sync,
                minimum_rank_histogram={str(k):v for k,v in hist.items()},maximum_class_size_range=maxrange,semantic_sha256=stream.hexdigest())
    assert result==z,(result,z)
    return dict(n=n,full_original_monoid_transformations=monoids,all_minimum_rank_transformations_checked=minwords,**{k:v for k,v in result.items() if k not in ('n','semantic_sha256','minimum_rank_histogram')})


def family_rows(s):
    sizes=list(range(1,s+2));classes=[];nextq=0
    for h in sizes:classes.append(list(range(nextq,nextq+h)));nextq+=h
    n=nextq;g=list(range(n))
    for C in classes:
        for q,t in zip(C,C[1:]+C[:1]):g[q]=t
    rows=[g]
    for left,right in zip(classes,classes[1:]):
        row=list(range(n))
        for i,q in enumerate(left):row[q]=right[i]
        for i,q in enumerate(right):row[q]=left[i] if i<len(left) else left[0]
        rows.append(row)
    return classes,rows


def verify_mixed_scope(z):
    n=z['n'];allmaps=list(product(range(n),repeat=n));defect=[f for f in allmaps if len(set(f))==n-1]
    stream=sha256();count=monoids=controls=0
    for a,b in product(defect,allmaps):
        rows=[a,b]
        if not sc(rows):continue
        M=full_monoid(rows);r=min(len(set(w)) for w in M);monoids+=len(M)
        K=next(P for P in combinations(range(n),2) if a[P[0]]==a[P[1]])
        orbit=sorted({tuple(sorted((v[K[0]],v[K[1]]))) for v in M})
        for u in M:
            if len(set(u))==r:
                for x,y in orbit:assert u[x]==u[y];controls+=1
        count+=1;stream.update(json.dumps([a,b,K,orbit,r],separators=(',',':')).encode()+b'\n')
    assert z==dict(n=n,all_defect_one_arbitrary_binary_inputs=len(defect)*len(allmaps),strongly_connected=count,semantic_sha256=stream.hexdigest())
    return dict(n=n,all_binary_inputs=len(defect)*len(allmaps),sc_inputs=count,full_original_monoid_transformations=monoids,uniform_minimum_word_kernel_orbit_controls=controls)


def sc_large(rows):
    n=len(rows[0]);pred=[[] for _ in range(n)]
    for f in rows:
        for q,t in enumerate(f):pred[t].append(q)
    for backward in (True,False):
        seen={0};todo=deque([0])
        while todo:
            q=todo.popleft()
            for t in pred[q] if backward else (f[q] for f in rows):
                if t not in seen:seen.add(t);todo.append(t)
        assert len(seen)==n


def verify_family(z):
    s=z['s'];assert s>=1;C,rs=family_rows(s);n=len(rs[0]);ids={q:i for i,B in enumerate(C) for q in B}
    assert z['n']==n and z['rows_sha256']==digest(rs) and z['stable_partition_sha256']==digest(C)
    assert z['stable_class_sizes']==list(map(len,C)) and z['minimum_rank']==len(C)
    assert z['class_size_range']==s and z['charged_rank_word_length']==s*(s+1)*(s+2)//3
    assert z['strongly_connected'] is True and z['original_letter_ranks']==[n]+[n-1]*s
    sc_large(rs)
    for f in rs:
        assert all(len({ids[f[q]] for q in B})==1 for B in C)
        assert len({ids[f[B[0]]] for B in C})==len(C)
    controls=macroletters=literal=0;word=[]
    assert len(z['programs'])==s
    for h,prog in zip(range(2,s+2),z['programs']):
        assert prog==dict(h=h,unit_letters=[h-1,h-1],root_g_power=h-1,root_tail_letters=[h-1,h-1],root_repetitions=h-2,charged_length=h*(h-1))
        f=rs[h-1];block=C[h-1];u=[f[f[q]] for q in range(n)]
        assert u==[block[0] if q==block[-1] else q for q in range(n)];controls+=2*n
        v=[]
        for q in block:
            x=q
            for _ in range(h-1):x=rs[0][x];macroletters+=1
            x=f[f[x]];macroletters+=2;v.append(x)
        assert v==[block[0]]+block[:-1]
        for q in set(u[x] for x in block):
            x=q
            for _ in range(h-2):x=v[x-block[0]]
            assert x==block[0]
        if s<=20:word.extend([h-1,h-1]+([0]*(h-1)+[h-1,h-1])*(h-2))
    if s<=20:
        assert len(word)==z['charged_rank_word_length'];current=list(range(n))
        for a in word:current=[rs[a][q] for q in current];literal+=n
        assert len(set(current))==s+1 and all(len({current[q] for q in B})==1 for B in C)
    return dict(s=s,n=n,unit_original_state_letter_controls=controls,root_original_state_letter_controls=macroletters,literal_whole_rank_word_state_letter_controls=literal)


def verify_non_sc(z):
    assert z==dict(rows=[[0,0,2],[0,2,2]],mergeable_pair=[0,1],prefix=[1],deadlock_image=[0,2])
    rs=z['rows'];assert not sc(rs);M=full_monoid(rs)
    assert any(w[0]==w[1] for w in M) and any(w[1]==w[2] for w in M)
    assert all(w[0]!=w[2] for w in M)
    assert [rs[1][q] for q in z['mergeable_pair']]==z['deadlock_image']
    return len(M)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('direct_attack/data/corank_one_stability_quotient.json'))
    ap.add_argument('--out',type=Path,default=Path('direct_attack/data/corank_one_stability_quotient_checks.json'));args=ap.parse_args();data=json.loads(args.source.read_text(encoding='utf-8'))
    assert [z['n'] for z in data['scopes']]==[2,3,4]
    assert [z['n'] for z in data['mixed_scopes']]==[2,3,4]
    assert [z['s'] for z in data['sharp_families']]==list(range(1,17))+[20,24,32,64,128]
    scopes=[verify_scope(z) for z in data['scopes']];mixed=[verify_mixed_scope(z) for z in data['mixed_scopes']]
    families=[verify_family(z) for z in data['sharp_families']];boundary=verify_non_sc(data['non_sc'])
    mutations=[];base=data['sharp_families'][0]
    for key,val in [('n',4),('rows_sha256','0'*64),('minimum_rank',1),('class_size_range',0),('charged_rank_word_length',1),('stable_partition_sha256','0'*64),('stable_class_sizes',[1,1])]:
        z=copy.deepcopy(base);z[key]=val;mutations.append(z)
    z=copy.deepcopy(base);z['programs'][0]['root_repetitions']+=1;mutations.append(z)
    for z in mutations:
        try:verify_family(z)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,scopes=scopes,mixed_scopes=mixed,sharp_families=families,non_sc_original_monoid_transformations=boundary,corruptions_rejected=len(mutations),
             all_binary_inputs=sum(z['all_labeled_binary_inputs'] for z in scopes),sc_inputs=sum(z['strongly_connected'] for z in scopes),
             full_original_monoid_transformations=sum(z['full_original_monoid_transformations'] for z in scopes),all_minimum_rank_transformations_checked=sum(z['all_minimum_rank_transformations_checked'] for z in scopes),
             maximum_n=max(z['n'] for z in families),unit_original_state_letter_controls=sum(z['unit_original_state_letter_controls'] for z in families),
             root_original_state_letter_controls=sum(z['root_original_state_letter_controls'] for z in families),literal_whole_rank_word_state_letter_controls=sum(z['literal_whole_rank_word_state_letter_controls'] for z in families),
             mixed_all_binary_inputs=sum(z['all_binary_inputs'] for z in mixed),mixed_sc_inputs=sum(z['sc_inputs'] for z in mixed),
             mixed_full_original_monoid_transformations=sum(z['full_original_monoid_transformations'] for z in mixed),uniform_minimum_word_kernel_orbit_controls=sum(z['uniform_minimum_word_kernel_orbit_controls'] for z in mixed),
             boundary='PROVED paper SC defect-one kernel stability, SC all-corank<=1 canonical group quotient and unique minimum-rank kernel; class-size range<=singular-letter count, sharp EVERY s>=1. Independent complete monoids and finite family controls are COMPUTATIONALLY VERIFIED only in recorded scopes. No formal theorem, publication priority or unrestricted reset bound; general Cerny OPEN.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k not in ('scopes','mixed_scopes','sharp_families')}),flush=True)


if __name__=='__main__':main()
