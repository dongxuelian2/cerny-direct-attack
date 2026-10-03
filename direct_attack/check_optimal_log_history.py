"""Independent all-source forward distances and determinant-minor history rank."""
import argparse
from collections import Counter,deque
import copy
from itertools import combinations
import json
from pathlib import Path


def determinant(matrix):
    a=[row[:] for row in matrix]
    n=len(a)
    if n==0:return 1
    sign=1; previous=1
    for j in range(n-1):
        p=next((p for p in range(j,n) if a[p][j]),None)
        if p is None:return 0
        if p!=j:a[j],a[p]=a[p],a[j];sign=-sign
        pivot=a[j][j]
        for x in range(j+1,n):
            for y in range(j+1,n):
                value=a[x][y]*pivot-a[x][j]*a[j][y]
                assert value%previous==0
                a[x][y]=value//previous
            a[x][j]=0
        previous=pivot
    return sign*a[-1][-1]


def minor_rank(matrix):
    for r in range(min(len(matrix),len(matrix[0])),0,-1):
        for ri in combinations(range(len(matrix)),r):
            for ci in combinations(range(len(matrix[0])),r):
                if determinant([[matrix[i][j] for j in ci] for i in ri]):return r
    return 0


def verify(z):
    assert z['n']==7 and z['d']==3
    n=7;Q=127
    blocks=[[0],[1,2],[3,4,5,6]]
    selected=lambda k:{q for i,B in enumerate(blocks) if k>>i&1 for q in B}
    originals=[]
    for j in range(6):
        row=[j+1 if q==j else j if q==j+1 else q for q in range(n)]
        originals.append(row)
    for k in range(2,7):
        block=next(i for i in (1,2) if (k+1)>>i&1)
        X=selected(k+1)-{blocks[block][0]}; S=selected(k)
        row=[None]*n
        for left,right in ((X,S),(set(range(n))-X,set(range(n))-S)):
            for x,y in zip(sorted(left),sorted(right)):row[x]=y
        originals.append(row)
    for s,t in ((1,2),(2,1),(3,4),(4,3)):
        originals.append([t if q==s else q for q in range(n)])
    assert originals==z['original_labeled_rows']
    rows=sorted(set(map(tuple,originals)))
    assert [list(row) for row in rows]==z['unique_induced_rows']
    def push(S,row): return sum(1<<q for q in {row[r] for r in range(n) if S>>r&1})
    edges={S:sorted({push(S,row) for row in rows}) for S in range(1,Q+1)}
    move_label={}
    for S in edges:
        for index,row in enumerate(rows):move_label.setdefault((S,push(S,row)),index)
    original_label={tuple(row):originals.index(list(row)) for row in rows}
    distances={};trees={};vertices=0
    for start in range(1,Q+1):
        dist={start:0};previous={};queue=deque([start])
        while queue:
            S=queue.popleft()
            for T in edges[S]:
                if T not in dist:
                    dist[T]=dist[S]+1;previous[T]=(S,move_label[S,T]);queue.append(T)
        distances[start]=dist;trees[start]=previous;vertices+=len(dist)
    assert set(distances[Q])==set(range(1,Q+1))
    rt=min(distances[Q][1<<q] for q in range(n))
    # Every entry is ordinary all-source into-subset transport, with strict arrivals.
    transport={}
    for start,dist in distances.items():
        transport[start]={S:min(ell for T,ell in dist.items() if T&S==T) for S in range(1,Q+1)}
    e={};parents={};G={Q:0};W={Q:0}
    for S in sorted(range(1,Q),key=int.bit_count,reverse=True):
        larger=[T for T in range(1,Q+1) if T.bit_count()>S.bit_count()]
        cost=min(transport[T][S] for T in larger)
        goals=[T for T in larger if transport[T][S]==cost]
        e[S]=cost;parents[S]=goals
        assert all(T.bit_count()==S.bit_count()+1 for T in goals)
        G[S]=cost+min(G[T] for T in goals)
        W[S]=cost+max(W[T] for T in goals)
    for name,actual in (('extension',e),('parents',parents),('best',G),('worst',W)):
        assert {int(k):v for k,v in z[name].items()}==actual
    P=min(G[1<<q] for q in range(n))
    assert P==z['P']==rt==9
    assert z['singleton_G']==[G[1<<q] for q in range(n)]
    chains=[];hist=Counter();ranks=0;word_certificates=[]
    def visit(S,trace):
        nonlocal ranks
        if S==Q:
            proper=[T for T in trace if 1<T.bit_count()<n]
            raw=[[int(T>>q&1) for q in range(n)] for T in proper]+[[1]*n]
            centered=[[n*int(T>>q&1)-T.bit_count() for q in range(n)] for T in proper]
            r=minor_rank(raw); c=minor_rank(centered)
            assert r==c+1
            ranks+=2;hist[c]+=1
            costs=[e[T] for T in trace[:-1]]
            assert sum(costs)==P and len(proper)==n-2
            chains.append(dict(sets=trace[:],phase_costs=costs,normalized_dimension=c,proper_stages=len(proper)))
            word=[];phase_words=[]
            for child,parent in zip(trace[:-1],trace[1:]):
                endpoint=min(T for T,ell in distances[parent].items() if T&child==T and ell==e[child])
                current=endpoint; backward=[]
                while current!=parent:
                    before,label=trees[parent][current]
                    backward.append(original_label[rows[label]])
                    current=before
                phase=list(reversed(backward))
                assert len(phase)==e[child]
                image=parent
                for label in phase:image=push(image,originals[label])
                assert image&child==image
                word=phase+word;phase_words.append(phase)
            image=Q
            for label in word:image=push(image,originals[label])
            assert image==trace[0] and len(word)==P
            word_certificates.append(dict(endpoint_set=trace[0],sets=trace[:],
                 phase_original_row_indices=phase_words,whole_original_row_indices=word,cost=P))
            return
        for T in parents[S]:
            if e[S]+G[T]==G[S]:visit(T,trace+[T])
    for q in range(n):
        if G[1<<q]==P:visit(1<<q,[1<<q])
    assert chains==z['optimal_chains'] and len(chains)==z['optimal_endpoint_histories']==68
    assert {int(k):v for k,v in z['normalized_dimension_histogram'].items()}==dict(hist)=={3:14,4:34,5:20}
    assert z['minimum_normalized_dimension']==min(hist)==3
    assert z['maximum_normalized_dimension']==max(hist)==5
    return dict(verified=True,n=n,original_labeled_rows=len(originals),unique_induced_rows=len(rows),
                actual_images=Q,all_source_forward_vertices=vertices,transport_entries=Q*Q,
                optimal_endpoint_histories=len(chains),normalized_histogram=dict(hist),exact_minor_rank_checks=ranks,
                rt=rt,P=P,minimum_normalized_dimension=min(hist),maximum_normalized_dimension=max(hist),
                literal_optimal_reset_words=len(word_certificates),literal_original_letters=sum(w['cost'] for w in word_certificates),
                word_certificates=word_certificates,word_index_boundary='indices into generator certificate original_labeled_rows',
                interpretation='finite all optimal endpoint chains; high-dimension optimal choices DO exist; no all-n guarantee')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default='direct_attack/data/optimal_log_history_n7.json')
    ap.add_argument('--out',default='direct_attack/data/optimal_log_history_n7_checks.json')
    args=ap.parse_args()
    z=json.loads(Path(args.root).read_text(encoding='utf-8'))
    result=verify(z)
    rejected=[]
    for name,change in (
        ('minimum_dimension',lambda x:x.update(minimum_normalized_dimension=2)),
        ('history_count',lambda x:x.update(optimal_endpoint_histories=67)),
        ('histogram',lambda x:x['normalized_dimension_histogram'].update({'3':13})),
        ('parent',lambda x:x['parents']['6'].append(127)),
        ('chain_cost',lambda x:x['optimal_chains'][0]['phase_costs'].__setitem__(0,2)),
        ('original_row',lambda x:x['original_labeled_rows'][0].__setitem__(0,0)),
    ):
        bad=copy.deepcopy(z);change(bad)
        try:verify(bad)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('corruption accepted: '+name)
    result.update(status='COMPUTATIONALLY VERIFIED finite only; no formal proof kernel',rejected_corruptions=rejected)
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='word_certificates'}))


if __name__=='__main__':main()
