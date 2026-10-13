"""Independent forward rank-drop DAGs, augmented full reachability and block minors."""
import argparse
from collections import deque
import copy
from itertools import permutations
import json
from pathlib import Path


def determinant(matrix):
    value=0;size=len(matrix)
    for p in permutations(range(size)):
        term=(-1)**sum(p[i]>p[j] for i in range(size) for j in range(i+1,size))
        for i,j in enumerate(p):term*=matrix[i][j]
        value+=term
    return value


def verify(z):
    inputs=json.loads(Path('scripts/direct_attack/data/optimal_saturation_inputs.json').read_text())['records']
    assert len(z['records'])==2 and [r['d'] for r in z['records']]==[3,4]
    out=[];controls=0;augmented_vertices=0;literal_letters=0
    for r,source in zip(z['records'],inputs):
        n=source['n'];d=source['d'];Q=(1<<n)-1;rows=source['rows']
        assert r['n']==n and r['base_original_rows']==rows
        assert r['original_letter_ranks']==[n-1]*len(rows)
        assert all(len(row)==n and len(set(row))==n-1 for row in rows)
        added=[[q+1 if t==q else q if t==q+1 else t for t in range(n)] for q in range(n-1)]
        assert added==r['added_original_permutations']
        allrows=rows+added;tables=[];pop=[S.bit_count() for S in range(Q+1)]
        for a,row in enumerate(allrows):
            table=[0]*(Q+1)
            for S in range(1,Q+1):
                b=S&-S;table[S]=table[S^b]|(1<<row[b.bit_length()-1])
                assert pop[table[S]]>=pop[S]-1
                if a>=len(rows):assert pop[table[S]]==pop[S]
                controls+=1
            tables.append(table)
        # ALL-SUBSET forward DAG. A shortest length-(n-1) reset drops
        # exactly one point per letter; added permutation edges never qualify.
        finish=[False]*(Q+1);counts=[0]*(Q+1)
        for q in range(n):finish[1<<q]=True;counts[1<<q]=1
        for S in sorted(range(1,Q+1),key=lambda S:(pop[S],S)):
            if pop[S]==1:continue
            for a in range(len(rows)):
                T=tables[a][S]
                if pop[T]==pop[S]-1 and finish[T]:finish[S]=True;counts[S]+=counts[T]
        assert finish[Q]
        reached={Q};queue=deque([Q])
        while queue:
            S=queue.popleft()
            for a in range(len(rows)):
                T=tables[a][S]
                if pop[T]==pop[S]-1 and finish[T] and T not in reached:reached.add(T);queue.append(T)
        assert sorted(reached)==r['all_optimal_growth_masks']
        roots=sorted(S for S in reached if pop[S]==1)
        assert roots==r['optimal_inverse_roots']
        B=[set(range(2**i-1,2**(i+1)-1)) for i in range(d)]
        proper=[sum(1<<q for i,block in enumerate(B) if k>>i&1 for q in block) for k in range(2,n)]
        assert proper==r['canonical_proper_masks']
        assert reached==set(roots+proper+[Q])
        assert r['rt']==r['P']==n-1 and r['proper_stage_count']==n-2
        assert r['raw_proper_plus_Q_rank']==d and r['normalized_proper_rank']==d-1
        # Upper rank from constant-on-block cells, lower from explicitly
        # recovered block indicators. B0=S3-S2, Bi=S_(2^i) for i>=1.
        for S in proper:
            assert all(len({int(S>>q&1) for q in block})==1 for block in B)
        assert proper[1]&~proper[0]==sum(1<<q for q in B[0])
        for i in range(1,d):assert proper[2**i-2]==sum(1<<q for q in B[i])
        representatives=[min(block) for block in B]
        matrix=[[n*int(proper[2**i-2]>>q&1)-2**i for q in representatives[1:]] for i in range(1,d)]
        assert determinant(matrix)==n**(d-2)!=0
        words=[]
        def visit(S,path,trace):
            if pop[S]==1:
                words.append(dict(indices=path[:],forward=trace[:],endpoint=S));return
            for a in range(len(rows)):
                T=tables[a][S]
                if pop[T]==pop[S]-1 and finish[T]:visit(T,path+[a],trace+[T])
        visit(Q,[],[Q]);words.sort(key=lambda w:(w['endpoint'],w['indices']))
        assert counts[Q]==len(words)==r['shortest_original_word_count']
        assert len(roots)==r['optimal_endpoint_chain_count']
        assert [(w['endpoint'],w['indices']) for w in words]==[
            (w['endpoint'],w['original_indices']) for w in r['all_shortest_original_words']]
        for w,certificate in zip(words,r['all_shortest_original_words']):
            assert len(w['indices'])==n-1
            inverse=[w['endpoint']];target={q for q in range(n) if w['endpoint']>>q&1}
            for a in reversed(w['indices']):
                target={q for q in range(n) if rows[a][q] in target};inverse.append(sum(1<<q for q in target))
            assert inverse==certificate['inverse_sets']==list(reversed(w['forward']))
            assert inverse[1:-1]==proper
            for start in range(n):
                q=start
                for a in w['indices']:q=rows[a][q]
                assert 1<<q==w['endpoint']
            seed=next(q for q in range(n) if w['endpoint']>>q&1)
            block=next(block for block in B if seed in block)
            full_rank=d+(len(block)>1)
            assert full_rank==certificate['full_inverse_raw_rank']
            literal_letters+=n-1
        # Complete ordinary forward closure AFTER adjoining all adjacent
        # swaps: all nonempty subsets are literally reached. Membership costs
        # are separate from the minimum reset word; no cheap macro is used.
        actual={Q};queue=deque([Q])
        while queue:
            S=queue.popleft()
            for table in tables:
                T=table[S]
                if T not in actual:actual.add(T);queue.append(T)
        assert len(actual)==r['augmented_completely_reachable_count']==Q
        augmented_vertices+=len(actual)
        assert r['inverse_all_subset_vertices']==Q and r['inverse_label_edges']==Q*len(rows)
        out.append(dict(n=n,d=d,rt=n-1,P=n-1,proper_stages=n-2,
                        normalized_rank=d-1,all_shortest_words=len(words),optimal_endpoint_chains=len(roots),
                        full_inverse_ranks=[w['full_inverse_raw_rank'] for w in r['all_shortest_original_words']],
                        augmented_actual_images=len(actual),all_minimum_forward_vertices=len(reached),
                        centered_block_minor=determinant(matrix)))
    return dict(verified=True,records=out,all_original_label_subset_rank_controls=controls,
                augmented_full_forward_vertices=augmented_vertices,literal_shortest_original_letters=literal_letters,
                boundary='finite n7/15 low-dimensional ALL optimal histories; general permutation-saturation and complete-reachability transfer proved separately; no arbitrary-d family or formal kernel')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',default='scripts/direct_attack/data/optimal_saturation_history.json')
    ap.add_argument('--out',default='scripts/direct_attack/data/optimal_saturation_history_checks.json')
    args=ap.parse_args();z=json.loads(Path(args.root).read_text());result=verify(z);rejected=[]
    for name,change in (
        ('rank',lambda x:x['records'][1].update(normalized_proper_rank=4)),
        ('optimal_mask',lambda x:x['records'][1]['all_optimal_growth_masks'].append(3)),
        ('word_omission',lambda x:x['records'][0]['all_shortest_original_words'].pop()),
        ('permutation_row',lambda x:x['records'][1]['added_original_permutations'][0].__setitem__(0,0)),
        ('complete_reachability',lambda x:x['records'][1].update(augmented_completely_reachable_count=32766)),
        ('scope',lambda x:x['records'].append(copy.deepcopy(x['records'][-1]))),
    ):
        bad=copy.deepcopy(z);change(bad)
        try:verify(bad)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('corruption accepted: '+name)
    result.update(status='COMPUTATIONALLY VERIFIED finite d3/d4; general paper theorem separate; no formal verification',rejected_corruptions=rejected)
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
