"""Test the union transfer needed to generalize proper-extension arguments."""
from collections import deque
import json
from pathlib import Path
from direct_attack.core import graph, bfs, strongly_connected
from direct_attack.mine import inputs


def inspect(rows):
    n=len(rows[0]);N=1<<n;Q=N-1;g=graph(rows);f=bfs(g,[Q])
    R=[s for s,d in enumerate(f) if d>=0]
    if not all(f[1<<q]>=0 for q in range(n)):return None
    rho=[max((t.bit_count() for t in R if t & x==t),default=0) for x in range(N)]
    # All distinct transformations induced by words of length <=4.
    queue=deque([tuple(range(n))]);words={tuple(range(n)):[]}
    while queue:
        transform=queue.popleft();w=words[transform]
        for S in R:
            for T in R:
                U=S|T
                if S>=T or U not in R or U in (S,T,Q):continue
                pre=lambda x:sum(1<<q for q,z in enumerate(transform) if x>>z&1)
                X,Y,Z=pre(S),pre(T),pre(U)
                if rho[Z]<=U.bit_count():continue
                # Preserve properness of the union: every union point has a fiber.
                image=sum(1<<z for z in set(transform))
                if U & image!=U:continue
                if rho[X]>S.bit_count() or rho[Y]>T.bit_count():continue
                V=next(v for v in R if v & Z==v and v.bit_count()>U.bit_count())
                return dict(n=n,rows=[list(row) for row in rows],S=S,T=T,union=U,
                            word=w,transform=list(transform),preimages=[X,Y,Z],
                            capacities=[rho[X],rho[Y],rho[Z]],larger_image=V,
                            reachable=R,scope='Exact union-transfer counterexample; not a reset-bound counterexample.')
        if len(w)==4:continue
        for a,row in enumerate(rows):
            next_transform=tuple(row[q] for q in transform)
            if next_transform not in words:words[next_transform]=w+[a];queue.append(next_transform)
    return None


def main():
    out=Path('direct_attack/data/union_capacity');out.mkdir(exist_ok=True);counts={}
    for n in [2,3,4,5]:
        count=0
        for rows in inputs(n,'first-map-orbits',0,0,2):
            count+=1
            if not strongly_connected(rows):continue
            c=inspect(rows)
            if c:
                counts[n]=count
                (out/'witness.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
                report=dict(checked=counts,refuted=True,first_n=n,word_length_limit=4,
                            scope='Smaller binary automata checked only for transformations of word length <=4; no unrestricted minimality claim.')
                (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
                print(json.dumps(c));print(json.dumps(report));return
        counts[n]=count
    raise RuntimeError('No obstruction found in the declared finite scope')


if __name__=='__main__':main()
