"""Standalone checker for finite exact-formula witnesses. Python >=3.10.

The lower bound is checked by complete ordinary subset BFS; the upper bound
is the independently known avoid-or-compress / Pin--Frankl minimum.
"""
from collections import deque
import json
from pathlib import Path

def apply(states,word,rows):
    states=set(states)
    for letter in word:states={rows['ab'.index(letter)][q] for q in states}
    return states

def ac(rows,S,A):
    start=frozenset(S);A=set(A);words={start:''};todo=deque([start])
    while todo:
        T=todo.popleft()
        if len(T)<len(S) or not A<=T:return len(words[T])
        for letter,row in zip('ab',rows):
            U=frozenset(row[q] for q in T)
            if U not in words:words[U]=words[T]+letter;todo.append(U)
    return None

def strong(rows):
    n=len(rows[0])
    for root in range(n):
        seen={root};todo=[root]
        while todo:
            q=todo.pop()
            for row in rows:
                if row[q] not in seen:seen.add(row[q]);todo.append(row[q])
        if len(seen)!=n:return False
    return True

def verify(path):
    data=json.loads(path.read_text(encoding='utf-8'));found=set()
    for z in data['certificates']:
        n,s,r=z['n'],z['s'],z['r'];rows=z['rows'];S=set(z['S']);A=set(z['A'])
        assert len(rows)==2 and all(len(row)==n and set(row)<=set(range(n)) for row in rows)
        assert len(S)==s and len(A)==r and A<S
        assert strong(rows)
        assert apply(range(n),z['reaching'],rows)==S
        assert len(apply(range(n),z['reset'],rows))==1
        assert ac(rows,S,A)==z['value']==min(n-r,(n-s+2)*(n-s+1)//2)
        attained=apply(S,z['attaining'],rows)
        assert len(z['attaining'])==z['value'] and (len(attained)<s or not A<=attained)
        assert (n,s,r) not in found;found.add((n,s,r))
    expected={(n,s,r) for n in range(2,11) for s in range(2,n+1) for r in range(1,s)}
    assert found==expected and len(found)==165
    print(json.dumps(dict(verified=True,triples=165,minimum_n=2,maximum_n=10,
                         scope='Finite exact values only; no all-parameter theorem.')))

if __name__=='__main__':verify(Path(__file__).with_name('formula_certificates.json'))
