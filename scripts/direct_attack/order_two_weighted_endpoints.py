"""Literal controls for all-n weighted endpoint words and the NEW three-a metric."""
from pathlib import Path
import itertools
import json
import random
from .periodic_three_a_gap import family

ROOT = Path(__file__).resolve().parents[2]


def endpoint(a):
    M, L = len(a)-1, (len(a)-1)//2
    mixed = [j for j in range(1, L) if a[j] % L != a[j+L] % L]
    if not mixed:
        return dict(rows=[a, list(range(1, M))+[0, M]], nonsync=True)
    j = min(mixed)
    assert j <= L-2
    k_plus, k_minus = (-a[j]) % L, (-a[j+L]) % L
    word = lambda k: [0]+[1]*j+[0]+[1]*k+[0]
    return dict(rows=[a, list(range(1, M))+[0, M]], j=j,
                positive_word=word(k_plus), negative_word=word(k_minus))


def main():
    rng = random.Random(2026100307)
    records=[]
    M,L=8,4
    rest=[q for q in range(M) if q not in (0,L)]
    for A in itertools.permutations(rest):
        a=[0]*(M+1);a[0]=a[L]=M
        for q,x in zip(rest,A):a[q]=x
        records.append(endpoint(a))
    for M in (6,10,12,16,18,20,24,32,48,64,128,256):
        L=M//2;rest=[q for q in range(M) if q not in (0,L)]
        for _ in range(5):
            A=rest[:];rng.shuffle(A)
            a=[0]*(M+1);a[0]=a[L]=M
            for q,x in zip(rest,A):a[q]=x
            records.append(endpoint(a))
        # Place the two mixed inputs at L-2,L-1; the prescribed plus word
        # attains cost M. This is an upper-word control, not a minimum claim.
        pairs=list(range(1,L));pairs.remove(1);pairs.remove(2)
        output=pairs+[1,2]
        a=[0]*(M+1);a[0]=a[L]=M
        for q,x in zip(range(1,L),output):a[q]=x;a[q+L]=x+L
        a[M-2],a[M-1]=a[M-1],a[M-2]
        records.append(endpoint(a))
    barriers=[]
    for p in range(3,9):
        z=family(p,2)
        barriers.append({key:z[key] for key in ('p','m','rows','subset','three_a_word')})
    data=dict(scope='COMPLETE M8 endpoint words only; other endpoints controls; NEW weighted three-a metric',
              endpoints=records,weighted_three_a_controls=barriers)
    (ROOT/'scripts/direct_attack/data/order_two_weighted_endpoints.json').write_text(
        json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(endpoint_inputs=len(records),complete_M8=720,barrier_controls=len(barriers))))


if __name__=='__main__':main()
