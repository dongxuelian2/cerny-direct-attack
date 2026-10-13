"""Actual membership, all-word shortest phases and independent global policy audit."""
from collections import deque
from copy import deepcopy
import json
from pathlib import Path


def compose(u,v):
    return [v[q] for q in u]


def power(row,t):
    out=list(range(len(row)))
    while t:
        if t&1:
            out=compose(out,row)
        row=compose(row,row)
        t//=2
    return out


def bits(qs):
    return sum(1<<q for q in qs)


def apply(S,row):
    return bits(set(row[q] for q in range(len(row)) if S>>q&1))


def inverse(S,row):
    return bits(q for q,t in enumerate(row) if S>>t&1)


def first_inverse_a(S,p):
    C=S&((1<<p)-1)
    D=S>>p
    return ((C>>1)|((C&1)<<(p-1)))|(((D>>1)|((D&1)<<p))<<p)


def inverse_b(S,p,k):
    lo=(1<<k)-1
    coordinates=((S>>p)&lo)|(S&(((1<<p)-1)^lo))
    return coordinates|(coordinates<<p)|((1<<(2*p)) if coordinates&1 else 0)


def B(j,p):
    interval=(1<<j)-1
    return interval|(interval<<p)|(1<<(2*p))


def H(j,t,p):
    interval=((1<<j)-1)<<t
    return interval|(interval<<p)


def graph(rows):
    n=len(rows['a'])
    full=(1<<n)-1
    dist={full:0}
    todo=deque([full])
    while todo:
        S=todo.popleft()
        for row in rows.values():
            T=apply(S,row)
            if T not in dist:
                dist[T]=dist[S]+1
                todo.append(T)
    return dist


def inverse_policy(rows,R):
    """Per-target reverse BFS; collect ALL shortest larger-parent ties."""
    full=(1<<len(rows['a']))-1
    G={full:0}
    E={}
    visited=0
    for S in sorted(R,key=lambda X:(-X.bit_count(),X)):
        if S==full:
            continue
        k=S.bit_count()
        parents=[U for U in G if U.bit_count()>k]
        parents.sort(key=lambda U:G[U])
        todo=deque([S])
        dist={S:0}
        depth=None
        tail=None
        while todo:
            T=todo.popleft()
            if depth is not None and dist[T]>depth:
                break
            if T.bit_count()>k:
                selected=next((U for U in parents if U&~T==0),None)
                if selected is not None:
                    depth=dist[T]
                    tail=G[selected] if tail is None else min(tail,G[selected])
            if depth is not None:
                continue
            for row in rows.values():
                U=inverse(T,row)
                if U not in dist:
                    dist[U]=dist[T]+1
                    todo.append(U)
        assert depth is not None and depth>0 and tail is not None
        visited+=len(dist)
        E[S]=depth
        G[S]=depth+tail
    return E,G,visited


