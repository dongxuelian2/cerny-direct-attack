"""Independent ALL-SOURCE forward transport, shortest-word DAG and minor ranks."""
import argparse
from collections import deque
import copy
from itertools import combinations
import json
from pathlib import Path


def det(matrix):
    a=[r[:] for r in matrix];sign=1;previous=1
    for j in range(len(a)-1):
        p=next((p for p in range(j,len(a)) if a[p][j]),None)
        if p is None:return 0
        if p!=j:a[j],a[p]=a[p],a[j];sign=-sign
        pivot=a[j][j]
        for x in range(j+1,len(a)):
            for y in range(j+1,len(a)):
                value=a[x][y]*pivot-a[x][j]*a[j][y]
                assert value%previous==0
                a[x][y]=value//previous
            a[x][j]=0
        previous=pivot
    return sign*a[-1][-1]


def rank(matrix):
    for k in range(min(len(matrix),len(matrix[0])),0,-1):
        for r in combinations(range(len(matrix)),k):
            for c in combinations(range(len(matrix[0])),k):
                if det([[matrix[i][j] for j in c] for i in r]):return k
    return 0


def verify(z):
    inputs=[[[0,2,3,4,1],[1,0,3,2,0]],[[0,0,2,4,3],[2,0,3,4,1]]]
    summaries=[];total_vertices=0;total_entries=0;rank_checks=0;literal_letters=0
    assert len(z['records'])==2
    for r,rows,expected_rt in zip(z['records'],inputs,(15,14)):
        assert r['n']==5 and r['rows']==rows
        assert json.loads(Path(r['source']).read_text())['rows']==rows
        n=5;Q=31
        def move(S,a):return sum(1<<q for q in {rows[a][q] for q in range(n) if S>>q&1})
        edges={S:[move(S,a) for a in range(2)] for S in range(1,Q+1)}
        def bfs(start):
            d={start:0};queue=deque([start])
            while queue:
                S=queue.popleft()
                for T in edges[S]:
                    if T not in d:d[T]=d[S]+1;queue.append(T)
            return d
        closure=bfs(Q);R=sorted(closure)
        assert R==r['actual_images'] and r['completely_reachable']==(len(R)==Q)
        D={S:bfs(S) for S in R}
        vertices=sum(map(len,D.values()));entries=len(R)**2
        total_vertices+=vertices;total_entries+=entries
        transport={T:{S:min(ell for U,ell in D[T].items() if U&S==U) for S in R} for T in R}
        e={};parents={};G={Q:0};W={Q:0}
        for S in sorted(set(R)-{Q},key=int.bit_count,reverse=True):
            larger=[T for T in R if T.bit_count()>S.bit_count()]
            e[S]=min(transport[T][S] for T in larger)
            parents[S]=[T for T in larger if transport[T][S]==e[S]]
            G[S]=e[S]+min(G[T] for T in parents[S]);W[S]=e[S]+max(W[T] for T in parents[S])
        for name,actual in (('extension',e),('best',G),('worst',W),('parents',parents)):
            assert {int(k):v for k,v in r[name].items()}==actual
        rt=min(closure[1<<q] for q in range(n));P=min(G[1<<q] for q in range(n))
        assert rt==P==expected_rt==r['rt']==r['P']
        assert r['singleton_G']==[G[1<<q] for q in range(n)]
        chains=[]
        def normalized(sets):
            nonlocal rank_checks
            raw=rank([[int(S>>q&1) for q in range(n)] for S in sets]+[[1]*n])
            centered=rank([[n*int(S>>q&1)-S.bit_count() for q in range(n)] for S in sets])
            assert raw==centered+1;rank_checks+=2
            return centered
        def visit(S,path):
            if S==Q:
                proper=[T for T in path if 1<T.bit_count()<n]
                chains.append(dict(sets=path[:],phase_costs=[e[T] for T in path[:-1]],
                                   proper_stages=len(proper),normalized_dimension=normalized(proper)))
            else:
                for T in parents[S]:
                    if e[S]+G[T]==G[S]:visit(T,path+[T])
        for q in range(n):
            if G[1<<q]==P:visit(1<<q,[1<<q])
        assert chains==r['optimal_chains'] and len(chains)==r['optimal_endpoint_histories']==1
        independent=any(c['proper_stages']==c['normalized_dimension'] for c in chains)
        assert independent==r['independent_optimal_chain']==False
        assert chains[0]['normalized_dimension']==2 and chains[0]['proper_stages']==3
        # Independent enumeration uses the forward shortest-image DAG. Every
        # prefix of a shortest reset word is a shortest path to its own image.
        tail={S:min(D[S][1<<q] for q in range(n)) for S in R}
        word_indices=[]
        def words(S,path):
            if len(path)==rt:
                assert S.bit_count()==1;word_indices.append(path[:]);return
            for a,T in enumerate(edges[S]):
                if closure[T]==len(path)+1 and closure[T]+tail[T]==rt:words(T,path+[a])
        words(Q,[])
        assert word_indices==[w['original_indices'] for w in r['shortest_original_words']]
        assert len(word_indices)==r['shortest_original_word_count']
        assert r['words_exhaustively_tested']==2**rt
        independent_word=False;word_summaries=[]
        for w in r['shortest_original_words']:
            word=w['original_indices'];assert w['word']==''.join('ab'[a] for a in word)
            image=set(range(n))
            for a in word:image={rows[a][q] for q in image}
            assert len(image)==1 and sum(1<<q for q in image)==w['goal']
            literal_letters+=len(word)
            current=image;full=[w['goal']];records=[];costs=[];last=0;maximum=1
            for step,a in enumerate(reversed(word),1):
                current={q for q in range(n) if rows[a][q] in current}
                mask=sum(1<<q for q in current);full.append(mask)
                if len(current)>maximum:
                    maximum=len(current);records.append(mask);costs.append(step-last);last=step
            assert current==set(range(n)) and full==w['full_inverse_sets']
            assert records==w['record_sets'] and costs==w['record_costs'] and sum(costs)==rt
            proper=records[:-1];dimension=normalized(proper)
            full_rank=rank([[int(S>>q&1) for q in range(n)] for S in full]);rank_checks+=1
            assert dimension==w['normalized_record_dimension']
            assert full_rank==w['full_inverse_raw_dimension']==5
            independent_word|=dimension==len(proper)
            word_summaries.append(dict(word=w['word'],record_sets=records,record_costs=costs,
                                       normalized_dimension=dimension,full_inverse_raw_dimension=full_rank))
        assert independent_word==r['independent_shortest_record_history']==True
        # Check the shared-core Boolean diamond, the exact dependence used.
        proper=chains[0]['sets'][1:-1];A,B,C=proper
        assert A==B&C and B|C==Q
        assert all(int(A>>q&1)+1==int(B>>q&1)+int(C>>q&1) for q in range(n))
        summaries.append(dict(source=r['source'],actual_images=len(R),rt=rt,P=P,
                              all_source_vertices=vertices,transport_entries=entries,
                              optimal_chain=chains[0],shortest_words=word_summaries,
                              independent_optimal_chain=False,independent_shortest_record_history=True))
    return dict(verified=True,records=summaries,all_source_vertices=total_vertices,
                transport_entries=total_entries,exact_minor_rank_checks=rank_checks,
                literal_shortest_reset_words=5,literal_original_letters=literal_letters,
                interpretation='existence of independent optimal locally shortest policy stages REFUTED at n5; nongreedy shortest-word independence survives these examples')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',default='scripts/direct_attack/data/optimal_phase_independence.json')
    ap.add_argument('--out',default='scripts/direct_attack/data/optimal_phase_independence_checks.json')
    args=ap.parse_args();z=json.loads(Path(args.root).read_text());result=verify(z);rejected=[]
    for name,change in (
        ('independent_optimum',lambda x:x['records'][1].update(independent_optimal_chain=True)),
        ('chain_count',lambda x:x['records'][0].update(optimal_endpoint_histories=2)),
        ('omitted_shortest_word',lambda x:x['records'][1]['shortest_original_words'].pop(0)),
        ('nongreedy_phase_cost',lambda x:x['records'][1]['shortest_original_words'][0]['record_costs'].__setitem__(1,5)),
        ('normalized_rank',lambda x:x['records'][1]['optimal_chains'][0].update(normalized_dimension=3)),
        ('parent',lambda x:x['records'][1]['parents']['3'].append(19)),
        ('reset_threshold',lambda x:x['records'][1].update(rt=13)),
    ):
        bad=copy.deepcopy(z);change(bad)
        try:verify(bad)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('corruption accepted: '+name)
    result.update(status='COMPUTATIONALLY VERIFIED finite; paper state-minimality lemma separate; no formal proof kernel',rejected_corruptions=rejected)
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))


if __name__=='__main__':main()
