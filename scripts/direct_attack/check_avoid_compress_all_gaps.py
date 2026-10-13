"""Independent cell-error identity, BFS, rooted graph and original reset words."""
import argparse
from collections import deque
import copy
from hashlib import sha256
import json
from pathlib import Path
from direct_attack.check_avoid_compress_sharp_faces import image,compose_word,power,exact,check_sc,as_set


def independent(r,g,k):
    M=k*g+1;n=r+M+1;U=list(range(r+1,n));core=[0]+U[:g]+list(range(r,0,-1))
    a=list(range(n));b=[None]*n
    for i,q in enumerate(U):a[q]=U[(i+1)%M]
    for i,q in enumerate(core):b[q]=core[(i+1)%len(core)]
    for q in U[g:-1]:
        j=q-r;b[q]=r if j%g==0 else q+1
    b[U[-1]]=U[g]
    color=list(range(r+1))+[r+1+(i%g) for i in range(M)]
    ta=list(range(r+g+1));tb=ta[:]
    for i in range(g):ta[r+1+i]=r+1+(i+1)%g
    cellcore=[0]+list(range(r+1,r+g+1))+list(range(r,0,-1))
    for i,q in enumerate(cellcore):tb[q]=cellcore[(i+1)%len(cellcore)]
    return [a,b],frozenset(core),frozenset(range(r)),color,[ta,tb]


def cell_distance(transitions,start,targets):
    ds={start:0};todo=deque([start])
    while todo:
        q=todo.popleft()
        if q in targets:return ds[q]
        for row in transitions:
            t=row[q]
            if t not in ds:ds[t]=ds[q]+1;todo.append(t)
    raise AssertionError('cell unreachable')


def verify(z):
    r,g,k=z['A_size'],z['g'],z['k'];assert r>=1 and g>=2 and k>=2
    M=k*g+1;n=r+M+1;s=r+g+1;assert n==z['n'] and M==z['M']
    rs,S,A,color,trans=independent(r,g,k);Q=frozenset(range(n));check_sc(rs)
    assert as_set(z['S'])==S and as_set(z['A'])==A
    assert z['rows_sha256']==sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest()
    if z['explicit_rows'] is not None:assert z['explicit_rows']==rs
    # Verify the exact n-by-s error identity using sparse unit rows.
    for a,row in enumerate(rs):
        assert sorted(trans[a])==list(range(s))
        for q,t in enumerate(row):
            actual=[0]*s;expected=[0]*s;actual[color[t]]=1;expected[trans[a][color[q]]]=1
            if q==n-1:expected[r+1]+=1;expected[r+2]-=1
            assert actual==expected
    assert cell_distance(trans,r+1,{r+g})==g-1
    assert cell_distance(trans,r+2,A)==g
    assert cell_distance(trans,r+1,A)==g+1
    fibers={q:frozenset(p for p,t in enumerate(rs[1]) if t==q) for q in range(n)}
    collisions=[C for C in fibers.values() if len(C)>1]
    assert collisions==[frozenset(r+j for j in range(g,M,g))]
    assert all(color[q]==r+g for q in collisions[0]) and len(set(rs[0]))==n
    assert z['reachable_word']==[1]*(g+1) and image(Q,compose_word(rs,z['reachable_word']))==S
    ac,v,e=exact(rs,S,A);assert ac==z['ac']==M+1 and v==z['avoid_compress_vertices']
    for w in (z['first_success_word'],z['attaining_word']):
        T=image(S,compose_word(rs,w));assert len(w)==ac and (not A<=T or len(T)<len(S))
    assert z['attaining_word']==[0]*(M-1)+[1,1]
    T=image(S,compose_word(rs,z['attaining_word']));assert r-1 not in T and len(T)==s
    c=z['macro_c'];assert c==[0]*(M-1)+[1]*s;cr=compose_word(rs,c)
    assert all(cr[q]==q for q in range(r+1)) and cr[r+1]==0
    assert all(cr[q]==q-1 for q in range(r+2,r+g+1))
    word=z['rooted_word'];assert word==c*g+[1];vr=compose_word(rs,word);root=r+1
    assert root==z['root'] and vr[root]==root
    pred={q:[] for q in S}
    for q in S:assert vr[q] in S;pred[vr[q]].append(q)
    height={root:0};todo=deque([root])
    while todo:
        q=todo.popleft()
        for t in pred[q]:
            if t not in height:height[t]=height[q]+1;todo.append(t)
    assert set(height)==S and max(height.values())==z['rooted_height']==r+1
    assert len(image(image(Q,compose_word(rs,[1]*(g+1))),power(vr,r+1)))==1
    length=g+1+(r+1)*len(word);assert length==z['reset_length']==g+1+(r+1)*(g*(n+g-1)+1)
    literal=z['literal_reset_word'];letters=0
    if literal is not None:
        assert literal==[1]*(g+1)+word*(r+1) and len(literal)==length
        assert len(image(Q,compose_word(rs,literal)))==1;letters=length
    extra={};finite=z['finite_exact_reset']
    if finite is not None:
        rt,j,f=exact(rs,Q);assert rt==finite['rt'] and j==finite['vertices']
        assert len(finite['word'])==rt and len(image(Q,compose_word(rs,finite['word'])))==1
        extra=dict(rt=rt,full_reset_vertices=j)
    return dict(n=n,A_size=r,g=g,k=k,ac=ac,safe_vertices=v,safe_edges=e,cell_identity_controls=2*n,
                original_macro_state_letter_controls=n*(len(c)+len(word)),rooted_states=len(height),literal_reset_letters=letters,**extra)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('scripts/direct_attack/data/avoid_compress_all_gaps.json'))
    ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/avoid_compress_all_gaps_checks.json'))
    args=ap.parse_args();data=json.loads(args.source.read_text());reports=[verify(z) for z in data['records']]
    base=data['records'][0];mutations=[]
    for key,value in [('ac',base['ac']-1),('root',0),('rooted_height',base['rooted_height']+1),('rows_sha256','0'*64),('reset_length',0),('attaining_word',[0]*base['ac'])]:
        b=copy.deepcopy(base);b[key]=value;mutations.append(b)
    b=copy.deepcopy(base);b['rooted_word']=[0]*len(b['rooted_word']);mutations.append(b)
    b=copy.deepcopy(base);b['finite_exact_reset']['rt']-=1;mutations.append(b)
    b=copy.deepcopy(base);b['explicit_rows'][1][-1]=r if (r:=b['A_size']) else 0;mutations.append(b)
    for b in mutations:
        try:verify(b)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,parameters=len(reports),maximum_n=max(z['n'] for z in reports),maximum_g=max(z['g'] for z in reports),reports=reports,
             safe_vertices=sum(z['safe_vertices'] for z in reports),safe_edges=sum(z['safe_edges'] for z in reports),
             cell_identity_controls=sum(z['cell_identity_controls'] for z in reports),
             original_macro_state_letter_controls=sum(z['original_macro_state_letter_controls'] for z in reports),
             rooted_states=sum(z['rooted_states'] for z in reports),literal_reset_letters=sum(z['literal_reset_letters'] for z in reports),
             full_reset_scopes=sum('rt' in z for z in reports),full_reset_vertices=sum(z.get('full_reset_vertices',0) for z in reports),corruptions_rejected=len(mutations),
             boundary='PROVED paper r>=1 g>=2 k>=2; only listed g>=3 finite scopes newly checked; fixed-cardinality infinite progressions sharp, remaining n and general Cerny OPEN; no formal kernel')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='reports'}),flush=True)


if __name__=='__main__':main()
