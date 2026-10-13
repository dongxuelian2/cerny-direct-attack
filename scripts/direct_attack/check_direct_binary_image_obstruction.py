"""Original rows, independent weighted stall BFS and ordinary subset/preimage BFS."""
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


def evaluate(word,rows):
    f=list(range(len(rows['a'])))
    for x in word:
        f=compose(f,rows[x])
    return f


def image(S,row):
    out=0
    while S:
        bit=S&-S
        out|=1<<row[bit.bit_length()-1]
        S-=bit
    return out


def preimage(S,row):
    return sum(1<<q for q,t in enumerate(row) if S>>t&1)


def forward(rows):
    full=(1<<len(rows['a']))-1
    dist={full:0}
    todo=deque([full])
    while todo:
        S=todo.popleft()
        for row in rows.values():
            T=image(S,row)
            if T not in dist:
                dist[T]=dist[S]+1
                todo.append(T)
    return dist


def reverse(T,rows):
    full=(1<<len(rows['a']))-1
    dist={T:0}
    todo=deque([T])
    while todo:
        S=todo.popleft()
        if S==full:
            return dist[S],len(dist)
        for row in rows.values():
            R=preimage(S,row)
            if R not in dist:
                dist[R]=dist[S]+1
                todo.append(R)
    raise AssertionError('no full actual parent reached')


def connected(rows):
    n=len(rows['a'])
    edges=[set(row[q] for row in rows.values()) for q in range(n)]
    back=[set() for q in range(n)]
    for q in range(n):
        for t in edges[q]:
            back[t].add(q)
    for adj in (edges,back):
        seen={0}
        todo=deque([0])
        while todo:
            q=todo.popleft()
            for t in adj[q]-seen:
                seen.add(t)
                todo.append(t)
        assert len(seen)==n


def first_stall_counts(rows,p):
    n=2*p+1
    back=[[] for q in range(n)]
    for x,row in rows.items():
        for q,t in enumerate(row):
            back[t].append((q,int(x=='a')))
    inf=10**12
    dist=[inf]*n
    dist[2*p]=0
    todo=deque([2*p])
    while todo:
        t=todo.popleft()
        for q,cost in back[t]:
            if dist[q]>dist[t]+cost:
                dist[q]=dist[t]+cost
                if cost:
                    todo.append(q)
                else:
                    todo.appendleft(q)
    assert dist[p]+1==p+1
    return [dist[q]+1 for q in range(p)]


def validate(z):
    p=z['p']
    assert p>=2
    n=2*p+1
    s=p//2
    k=p-s
    rows=z['rows']
    assert z['n']==n and z['s']==s and z['k']==k
    a=[]
    for q in range(n):
        a.append((q+1)%p if q<p else p+((q-p+1)%(p+1)))
    pi=[q if q<p else (q-p)%p for q in range(n)]
    b=[p+i if i<k else i for i in pi]
    assert rows==dict(a=a,b=b)
    assert len(set(a))==n and len(set(b))==p and compose(b,b)==b
    E=set(b)
    assert z['initial_image']==sorted(E)
    assert set(b[q] for q in E)==E and len(E)>1
    connected(rows)
    for x,row in rows.items():
        for q,t in enumerate(row):
            assert (pi[t]-pi[q])%p==((1-int(q==2*p))%p if x=='a' else 0)
    assert [q for q,t in enumerate(b) if t==2*p]==[]
    assert [q for q,t in enumerate(a) if t==2*p]==[2*p-1]
    counts=first_stall_counts(rows,p)
    expected=[p-i+1+(p if i>=k else 0) for i in range(p)]
    assert counts==z['first_stall_a_counts']==expected
    assert min(counts)==p-k+2
    A=set(range(s,p)) if p%2==0 else set(range(s))
    T={q for q in range(n) if pi[q] in A}
    assert len(T)==p and z['projected_target']==sorted(A) and z['target']==sorted(T)
    M=(p*p+3*p)//2-k
    assert z['entering_a_count']==M and z['image_extension']==M+1
    low=k*p+1
    base=(k-1)*(p+1)
    alpha=min(A)
    feasible=[]
    for t in range(low,low+p):
        i=(alpha-1-t)%p
        if t>=base+counts[i]:
            feasible.append(t)
    assert feasible and min(feasible)==M
    entering=compose(b,power(a,M))
    assert set(entering)==T
    d=compose(power(a,p+1),b)
    e=compose(power(a,p),b)
    assert all(d[p+j]==p+j for j in range(k))
    assert [d[i] for i in range(k,p)]==list(range(k+1,p))+[p]
    assert [e[p+j] for j in range(k)]==[p]+[p+j-1 for j in range(1,k)]
    reset=compose(compose(b,power(d,p-k)),power(e,k-1))
    assert set(reset)=={p}
    assert z['reset_first_macro_a']==p+1 and z['reset_first_macro_repetitions']==p-k
    assert z['reset_second_macro_a']==p and z['reset_second_macro_repetitions']==k-1
    assert z['reset_upper_bound']==1+(p+2)*(p-k)+(p+1)*(k-1)==p*p+p-k <= (n-1)**2
    assert z['reset_lower_bound']==(p-2)*(p+1)+min(counts)+1==p*p-k+1
    if p<=24:
        assert z['literal_entering_word']=='b'+'a'*M
        r='b'+('a'*(p+1)+'b')*(p-k)+('a'*p+'b')*(k-1)
        assert z['literal_reset_word']==r
        assert len(r)==z['reset_upper_bound'] and set(evaluate(r,rows))=={p}
        assert len(z['literal_entering_word'])==z['image_extension']
        assert set(evaluate(z['literal_entering_word'],rows))==T
    if p==6:
        extra=z['extra_finite_target']
        assert extra['actual_word']=='b'+'a'*27 and extra['image_extension']==28
        assert set(evaluate(extra['actual_word'],rows))==set(extra['target'])
        assert len(extra['target'])==p
    return T


