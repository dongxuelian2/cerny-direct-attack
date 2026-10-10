"""Independent Boolean-layer synthesis over a fixed literal alphabet pool.

Short subset reachability, pair mergeability and state connectivity are
encoded as finite Boolean closures. No pair potential or rank is used.
Negative solver outputs are still diagnostics, pending a checked proof.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import z3
from alphabet_check import certificate, verify


def main():
    ap=argparse.ArgumentParser();ap.add_argument("pool",type=Path)
    ap.add_argument("--pattern",type=int,default=8)
    ap.add_argument("--subset",nargs="+",type=int,required=True)
    ap.add_argument("--timeout-ms",type=int,default=120000)
    ap.add_argument("--out",type=Path,required=True);args=ap.parse_args()
    data=json.loads(args.pool.read_text());n,s,t=data["n"],data["s"],data["target"]
    record=data["records"][args.pattern];rows=record["letters"]
    S=frozenset(args.subset);assert len(S)==s and S<=set(range(n))
    solver=z3.Tactic("sat").solver();solver.set(timeout=args.timeout_ms)
    selected=[z3.Bool(f"selected_{i}") for i in range(len(rows))]
    def activations(states,transform):
        result={}
        for state in states:
            targets={}
            for i,row in enumerate(rows):
                target=transform(state,row);targets.setdefault(target,[]).append(selected[i])
            result[state]={target:z3.Or(variables) for target,variables in targets.items()}
        return result
    subsets=list(map(frozenset,combinations(range(n),s)))
    transitions=activations(subsets,lambda state,row:frozenset(row[q] for q in state))
    reach={state:z3.BoolVal(state==S) for state in subsets}
    for depth in range(t-1):
        for state in subsets:
            solver.add([z3.Not(z3.And(reach[state],active)) for target,active in transitions[state].items()
                        if len(target)<s])
        if depth==t-2:break
        following={state:z3.Bool(f"subset_{depth+1}_{'_'.join(map(str,sorted(state)))}") for state in subsets}
        for target in subsets:
            solver.add(following[target]==z3.Or([reach[target]]+
                       [z3.And(reach[state],transitions[state][target])
                        for state in subsets if target in transitions[state]]))
        reach=following
    pairs=list(combinations(range(n),2));P=len(pairs)
    pair_edges=activations(pairs,lambda pair,row:None if row[pair[0]]==row[pair[1]] else
                           tuple(sorted((row[pair[0]],row[pair[1]]))))
    merge={p:z3.BoolVal(False) for p in pairs}
    for depth in range(1,P+1):
        following={p:z3.Bool(f"merge_{depth}_{p[0]}_{p[1]}") for p in pairs}
        for pair in pairs:
            solver.add(following[pair]==z3.Or([merge[pair]]+
                        [active if target is None else z3.And(active,merge[target])
                         for target,active in pair_edges[pair].items()]))
        merge=following
    solver.add(list(merge.values()))
    state_edges=activations(range(n),lambda q,row:row[q])
    for backward in (False,True):
        reachable=[z3.BoolVal(q==0) for q in range(n)]
        for depth in range(1,n):
            following=[z3.Bool(f"conn_{backward}_{depth}_{q}") for q in range(n)]
            for q in range(n):
                terms=[reachable[q]]
                for p in range(n):
                    source,target=(q,p) if backward else (p,q)
                    if target in state_edges[source]:terms.append(z3.And(reachable[p],state_edges[source][target]))
                solver.add(following[q]==z3.Or(terms))
            reachable=following
        solver.add(reachable)
    start=time.monotonic();answer=solver.check();witness=None
    if answer==z3.sat:
        model=solver.model();candidate=[row for row,sel in zip(rows,selected) if z3.is_true(model.eval(sel))]
        assert len(candidate)<=26,"Indexed-letter certificate required"
        witness=certificate(candidate,S,0)
        if witness is not None:assert witness["value"]>=t and verify(witness)
        status="witness_verified" if witness is not None else "sat_model_unreachable"
    elif answer==z3.unsat:status="unsat_boolean_layers_not_certified"
    else:status="unknown: "+solver.reason_unknown()
    result=dict(n=n,s=s,target=t,pattern=args.pattern,S=sorted(S),
                alphabet_pool_size=len(rows),alphabet_size_cutoff=None,status=status,
                witness=witness,seconds=time.monotonic()-start,
                scope="Finite complete pool with fixed subset; negative output is not certified.")
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="witness"}),flush=True)
    if witness:print(json.dumps(witness),flush=True)


if __name__=="__main__":main()
