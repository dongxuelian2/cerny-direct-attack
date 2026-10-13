"""Independent finite checks of the reconstructed sharp top-image boundary."""
from collections import deque
import json
from pathlib import Path


def main():
    records=[]
    for n in range(2,13):
        rows=[[(q+1)%n for q in range(n)],list(range(n))];rows[1][-1]=0
        Q=frozenset(range(n));S=Q-{n-2};queue=deque([Q]);d={Q:0};minimum=None
        while queue:
            T=queue.popleft()
            if T<=S:minimum=d[T];break
            A=d[T]
            for row in rows:
                U=frozenset(row[q] for q in T)
                if U not in d:d[U]=A+1;queue.append(U)
        assert minimum==n
        word=[1]+[0]*(n-1);T=Q
        for a in word:T=frozenset(rows[a][q] for q in T)
        assert T==S
        records.append(dict(n=n,rows=rows,start=sorted(S),exact_image_extension=minimum,
                            reach_word=word,short_bfs_vertices=len(d),verified=True))
    Path('scripts/direct_attack/data/top_rank_boundary.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(instances=len(records),verified=True)))


if __name__=='__main__':main()
