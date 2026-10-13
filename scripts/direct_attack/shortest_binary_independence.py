"""Exact original-word enumeration for the paper binary independence obstruction."""
import argparse
from collections import deque
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def rank(masks,n):
    basis={}
    for S in masks:
        v=[Fraction(int(S>>q&1)) for q in range(n)]
        for j,b in sorted(basis.items()):
            if v[j]:
                x=v[j];v=[a-x*c for a,c in zip(v,b)]
        p=next((j for j,x in enumerate(v) if x),None)
        if p is not None:
            x=v[p];basis[p]=[a/x for a in v]
    return len(basis)


def record(rows,word):
    n=len(rows[0]);Q=(1<<n)-1
    def image(S,a):return sum(1<<t for t in {rows[a][q] for q in range(n) if S>>q&1})
    def pre(S,a):return sum(1<<q for q in range(n) if S>>rows[a][q]&1)
    dist={Q:0};queue=deque([Q])
    while queue:
        S=queue.popleft()
        for a in range(2):
            T=image(S,a)
            if T not in dist:dist[T]=dist[S]+1;queue.append(T)
    rt=min(dist[1<<q] for q in range(n) if 1<<q in dist)
    tests=[];resets=[]
    for w in product(range(2),repeat=rt):
        S=Q;forward=[S]
        for a in w:S=image(S,a);forward.append(S)
        tests.append(dict(word=''.join('ab'[a] for a in w),image=S))
        if S.bit_count()!=1:continue
        inverse=[S]
        for a in reversed(w):S=pre(S,a);inverse.append(S)
        assert S==Q
        proper=inverse[1:-1]
        resets.append(dict(word=''.join('ab'[a] for a in w),forward_sets=forward,inverse_sets=inverse,
                           normalized_proper_dimension=rank(proper+[Q],n)-1,
                           raw_full_inverse_dimension=rank(inverse,n)))
    assert len(resets)==1 and resets[0]['word']==word
    return dict(n=n,rows=rows,original_letter_ranks=[len(set(r)) for r in rows],
                actual_images=sorted(dist),reset_threshold=rt,all_length_rt_words=tests,
                shortest_reset_words=resets,independent_proper_history=(
                    resets[0]['normalized_proper_dimension']==n-2),
                independent_full_inverse_history=(resets[0]['raw_full_inverse_dimension']==n))


def generate():
    main=record([[2,1,1,4,3],[3,0,1,1,2]],'abaa')
    main['pair_to_12_words']={'0,1':'a','0,2':'a','0,3':'ab','0,4':'aaba',
                             '1,2':'','1,3':'ba','1,4':'ba','2,3':'aba','2,4':'b','3,4':'b'}
    return dict(status='paper proof plus finite original-word certificate; independent checker required',
                main=main,
                initial_singleton_boundary=record([[1,0,0],[1,2,1]],'ba'),
                boundary='n5 refutes independent proper record-growth history among ALL globally shortest resets; n3 only refutes full histories including initial singleton; no long-phase or general Cerny conclusion')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='scripts/direct_attack/data/shortest_binary_independence.json')
    args=ap.parse_args();z=generate()
    Path(args.out).write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:{a:z[k][a] for a in ('n','reset_threshold','shortest_reset_words')} for k in ('main','initial_singleton_boundary')}))


if __name__=='__main__':main()