def build_chain(p):
    n=2*p+1
    s,k=p//2,(p+1)//2
    a=[(q+1)%p if q<p else p+(q-p+1)%(p+1) for q in range(n)]
    b=[]
    for q in range(n):
        i=q if q<p else (q-p)%p
        b.append(p+i if i<k else i)
    rows={'a':a,'b':b}
    full=(1<<n)-1
    if p==2:
        parent=(1<<0)|(1<<p)
        stages=[dict(target=1<<p,parent=parent,a_count=0,word='b',cost=1,kind='seed'),
                dict(target=parent,parent=full,a_count=3,word='baaa',cost=4,kind='terminal')]
        assert apply(parent,b)==1<<p and apply(full,compose(b,power(a,3)))==parent
        action=list(range(n))
        for x in 'baaab':
            action=compose(action,rows[x])
        assert set(action)=={p}
        return dict(p=p,n=n,rows=rows,stages=stages,cost=5,membership_controls=1,dominance_controls=0)
    d=compose(power(a,p+1),b)
    f=compose(power(a,p),b)
    membership=0
    # Actuality is checked by independent charged whole reach words,
    # rather than inferred from containment of a policy predecessor.
    for j in range(1,k):
        r=compose(compose(compose(b,power(d,s-j)),power(f,k-j-1)),power(a,(j+1)*(p+1)-1))
        assert apply(full,r)==B(j,p)
        membership+=1
    for j in range(2,s+1):
        t=k-j
        r=compose(compose(compose(b,power(d,s-j)),power(f,k-j)),power(a,j*(p+1)+t))
        assert apply(full,r)==H(j,t,p)
        membership+=1
    stages=[dict(target=1<<p,parent=B(1,p),a_count=0,word='b',cost=1,kind='seed')]
    current=B(1,p)
    j=1
    dominance=0
    while current.bit_count()<p:
        if current==B(j,p):
            L=p-k+j+1
            parent=H(j+1,k-j-1,p)
            X=current
            for t in range(L):
                assert inverse_b(X,p,k)&~X==0
                X=first_inverse_a(X,p)
                dominance+=1
            assert parent&~inverse_b(X,p,k)==0
            word='b'+'a'*L
            cost=L+1
            kind='odd'
            j+=1
        else:
            assert current==H(j,k-j,p)
            L=k-j
            parent=B(j,p)
            X=current
            for t in range(L):
                assert inverse_b(X,p,k)==X
                X=first_inverse_a(X,p)
                dominance+=1
            assert inverse_b(X,p,k)==parent
            word='b'+'a'*L
            cost=L+1
            kind='even'
        assert parent.bit_count()>current.bit_count() and parent.bit_count()<=p
        assert apply(parent,compose(b,power(a,L)))&~current==0
        stages.append(dict(target=current,parent=parent,a_count=L,word=word,cost=cost,kind=kind))
        current=parent
    if p%2:
        assert current==B(s,p)
        M=(p*p+3*p)//2-k
    else:
        assert current==H(s,0,p)
        M=s*(p+1)
        # Coordinate first-stall lower inequality for this terminal target.
        delta=[p-i+1+(p if i>=k else 0) for i in range(p)]
        base=(k-1)*(p+1)
        for t in range(k*p+1,M):
            i=(-1-t)%p
            assert t<base+delta[i]
    assert apply(full,compose(b,power(a,M)))==current
    stages.append(dict(target=current,parent=full,a_count=M,word='b'+'a'*M,cost=M+1,kind='terminal'))
    # Compose the ENTIRE reset in actual right-action order. Each image
    # may be strict inside its nominal target; only monotone containment
    # is used when the next phase is applied.
    common=full
    expected=full
    for phase in reversed(stages):
        assert phase['parent']==expected
        row=compose(b,power(a,phase['a_count']))
        common=apply(common,row)
        assert common&~phase['target']==0
        expected=phase['target']
    assert common==1<<p
    cost=sum(z['cost'] for z in stages)
    assert cost==p*p+p-k-1 < (n-1)**2
    if p<=24:
        word=''.join(z['word'] for z in reversed(stages))
        assert len(word)==cost
        action=list(range(n))
        for x in word:
            action=compose(action,rows[x])
        assert set(action)=={p}
    return dict(p=p,n=n,rows=rows,stages=stages,cost=cost,
                membership_controls=membership,dominance_controls=dominance)


def verify(z):
    expected=build_chain(z['p'])
    assert z==expected


def main():
    data=Path('scripts/direct_attack/data')
    family=json.loads((data/'direct_binary_image_obstruction.json').read_text())
    parameters=[z['p'] for z in family['records']]
    assert parameters==list(range(2,65))+[65,100,128,256,512,1024]
    controls=[build_chain(p) for p in parameters]
    small=[]
    for p in range(2,7):
        z=next(z for z in controls if z['p']==p)
        dist=graph(z['rows'])
        E,G,count=inverse_policy(z['rows'],dist)
        for phase in z['stages']:
            assert phase['target'] in dist and phase['parent'] in dist
            assert E[phase['target']]==phase['cost']
        P=min(G[1<<q] for q in range(z['n']))
        assert P==z['cost']
        small.append(dict(p=p,n=z['n'],images=len(dist),inverse_vertices=count,P=P,
                          rt=min(v for S,v in dist.items() if S.bit_count()==1)))
    corruptions=[]
    base=next(z for z in controls if z['p']==6)
    edits=[('phase parent',lambda z:z['stages'][1].__setitem__('parent',z['stages'][1]['parent']^1)),
           ('phase length',lambda z:z['stages'][1].__setitem__('cost',z['stages'][1]['cost']-1)),
           ('terminal length',lambda z:z['stages'][-1].__setitem__('cost',z['stages'][-1]['cost']-1)),
           ('total length',lambda z:z.__setitem__('cost',z['cost']-1))]
    for name,edit in edits:
        damaged=deepcopy(base)
        edit(damaged)
        try:
            verify(damaged)
        except AssertionError:
            corruptions.append(name)
        else:
            raise AssertionError('accepted corruption '+name)
    out=dict(verified=True,parameters=parameters,controls=controls,literal_whole_chain_controls=23,
             membership_controls=sum(z['membership_controls'] for z in controls),
             dominance_controls=sum(z['dominance_controls'] for z in controls),
             complete_small_policy_scopes=small,
             corruptions_rejected=corruptions,
             status='PROVED paper compatible genuinely-shortest policy upper for all p; exact equality P=upper only COMPUTATIONALLY VERIFIED in saved small scopes; arbitrary-p equality CONJECTURED; general Cerny and policy square OPEN; no formal kernel')
    (data/'direct_binary_policy_chain_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,controls=len(controls),literal_whole_chain_controls=23,membership_controls=out['membership_controls'],
                         dominance_controls=out['dominance_controls'],small_policy_scopes=small,
                         corruptions_rejected=corruptions)),flush=True)


if __name__=='__main__':
    main()
