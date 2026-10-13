"""Bounded all-alphabet synthesis over literal complete early-pair pools.

There is no fixed alphabet-size cutoff: every pool letter has a selection
variable. Individual transitions are constant, with lower pair potentials
and decreasing synchronization ranks. Negative output remains uncertified.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import z3
from alphabet_check import bfs, certificate, pair_distances, strong, verify


def solve(data, record, timeout):
    n,s,t=data["n"],data["s"],data["target"]
    pairs=list(combinations(range(n),2));P=len(pairs);rows=record["letters"]
    solver=z3.SolverFor("QF_BV")
    phi={p:z3.BitVec("phi_%d_%d"%p,(t+1).bit_length()) for p in pairs}
    psi={p:z3.BitVec("psi_%d_%d"%p,P.bit_length()) for p in pairs}
    selected=[z3.Bool(f"selected_{i}") for i in range(len(rows))]
    early={tuple(p):i+1 for i,p in enumerate(record["early_pairs"])}
    def value(table,x,y):
        return z3.BitVecVal(0,next(iter(table.values())).size()) if x==y else table[tuple(sorted((x,y)))]
    for p in pairs:
        solver.add(z3.ULE(phi[p],t),z3.UGT(psi[p],0),z3.ULE(psi[p],P))
        solver.add(phi[p]==early[p] if p in early else z3.UGT(phi[p],3))
        x,y=p
        solver.add(z3.Or([z3.And(chosen,z3.ULT(value(psi,row[x],row[y]),psi[p]))
                         for chosen,row in zip(selected,rows)]))
    for chosen,row in zip(selected,rows):
        solver.add(z3.Implies(chosen,z3.And([z3.ULE(phi[p],value(phi,row[p[0]],row[p[1]])+1)
                                          for p in pairs])))
    holes=[z3.Bool(f"hole_{q}") for q in range(n)]
    solver.add(z3.PbEq([(h,1) for h in holes],n-s))
    for x,y in pairs:solver.add(z3.Or(holes[x],holes[y],phi[x,y]==t))
    for direction in ("forward","backward"):
        ranks=[z3.BitVec(f"{direction}_{q}",n.bit_length()) for q in range(n)]
        solver.add(ranks[0]==0)
        for q in range(1,n):
            solver.add(z3.UGT(ranks[q],0),z3.ULT(ranks[q],n))
            solver.add(z3.Or([z3.And(chosen,z3.ULT(ranks[p],ranks[q]))
                             for chosen,row in zip(selected,rows) for p in range(n)
                             if (row[p]==q if direction=="forward" else row[q]==p)]))
    start=time.monotonic();solver.set(timeout=timeout);answer=solver.check();z=None
    if answer==z3.sat:
        model=solver.model();candidate=[row for row,v in zip(rows,selected) if z3.is_true(model.eval(v))]
        S={q for q in range(n) if not z3.is_true(model.eval(holes[q]))}
        assert strong(candidate)
        # A model may include redundant letters. Remove them while preserving
        # pair mergeability and connectivity, which cannot shorten compression.
        for i in range(len(candidate)-1,-1,-1):
            reduced=candidate[:i]+candidate[i+1:]
            if reduced and strong(reduced) and len(pair_distances(reduced))==P:
                candidate=reduced
        assert len(candidate)<=26, "General indexed-letter certificate needed"
        distances=pair_distances(candidate)
        assert len(distances)==P
        assert all(distances[p]>=t for p in combinations(sorted(S),2))
        z=certificate(candidate,S,0)
        if z is None:
            _,images=bfs(candidate,range(n),lambda T:False)
            for image in images:
                if len(image)==s and all(distances[p]>=t for p in combinations(sorted(image),2)):
                    z=certificate(candidate,image,0)
                    if z is not None:break
        if z is not None:
            assert z["value"]>=t and verify(z)
        status="witness_verified" if z is not None else "sat_model_unreachable"
    elif answer==z3.unsat:status="unsat_complete_pool_encoding_not_certified"
    else:status="unknown: "+solver.reason_unknown()
    return dict(pattern=record["pattern"],alphabet_pool_size=len(rows),
                alphabet_size_cutoff=None,status=status,witness=z,
                seconds=time.monotonic()-start)


def main():
    ap=argparse.ArgumentParser();ap.add_argument("pool",type=Path)
    ap.add_argument("--pattern",type=int)
    ap.add_argument("--timeout-ms",type=int,default=30000)
    ap.add_argument("--out",type=Path,required=True);args=ap.parse_args()
    data=json.loads(args.pool.read_text());records=[]
    for record in data["records"]:
        if args.pattern is not None and record["pattern"]!=args.pattern:continue
        result=solve(data,record,args.timeout_ms);records.append(result)
        args.out.write_text(json.dumps(dict(n=data["n"],s=data["s"],target=data["target"],
                                           records=records,scope="Finite complete letter-pool synthesis; negative output is not certified."),indent=2)+"\n")
        print(json.dumps({k:v for k,v in result.items() if k!="witness"}),flush=True)


if __name__=="__main__":main()
