"""Independent set preimages, reverse BFS, rooted graph and bounded-slack search."""
import argparse
from collections import deque
import copy
from hashlib import sha256
import json
from pathlib import Path

def independent_rows(m):
    n=2*m;cycle=[0,1,m,2,m+1];p=list(range(n))
    for i,q in enumerate(cycle):p[q]=cycle[(i+1)%5]
    f=p[:];f[m+1]=p[1]
    return [[(q+1)%n for q in range(n)],f]

def pre(S,row):return frozenset(q for q,t in enumerate(row) if t in S)

def full_reverse(rs,weighted):
    n=len(rs[0]);Q=frozenset(range(n));todo=deque(frozenset([q]) for q in range(n))
    dist={S:0 for S in todo};settled=set()
    while todo:
        S=todo.popleft()
        if S in settled:continue
        settled.add(S)
        if S==Q:return dist[S],len(settled)
        for i,row in enumerate(rs):
            T=pre(S,row)
            if not T:continue
            c=i if weighted else 1;d=dist[S]+c
            if d<dist.get(T,10**9):
                dist[T]=d
                if c:todo.append(T)
                else:todo.appendleft(T)
    raise AssertionError('not synchronizing')

def bounded_neutral(rs,limit):
    n=len(rs[0]);todo=deque((frozenset([q]),0) for q in range(n));seen=set(todo);largest=1
    while todo:
        S,k=todo.popleft();largest=max(largest,len(S))
        for i,row in enumerate(rs):
            T=pre(S,row);delta=len(T)-len(S)
            if delta<0:continue
            j=k+int(i==1 and delta==0)
            if j>limit:continue
            v=T,j
            if v not in seen:seen.add(v);todo.append(v)
    return largest,len(seen)

def literal(rs,word):
    R=set(range(len(rs[0])))
    assert all(type(a)==int and 0<=a<len(rs) for a in word)
    for a in word:R={rs[a][q] for q in R}
    assert len(R)==1
    return next(iter(R))

def verify(z):
    m=z['m'];assert m>=3 and m%2; n=2*m;assert z['n']==n
    rs=independent_rows(m);a,f=rs
    assert z['rows_sha256']==sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest()
    if z['explicit_rows'] is not None:assert z['explicit_rows']==rs
    assert len(set(a))==n and len(set(f))==n-1
    fibers={q:pre({q},f) for q in range(n)}
    assert [q for q,C in fibers.items() if not C]==[0]
    assert [(q,C) for q,C in fibers.items() if len(C)>1]==[(m,frozenset([1,m+1]))]
    assert z['excluded']==0 and z['duplicate']==m and z['kernel_pair']==[1,m+1]
    assert z['simple'] and z['strongly_connected']
    # Every congruence invariant under the full cycle is a residue partition.
    divisors=[d for d in range(2,n) if n%d==0]
    for d in divisors:
        assert any(x%d==y%d and f[x]%d!=f[y]%d for x in range(n) for y in range(x+1,n))
    # Every whole antipodal pair has zero inverse cardinality change.
    blocks=[frozenset([j,j+m]) for j in range(m)]
    for C in blocks:assert len(pre(C,f))==2
    assert fibers[m] in blocks
    if m>=5:
        assert pre(blocks[1],f)==frozenset([0,2])
        assert pre(blocks[2],f)==frozenset([m,m+2])
        for j,C in enumerate(blocks):
            if j not in (1,2):assert pre(C,f) in blocks
        # With only one neutral f, the first next growth has one of these
        # two triples. Every rotating growth from either yields two blocks.
        triples=[pre({m,m+2},f),pre({m-2,m},f)]
        for T in triples:
            assert len(T)==3
            winners=[]
            for k in range(n):
                R=frozenset((q+k)%n for q in T);U=pre(R,f)
                if len(U)>len(R):
                    winners.append(U)
                    assert len(U)==4 and all((q+m)%n in U for q in U)
            assert len(winners)==1
    assert z['minimum_required_f_lower']==(n if m==3 else n+1)
    assert z['required_corank_slack_lower']==(1 if m==3 else 2)
    macro=z['original_rooted_macro'];assert macro==[1,1]+[0]*(m-1)
    g=[]
    for q in range(n):
        t=q
        for i in macro:t=rs[i][t]
        g.append(t)
    root=m+1;assert z['root']==root and g[root]==root
    reverse=[[] for _ in range(n)]
    for q,t in enumerate(g):reverse[t].append(q)
    heights={root:0};todo=deque([root])
    while todo:
        q=todo.popleft()
        for t in reverse[q]:
            if t not in heights:heights[t]=heights[q]+1;todo.append(t)
    assert len(heights)==n
    H=max(heights.values());assert H==z['rooted_height']==(4 if m==3 else 2*m-3)
    assert z['reset_length']==len(macro)*H
    assert z['square_slack']==(n-1)**2-z['reset_length']>0
    report=dict(m=m,n=n,macro_state_letter_controls=n*len(macro),
                antipodal_balanced_pairs=m,proper_cycle_congruences=len(divisors))
    if m<=9:
        rt,vertices=full_reverse(rs,False);mf,weighted_vertices=full_reverse(rs,True)
        assert rt==z['finite_exact_rt'] and len(z['finite_shortest_word'])==rt
        literal(rs,z['finite_shortest_word'])
        w=z['finite_minimum_f']['original_word'];literal(rs,w)
        assert mf==z['finite_minimum_f']['minimum_f']==w.count(1)
        assert mf==(n if m==3 else n+1)
        zero,v0=bounded_neutral(rs,0);one,v1=bounded_neutral(rs,1)
        assert zero==2 and one==(n if m==3 else 4)
        report.update(rt=rt,minimum_f=mf,reverse_vertices=vertices,weighted_reverse_vertices=weighted_vertices,
                      no_neutral_max_size=zero,one_neutral_max_size=one,bounded_slack_vertices=v0+v1,
                      literal_letters=rt+len(w))
    return report

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('direct_attack/data/antipodal_corank_slack.json'))
    ap.add_argument('--out',type=Path,default=Path('direct_attack/data/antipodal_corank_slack_checks.json'))
    args=ap.parse_args();data=json.loads(args.source.read_text());reports=[verify(z) for z in data['records']]
    base=data['records'][0];mutations=[]
    for key,value in [('rows_sha256','0'*64),('rooted_height',3),('minimum_required_f_lower',5),('reset_length',15),('finite_exact_rt',12)]:
        b=copy.deepcopy(base);b[key]=value;mutations.append(b)
    b=copy.deepcopy(base);b['finite_minimum_f']['minimum_f']=5;mutations.append(b)
    b=copy.deepcopy(base);b['finite_shortest_word']=[0]*13;mutations.append(b)
    for b in mutations:
        try:verify(b)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,parameters=len(reports),maximum_n=max(r['n'] for r in reports),reports=reports,
             macro_state_letter_controls=sum(r['macro_state_letter_controls'] for r in reports),
             finite_reverse_vertices=sum(r.get('reverse_vertices',0) for r in reports),
             finite_weighted_reverse_vertices=sum(r.get('weighted_reverse_vertices',0) for r in reports),
             bounded_slack_vertices=sum(r.get('bounded_slack_vertices',0) for r in reports),
             corruptions_rejected=len(mutations),boundary='paper ALL odd m>=3; finite exact rt/minimum-f m3/5/7/9 only; no formal kernel')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='reports'}),flush=True)

if __name__=='__main__':main()
