"""Independent labelled-orbit audit of the finite unique-kernel cover.

First transformations are generated as labelled rows and conjugacy is marked
explicitly. No chain/cycle canonical-form classification is used here.
Pair lengths are computed by ordinary forward BFS, not reverse pair BFS.
"""
from collections import deque
from itertools import product,permutations,combinations
import json
from pathlib import Path
from audit_small import bfs,strong

ROOT=Path(__file__).resolve().parent

def pair_length(rows,pair):
    start=frozenset(pair);queue=deque([(start,0)]);seen={start}
    while queue:
        S,d=queue.popleft()
        if len(S)==1:return d
        for row in rows:
            T=frozenset(row[x] for x in S)
            if T not in seen:seen.add(T);queue.append((T,d+1))
    return None

def audit(n):
    perms=list(permutations(range(n)));labelled={row for row in product(range(n),repeat=n) if len(set(row))==n-1}
    marked=set();firsts=[]
    for row in sorted(labelled):
        if row in marked:continue
        firsts.append(row)
        for perm in perms:
            image=[None]*n
            for q in range(n):image[perm[q]]=perm[row[q]]
            marked.add(tuple(image))
    assert marked==labelled
    tested=valid=0;best=0;best_data=None;s=n-3;pairs=list(combinations(range(n),2));subsets=list(combinations(range(n),s))
    for first in firsts:
        kernel=[pair for pair in pairs if first[pair[0]]==first[pair[1]]];assert len(kernel)==1
        p,q=kernel[0]
        for perm in perms:
            collapsed=list(perm);collapsed[q]=collapsed[p]
            for second in (perm,collapsed):
                tested+=1;rows=[first,second]
                if not strong(rows):continue
                distances={pair:pair_length(rows,pair) for pair in pairs}
                if any(d is None for d in distances.values()):continue
                valid+=1
                for S in subsets:
                    value=min(distances[pair] for pair in combinations(S,2))
                    if value>best:
                        best=value;best_data=dict(rows=[list(row) for row in rows],S=list(S),value=value)
    expected=json.loads((ROOT/f'compression_kernel_n{n}.json').read_text())
    assert (len(firsts),tested,valid,best)==(expected['first_rank_one_classes'],expected['tested'],expected['strong_sync'],expected['maximum_compression_in_unique_kernel_cover'])
    rows=expected['rows'];S=[q for q in range(n) if expected['S_mask']>>q&1]
    w,_=bfs(rows,S,lambda T:len(T)<s);v,_=bfs(rows,range(n),lambda T:T==frozenset(S))
    assert len(w)==best and (v is not None)==expected['witness_reachable']
    return dict(n=n,s=s,labelled_rank_one_maps=len(labelled),first_orbits=len(firsts),tested=tested,strong_sync=valid,
                maximum_compression=best,cpp_matches=True,cpp_witness_reachable=v is not None,
                independent_generation='All labelled rank-one transformations with explicit conjugacy marking.',
                independent_distance='Ordinary forward BFS for each pair.')

def main():
    records=[]
    for n in (5,6):
        records.append(audit(n));print(json.dumps(records[-1]),flush=True)
    (ROOT/'compression_cover_audit.json').write_text(json.dumps(dict(records=records,scope='Finite n=5,6 only; no all-parameter refutation.'),indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
