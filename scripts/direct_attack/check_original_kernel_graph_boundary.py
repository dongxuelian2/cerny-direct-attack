"""Independent class joins, pair-word enumeration and chain controls."""
import argparse
from collections import deque
import copy
from hashlib import sha256
from itertools import product,combinations
import json
from pathlib import Path


def blocks(n,sets):
    classes=[{q} for q in range(n)]
    for S in sets:
        touched=[C for C in classes if C&S]
        if touched:
            new=set().union(*touched)
            classes=[C for C in classes if not C&S]+[new]
    return sorted(sorted(C) for C in classes)


def independent_forward(rows):
    n=len(rows[0]);fibers=[{q for q in range(n) if f[q]==t} for f in rows for t in set(f)]
    current=blocks(n,fibers);counts=[len(current)]
    while True:
        sets=[set(C) for C in current]+[{f[q] for q in C} for f in rows for C in current]
        new=blocks(n,sets)
        if new==current:break
        current=new;counts.append(len(current))
    seed={p for p in combinations(range(n),2) if any(f[p[0]]==f[p[1]] for f in rows)}
    distances={p:0 for p in seed};todo=deque(seed)
    while todo:
        x,y=todo.popleft()
        for f in rows:
            if f[x]==f[y]:continue
            T=tuple(sorted((f[x],f[y])))
            if T not in distances:distances[T]=distances[x,y]+1;todo.append(T)
    forest_classes=[{q} for q in range(n)];cost=0
    for (x,y),d in sorted(distances.items(),key=lambda z:(z[1],z[0])):
        X=next(C for C in forest_classes if x in C);Y=next(C for C in forest_classes if y in C)
        if X is not Y:forest_classes.remove(X);forest_classes.remove(Y);forest_classes.append(X|Y);cost+=d
    assert sorted(sorted(C) for C in forest_classes)==current
    depth=len(counts)-1;D=counts[0]-counts[-1]
    assert depth<=D and cost<=D*(D+1)//2
    for C in current:
        for f in rows:assert any({f[q] for q in C}<=set(K) for K in current)
    return dict(partition=current,component_counts=counts,depth=depth,forest_image_word_cost=cost)


def scope(z):
    n=z['n'];maps=list(product(range(n),repeat=n));stream=sha256();inputs=maxdepth=maxcost=0
    for a in maps:
        for b in maps:
            report=independent_forward([a,b]);inputs+=1
            maxdepth=max(maxdepth,report['depth']);maxcost=max(maxcost,report['forest_image_word_cost'])
            stream.update(json.dumps([a,b,report],separators=(',',':')).encode()+b'\n')
    assert inputs==z['labeled_binary_inputs'] and maxdepth==z['maximum_depth'] and maxcost==z['maximum_forest_image_word_cost']
    assert stream.hexdigest()==z['semantic_sha256']
    return dict(n=n,inputs=inputs,maximum_depth=maxdepth,maximum_forest_cost=maxcost)


def compose(rows,w):
    f=list(range(len(rows[0])))
    for a in w:f=[rows[a][q] for q in f]
    return f


def chain(z):
    n=z['n'];a=[min(q+1,n-1) for q in range(n)];b=[(q+1)%(n-1) if q<n-1 else 0 for q in range(n)];rs=[a,b]
    assert sha256(json.dumps(rs,separators=(',',':')).encode()).hexdigest()==z['rows_sha256']
    assert z['explicit_rows']==(rs if n<=40 else None)
    assert z['original_letter_ranks']==[len(set(f)) for f in rs]==[n-1,n-1]
    expected=[[q] for q in range(n-2)]+[[n-2,n-1]]
    assert expected==z['forward_partition']
    for f in rs:
        assert f[n-2]==f[n-1]
        if n<=40:assert all(f[q]!=f[t] for q in range(n) for t in range(q+1,n) if t!=n-1 or q!=n-2)
        else:assert len(set(f))==n-1
    assert z['rt']==n-1 and z['reset_word_kind']=='a^(n-1)'
    assert z['all_shortest_word_kinds']==['a^(n-1)','a^(n-2)b'] and z['strongly_connected'] is True
    # Explicit b cycle plus the a entrance and b exit of the last state prove SC.
    assert b[:n-1]==list(range(1,n-1))+[0] and a[n-2]==n-1 and b[n-1]==0
    letters=word_scopes=0
    if n<=40:
        for w in ([0]*(n-1),[0]*(n-2)+[1]):
            assert len(set(compose(rs,w)))==1;letters+=len(w)
        assert independent_forward(rs)['partition']==expected
    if n<=8:
        shortest=[]
        for w in product(range(2),repeat=n-1):
            word_scopes+=1
            if len(set(compose(rs,w)))==1:shortest.append(w)
        assert set(shortest)=={tuple([0]*(n-1)),tuple([0]*(n-2)+[1])}
    return dict(n=n,literal_reset_letters=letters,enumerated_words=word_scopes)


