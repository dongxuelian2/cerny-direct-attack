"""Forward kernel-congruence certificates and finite terminal-graph boundary."""
import argparse
from collections import deque
from hashlib import sha256
from itertools import product,combinations
import json
from pathlib import Path


def partition(n,edges):
    parent=list(range(n))
    def root(q):
        while parent[q]!=q:q=parent[q]
        return q
    for q,t in edges:parent[root(q)]=root(t)
    return sorted(sorted(q for q in range(n) if root(q)==v) for v in {root(q) for q in range(n)})


def forward(rows):
    n=len(rows[0]);seed={p for p in combinations(range(n),2) if any(f[p[0]]==f[p[1]] for f in rows)}
    edges=set(seed);old=partition(n,edges);counts=[len(old)];levels={p:0 for p in edges};depth=0
    while True:
        new=edges|{tuple(sorted((f[x],f[y]))) for f in rows for x,y in edges if f[x]!=f[y]}
        now=partition(n,new)
        if now==old:break
        depth+=1
        for p in new-edges:levels[p]=depth
        edges=new;old=now;counts.append(len(old))
    forest=[];sp=set()
    for p in sorted(edges,key=lambda p:(levels[p],p)):
        if len(partition(n,sp|{p}))<len(partition(n,sp)):sp.add(p);forest.append(levels[p])
    initial=counts[0];final=counts[-1];D=initial-final
    assert depth<=D and sum(forest)<=D*(D+1)//2
    return dict(partition=old,component_counts=counts,depth=depth,forest_image_word_cost=sum(forest))


def scope(n):
    maps=list(product(range(n),repeat=n));stream=sha256();max_depth=max_cost=inputs=0
    for a in maps:
        for b in maps:
            z=forward([a,b]);inputs+=1;max_depth=max(max_depth,z['depth']);max_cost=max(max_cost,z['forest_image_word_cost'])
            stream.update(json.dumps([a,b,z],separators=(',',':')).encode()+b'\n')
    return dict(n=n,labeled_binary_inputs=inputs,maximum_depth=max_depth,maximum_forest_image_word_cost=max_cost,semantic_sha256=stream.hexdigest())


def chain(n):
    a=list(range(1,n))+[n-1];b=list(range(1,n-1))+[0,0];rs=[a,b];z=forward(rs)
    assert z['partition']==[[q] for q in range(n-2)]+[[n-2,n-1]] and z['depth']==0
    return dict(n=n,rows_sha256=sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest(),explicit_rows=rs if n<=40 else None,
                original_letter_ranks=[n-1,n-1],forward_partition=z['partition'],rt=n-1,reset_word_kind='a^(n-1)',
                all_shortest_word_kinds=['a^(n-1)','a^(n-2)b'],strongly_connected=True)


def terminal():
    rows=[[2,3,4,1,0,5],[0,5,3,2,3,1]];n=6;pairs=list(combinations(range(n),2));index={p:i for i,p in enumerate(pairs)}
    pred=[[] for _ in pairs];ds=[0]*len(pairs);choice=[None]*len(pairs);todo=deque()
    for i,(x,y) in enumerate(pairs):
        for a,f in enumerate(rows):
            if f[x]==f[y]:
                if not ds[i]:ds[i]=1;choice[i]=a;todo.append(i)
            else:pred[index[tuple(sorted((f[x],f[y]))) ]].append((i,a))
    while todo:
        i=todo.popleft()
        for j,a in pred[i]:
            if not ds[j]:ds[j]=ds[i]+1;choice[j]=a;todo.append(j)
    assert all(ds)
    layers=[dict(length=k,partition=partition(n,[p for p,d in zip(pairs,ds) if d<=k])) for k in range(1,max(ds)+1)]
    lam=next(z['length'] for z in layers if len(z['partition'])==1)
    Q=(1<<n)-1;prev={Q:None};todo=deque([Q]);endpoint=None
    while todo:
        S=todo.popleft()
        if S.bit_count()==1:endpoint=S;break
        for a,row in enumerate(rows):
            T=sum(1<<q for q in {row[q] for q in range(n) if S>>q&1})
            if T not in prev:prev[T]=(S,a);todo.append(T)
    word=[];S=endpoint
    while prev[S] is not None:S,a=prev[S];word.append(a)
    word=word[::-1]
    return dict(n=n,rows=rows,pair_distances=ds,terminal_layers=layers,connectivity_threshold=lam,
                state5_compress_with_another=min(d for (x,y),d in zip(pairs,ds) if y==5),rt=len(word),reset_word=word,subset_vertices_to_first_reset=len(prev))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/original_kernel_graph_boundary.json'));args=ap.parse_args()
    records=[chain(n) for n in list(range(3,41))+[65,129,257,513,1025,2051,4096]]
    out=dict(binary_scopes=[scope(n) for n in range(2,5)],chains=records,terminal=terminal(),
             status='PROVED paper general forward component stagnation and depth/certificate cost; forward kernel closure connectivity NOT necessary for sync even binary SC corank-one, EVERY n>=3; finite n6 terminal connectivity7 refutes n-step shortcut, no state-minimum claim; general Cerny OPEN, no formal kernel, priority OPEN')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(binary_inputs=sum(z['labeled_binary_inputs'] for z in out['binary_scopes']),chains=len(records),maximum_n=max(z['n'] for z in records),terminal=out['terminal'])),flush=True)


if __name__=='__main__':main()
