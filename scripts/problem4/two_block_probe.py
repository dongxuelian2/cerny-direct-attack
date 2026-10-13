"""Adversarial finite checks of a proposed two-block family; no uniform claim."""
from collections import deque
import json
from pathlib import Path
from alphabet_check import apply,pair_distances,strong
from protected_core_probe import scores
from protected_padding import reset_word

ROOT=Path(__file__).resolve().parent

def construct(p,t,k=0):
    # P precedes U; H is the last block of coordinates.
    n=p+2*t+1+k;U=list(range(p,p+2*t+1));H=list(range(p+2*t+1,n))
    a=list(range(n));a[p-2],a[p-1]=p-1,p-2
    for q,v in zip(U,U[1:]+U[:1]):a[q]=v
    b=list(range(n))
    for q in range(1,p):b[q]=q-1
    chain=[0]+H+[p+t]
    for q,v in zip(chain,chain[1:]):b[q]=v
    for j in range(2*t):b[p+j]=p-1 if j in (t-1,2*t-1) else p+j+1
    rows=[a,b];S=set(range(p+t))|set(H);B=set(range(p))|set(H)|set(U[t:2*t])
    e=("a"*(2*t)+"b"*len(B))*t
    reaching="b"*t+e+"a"*(t+1)
    return rows,S,B,e,reaching

def main():
    records=[];failures=[]
    for t in range(2,9):
        for p in range(4,t+4):
            for k in (0,1,2):
                rows,S,B,e,reaching=construct(p,t,k);n=len(rows[0]);tested=dict(n=n,p=p,t=t,k=k)
                assert strong(rows) and apply(range(n),reaching,rows)==S
                assert all(apply([q],e,rows)=={q} for q in B)
                # The odd U-cycle length isolates the P transposition under
                # a^(2t+1), even when t itself is even.
                assert all(apply([q],"a"*(2*t+1),rows)==({p-1} if q==p-2 else
                           {p-2} if q==p-1 else {q}) for q in B)
                assert apply(B,"ab"+e,rows)==B-{p+t+1}
                sync=len(pair_distances(rows))==n*(n-1)//2
                if not sync:
                    failures.append(dict(**tested,reason="not synchronizing"));continue
                values=scores(rows,S);value=values[0];compression=max(values.values())
                # The highest local score is bounded by compression, but may
                # be strictly smaller: compute shortest compression separately.
                queue=deque([frozenset(S)]);dist={frozenset(S):0};actual_compression=None
                while queue and actual_compression is None:
                    T=queue.popleft()
                    for row in rows:
                        V=frozenset(row[q] for q in T)
                        if len(V)<len(S):actual_compression=dist[T]+1;break
                        if V not in dist:dist[V]=dist[T]+1;queue.append(V)
                expected=min(p+2*t,3*t+2)
                tested.update(root_value=value,compression=actual_compression,expected_root_value=expected,
                              full_protected_value=min(values[q] for q in {0}|set(range(p+2*t+1,n))))
                assert tested["full_protected_value"]==value
                if actual_compression!=3*t+2:
                    failures.append(dict(**tested,reason="proposed compression pattern fails"))
                if value!=expected:failures.append(dict(**tested,reason="proposed local formula fails"))
                records.append(tested)
    out=dict(records=records,failures=failures,
             scope="Finite two-block family audit only. No claim that its proposed formula is uniform or globally extremal.")
    (ROOT/"two_block_probe.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(dict(instances=len(records),failures=failures)))

if __name__=="__main__":main()