def terminal(z):
    rows=z['rows'];assert rows==[[2,3,4,1,0,5],[0,5,3,2,3,1]];n=6;pairs=list(combinations(range(n),2));ds={};words=0
    for length in range(1,11):
        for w in product(range(2),repeat=length):
            f=compose(rows,w);words+=1
            for p in pairs:
                if p not in ds and f[p[0]]==f[p[1]]:ds[p]=length
    assert [ds[p] for p in pairs]==z['pair_distances']==[6,2,3,3,7,7,10,4,9,5,1,9,6,8,8]
    layers=[dict(length=k,partition=blocks(n,[set(p) for p in pairs if ds[p]<=k])) for k in range(1,11)]
    assert layers==z['terminal_layers']
    assert z['connectivity_threshold']==z['state5_compress_with_another']==7
    assert layers[5]['partition']==[list(range(5)),[5]] and layers[6]['partition']==[list(range(6))]
    assert [len(set(row)) for row in rows]==[6,5]
    for start in range(n):
        reached={start};todo=[start]
        for q in todo:
            for f in rows:
                if f[q] not in reached:reached.add(f[q]);todo.append(f[q])
        assert len(reached)==n
    Q=frozenset(range(n));distance={Q:0};todo=deque([Q]);first_count=None;rt=None
    while todo:
        S=todo.popleft()
        if len(S)==1 and rt is None:rt=distance[S];first_count=len(distance)
        for f in rows:
            T=frozenset(f[q] for q in S)
            if T not in distance:distance[T]=distance[S]+1;todo.append(T)
    assert rt==z['rt'] and rt<25 and first_count==z['subset_vertices_to_first_reset']
    assert len(z['reset_word'])==rt and len(set(compose(rows,z['reset_word'])))==1
    return dict(rt=rt,subset_vertices=len(distance),enumerated_words=words,pair_vertices=len(pairs))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('scripts/direct_attack/data/original_kernel_graph_boundary.json'))
    ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/original_kernel_graph_boundary_checks.json'));args=ap.parse_args();data=json.loads(args.source.read_text())
    assert [z['n'] for z in data['binary_scopes']]==[2,3,4]
    assert [z['n'] for z in data['chains']]==list(range(3,41))+[65,129,257,513,1025,2051,4096]
    sr=[scope(z) for z in data['binary_scopes']];cr=[chain(z) for z in data['chains']];tr=terminal(data['terminal']);bad=[]
    for key,value in [('rt',0),('connectivity_threshold',6),('state5_compress_with_another',6),('reset_word',[])]:
        z=copy.deepcopy(data['terminal']);z[key]=value;bad.append((terminal,z))
    z=copy.deepcopy(data['terminal']);z['pair_distances'][4]-=1;bad.append((terminal,z))
    z=copy.deepcopy(data['terminal']);z['terminal_layers'][5]['partition']=[list(range(6))];bad.append((terminal,z))
    for key,value in [('rt',1),('rows_sha256','0'*64),('forward_partition',[[0,1,2]]),('all_shortest_word_kinds',[]),('strongly_connected',False)]:
        z=copy.deepcopy(data['chains'][0]);z[key]=value;bad.append((chain,z))
    z=copy.deepcopy(data['binary_scopes'][0]);z['semantic_sha256']='0'*64;bad.append((scope,z))
    for check,z in bad:
        try:check(z)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,labeled_binary_inputs=sum(z['inputs'] for z in sr),chain_parameters=len(cr),maximum_n=max(z['n'] for z in cr),
             literal_reset_letters=sum(z['literal_reset_letters'] for z in cr),chain_words_enumerated=sum(z['enumerated_words'] for z in cr),terminal_report=tr,
             corruptions_rejected=len(bad),binary_reports=sr,chain_reports=cr,
             boundary='General forward-congruence depth/forest lemma and all-n failure PROVED paper; finite n6 original terminal connectivity7, rt below square; only listed finite scopes COMPUTATIONALLY VERIFIED, priority and Cerny OPEN, no formal kernel')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if not k.endswith('_reports')}),flush=True)


if __name__=='__main__':main()
