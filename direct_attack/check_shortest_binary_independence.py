"""Independent inverse growth trees, literal state runs and determinant ranks."""
import argparse
from collections import deque
import copy
from itertools import combinations,permutations
import json
from pathlib import Path


def determinant(matrix):
    # Tiny matrices: Leibniz expansion is independent of generator elimination.
    size=len(matrix);value=0
    for p in permutations(range(size)):
        sign=(-1)**sum(p[i]>p[j] for i in range(size) for j in range(i+1,size))
        term=sign
        for i,j in enumerate(p):term*=matrix[i][j]
        value+=term
    return value


def minor_rank(matrix):
    for k in range(min(len(matrix),len(matrix[0])),0,-1):
        for r in combinations(range(len(matrix)),k):
            for c in combinations(range(len(matrix[0])),k):
                if determinant([[matrix[i][j] for j in c] for i in r]):return k
    return 0


def verify(z):
    out=[];state_controls=0;rank_checks=0
    for key,rows,word in (
        ('main',[[2,1,1,4,3],[3,0,1,1,2]],'abaa'),
        ('initial_singleton_boundary',[[1,0,0],[1,2,1]],'ba'),
    ):
        r=z[key];n=len(rows[0]);Q=set(range(n));qmask=(1<<n)-1
        assert r['n']==n and r['rows']==rows
        assert r['original_letter_ranks']==[n-1,n-1]
        # Paper lower bound: each original rank-(n-1) row loses at most one
        # image point from ANY subset; check every subset as a finite control.
        for S in range(1,1<<n):
            states={q for q in Q if S>>q&1}
            for row in rows:
                assert len({row[q] for q in states})>=len(states)-1;state_controls+=1
        # Independently enumerate only +1 inverse steps. A reset of n-1
        # letters MUST grow at every step, so this is exhaustive at the lower bound.
        growing_paths=[];tree_vertices=0
        def visit(states,reverse,trace):
            nonlocal tree_vertices
            tree_vertices+=1
            if len(reverse)==n-1:
                if states==Q:growing_paths.append((''.join(reversed(reverse)),trace[:]))
                return
            for label,row in zip('ab',rows):
                parent={q for q in Q if row[q] in states}
                if len(parent)==len(states)+1:visit(parent,reverse+[label],trace+[parent])
        for q in Q:visit({q},[],[{q}])
        assert len(growing_paths)==1 and growing_paths[0][0]==word
        assert r['reset_threshold']==n-1 and len(r['shortest_reset_words'])==1
        # Check every full original word retained by the generator by direct
        # runs of EACH original state, rather than subset table composition.
        expected_words=[]
        def enumerate_words(prefix):
            if len(prefix)==n-1:
                ends=[]
                for q in Q:
                    t=q
                    for a in prefix:t=rows['ab'.index(a)][t]
                    ends.append(t)
                expected_words.append(dict(word=prefix,image=sum(1<<q for q in set(ends))))
            else:
                for a in 'ab':enumerate_words(prefix+a)
        enumerate_words('')
        assert expected_words==r['all_length_rt_words']
        certificate=r['shortest_reset_words'][0];assert certificate['word']==word
        inverse=[sum(1<<q for q in states) for states in growing_paths[0][1]]
        assert inverse==certificate['inverse_sets']
        forward=[qmask];states=Q
        for a in word:
            states={rows['ab'.index(a)][q] for q in states};forward.append(sum(1<<q for q in states))
        assert forward==certificate['forward_sets'] and len(states)==1
        proper=inverse[1:-1]
        raw=minor_rank([[int(S>>q&1) for q in range(n)] for S in proper]+[[1]*n])
        centered=minor_rank([[n*int(S>>q&1)-S.bit_count() for q in range(n)] for S in proper])
        full=minor_rank([[int(S>>q&1) for q in range(n)] for S in inverse]);rank_checks+=3
        assert raw==centered+1
        assert centered==certificate['normalized_proper_dimension']==(2 if n==5 else 1)
        assert full==certificate['raw_full_inverse_dimension']==n-1
        assert r['independent_proper_history']==(centered==n-2)
        assert r['independent_full_inverse_history']==False
        # Independently recover actual image membership and strong connectivity.
        actual={qmask};queue=deque([Q])
        while queue:
            S=queue.popleft()
            for row in rows:
                T={row[q] for q in S};mask=sum(1<<q for q in T)
                if mask not in actual:actual.add(mask);queue.append(T)
        assert sorted(actual)==r['actual_images']
        for start in Q:
            reached={start};queue=deque([start])
            while queue:
                q=queue.popleft()
                for row in rows:
                    if row[q] not in reached:reached.add(row[q]);queue.append(row[q])
            assert reached==Q
        if n==5:
            assert inverse==[2,6,7,30,31]
            assert all(int(6>>q&1)+1==int(7>>q&1)+int(30>>q&1) for q in Q)
            pair_words=r['pair_to_12_words']
            assert set(pair_words)=={str(s)+','+str(t) for s,t in combinations(range(n),2)}
            for pair,w in pair_words.items():
                states=set(map(int,pair.split(',')))
                for a in w:states={rows['ab'.index(a)][q] for q in states}
                assert states=={1,2}
            # Congruence identifying 1,2 also identifies 0 via b, then 3
            # via b on 0,1, then 4 via a on 0,3. Every pair therefore
            # generates the universal relation: the automaton is simple.
            assert rows[1][1]==0 and rows[1][2]==1
            assert rows[1][0]==3 and rows[1][1]==0
            assert rows[0][0]==2 and rows[0][3]==4
        else:
            assert inverse==[1,6,7]
            assert all(int(1>>q&1)+int(6>>q&1)==1 for q in Q)
        out.append(dict(n=n,rt=n-1,unique_shortest_original_word=word,strongly_connected=True,
                        simple=(True if n==5 else None),
                        inverse_growth_tree_vertices=tree_vertices,actual_images=len(actual),
                        inverse_sets=inverse,proper_normalized_rank=centered,full_raw_rank=full))
    return dict(verified=True,records=out,all_subset_rank_defect_controls=state_controls,
                determinant_rank_checks=rank_checks,all_shortest_length_words_literally_tested=20,
                boundary='n5 proper-stage independence REFUTED on a unique globally shortest word; n3 full-history including seed is a different convention; no long-phase bound or Cerny proof')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',default='direct_attack/data/shortest_binary_independence.json')
    ap.add_argument('--out',default='direct_attack/data/shortest_binary_independence_checks.json')
    args=ap.parse_args();z=json.loads(Path(args.root).read_text());result=verify(z);rejected=[]
    for name,change in (
        ('shortest_word',lambda x:x['main']['shortest_reset_words'][0].update(word='baaa')),
        ('rank',lambda x:x['main']['shortest_reset_words'][0].update(normalized_proper_dimension=3)),
        ('independent_exists',lambda x:x['main'].update(independent_proper_history=True)),
        ('threshold',lambda x:x['main'].update(reset_threshold=3)),
        ('omitted_test_word',lambda x:x['main']['all_length_rt_words'].pop()),
        ('n3_convention',lambda x:x['initial_singleton_boundary'].update(independent_proper_history=False)),
        ('simplicity_pair_word',lambda x:x['main']['pair_to_12_words'].update({'3,4':'a'})),
    ):
        bad=copy.deepcopy(z);change(bad)
        try:verify(bad)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('accepted corruption: '+name)
    result.update(status='COMPUTATIONALLY VERIFIED finite; paper proofs separate; no formal kernel',rejected_corruptions=rejected)
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
