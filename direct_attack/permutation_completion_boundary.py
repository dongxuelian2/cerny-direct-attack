"""Nearest permutation lifts, general theorem controls, and impossible transfer."""
import argparse
from collections import deque
from hashlib import sha256
from itertools import product,permutations
import json
from pathlib import Path


def completions(row):
    n=len(row);fibers=[tuple(q for q,t in enumerate(row) if t==v) for v in sorted(set(row))]
    missing=tuple(sorted(set(range(n))-set(row)));out=[]
    for reps in product(*fibers):
        remaining=[q for q in range(n) if q not in reps]
        for destinations in permutations(missing):
            p=list(row)
            for q,t in zip(remaining,destinations):p[q]=t
            out.append(tuple(p))
    return sorted(out)


def push(S,row):return sum(1<<q for q in {row[q] for q in range(len(row)) if S>>q&1})


def closure(rows):
    n=len(rows[0]);Q=(1<<n)-1;todo=deque([Q]);seen={Q}
    while todo:
        S=todo.popleft()
        for row in rows:
            T=push(S,row)
            if T not in seen:seen.add(T);todo.append(T)
    return sorted(seen)


def components(rows,cs):
    n=len(rows[0]);seed={tuple([i,j]) for row in rows for i in range(n) for j in range(i+1,n) if row[i]==row[j]}
    seen=set(seed);todo=deque(seed);moves=[p for alphabet in cs for p in alphabet]
    while todo:
        x,y=todo.popleft()
        for p in moves:
            e=tuple(sorted([p[x],p[y]]))
            if e not in seen:seen.add(e);todo.append(e)
    parent=list(range(n))
    def find(q):
        while parent[q]!=q:q=parent[q]
        return q
    for x,y in seen:parent[find(x)]=find(y)
    return len({find(q) for q in range(n)}),len(seen)


def strong(rows):
    n=len(rows[0]);graphs=[[[] for _ in range(n)] for _ in range(2)]
    for row in rows:
        for q,t in enumerate(row):graphs[0][q].append(t);graphs[1][t].append(q)
    for graph in graphs:
        seen={0};todo=[0]
        for q in todo:
            for t in graph[q]:
                if t not in seen:seen.add(t);todo.append(t)
        if len(seen)!=n:return False
    return True


def all_maps(n):
    digest=sha256();count=0;completion_count=0;controls=0
    for row in product(range(n),repeat=n):
        cs=completions(row);count+=1;completion_count+=len(cs)
        digest.update(json.dumps([row,cs],separators=(',',':')).encode()+b'\n')
        for p in cs:
            assert sorted(p)==list(range(n))
            assert sum(x==y for x,y in zip(row,p))==len(set(row));controls+=n
    return dict(n=n,maps=count,closest_permutations=completion_count,row_controls=controls,semantic_sha256=digest.hexdigest())


def binary_cover(n):
    maps=[row for row in product(range(n),repeat=n) if len(set(row))>=n-1];cs=[completions(row) for row in maps]
    total=sync=singular=sc_non_sync_full=non_sync_full=0;hist={};first=None
    for i,row in enumerate(maps):
        for j,other in enumerate(maps):
            total+=1;rs=[row,other]
            if len(set(row))==len(set(other))==n:continue
            singular+=1;im=closure(rs);yes=any(S.bit_count()==1 for S in im)
            d,edges=components(rs,[cs[i],cs[j]]);hist[d]=hist.get(d,0)+1
            if yes:sync+=1;assert d==1
            elif d==1:
                non_sync_full+=1
                if strong(rs):
                    sc_non_sync_full+=1
                    if first is None:first=dict(rows=rs,images=im,normal_edges=edges)
    return dict(n=n,maps=len(maps),labeled_inputs=total,inputs_with_singular=singular,sync_inputs=sync,
                nonsync_full_completion=non_sync_full,SC_nonsync_full_completion=sc_non_sync_full,
                component_histogram=hist,first_SC_nonsync_full=first,
                scope='complete labeled binary alphabets with every letter rank n or n-1; full-G count restricted to inputs with a singular letter')


def family(n):
    assert n>=3;a=list(range(n));a[0],a[1]=1,0;b=[2,2]+list(range(3,n))+[0]
    cp=list(range(1,n))+[0];cm=b[:];cm[1]=1
    rs=[a,b];ims=closure(rs);assert ims==sorted([(1<<n)-1,((1<<n)-1)^1,((1<<n)-1)^2])
    return dict(n=n,rows_sha256=sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest(),explicit_rows=rs if n<=40 else None,
                closest_completion_hashes=[sha256(json.dumps(p,separators=(',',':')).encode()).hexdigest() for p in [cp,cm]],
                images=ims,minimum_rank=n-1,strongly_connected=True,full_completion_group=True,
                original_permutation_group_order=2,completions_unrepresentable=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/permutation_completion_boundary.json'))
    args=ap.parse_args();out=dict(all_map_scopes=[all_maps(n) for n in range(2,6)],binary_scopes=[binary_cover(n) for n in range(2,5)],
                               families=[family(n) for n in list(range(3,41))+[65,129,257,513,1025,2051,4096]],
                               status='PROVED paper general synchronization implies nearest-completion group Sn; converse fails binary SC every n>=3, exact minimum rank n-1, completions impossible in original monoid; subset-neutral compatibility exact; no formal kernel; Cerny OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(all_maps=sum(z['maps'] for z in out['all_map_scopes']),binary_inputs=sum(z['labeled_inputs'] for z in out['binary_scopes']),family_parameters=len(out['families']),maximum_n=max(z['n'] for z in out['families']),binary_scopes=out['binary_scopes'])),flush=True)


if __name__=='__main__':main()
