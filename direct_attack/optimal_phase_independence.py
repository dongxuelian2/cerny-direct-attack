"""All optimal actual-image chains versus ALL shortest original reset words.

Two retained n5 automata are reused; the new claim concerns existence,
not the previously refuted assertion about every shortest history.
"""
import argparse
from collections import deque
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def rank(sets,n):
    basis={}
    for S in sets:
        v=[Fraction(int(S>>q&1)) for q in range(n)]
        for j,b in sorted(basis.items()):
            if v[j]:
                x=v[j];v=[a-x*c for a,c in zip(v,b)]
        j=next((j for j,x in enumerate(v) if x),None)
        if j is not None:
            x=v[j];basis[j]=[a/x for a in v]
    return len(basis)


def record(source):
    path=Path('direct_attack/data/n5_extremal')/('extremal_'+source+'.profile.json')
    rows=json.loads(path.read_text())['rows'];n=5;Q=31
    push=[[sum(1<<q for q in {row[r] for r in range(n) if S>>r&1})
           for row in rows] for S in range(Q+1)]
    pre=[[sum(1<<q for q in range(n) if S>>row[q]&1)
          for row in rows] for S in range(Q+1)]
    full={Q:0};queue=deque([Q])
    while queue:
        S=queue.popleft()
        for T in push[S]:
            if T not in full:full[T]=full[S]+1;queue.append(T)
    R=sorted(full);e={};parents={};G={Q:0};W={Q:0};vertices=0
    for S in sorted(set(R)-{Q},key=int.bit_count,reverse=True):
        dist={S:0};queue=deque([S]);best=None;goals=set()
        while queue:
            T=queue.popleft()
            if best is not None and dist[T]>=best:continue
            for U in pre[T]:
                if U in dist:continue
                dist[U]=dist[T]+1
                actual=[A for A in R if A.bit_count()>S.bit_count() and A&U==A]
                if actual:
                    if best is None:best=dist[U]
                    if dist[U]==best:goals.update(actual)
                elif U:queue.append(U)
        assert best is not None and goals
        vertices+=len(dist);e[S]=best;parents[S]=sorted(goals)
        G[S]=best+min(G[T] for T in goals);W[S]=best+max(W[T] for T in goals)
    P=min(G[1<<q] for q in range(n));rt=min(full[1<<q] for q in range(n))
    chains=[]
    def visit(S,trace):
        if S==Q:
            proper=[T for T in trace if 1<T.bit_count()<n]
            chains.append(dict(sets=trace[:],phase_costs=[e[T] for T in trace[:-1]],
                               proper_stages=len(proper),normalized_dimension=rank(proper+[Q],n)-1))
        else:
            for T in parents[S]:
                if e[S]+G[T]==G[S]:visit(T,trace+[T])
    for q in range(n):
        if G[1<<q]==P:visit(1<<q,[1<<q])
    words=[]
    for word in product(range(len(rows)),repeat=rt):
        S=Q
        for a in word:S=push[S][a]
        if S.bit_count()!=1:continue
        goal=S;maximum=1;milestones=[];costs=[];full_inverse=[S];last=0
        for step,a in enumerate(reversed(word),1):
            S=pre[S][a];full_inverse.append(S)
            if S.bit_count()>maximum:
                maximum=S.bit_count();milestones.append(S);costs.append(step-last);last=step
        assert S==Q and last==rt
        proper=[T for T in milestones if T!=Q]
        words.append(dict(original_indices=list(word),word=''.join('ab'[a] for a in word),goal=goal,
                          record_sets=milestones,record_costs=costs,full_inverse_sets=full_inverse,
                          normalized_record_dimension=rank(proper+[Q],n)-1,
                          full_inverse_raw_dimension=rank(full_inverse,n)))
    return dict(source=str(path).replace('\\','/'),n=n,rows=rows,actual_images=R,
                completely_reachable=len(R)==Q,rt=rt,P=P,
                extension=e,best=G,worst=W,parents=parents,
                singleton_G=[G[1<<q] for q in range(n)],optimal_chains=chains,
                optimal_endpoint_histories=len(chains),
                independent_optimal_chain=any(c['proper_stages']==c['normalized_dimension'] for c in chains),
                shortest_original_words=words,words_exhaustively_tested=len(rows)**rt,
                shortest_original_word_count=len(words),
                independent_shortest_record_history=any(
                    len(w['record_sets'])-1==w['normalized_record_dimension'] for w in words),
                inverse_vertices=vertices)


def generate():
    return dict(status='finite certificate; independent all-source/DAG/minor checker required',
                definition='proper stages exclude initial singleton and Q; normalized indicator rank is raw rank with Q minus one',
                records=[record(s) for s in ('004','005')],
                boundary='refutes independent OPTIMAL locally shortest actual-image chain existence; independent nongreedy globally shortest reset histories exist here; general Cerny OPEN')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='direct_attack/data/optimal_phase_independence.json')
    args=ap.parse_args();z=generate()
    Path(args.out).write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ('source','rt','P','optimal_endpoint_histories',
          'independent_optimal_chain','shortest_original_word_count','independent_shortest_record_history')}
          for r in z['records']]))


if __name__=='__main__':main()
