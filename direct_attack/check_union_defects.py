"""Ordinary-set exact checking of universal union-defect accounting."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path
from direct_attack.mine import inputs


def data(rows):
    n=len(rows[0]);Q=frozenset(range(n));R={Q};queue=deque([Q])
    while queue:
        S=queue.popleft()
        for row in rows:
            T=frozenset(row[q] for q in S)
            if T not in R:R.add(T);queue.append(T)
    if not all(frozenset([q]) in R for q in Q):return None
    identity=tuple(range(n));words={identity:[]};queue=deque([identity])
    while queue:
        u=queue.popleft()
        for a,row in enumerate(rows):
            v=tuple(row[q] for q in u)
            if v not in words:words[v]=words[u]+[a];queue.append(v)
    sets=[frozenset(q for q in Q if mask>>q&1) for mask in range(1<<n)]
    rho={X:max([len(T) for T in R if T<=X],default=0) for X in sets}
    return Q,sets,rho,words


def main():
    cases=[]
    for n in [2,3]:
        cases.extend(rows for rows in inputs(n,'first-map-orbits',0,0,2))
    cases.extend([[[2,0,0,1],[1,2,3,0]],[[0,0,2,2],[1,3,0,2]],
                  [[1,0,0,2],[1,2,3,0]],[[0,2,1,1],[2,1,3,0]]])
    counts=dict(automata=0,transformations=0,proper_union_instances=0,sufficient_transfers=0,
                failed_transfers=0,equality_failures=0);examples=[]
    for rows in cases:
        result=data(rows)
        if result is None:continue
        Q,sets,rho,words=result;counts['automata']+=1
        pairs=[(S,T,S|T,S&T) for S,T in combinations(sets[1:],2) if S|T!=Q]
        for u,w in words.items():
            actual=tuple(range(len(Q)))
            for a in w:actual=tuple(rows[a][q] for q in actual)
            assert actual==u;counts['transformations']+=1
            pre={X:frozenset(q for q,z in enumerate(u) if z in X) for X in sets}
            F={X:rho[pre[X]]-len(X) for X in sets};D={X:len(pre[X])-rho[pre[X]] for X in sets};image=frozenset(u)
            for S,T,U,I in pairs:
                counts['proper_union_instances']+=1
                assert F[S]+F[T]==F[U]+len(pre[I])-len(I)+D[U]-D[S]-D[T]
                penalty=len(I-image)+D[S]+D[T]-D[U]
                if F[U]>penalty:
                    assert F[S]>0 or F[T]>0;counts['sufficient_transfers']+=1
                if F[U]>0 and F[S]<=0 and F[T]<=0:
                    assert F[U]<=penalty;counts['failed_transfers']+=1
                    if F[U]==penalty:counts['equality_failures']+=1
                    if rows==[[0,0,0],[1,2,1]] and S==frozenset([1]) and T==frozenset([2]) and w==[1] or rows==[[2,0,0,1],[1,2,3,0]] and S==frozenset([0,3]) and T==frozenset([2,3]) and w==[0,0]:
                        examples.append(dict(rows=rows,S=sorted(S),T=sorted(T),word=w,gain=F[U],missing_overlap=len(I-image),defects=[D[S],D[T],D[U]],penalty=penalty))
    # The first-map representatives may not retain this particular labeling;
    # add its independent fixed witness to the audit rather than infer it.
    if not any(len(c['rows'][0])==3 for c in examples):
        rows=[[0,0,0],[1,2,1]];Q,sets,rho,words=data(rows);S=frozenset([1]);T=frozenset([2]);u=tuple(rows[1])
        pre=lambda X:frozenset(q for q,z in enumerate(u) if z in X)
        assert rho[pre(S|T)]-2==1 and rho[pre(S)]-1==rho[pre(T)]-1==0
        assert len(pre(S))-rho[pre(S)]==1
        examples.append(dict(rows=rows,S=[1],T=[2],word=[1],gain=1,missing_overlap=0,defects=[1,0,0],penalty=1))
    assert any(len(c['rows'][0])==4 for c in examples)
    report=dict(verified=True,counts=counts,equality_examples=examples,
                boundary='Complete binary first-map covering inputs n2/3 that synchronize every state to every singleton, plus four fixed n4 inputs; all generated transformations and proper unions checked. The universal result is proved on paper.')
    out=Path('direct_attack/data/union_defects');out.mkdir(parents=True,exist_ok=True)
    (out/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':main()
