"""Independent set BFS, full original macro rows, SC, and reset verification."""
import argparse
from collections import deque
import copy
from hashlib import sha256
import json
from pathlib import Path


def independent(n,r,gap):
    if gap==1:
        outside=list(range(n-r));anchors=list(range(n-r,n));core=[outside[0]]+anchors
        successor={q:core[(i+1)%len(core)] for i,q in enumerate(core)}
        rs=[[q+1 if q in outside else q for q in range(n)],
            [successor.get(q,anchors[0]) for q in range(n)]]
        S=frozenset(core);A=frozenset(anchors)
    else:
        assert gap==2 and r<=n-3
        A=frozenset(range(r));U=list(range(r,n));M=len(U)
        rs=[list(range(n)),[0]*n]
        cycle=U if M%2 else U[1:]
        for i,q in enumerate(cycle):rs[0][q]=cycle[(i+1)%len(cycle)]
        if M%2==0:rs[0][U[0]]=U[1]
        for q in A:rs[1][q]=q+1
        for i,q in enumerate(U):rs[1][q]=0 if i%2==(0 if M%2 else 1) else U[1]
        if M%2==0:rs[1][U[0]]=U[1]
        S=A|frozenset(U[:2])
    return rs,S,A


def image(S,row):return frozenset(row[q] for q in S)
def as_set(mask):return frozenset(q for q in range(mask.bit_length()) if mask>>q&1)


def compose_word(rs,word):
    out=list(range(len(rs[0])))
    for a in word:
        assert type(a)==int and 0<=a<len(rs)
        out=[rs[a][q] for q in out]
    return out


def power(row,k):
    out=list(range(len(row)))
    while k:
        if k&1:out=[row[q] for q in out]
        row=[row[q] for q in row];k//=2
    return out


def exact(rs,start,A=None):
    todo=deque([start]);dist={start:0};size=len(start);edges=0
    while todo:
        S=todo.popleft()
        if (A is None and len(S)==1) or (A is not None and (len(S)<size or not A<=S)):
            return dist[S],len(dist),edges
        for row in rs:
            edges+=1;T=image(S,row)
            if T not in dist:dist[T]=dist[S]+1;todo.append(T)
    raise AssertionError('not synchronizing')


def check_sc(rs):
    n=len(rs[0]);graphs=[[[] for _ in range(n)] for _ in range(2)]
    for row in rs:
        for q,t in enumerate(row):graphs[0][q].append(t);graphs[1][t].append(q)
    for graph in graphs:
        seen={0};todo=[0]
        for q in todo:
            for t in graph[q]:
                if t not in seen:seen.add(t);todo.append(t)
        assert len(seen)==n


def verify(z):
    n,r,gap=z['n'],z['A_size'],z['gap'];assert gap in (1,2) and 1<=r<n
    rs,S,A=independent(n,r,gap);Q=frozenset(range(n))
    assert z['S']==sum(1<<q for q in S) and z['A']==sum(1<<q for q in A)
    assert len(A)==r and len(S)==r+gap and A<S
    assert z['rows_sha256']==sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest()
    if z['explicit_rows'] is not None:assert z['explicit_rows']==rs
    check_sc(rs)
    assert z['reachable_word']==[1] and image(Q,compose_word(rs,z['reachable_word']))==S
    ac,vertices,edges=exact(rs,S,A)
    assert ac==z['ac']==n-r and vertices==z['avoid_compress_vertices']
    for word in (z['first_success_word'],z['attaining_word']):
        assert len(word)==ac
        T=image(S,compose_word(rs,word));assert len(T)<len(S) or not A<=T
    program=z['reset_program'];h,t=program['h'],program['t'];M=n-r
    assert program['loops']==r-1 if gap==1 else program['loops']==r
    assert program['power']==r and program['initial']==([] if gap==1 else [1])
    assert h==([0]*M if gap==1 else [0]*(M-1)+[1])
    assert t==([0,1] if gap==2 and M%2 else [1])
    hr,tr=compose_word(rs,h),compose_word(rs,t)
    if gap==1:
        core=[0]+list(range(M,n));assert [tr[q] for q in core]==core[1:]+core[:1]
        assert hr[0]==core[1] and all(hr[q]==q for q in core[1:])
    else:
        core=list(range(r+2));assert [tr[q] for q in core]==core[1:]+core[:1]
        assert hr[r]==hr[r+1]==0 and all(hr[q]==tr[q] for q in range(r))
    R=image(Q,compose_word(rs,program['initial']));R=image(R,hr)
    tp=power(tr,program['power'])
    for _ in range(program['loops']):R=image(image(R,tp),hr)
    assert len(R)==1
    length=len(program['initial'])+len(h)*(1+program['loops'])+len(t)*program['power']*program['loops']
    assert length==z['reset_length']==(r*(n-1) if gap==1 else 1+(r+1)*M+r*r*len(t))
    literal=z['literal_reset_word'];letters=0
    if literal is not None:
        assert literal==program['initial']+h+(t*r+h)*program['loops'] and len(literal)==length
        assert len(image(Q,compose_word(rs,literal)))==1;letters=len(literal)
    finite=z['finite_exact_reset'];extra={}
    if finite is not None:
        rt,v,e=exact(rs,Q);assert finite['rt']==rt and finite['vertices']==v
        assert len(finite['word'])==rt and len(image(Q,compose_word(rs,finite['word'])))==1
        extra=dict(rt=rt,full_reset_vertices=v,full_reset_edges=e)
    return dict(n=n,A_size=r,gap=gap,ac=ac,safe_bfs_vertices=vertices,safe_bfs_edges=edges,
                macro_state_letter_controls=n*(len(h)+len(t)),literal_reset_letters=letters,**extra)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('scripts/direct_attack/data/avoid_compress_sharp_faces.json'))
    ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/avoid_compress_sharp_faces_checks.json'))
    args=ap.parse_args();z=json.loads(args.source.read_text());reports=[verify(a) for a in z['records']]
    base=next(a for a in z['records'] if a['n']==8 and a['A_size']==2 and a['gap']==2)
    mutations=[]
    for key,value in [('ac',5),('S',7),('A',1),('reset_length',31),('rows_sha256','0'*64),('attaining_word',[0]*6)]:
        b=copy.deepcopy(base);b[key]=value;mutations.append(b)
    b=copy.deepcopy(base);b['reset_program']['power']=1;mutations.append(b)
    b=copy.deepcopy(base);b['finite_exact_reset']['rt']-=1;mutations.append(b)
    b=copy.deepcopy(base);b['literal_reset_word']=[0]*base['reset_length'];mutations.append(b)
    for b in mutations:
        try:verify(b)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,parameters=len(reports),maximum_n=max(a['n'] for a in reports),reports=reports,
             safe_bfs_vertices=sum(a['safe_bfs_vertices'] for a in reports),safe_bfs_edges=sum(a['safe_bfs_edges'] for a in reports),
             macro_state_letter_controls=sum(a['macro_state_letter_controls'] for a in reports),
             literal_reset_letters=sum(a['literal_reset_letters'] for a in reports),
             full_reset_scopes=sum('rt' in a for a in reports),full_reset_vertices=sum(a.get('full_reset_vertices',0) for a in reports),
             corruptions_rejected=len(mutations),boundary='all-n proof is paper; exact ac and original-word certificates checked only listed parameters; finite rt only n<=10; no formal kernel; Cerny OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='reports'}),flush=True)


if __name__=='__main__':main()
