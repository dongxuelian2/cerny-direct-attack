"""Counterexample-guided synthesis of exact avoid-or-compress witnesses.

Z3 is used only to propose transition rows. Every accepted witness is checked
by independent ordinary-set graph search. A timeout is never an UNSAT claim.
Reachability is checked after synthesis, not bounded in the SMT encoding.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import time
import z3
from audit_small import bfs, strong

def bad_words(rows, s, r, target):
    start=frozenset(range(s));A=set(range(r));todo=deque([start]);words={start:''};bad=[]
    while todo:
        S=todo.popleft();word=words[S]
        if len(S)<s or not A<=S:
            bad.append(word)
            if len(bad)>=24:break
            continue
        if len(word)>=target-1:continue
        for letter,row in zip('ab',rows):
            T=frozenset(row[q] for q in S)
            if T not in words:words[T]=word+letter;todo.append(T)
    return bad

def nonmergeable_pairs(rows):
    n=len(rows[0]);pairs=[(p,q) for p in range(n) for q in range(p+1,n)]
    reverse={pair:[] for pair in pairs};merged=set()
    for pair in pairs:
        for row in rows:
            p,q=sorted((row[pair[0]],row[pair[1]]))
            if p==q:merged.add(pair)
            else:reverse[p,q].append(pair)
    todo=deque(merged)
    while todo:
        pair=todo.popleft()
        for source in reverse[pair]:
            if source not in merged:merged.add(source);todo.append(source)
    return sorted(set(pairs)-merged)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('n',type=int);ap.add_argument('s',type=int);ap.add_argument('r',type=int)
    ap.add_argument('--iterations',type=int,default=1000);ap.add_argument('--timeout-ms',type=int,default=30000)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--resume',action='store_true')
    ap.add_argument('--sync-cegis',action='store_true')
    args=ap.parse_args();n,s,r=args.n,args.s,args.r;assert 1<=r<s<=n
    target=min(n-r,(n-s+2)*(n-s+1)//2);bits=n.bit_length();pair_count=n*(n-1)//2;hbits=pair_count.bit_length()
    solver=z3.SolverFor('QF_ABV');solver.set(timeout=args.timeout_ms)
    state=z3.BitVecSort(bits);height=z3.BitVecSort(hbits)
    rows=[[z3.BitVec(f'{letter}_{q}',bits) for q in range(n)] for letter in 'ab']
    tables=[]
    for row in rows:
        for v in row:solver.add(z3.ULT(v,n))
        table=z3.K(state,z3.BitVecVal(0,bits))
        for q,v in enumerate(row):table=z3.Store(table,z3.BitVecVal(q,bits),v)
        tables.append(table)
    # Some letter is singular; alphabet exchange lets it be the first one.
    solver.add(z3.Not(z3.Distinct(rows[0])))
    # Exact strong-connectivity certificates: ranks to/from state zero.
    for direction in ('forward','backward'):
        rank=[z3.BitVec(f'{direction}_{q}',bits) for q in range(n)]
        solver.add(rank[0]==0)
        for q in range(1,n):
            solver.add(z3.UGT(rank[q],0),z3.ULT(rank[q],n))
            if direction=='forward':
                solver.add(z3.Or([z3.And(z3.ULT(rank[p],rank[q]),z3.Or(rows[0][p]==q,rows[1][p]==q)) for p in range(n)]))
            else:
                solver.add(z3.Or([z3.And(z3.ULT(rank[p],rank[q]),z3.Or(rows[0][q]==p,rows[1][q]==p)) for p in range(n)]))
    # Pair graph reaches a diagonal iff the automaton is synchronizing.
    if not args.sync_cegis:
        H=z3.Array('pair_height',z3.BitVecSort(2*bits),height)
        for p in range(n):
            for q in range(n):
                hpq=z3.Select(H,z3.BitVecVal((p<<bits)|q,2*bits))
                if p==q:solver.add(hpq==0)
                else:
                    solver.add(z3.UGT(hpq,0),z3.ULE(hpq,pair_count),hpq==z3.Select(H,z3.BitVecVal((q<<bits)|p,2*bits)))
                if p<q:
                    solver.add(z3.Or([z3.ULT(z3.Select(H,z3.Concat(row[p],row[q])),hpq) for row in rows]))
    traces={'':[z3.BitVecVal(q,bits) for q in range(s)]};safe=set();blocked=[];trap_cuts=[]
    def require_escape(trap):
        table=z3.K(z3.BitVecSort(2*bits),z3.BoolVal(False))
        for p,q in trap:
            table=z3.Store(table,z3.BitVecVal((p<<bits)|q,2*bits),True)
            table=z3.Store(table,z3.BitVecVal((q<<bits)|p,2*bits),True)
        solver.add(z3.Or([z3.Not(z3.Select(table,z3.Concat(row[p],row[q]))) for p,q in trap for row in rows]))
        trap_cuts.append(trap)
    def require_safe(word):
        if word in safe:return
        if word[:-1] not in traces:require_safe(word[:-1])
        if word not in traces:traces[word]=[z3.Select(tables['ab'.index(word[-1])],q) for q in traces[word[:-1]]]
        images=traces[word];solver.add(z3.Distinct(images))
        for q in range(r):solver.add(z3.Or([v==q for v in images]))
        safe.add(word)
    for word in ('a','b','aa','ab','ba','bb'):
        if len(word)<target:require_safe(word)
    if args.resume and args.out.exists():
        prior=json.loads(args.out.read_text());assert (prior['n'],prior['s'],prior['r'])==(n,s,r)
        for word in prior['safe_constraints']:require_safe(word)
        for candidate in prior.get('blocked_unreachable_rows',[]):
            solver.add(z3.Or([rows[i][q]!=candidate[i][q] for i in range(2) for q in range(n)]));blocked.append(candidate)
        for trap in prior.get('synchronization_trap_cuts',[]):require_escape(trap)
    begin=time.monotonic();iterations=0;status='iteration_limit';witness=None;stats={}
    def checkpoint():
        report=dict(n=n,s=s,r=r,target=target,z3_version=z3.get_version_string(),status=status,
                    iterations=iterations,seconds=time.monotonic()-begin,safe_constraints=sorted(safe,key=lambda w:(len(w),w)),
                    blocked_unreachable_rows=blocked,witness=witness,statistics=stats,
                    synchronization_trap_cuts=trap_cuts,synchronization_encoding='CEGIS invariant-pair-set cuts' if args.sync_cegis else 'strict pair heights',
                    scope='SMT proposals with independent graph checks; no all-parameter proof.')
        args.out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    for iterations in range(1,args.iterations+1):
        result=solver.check();stats={str(k):v for k,v in solver.statistics()}
        if result==z3.unknown:status='unknown: '+solver.reason_unknown();checkpoint();break
        if result==z3.unsat:status='unsat_encoding_unverified';checkpoint();break
        model=solver.model();candidate=[[model.eval(v).as_long() for v in row] for row in rows]
        assert strong(candidate)
        bad=bad_words(candidate,s,r,target)
        if bad:
            for word in bad:require_safe(word)
        else:
            trap=nonmergeable_pairs(candidate)
            if trap:
                assert args.sync_cegis
                require_escape(trap)
                reaching=None
            else:reaching,_=bfs(candidate,range(n),lambda S:S==frozenset(range(s)))
            if trap:pass
            elif reaching is None:
                solver.add(z3.Or([rows[i][q]!=candidate[i][q] for i in range(2) for q in range(n)]));blocked.append(candidate)
            else:
                reset,_=bfs(candidate,range(n),lambda S:len(S)==1);assert reset is not None
                attaining,_=bfs(candidate,range(s),lambda S:len(S)<s or not set(range(r))<=S)
                assert len(attaining)==target
                witness=dict(rows=candidate,S=list(range(s)),A=list(range(r)),value=target,
                             reaching=reaching,attaining=attaining,reset=reset)
                status='witness_verified';checkpoint();print(json.dumps(dict(status=status,n=n,s=s,r=r,target=target,witness=witness)),flush=True);break
        if iterations%10==0:
            checkpoint();print(json.dumps(dict(n=n,s=s,r=r,iteration=iterations,safe_constraints=len(safe),unreachable=len(blocked),seconds=time.monotonic()-begin)),flush=True)
    else:checkpoint()
    print(json.dumps(dict(status=status,iterations=iterations,seconds=time.monotonic()-begin,safe_constraints=len(safe))),flush=True)

if __name__=='__main__':main()
