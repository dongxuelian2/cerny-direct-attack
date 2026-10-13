"""Independent inverse-set BFS for all shortest image-extension tie choices."""
from collections import deque
import json
from pathlib import Path


def verify(c):
    n=c['n'];rows=c['rows'];Q=frozenset(range(n));mask=lambda S:sum(1<<q for q in S)
    step=lambda S,a:frozenset(rows[a][q] for q in S)
    def apply(S,w):
        for a in w:S=step(S,a)
        return S
    reachable={Q:0};queue=deque([Q])
    while queue:
        S=queue.popleft()
        for a in range(len(rows)):
            T=step(S,a)
            if T not in reachable:reachable[T]=reachable[S]+1;queue.append(T)
    best={Q:0};worst={Q:0};extensions={}
    for S in sorted((S for S in reachable if S!=Q),key=len,reverse=True):
        queue=deque([S]);d={S:0};cost=None;targets=set()
        while queue:
            X=queue.popleft()
            if cost is not None and d[X]>cost:break
            Ts={T for T in reachable if len(T)>len(S) and T<=X}
            if Ts:
                cost=d[X];targets|=Ts;continue
            if cost is not None:continue
            for a,row in enumerate(rows):
                Y=frozenset(q for q in Q if row[q] in X)
                if Y not in d:d[Y]=d[X]+1;queue.append(Y)
        assert cost is not None
        extensions[S]=cost
        best[S]=cost+min(best[T] for T in targets)
        worst[S]=cost+max(worst[T] for T in targets)
    assert c['extension']=={str(mask(S)):v for S,v in extensions.items()}
    if 'extension_bound_test' in c:
        assert c['extension_bound_test']['max_cost']==max(extensions.values())
        assert c['extension_bound_test']['bound']==2*n
    assert c['best']=={str(mask(S)):v for S,v in best.items()}
    assert c['worst']=={str(mask(S)):v for S,v in worst.items()}
    singleton_costs=[best[frozenset([q])] for q in Q]
    assert c['best_policy']==min(singleton_costs)
    assert c['worst_policy']==max(worst[frozenset([q])] for q in Q)
    assert c['rt']==min(v for S,v in reachable.items() if len(S)==1)
    assert len(c['reset_word'])==c['best_policy'] and len(apply(Q,c['reset_word']))==1
    old=None
    for phase in c['phases']:
        S=frozenset(q for q in Q if phase['start']>>q&1)
        T=frozenset(q for q in Q if phase['larger']>>q&1)
        assert S in reachable and T in reachable and len(T)>len(S)
        assert old is None or old==S
        assert len(phase['word'])==extensions[S] and apply(T,phase['word'])<=S
        old=T
    assert old==Q
    return dict(n=n,rt=c['rt'],best_policy=c['best_policy'],reachable=len(reachable),verified=True)


def main():
    paths=[p for root in Path('scripts/direct_attack/data').glob('image_extension_policy*')
           for p in sorted(root.glob('witness_*.json'))]
    transport=Path('scripts/direct_attack/data/singleton_transport/witness.json')
    if transport.exists():paths.append(transport)
    records=[dict(file=str(p),**verify(json.loads(p.read_text()))) for p in paths]
    Path('scripts/direct_attack/data/image_policy_checks.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(checked=len(records),verified=True)))


if __name__=='__main__':main()
