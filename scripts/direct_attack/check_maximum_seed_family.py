"""Ordinary all-source arrays, complete closed images, words and parameter controls."""
from collections import deque
import json
from pathlib import Path
import time
from direct_attack.audit_sparse_policy import ordinary_forward


def verify(c):
    n=c['n'];j=n-4;Q=frozenset(range(n));rows=c['rows'];a=[q%2 for q in Q];a[j+1]=0
    assert rows==[a,[(q+1)%n for q in range(n)],[0,0]+[(q-1)%3 for q in range(2,n)]]
    def apply(T,w):
        for x in w:T=frozenset(rows[x][q] for q in T)
        return T
    R={Q}|{frozenset([q]) for q in Q}
    for q in Q:R|={frozenset([q,(q+1)%n]),frozenset([q,(q+2)%n]),frozenset([q,(q+1)%n,(q+2)%n])}
    seen={Q};queue=deque([Q])
    while queue:
        T=queue.popleft()
        for x in range(3):
            U=apply(T,[x]);assert U in R
            if U not in seen:seen.add(U);queue.append(U)
    assert seen==R and c['reachable']==len(R)==4*n+1
    p=ordinary_forward(rows)
    for key in ['extension','best','worst','forward']:assert c[key]=={str(T):v for T,v in p[key].items()}
    assert c['rt']==min(p['forward'][1<<q] for q in Q)==c['best_policy']==min(p['best'][1<<q] for q in Q)==2
    assert apply(Q,c['reset_word'])==frozenset([0]) and len(c['reset_word'])==2
    merged=[T for T in R if len(T)>1 and any(len(apply(T,[x]))==1 for x in range(3))]
    kappa=max(map(len,merged));maximum=[T for T in merged if len(T)==kappa];assert kappa==c['seed_budget']['kappa']==3
    mask=lambda T:sum(1<<q for q in T)
    assert c['seed_budget']['anchor_best']==1+min(p['best'][mask(T)] for T in maximum)
    T=frozenset([j,j+1,j+2]);assert c['large_seed']==mask(T)
    assert apply(Q,c['seed_reach_word'])==T and len(c['seed_reach_word'])==n-3
    assert apply(Q,c['forced_seed_reset_word'])==frozenset([0]) and len(c['forced_seed_reset_word'])==n-2
    if c['valid_parameter']:
        assert n%6==0 and maximum==[T] and p['best'][mask(T)]==p['extension'][mask(T)]==n-3
        assert c['seed_budget']['anchor_best']==n-2
    else:
        assert n%6==2 and c['seed_budget']['anchor_best']==2
        cheap=frozenset([n-1,0,1]);assert cheap in maximum and p['best'][mask(cheap)]==1 and apply(cheap,[2])==frozenset([0])
    return dict(n=n,valid_parameter=c['valid_parameter'],R=len(R),P=2,Fk=c['seed_budget']['anchor_best'],all_entries_checked=True)


def main():
    root=Path('scripts/direct_attack/data/maximum_seed_family');started=time.monotonic()
    records=[verify(json.loads(p.read_text())) for p in sorted(root.glob('n*.json'),key=lambda p:int(p.stem[1:]))]
    c=json.loads((root/'n12.json').read_text());rejected=[]
    for field in ['valid_parameter','seed_reach_word','seed_budget']:
        d=json.loads(json.dumps(c))
        if field=='valid_parameter':d[field]=False
        elif field=='seed_reach_word':d[field]=d[field][:-1]
        else:d[field]['anchor_best']-=1
        try:verify(d)
        except AssertionError:rejected.append(field)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,corruptions_rejected=rejected,seconds=time.monotonic()-started,
                boundary='Every saved e/G/W/forward entry independently recomputed by ordinary all-source BFS. Complete actual image closure, unique maximum seed, words and three excluded-parameter controls checked. Arbitrary-n ratio obstruction follows from paper proof.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(records),corruptions_rejected=rejected,seconds=report['seconds'])))


if __name__=='__main__':main()
