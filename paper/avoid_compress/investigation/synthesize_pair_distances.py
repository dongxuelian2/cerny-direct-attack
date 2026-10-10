"""Exact pair-distance SMT synthesis, without enumerating short words.

Finite positive Bellman distances certify synchronization and are constrained
below by the compression target. Accepted rows are independently audited.
An unknown or unverified UNSAT is never used as a counterexample theorem.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import z3
from core_pair_probe import pair_distances
from audit_small import bfs,strong

def main():
    ap=argparse.ArgumentParser();ap.add_argument('n',type=int);ap.add_argument('s',type=int);ap.add_argument('target',type=int)
    ap.add_argument('p',type=int);ap.add_argument('q',type=int);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--first',type=Path);ap.add_argument('--timeout-ms',type=int,default=60000);ap.add_argument('--iterations',type=int,default=100)
    ap.add_argument('--free-subset',action='store_true',help='Choose the s-subset using hole variables; useful when the first map is fixed.')
    args=ap.parse_args();n,s,target,p,q=args.n,args.s,args.target,args.p,args.q;assert 0<=p<q<n and 2<=s<=n
    bits=n.bit_length();maximum=n*(n-1)//2;hb=maximum.bit_length();solver=z3.SolverFor('QF_ABV');solver.set(timeout=args.timeout_ms)
    rows=[[z3.BitVec(f'{letter}_{x}',bits) for x in range(n)] for letter in 'ab']
    for row in rows:
        for x in row:solver.add(z3.ULT(x,n))
        for x,y in combinations(range(n),2):
            if (x,y)!=(p,q):solver.add(row[x]!=row[y])
    solver.add(rows[0][p]==rows[0][q])
    if args.first:
        first=json.loads(args.first.read_text());assert len(first)==n
        solver.add([value==first[x] for x,value in enumerate(rows[0])])
    H=z3.Array('pair_distance',z3.BitVecSort(2*bits),z3.BitVecSort(hb))
    def get(x,y):
        x=z3.BitVecVal(x,bits) if isinstance(x,int) else x
        y=z3.BitVecVal(y,bits) if isinstance(y,int) else y
        return z3.Select(H,z3.Concat(x,y))
    for x in range(n):
        solver.add(get(x,x)==0)
        for y in range(x+1,n):
            h=get(x,y);solver.add(h==get(y,x),z3.UGT(h,0),z3.ULE(h,maximum))
            values=[get(row[x],row[y]) for row in rows]
            smaller=z3.If(z3.ULT(values[0],values[1]),values[0],values[1])
            solver.add(h==smaller+1)
    holes=None
    if args.free_subset:
        holes=[z3.Bool(f'hole_{x}') for x in range(n)];solver.add(z3.PbEq([(v,1) for v in holes],n-s))
        for x,y in combinations(range(n),2):solver.add(z3.Or(holes[x],holes[y],z3.UGE(get(x,y),target)))
    else:
        for x,y in combinations(range(s),2):solver.add(z3.UGE(get(x,y),target))
    # Exact graph strong-connectivity certificates, with ranks bounded by n-1.
    for direction in ('forward','backward'):
        ranks=[z3.BitVec(f'{direction}_{x}',bits) for x in range(n)];solver.add(ranks[0]==0)
        for x in range(1,n):
            solver.add(z3.UGT(ranks[x],0),z3.ULT(ranks[x],n))
            solver.add(z3.Or([z3.And(z3.ULT(ranks[y],ranks[x]),z3.Or([row[y]==x if direction=='forward' else row[x]==y for row in rows])) for y in range(n)]))
    begin=time.monotonic();records=[];status='iteration_limit';witness=None
    for iteration in range(1,args.iterations+1):
        answer=solver.check()
        if answer==z3.unknown:status='unknown: '+solver.reason_unknown();break
        if answer==z3.unsat:status='unsat_unverified_encoding';break
        model=solver.model();candidate=[[model.eval(value).as_long() for value in row] for row in rows]
        S={x for x in range(n) if not z3.is_true(model.eval(holes[x]))} if holes else set(range(s))
        assert strong(candidate);dist=pair_distances(candidate)
        assert len(dist)==maximum and all(model.eval(get(x,y)).as_long()==d for (x,y),d in dist.items())
        assert min(dist[pair] for pair in combinations(sorted(S),2))>=target
        reaching,_=bfs(candidate,range(n),lambda T:T==S)
        compression,_=bfs(candidate,S,lambda T:len(T)<s)
        assert len(compression)==target
        if reaching is not None:
            reset,_=bfs(candidate,range(n),lambda T:len(T)==1)
            _,images=bfs(candidate,S,lambda T:False)
            scores={x:min(len(word) for T,word in images.items() if len(T)<s or x not in T) for x in S}
            protected=[x for x in S if scores[x]>=target]
            witness=dict(rows=candidate,S=sorted(S),reaching=reaching,reset=reset,attaining=compression,
                         compression=target,protected=protected,avoid_or_compress_scores=scores)
            status='compression_witness_verified';break
        records.append(candidate)
        solver.add(z3.Or([value!=candidate[i][x] for i,row in enumerate(rows) for x,value in enumerate(row)]))
    report=dict(n=n,s=s,target=target,kernel_pair=[p,q],first_file=str(args.first) if args.first else None,
                free_subset=args.free_subset,
                status=status,iterations=iteration,seconds=time.monotonic()-begin,blocked_unreachable_rows=records,witness=witness,
                scope='Exact finite pair Bellman equations; negative solver answers unverified.')
    args.out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)

if __name__=='__main__':main()
