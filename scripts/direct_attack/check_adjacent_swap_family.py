"""Ordinary-set closure, exact specified transports, and independent all-source small arrays."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path
import time
from direct_attack.audit_sparse_policy import ordinary_forward


def verify(c):
    n=c['n'];L=n-1;f=L;rows=c['rows'];Q=frozenset(range(n))
    swap=list(range(n));swap[0],swap[1]=swap[1],swap[0]
    assert rows==[[(q+1)%L for q in range(L)]+[L],[L]*(L-1)+[L-2,0],swap]
    def apply(S,w):
        for a in w:S=frozenset(rows[a][q] for q in S)
        return S
    R={Q}|{frozenset([q]) for q in Q}|{frozenset(T) for T in combinations(range(n),2)}
    R|={frozenset([f,*T]) for T in combinations(range(L),2)}
    dist={Q:0};queue=deque([Q]);edges={}
    while queue:
        T=queue.popleft();edges[T]=[apply(T,[a]) for a in range(3)]
        for U in edges[T]:
            assert U in R
            if U not in dist:dist[U]=dist[T]+1;queue.append(U)
    assert set(dist)==R and c['reachable']==len(R)==n*n-n+2
    assert c['forward']=={str(sum(1<<q for q in T)):d for T,d in dist.items()}
    def extension(S):
        d={T:0 for T in R if len(T)>len(S)};queue=deque(d)
        while queue:
            T=queue.popleft()
            if T<=S:return d[T]
            for U in edges[T]:
                if U not in d:d[U]=d[T]+1;queue.append(U)
        raise AssertionError('No extension')
    S=frozenset([L-2,L-1]);H=frozenset([0,L-2]);P=frozenset([f,0,L-2])
    assert c['target']==sum(1<<q for q in S) and c['larger_image']==sum(1<<q for q in P)
    assert apply(P,c['extension_word'])==S and len(c['extension_word'])==2*L+1
    assert apply(Q,c['reset_word'])==frozenset([f]) and len(c['reset_word'])==n+2
    assert c['rt']==min(dist[frozenset([q])] for q in Q)==n+2
    assert extension(frozenset([f]))==1 and extension(H)==L+1 and extension(P)==1
    assert c['best_policy']==n+2
    target_cost=extension(S);assert c['extension'][str(c['target'])]==target_cost
    frame=None
    if n>=8:
        assert target_cost==c['max_extension']==2*L+1
        def transport(T,predicate,alphabet=(0,1,2)):
            d={T:0};queue=deque([T])
            while queue:
                U=queue.popleft()
                if predicate(U):return d[U]
                for a in alphabet:
                    V=edges[U][a]
                    if V not in d:d[V]=d[U]+1;queue.append(V)
            raise AssertionError('Unreachable frame target')
        B=frozenset([f,0])
        frame=[transport(frozenset([0]),lambda T:T==frozenset([L-1]),(0,2)),
               transport(H,lambda T:T==S,(0,2)),
               transport(B,lambda T:T==frozenset([f])),
               transport(frozenset([f]),lambda T:T<=S),
               transport(B,lambda T:T<=S)]
        assert frame==[L-1,L,L+1,L-1,2*L]
    if n<=20:
        p=ordinary_forward(rows)
        for key in ['extension','best','worst','forward']:assert c[key]=={str(T):v for T,v in p[key].items()}
    return dict(n=n,images=len(R),target_extension=target_cost,rt=n+2,full_arrays_checked=n<=20,
                checked_policy_chain=[1,L+1,1],proof_frame_distances=frame)


def main():
    root=Path('scripts/direct_attack/data/adjacent_swap_family');started=time.monotonic()
    records=[verify(json.loads(p.read_text())) for p in sorted(root.glob('n*.json'),key=lambda p:int(p.stem[1:]))]
    c=json.loads((root/'n12.json').read_text());rejected=[]
    for field in ['extension_word','max_extension','forward']:
        d=json.loads(json.dumps(c))
        if field=='extension_word':d[field]=d[field][:-1]
        elif field=='max_extension':d[field]+=1
        else:d[field][str((1<<d['n'])-1)]=1
        try:verify(d)
        except AssertionError:rejected.append(field)
        else:raise AssertionError('Corruption accepted')
    report=dict(verified=True,records=records,seconds=time.monotonic()-started,corruptions_rejected=rejected,
                boundary='All closure and forward entries, target extension and exact three-phase policy chain independently checked through n63. Every e/G/W entry additionally all-source checked only through n20; arbitrary-n maxima rest on paper proof.')
    (root/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(records),full_array_cases=sum(r['full_arrays_checked'] for r in records),seconds=report['seconds'],corruptions_rejected=rejected)))


if __name__=='__main__':main()
