"""Ordinary full-image closure/all-source distances for every saved family entry."""
from collections import deque
import json
from pathlib import Path
import time
from direct_attack.audit_sparse_policy import ordinary_forward


def verify(c):
    n=c['n'];L=n-2;rows=c['rows'];Q=frozenset(range(n));C=Q-frozenset([0,1]);S=frozenset([0,n-1])
    assert rows==[[0,1]+[q+1 for q in range(2,n-1)]+[2],[1,2]+[1]*(n-3)+[0]]
    def apply(T,w):
        for a in w:T=frozenset(rows[a][q] for q in T)
        return T
    R={Q,frozenset([0,1])}|{frozenset([q]) for q in Q}
    for q in C:R|={frozenset([0,1,q]),frozenset([0,q]),frozenset([1,q])}
    reach={Q};queue=deque([Q])
    while queue:
        T=queue.popleft()
        for a in range(2):
            U=apply(T,[a]);assert U in R
            if U not in reach:reach.add(U);queue.append(U)
    assert reach==R and len(R)==4*n-4
    assert apply(frozenset([0,1,2]),c['extension_word'])==S and len(c['extension_word'])==2*L
    assert apply(Q,c['reset_word'])==frozenset([1]) and len(c['reset_word'])==n+1
    p=ordinary_forward(rows)
    for key in ['extension','best','worst','forward']:assert c[key]=={str(T):v for T,v in p[key].items()}
    target=(1<<(n-1))|1
    assert c['target']==target and c['extension'][str(target)]==c['max_extension']==max(p['extension'].values())==2*L
    assert c['rt']==min(d for T,d in p['forward'].items() if T.bit_count()==1)==n+1
    assert c['best_policy']==min(p['best'][1<<q] for q in Q)==n+1
    # Ordinary inverse BFS, including cardinality drops and empty preimages.
    dist={S:0};queue=deque([S]);ordinary=None
    while queue:
        T=queue.popleft()
        if len(T)>2:ordinary=dist[T];break
        for row in rows:
            U=frozenset(q for q in Q if row[q] in T)
            if U not in dist:dist[U]=dist[T]+1;queue.append(U)
    assert ordinary==c['ordinary_extension']==(4 if n==4 else n-1)
    X=frozenset(q for q in Q if apply(frozenset([q]),c['ordinary_preimage_word'])<=S)
    assert X==frozenset(c['ordinary_preimage'])==frozenset([0])|(C-frozenset([n-1]))
    assert max(len(T) for T in R if T<=X)==2 and len(X)-2==n-4
    ordinary_pre=frozenset(q for q in Q if apply(frozenset([q]),c['ordinary_extension_word'])<=S)
    assert len(ordinary_pre)>2 and len(c['ordinary_extension_word'])==ordinary
    # Independent first-drop frame: any larger triple first drops to {1,2}.
    for q in C:
        triple=frozenset([0,1,q]);assert apply(triple,[1])==(frozenset([0,1,2]) if q==n-1 else frozenset([1,2]))
    return dict(n=n,images=len(R),all_policy_entries_checked=len(p['best']),max_extension=2*L,rt=n+1,
                ordinary_extension=ordinary,ordinary_image_deficiency=n-4)


def main():
    root=Path('scripts/direct_attack/data/three_image_family');started=time.monotonic()
    records=[verify(json.loads(p.read_text())) for p in sorted(root.glob('n*.json'),key=lambda p:int(p.stem[1:]))]
    c=json.loads((root/'n6.json').read_text());corruptions=[]
    for name in ['extension_word','max_extension','rows']:
        d=json.loads(json.dumps(c))
        if name=='extension_word':d[name]=d[name][:-1]
        elif name=='max_extension':d[name]-=1
        else:d[name][1][-1]=1
        try:verify(d)
        except AssertionError:corruptions.append(name)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,seconds=time.monotonic()-started,corruptions_rejected=corruptions,
                boundary='Every saved e/G/worst/forward entry independently recomputed using ordinary-set all-source forward BFS; full family closure checked. Arbitrary-n conclusions rest on the paper proof.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(records),max_n=max(r['n'] for r in records),all_entries_checked=True,corruptions_rejected=corruptions,seconds=report['seconds'])))


if __name__=='__main__':main()
