"""Ordinary-set inverse BFS audit of the new local and union obstructions."""
from collections import deque
from functools import lru_cache
import json
from pathlib import Path


def distances(rows,with_worst=False):
    Q=frozenset(range(len(rows[0])));queue=deque([Q]);forward={Q:0};reach={Q:[]}
    while queue:
        S=queue.popleft()
        for a,row in enumerate(rows):
            T=frozenset(row[q] for q in S)
            if T not in forward:forward[T]=forward[S]+1;reach[T]=reach[S]+[a];queue.append(T)
    R=set(forward)
    @lru_cache(None)
    def contained(X):return tuple(T for T in R if T<=X)
    e={};best={Q:0};worst={Q:0};choices={}
    for S in sorted(R-{Q},key=len,reverse=True):
        queue=deque([S]);words={S:[]};cost=None;targets={}
        while queue:
            X=queue.popleft();w=words[X]
            if cost is not None and len(w)>cost:break
            larger=[T for T in contained(X) if len(T)>len(S)]
            if larger:
                cost=len(w)
                for T in larger:targets.setdefault(T,list(reversed(w)))
                continue
            if cost is not None:continue
            for a,row in enumerate(rows):
                Y=frozenset(q for q,z in enumerate(row) if z in X)
                if Y not in words:words[Y]=w+[a];queue.append(Y)
        assert cost is not None
        e[S]=cost;T=min(targets,key=lambda t:(best[t],tuple(sorted(t))))
        best[S]=cost+best[T];worst[S]=cost+max(worst[T] for T in targets);choices[S]=(T,targets[T])
    result=(Q,forward,reach,e,best,choices)
    return result+(worst,) if with_worst else result


def main():
    records=[];critical=[];decode=lambda s,n:frozenset(q for q in range(n) if s>>q&1)
    encode=lambda S:sum(1<<q for q in S)
    for name in ['local_rank_family','fixed_arm_family']:
        for path in sorted(Path('direct_attack/data',name).glob('n*.json')):
            c=json.loads(path.read_text());n=c['n'];rows=c['rows'];S=decode(c['start'],n)
            Q,f,reach,e,best,choices=distances(rows)
            assert e[S]==c['exact_extension'] and best[S]==c['exact_policy']
            assert min(d for T,d in f.items() if T<=S)==c['exact_avoiding']
            assert min(d for T,d in f.items() if len(T)==1)==c['rt']
            assert min(best[T] for T in f if len(T)==1)==c['best_policy']
            assert max(best[T]-n*(n-len(T)) for T in f if T!=Q)==c['local_excess']
            for key in ['reset_word','reach_word']:
                if key not in c:continue
                T=Q
                for a in c[key]:T=frozenset(rows[a][q] for q in T)
                assert len(T)==1 if key=='reset_word' else T==S
            records.append(dict(file=str(path),reachable=len(f),verified=True))
            print(json.dumps(records[-1]),flush=True)
            if c['exact_policy']>n*(n-len(S)):
                initial=S;phases=[];reset=[]
                while S!=Q:
                    T,w=choices[S];result=T
                    for a in w:result=frozenset(rows[a][q] for q in result)
                    assert result<=S and len(w)==e[S]
                    phases.append(dict(start=encode(S),larger=encode(T),word=w,cost=e[S],tail=best[T]))
                    reset=w+reset;S=T
                critical.append(dict(n=n,rows=rows,start=encode(initial),reach_word=reach[initial],
                                     extension=e[initial],policy=best[initial],bound=n*(n-len(initial)),
                                     avoiding=c['exact_avoiding'],word_into_start=reset,phases=phases))
    path=Path('direct_attack/data/union_capacity/witness.json');c=json.loads(path.read_text());n=c['n'];rows=c['rows']
    Q=frozenset(range(n));queue=deque([Q]);R={Q}
    while queue:
        S=queue.popleft()
        for row in rows:
            T=frozenset(row[q] for q in S)
            if T not in R:R.add(T);queue.append(T)
    S,T=decode(c['S'],n),decode(c['T'],n);U=S|T
    transform=list(range(n))
    for a in c['word']:transform=[rows[a][q] for q in transform]
    pre=lambda X:frozenset(q for q in Q if transform[q] in X)
    caps=[max((len(V) for V in R if V<=pre(X)),default=0) for X in [S,T,U]]
    assert transform==c['transform'] and caps==c['capacities']
    assert caps[0]<=len(S) and caps[1]<=len(T) and caps[2]>len(U)
    assert U<=set(transform) and S in R and T in R and U in R
    V=decode(c['larger_image'],n);assert V in R and V<=pre(U) and len(V)>len(U)
    assert sorted(map(encode,R))==c['reachable']
    report=dict(families=records,critical=critical,union=dict(n=n,verified=True))
    Path('direct_attack/data/new_image_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(family_instances=len(records),critical=len(critical),union_verified=True)))


if __name__=='__main__':main()
