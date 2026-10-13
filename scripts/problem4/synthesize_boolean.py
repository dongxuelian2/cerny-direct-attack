"""Boolean CEGIS synthesis with a prescribed sole one-letter kernel pair.

This is a restricted search. Positive witnesses are independently checked.
UNSAT or timeout never certifies the unrestricted conjecture here.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import time
import z3
from audit_small import bfs,strong
from synthesize_safe import bad_words,nonmergeable_pairs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('n',type=int);ap.add_argument('s',type=int);ap.add_argument('r',type=int)
    ap.add_argument('p',type=int);ap.add_argument('q',type=int);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--timeout-ms',type=int,default=30000);ap.add_argument('--iterations',type=int,default=1000)
    ap.add_argument('--resume',action='store_true');ap.add_argument('--target',type=int)
    ap.add_argument('--fixed-rows',type=Path)
    ap.add_argument('--compression-only',action='store_true',help='Diagnostic pair-compression search; does not certify avoid-or-compress sharpness.')
    args=ap.parse_args();n,s,r,p,q=args.n,args.s,args.r,args.p,args.q;assert 1<=r<s<=n and 0<=p<q<n
    target=args.target or min(n-r,(n-s+2)*(n-s+1)//2)
    solver=z3.Tactic('sat').solver();solver.set(timeout=args.timeout_ms)
    F=[[[z3.Bool(f'{letter}_{source}_{t}') for t in range(n)] for source in range(n)] for letter in 'ab']
    for row in F:
        for values in row:solver.add(z3.PbEq([(v,1) for v in values],1))
        for t in range(n):
            for x in range(n):
                for y in range(x+1,n):
                    if (x,y)!=(p,q):solver.add(z3.Or(z3.Not(row[x][t]),z3.Not(row[y][t])))
    for t in range(n):solver.add(F[0][p][t]==F[0][q][t])
    if args.fixed_rows:
        fixed=json.loads(args.fixed_rows.read_text())
        for i in range(2):
            for source in range(n):solver.add(F[i][source][fixed[i][source]])
    # Exact strong connectivity by bounded graph closure, not bounded words.
    for direction in (0,1):
        previous=[z3.BoolVal(t==0) for t in range(n)]
        for depth in range(1,n):
            current=[z3.Bool(f'reach_{direction}_{depth}_{t}') for t in range(n)]
            for t in range(n):
                terms=[previous[t]]
                for source in range(n):
                    edge=z3.Or(F[0][source][t],F[1][source][t]) if direction==0 else z3.Or(F[0][t][source],F[1][t][source])
                    terms.append(z3.And(previous[source],edge))
                solver.add(current[t]==z3.Or(terms))
            previous=current
        solver.add(previous)
    X={'':[z3.BoolVal(t<s) for t in range(n)]};safe=set();traps=[];blocked=[]
    def require_safe(word):
        if not word:return
        if word in safe:return
        require_safe(word[:-1]);previous=X[word[:-1]];row=F['ab'.index(word[-1])]
        current=[z3.Bool(f'image_{word}_{t}') for t in range(n)]
        for t in range(n):solver.add(current[t]==z3.Or([z3.And(previous[source],row[source][t]) for source in range(n)]))
        solver.add(z3.PbEq([(v,1) for v in current],s))
        if not args.compression_only:solver.add(current[:r])
        X[word]=current;safe.add(word)
    def escape(trap):
        trap=[tuple(pair) for pair in trap];C=set(trap)
        allowed=[(x,y) for x in range(n) for y in range(n) if x==y or tuple(sorted((x,y))) not in C]
        solver.add(z3.Or([z3.And(row[source][x],row[other][y]) for source,other in trap for row in F for x,y in allowed]))
        traps.append(trap)
    def block(candidate):
        solver.add(z3.Or([z3.Not(F[i][source][candidate[i][source]]) for i in range(2) for source in range(n)]));blocked.append(candidate)
    for word in ('a','b','aa','ab','ba','bb'):
        if len(word)<target:require_safe(word)
    if args.resume and args.out.exists():
        prior=json.loads(args.out.read_text());assert (prior['n'],prior['s'],prior['r'],prior['kernel_pair'])==(n,s,r,[p,q])
        for word in prior['safe_constraints']:require_safe(word)
        for trap in prior['trap_cuts']:escape(trap)
        for candidate in prior['blocked_rows']:block(candidate)
    start=time.monotonic();status='iteration_limit';witness=None;iterations=0
    def checkpoint():
        out=dict(n=n,s=s,r=r,target=target,kernel_pair=[p,q],status=status,iterations=iterations,
                 seconds=time.monotonic()-start,z3_version=z3.get_version_string(),
                 compression_only=args.compression_only,
                 safe_constraints=sorted(safe,key=lambda w:(len(w),w)),trap_cuts=traps,blocked_rows=blocked,witness=witness,
                 scope='Prescribed unique immediate kernel; all accepted certificates independently verified.')
        args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    for iterations in range(1,args.iterations+1):
        result=solver.check()
        if result==z3.unknown:status='unknown: '+solver.reason_unknown();checkpoint();break
        if result==z3.unsat:status='unsat_restricted_encoding_unverified';checkpoint();break
        model=solver.model();candidate=[[next(t for t in range(n) if z3.is_true(model.eval(F[i][source][t]))) for source in range(n)] for i in range(2)]
        assert strong(candidate)
        bad=bad_words(candidate,s,0 if args.compression_only else r,target)
        if bad:
            for word in bad:require_safe(word)
        else:
            trap=nonmergeable_pairs(candidate)
            if trap:escape(trap)
            else:
                reaching,_=bfs(candidate,range(n),lambda T:T==frozenset(range(s)))
                if reaching is None:block(candidate)
                else:
                    reset,_=bfs(candidate,range(n),lambda T:len(T)==1);assert reset is not None
                    attaining,_=bfs(candidate,range(s),lambda T:len(T)<s or (not args.compression_only and not set(range(r))<=T))
                    assert len(attaining)==target
                    witness=dict(rows=candidate,S=list(range(s)),A=list(range(r)),value=target,
                                 reaching=reaching,attaining=attaining,reset=reset)
                    status='compression_witness_only' if args.compression_only else 'witness_verified'
                    checkpoint();print(json.dumps(dict(status=status,witness=witness)),flush=True);break
        if iterations%10==0:
            checkpoint();print(json.dumps(dict(n=n,s=s,r=r,kernel=[p,q],iteration=iterations,constraints=len(safe),trap_cuts=len(traps),seconds=time.monotonic()-start)),flush=True)
    else:checkpoint()
    print(json.dumps(dict(status=status,iterations=iterations,seconds=time.monotonic()-start)),flush=True)

if __name__=='__main__':main()