def main():
    data=Path('scripts/direct_attack/data')
    source=json.loads((data/'direct_binary_image_obstruction.json').read_text())
    records=source['records']
    assert [z['p'] for z in records]==list(range(2,65))+[65,100,128,256,512,1024]
    scopes=source['scopes']
    assert scopes['literal_parameters']==list(range(2,25))
    assert scopes['forward_parameters']==scopes['inverse_parameters']==list(range(2,13))
    assert scopes['maximum_n']==2049
    for z in records:
        validate(z)
    index={z['p']:z for z in records}
    exact=[]
    for p in scopes['forward_parameters']:
        z=index[p]
        T=sum(1<<q for q in z['target'])
        dist=forward(z['rows'])
        full=(1<<z['n'])-1
        assert all(S==full or S.bit_count()<=p for S in dist)
        assert [S for S in dist if S.bit_count()>p]==[full]
        assert T in dist
        into=min(v for S,v in dist.items() if S&~T==0)
        inv,vertices=reverse(T,z['rows'])
        assert into==inv==z['image_extension']
        rt=min(v for S,v in dist.items() if S.bit_count()==1)
        assert z['reset_lower_bound']<=rt<=z['reset_upper_bound']
        record=dict(p=p,n=z['n'],forward_vertices=len(dist),inverse_vertices=vertices,
                    image_extension=into,rt=rt)
        if p==6:
            extra=sum(1<<q for q in z['extra_finite_target']['target'])
            value=min(v for S,v in dist.items() if S&~extra==0)
            backward,count=reverse(extra,z['rows'])
            assert value==backward==28>2*z['n']
            record['extra_finite_target']=dict(image_extension=value,inverse_vertices=count,
                                              status='COMPUTATIONALLY VERIFIED finite n13 target; no minimum-state or all-parameter maximum claim')
        exact.append(record)
    edits=[('projection row',lambda z:z['rows']['b'].__setitem__(2*z['p'],0)),
           ('first stall count',lambda z:z['first_stall_a_counts'].__setitem__(0,1)),
           ('entering exponent',lambda z:z.__setitem__('entering_a_count',z['entering_a_count']-1)),
           ('extension cost',lambda z:z.__setitem__('image_extension',z['image_extension']-1)),
           ('reset lower bound',lambda z:z.__setitem__('reset_lower_bound',z['reset_lower_bound']+1)),
           ('reset upper bound',lambda z:z.__setitem__('reset_upper_bound',z['reset_upper_bound']-1)),
           ('extra finite target',lambda z:z['extra_finite_target'].__setitem__('image_extension',27))]
    corruptions=[]
    for name,edit in edits:
        damaged=deepcopy(index[6])
        edit(damaged)
        try:
            validate(damaged)
        except AssertionError:
            corruptions.append(name)
        else:
            raise AssertionError('accepted corruption '+name)
    report=dict(verified=True,controls=len(records),literal_controls=23,exact_scopes=exact,
                forward_vertices=sum(z['forward_vertices'] for z in exact),
                inverse_vertices=sum(z['inverse_vertices'] for z in exact),
                extra_n13_inverse_vertices=next(z['extra_finite_target']['inverse_vertices'] for z in exact if z['p']==6),
                corruptions_rejected=corruptions,
                boundary='all-parameter proof is paper PROVED; finite original-row and ordinary-set BFS audits COMPUTATIONALLY VERIFIED; no formal proof; Cerny and compatible policy square OPEN')
    (data/'direct_binary_image_obstruction_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='exact_scopes'}),flush=True)


if __name__=='__main__':
    main()
