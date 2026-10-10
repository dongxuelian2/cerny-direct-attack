"""Bounded-alphabet synthesis with one-hot letters and exact Boolean closures.

No array-indexed pair potential or distance rank is used. Every accepted
positive is checked by ordinary forward BFS, including all reachable images.
Negative solver output is not a certified mathematical upper bound.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import z3
from alphabet_check import bfs, certificate, pair_distances, strong, verify
from early_pair_alphabet_pool import patterns


def main():
    ap=argparse.ArgumentParser()
    for name in ("n","s","target"):ap.add_argument(name,type=int)
    ap.add_argument("--letters",type=int,default=3)
    ap.add_argument("--protected",type=int,default=0)
    ap.add_argument("--early-pattern",type=int,choices=range(9))
    ap.add_argument("--holes",nargs="+",type=int)
    ap.add_argument("--fixed",type=Path)
    ap.add_argument("--timeout-ms",type=int,default=120000)
    ap.add_argument("--iterations",type=int,default=100)
    ap.add_argument("--out",type=Path,required=True);args=ap.parse_args()
    n,s,t,k=args.n,args.s,args.target,args.letters
    assert 2<=s<n and 2<=k<=26 and 0<=args.protected<s
    assert 1<=t<=(n-s+2)*(n-s+1)//2
    pairs=list(combinations(range(n),2));P=len(pairs);K=(0,1)
    solver=z3.Tactic("sat").solver();solver.set(timeout=args.timeout_ms)
    B=[[[z3.Bool(f"letter_{ell}_{q}_{u}") for u in range(n)] for q in range(n)] for ell in range(k)]
    for letter in B:
        for row in letter:solver.add(z3.PbEq([(v,1) for v in row],1))
        for x,y in pairs:
            if (x,y)!=K:solver.add([z3.Not(z3.And(letter[x][u],letter[y][u])) for u in range(n)])
    solver.add([B[0][0][u]==B[0][1][u] for u in range(n)])
    if args.fixed:
        fixed=json.loads(args.fixed.read_text());assert len(fixed)==k and all(len(row)==n for row in fixed)
        solver.add([B[ell][q][u]==(fixed[ell][q]==u) for ell in range(k) for q in range(n) for u in range(n)])
    edge={}
    for x,y in pairs:
        for u,v in pairs:
            active=z3.Bool(f"pair_edge_{x}_{y}_{u}_{v}")
            solver.add(active==z3.Or([z3.And(letter[x][u],letter[y][v]) for letter in B]+
                                    [z3.And(letter[x][v],letter[y][u]) for letter in B]))
            edge[x,y,u,v]=active
    merged={pair:z3.BoolVal(pair==K) for pair in pairs}
    short=None;tight=t==(n-s+2)*(n-s+1)//2
    start=time.monotonic()
    for depth in range(1,P+1):
        if depth>1:
            following={pair:z3.Bool(f"merge_{depth}_{pair[0]}_{pair[1]}") for pair in pairs}
            for x,y in pairs:
                solver.add(following[x,y]==z3.Or([merged[x,y]]+
                            [z3.And(edge[x,y,u,v],merged[u,v]) for u,v in pairs]))
            merged=following
        if tight and depth<=n-s:
            solver.add(z3.PbEq([(merged[pair],1) for pair in pairs],depth))
        if args.early_pattern is not None and depth<=3:
            assert tight and n-s>=3 and n>=6
            prefix=set(patterns()[args.early_pattern][:depth])
            solver.add([merged[pair]==(pair in prefix) for pair in pairs])
        if depth==t-1:short=dict(merged)
    solver.add(list(merged.values()))
    holes=[z3.Bool(f"hole_{q}") for q in range(n)]
    solver.add(z3.PbEq([(v,1) for v in holes],n-s))
    if args.holes is not None:
        assert len(set(args.holes))==n-s and set(args.holes)<=set(range(n))
        solver.add([holes[q]==(q in args.holes) for q in range(n)])
    if tight and n-s==3 and args.early_pattern==0:
        # Necessary uniform exclusion proved in TRIANGLE_MIXING_CASE_A.md.
        for letter in B:
            case_a=z3.And(z3.Not(z3.Or([letter[q][0] for q in range(n)])),
                          z3.Or([z3.And(letter[0][u],letter[1][u]) for u in (1,2)]),
                          z3.Or(letter[2][3:]))
            solver.add(z3.Not(case_a))
    if t>1:
        assert short is not None
        for x,y in pairs:solver.add(z3.Or(holes[x],holes[y],z3.Not(short[x,y])))
    state_edges={(q,u):z3.Or([letter[q][u] for letter in B]) for q in range(n) for u in range(n)}
    for backward in (False,True):
        reachable=[z3.BoolVal(q==0) for q in range(n)]
        for depth in range(1,n):
            following=[z3.Bool(f"conn_{backward}_{depth}_{q}") for q in range(n)]
            for q in range(n):
                solver.add(following[q]==z3.Or([reachable[q]]+
                            [z3.And(reachable[p],state_edges[q,p] if backward else state_edges[p,q])
                             for p in range(n)]))
            reachable=following
        solver.add(reachable)
    build_seconds=time.monotonic()-start;witness=None;rejected=[];status="iteration_limit"
    for iteration in range(1,args.iterations+1):
        answer=solver.check()
        if answer==z3.unknown:status="unknown: "+solver.reason_unknown();break
        if answer==z3.unsat:status="unsat_boolean_pair_encoding_not_certified";break
        model=solver.model()
        candidate=[[next(u for u in range(n) if z3.is_true(model.eval(letter[q][u]))) for q in range(n)] for letter in B]
        S={q for q in range(n) if not z3.is_true(model.eval(holes[q]))}
        distances=pair_distances(candidate)
        assert strong(candidate) and len(distances)==P
        assert all(distances[p]>=t for p in combinations(sorted(S),2))
        z=certificate(candidate,S,args.protected)
        if z is None or z["value"]<t:
            _,images=bfs(candidate,range(n),lambda T:False)
            for image in images:
                if len(image)==s and all(distances[p]>=t for p in combinations(sorted(image),2)):
                    alternative=certificate(candidate,image,args.protected)
                    if alternative is not None and alternative["value"]>=t:z=alternative;break
        if z is not None and z["value"]>=t:
            assert verify(z);witness=z;status="witness_verified";break
        rejected.append(dict(rows=candidate,S=sorted(S),reason="No qualifying actual image"))
        solver.add(z3.Or([z3.Not(B[ell][q][candidate[ell][q]]) for ell in range(k) for q in range(n)]))
    result=dict(n=n,s=s,target=t,letters=k,protected=args.protected,early_pattern=args.early_pattern,
                fixed_holes=args.holes,
                common_kernel=[0,1],build_seconds=build_seconds,seconds=time.monotonic()-start,
                status=status,iterations=iteration,witness=witness,rejected_candidates=rejected,
                scope="Bounded-alphabet exact Boolean pair closures; negative output not certified.")
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({key:value for key,value in result.items() if key not in ("witness","rejected_candidates")}),flush=True)
    if witness:print(json.dumps(witness),flush=True)


if __name__=="__main__":main()
