"""Fixed-first-letter SAT diagnostic for compression equality.

A Boolean pair graph computes all merges before the target. Its edges must
have a vertex cover of size n-s. This quantifies over S without word traces.
Accepted proposals are independently checked. Negative solver answers remain
unverified diagnostics, not refutations.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import z3
from core_pair_probe import pair_distances
from audit_small import bfs,strong
from synthesize_safe import nonmergeable_pairs

def solve(first,s,target,timeout,iterations):
    n=len(first);pairs=list(combinations(range(n),2));number={p:i for i,p in enumerate(pairs)}
    kernels=[p for p in pairs if first[p[0]]==first[p[1]]];assert len(kernels)==1
    p,q=kernels[0];solver=z3.Tactic('sat').solver();solver.set(timeout=timeout)
    B=[[z3.Bool(f'b_{x}_{t}') for t in range(n)] for x in range(n)]
    for row in B:solver.add(z3.PbEq([(v,1) for v in row],1))
    for x,y in pairs:
        if (x,y)!=(p,q):
            for t in range(n):solver.add(z3.Or(z3.Not(B[x][t]),z3.Not(B[y][t])))
    holes=[z3.Bool(f'hole_{t}') for t in range(n)]
    solver.add(z3.PbEq([(v,1) for v in holes],n-s))
    previous=[z3.BoolVal(False) for pair in pairs]
    # At each level, merged[pair] is exactly the existence of a shorter merge.
    for depth in range(1,target):
        current=[z3.Bool(f'merge_{depth}_{i}') for i in range(len(pairs))]
        for i,(x,y) in enumerate(pairs):
            fx,fy=first[x],first[y]
            terms=[previous[i],z3.BoolVal(True) if fx==fy else previous[number[tuple(sorted((fx,fy)))]]]
            for u in range(n):
                for v in range(n):
                    reached=z3.BoolVal(True) if u==v else previous[number[tuple(sorted((u,v)))]]
                    if z3.is_false(reached):continue
                    terms.append(z3.And(B[x][u],B[y][v],reached))
            solver.add(current[i]==z3.Or(terms))
        previous=current
    for (x,y),merged in zip(pairs,previous):solver.add(z3.Implies(merged,z3.Or(holes[x],holes[y])))
    # Exact strong connectivity by directed graph closure in both directions.
    for reverse in (False,True):
        R=[z3.BoolVal(t==0) for t in range(n)]
        for depth in range(1,n):
            T=[z3.Bool(f'connected_{reverse}_{depth}_{t}') for t in range(n)]
            for t in range(n):
                terms=[R[t]]
                for x in range(n):
                    edge=z3.Or(z3.BoolVal(first[t]==x),B[t][x]) if reverse else z3.Or(z3.BoolVal(first[x]==t),B[x][t])
                    terms.append(z3.And(R[x],edge))
                solver.add(T[t]==z3.Or(terms))
            R=T
        solver.add(R)
    start=time.monotonic();cuts=[];blocked=[];status='iteration_limit';witness=None
    for iteration in range(1,iterations+1):
        answer=solver.check()
        if answer==z3.unknown:status='unknown: '+solver.reason_unknown();break
        if answer==z3.unsat:status='unsat_unverified_fixed_first_cover';break
        model=solver.model();second=[next(t for t in range(n) if z3.is_true(model.eval(B[x][t]))) for x in range(n)]
        rows=[first,second];S=[t for t in range(n) if not z3.is_true(model.eval(holes[t]))]
        assert len(S)==s and strong(rows)
        distances=pair_distances(rows)
        assert all(pair not in distances or distances[pair]>=target for pair in combinations(S,2))
        trap=nonmergeable_pairs(rows)
        if trap:
            C=set(trap);allowed=[(u,v) for u in range(n) for v in range(n) if u==v or tuple(sorted((u,v))) not in C]
            # The fixed first letter preserves a nonmergeable trap automatically.
            assert all(first[x]!=first[y] and tuple(sorted((first[x],first[y]))) in C for x,y in trap)
            solver.add(z3.Or([z3.And(B[x][u],B[y][v]) for x,y in trap for u,v in allowed]));cuts.append(trap)
        else:
            reaching,_=bfs(rows,range(n),lambda T:T==frozenset(S))
            if reaching is None:
                solver.add(z3.Or([z3.Not(B[x][second[x]]) for x in range(n)]));blocked.append(second)
            else:
                compression,_=bfs(rows,S,lambda T:len(T)<s);reset,_=bfs(rows,range(n),lambda T:len(T)==1)
                assert len(compression)==target
                _,images=bfs(rows,S,lambda T:False)
                scores={q:min([len(w) for T,w in images.items() if len(T)<s or q not in T]) for q in S}
                protected=[q for q in S if scores[q]>=target]
                status='compression_witness_verified'
                witness=dict(rows=rows,S=S,compression=target,reaching=reaching,attaining=compression,reset=reset,protected=protected,avoid_or_compress_scores=scores)
                break
    return dict(n=n,s=s,target=target,first=first,kernel_pair=[p,q],status=status,iterations=iteration,
                seconds=time.monotonic()-start,trap_cuts=len(cuts),blocked_rows=len(blocked),witness=witness,
                scope='Fixed first rank-one map; sole kernel union. Negative answers unverified.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('first',type=Path);ap.add_argument('s',type=int);ap.add_argument('target',type=int)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--timeout-ms',type=int,default=30000);ap.add_argument('--iterations',type=int,default=100)
    args=ap.parse_args();first=json.loads(args.first.read_text());result=solve(first,args.s,args.target,args.timeout_ms,args.iterations)
    args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))

if __name__=='__main__':main()
