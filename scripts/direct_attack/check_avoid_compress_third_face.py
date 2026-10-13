"""Independent cycle/branches, ordinary subset BFS, and rooted reset graph."""
import argparse
from collections import deque
import copy
from hashlib import sha256
import json
from pathlib import Path
from direct_attack.check_avoid_compress_sharp_faces import image,compose_word,power,exact,check_sc,as_set


def independent(r,M):
    n=r+M+1;U=list(range(r+1,n));core=[0,U[0],U[1]]+list(range(r,0,-1))
    a=list(range(n));b=[None]*n
    for i,q in enumerate(U):a[q]=U[(i+1)%M]
    for i,q in enumerate(core):b[q]=core[(i+1)%len(core)]
    for i,q in enumerate(U[2:],2):
        if i==M-1:b[q]=U[2]
        elif i%2:b[q]=r
        else:b[q]=U[i+1]
    return [a,b],frozenset(core),frozenset(range(r)),core


def verify(z):
    r,M,n=z['A_size'],z['M'],z['n'];assert r>=1 and M>=5 and M%2 and n==r+M+1
    rs,S,A,core=independent(r,M);Q=frozenset(range(n));s=r+3
    assert as_set(z['S'])==S and as_set(z['A'])==A and len(S)==r+3
    assert z['rows_sha256']==sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest()
    if z['explicit_rows'] is not None:assert z['explicit_rows']==rs
    check_sc(rs);assert len(set(rs[0]))==n and len(set(rs[1]))==r+1+(M+3)//2<n
    assert z['reachable_word']==[1]*3 and image(Q,compose_word(rs,z['reachable_word']))==S
    ac,vertices,edges=exact(rs,S,A)
    assert ac==z['ac']==M+1 and vertices==z['avoid_compress_vertices']
    for word in (z['first_success_word'],z['attaining_word']):
        assert len(word)==ac
        T=image(S,compose_word(rs,word));assert not A<=T or len(T)<len(S)
    target=image(S,compose_word(rs,z['attaining_word']))
    assert z['attaining_word']==[0]*(M-1)+[1,1] and len(target)==s and r-1 not in target
    c=z['macro_c'];assert c==[0]*(M-1)+[1]*s
    cr=compose_word(rs,c)
    assert all(cr[q]==q for q in range(r+1)) and cr[r+1]==0 and cr[r+2]==r+1
    v=z['rooted_word'];assert v==c+c+[1];vr=compose_word(rs,v)
    root=r+1;assert root==z['root'] and vr[root]==root
    pred={q:[] for q in S}
    for q in S:assert vr[q] in S;pred[vr[q]].append(q)
    height={root:0};todo=deque([root])
    while todo:
        q=todo.popleft()
        for t in pred[q]:
            if t not in height:height[t]=height[q]+1;todo.append(t)
    assert set(height)==S and max(height.values())==z['rooted_height']==r+1
    assert len(image(image(Q,compose_word(rs,[1]*3)),power(vr,r+1)))==1
    length=3+(r+1)*len(v);assert length==z['reset_length']==3+(r+1)*(2*n+3)
    literal=z['literal_reset_word'];letters=0
    if literal is not None:
        assert literal==[1]*3+v*(r+1) and len(literal)==length
        assert len(image(Q,compose_word(rs,literal)))==1;letters=length
    extra={};finite=z['finite_exact_reset']
    if finite is not None:
        rt,k,e=exact(rs,Q);assert rt==finite['rt'] and k==finite['vertices']
        assert len(finite['word'])==rt and len(image(Q,compose_word(rs,finite['word'])))==1
        extra=dict(rt=rt,full_reset_vertices=k)
    return dict(n=n,A_size=r,M=M,ac=ac,safe_bfs_vertices=vertices,safe_bfs_edges=edges,
                original_macro_state_letter_controls=n*(len(c)+len(v)),rooted_states=len(height),literal_reset_letters=letters,**extra)


def counter(z):
    rs=z['rows'];assert rs==[[2,0,5,1,3,1],[0,1,3,2,4,4]]
    Q=frozenset(range(6));S=as_set(z['S']);A=as_set(z['A']);check_sc(rs)
    assert S==frozenset(range(4)) and A==frozenset([0])
    assert image(Q,compose_word(rs,z['reachable_word']))==S
    ac,k,e=exact(rs,S,A);rt,v,f=exact(rs,Q)
    assert ac==z['ac']==5 and k==z['safe_vertices'] and rt==z['rt']==18 and v==z['full_reset_vertices']
    assert ac>z['refuted_bound']==6-len(S)+2
    assert len(z['attaining_word'])==ac and (not A<=image(S,compose_word(rs,z['attaining_word'])) or len(image(S,compose_word(rs,z['attaining_word'])))<len(S))
    assert len(z['reset_word'])==rt and len(image(Q,compose_word(rs,z['reset_word'])))==1
    return dict(verified=True,ac=ac,rt=rt,safe_vertices=k,safe_edges=e,full_vertices=v,full_edges=f)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('scripts/direct_attack/data/avoid_compress_third_face.json'))
    ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/avoid_compress_third_face_checks.json'))
    args=ap.parse_args();data=json.loads(args.source.read_text());reports=[verify(z) for z in data['records']];c=counter(data['finite_counterexample'])
    base=next(z for z in data['records'] if z['A_size']==1 and z['M']==5);mutations=[]
    for key,value in [('ac',5),('root',0),('rooted_height',3),('S',7),('reset_length',36),('rows_sha256','0'*64),('attaining_word',[0]*6)]:
        b=copy.deepcopy(base);b[key]=value;mutations.append(b)
    b=copy.deepcopy(base);b['rooted_word']=[0]*len(b['rooted_word']);mutations.append(b)
    b=copy.deepcopy(base);b['finite_exact_reset']['rt']-=1;mutations.append(b)
    for b in mutations:
        try:verify(b)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,parameters=len(reports),maximum_n=max(z['n'] for z in reports),reports=reports,finite_counterexample=c,
             safe_bfs_vertices=sum(z['safe_bfs_vertices'] for z in reports),safe_bfs_edges=sum(z['safe_bfs_edges'] for z in reports),
             original_macro_state_letter_controls=sum(z['original_macro_state_letter_controls'] for z in reports),
             rooted_states=sum(z['rooted_states'] for z in reports),literal_reset_letters=sum(z['literal_reset_letters'] for z in reports),
             full_reset_scopes=sum('rt' in z for z in reports),full_reset_vertices=sum(z.get('full_reset_vertices',0) for z in reports),
             corruptions_rejected=len(mutations),boundary='PROVED paper r>=1 odd M>=5; listed exact ac and charged original-word reset certificates COMPUTATIONALLY VERIFIED; missing parity OPEN; no formal kernel; Cerny OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='reports'}),flush=True)


if __name__=='__main__':main()
