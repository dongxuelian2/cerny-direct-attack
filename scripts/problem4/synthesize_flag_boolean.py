"""General bounded-alphabet F2-flag CEGIS, with ordinary BFS positives.

No common kernel, prescribed ranks or permutation letters. Only proved
pruning is used. Negative output is diagnostic, never an upper certificate.
"""
import argparse
from functools import reduce
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time
import z3
from alphabet_check import bfs,certificate,pair_distances,strong,verify


def main():
    ap=argparse.ArgumentParser()
    for key in ('n','s','r'):ap.add_argument(key,type=int)
    ap.add_argument('--letters',type=int,default=2)
    ap.add_argument('--span-cover-h',type=int)
    ap.add_argument('--cycle-five',action='store_true')
    ap.add_argument('--independent-flag',action='store_true')
    ap.add_argument('--cover-by-images',action='store_true')
    ap.add_argument('--no-flag',action='store_true')
    ap.add_argument('--synchronization-rank',action='store_true')
    ap.add_argument('--resume',type=Path)
    ap.add_argument('--resume-trap-limit',type=int)
    ap.add_argument('--minimal-traps',action='store_true')
    ap.add_argument('--protected-state',type=int)
    ap.add_argument('--protected-predecessor-size',type=int,choices=[0,1,2,3])
    ap.add_argument('--fixed-predecessor',type=str)
    ap.add_argument('--second-predecessor',action='store_true')
    ap.add_argument('--fixed-second-predecessor',type=str)
    ap.add_argument('--local-prefix-depth',type=int,choices=[0,1,2],default=0)
    ap.add_argument('--protected-isolation-depth',type=int,default=0)
    ap.add_argument('--fixed',type=Path)
    ap.add_argument('--timeout-ms',type=int,default=30000)
    ap.add_argument('--total-seconds',type=int,default=180)
    ap.add_argument('--iterations',type=int,default=1000)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();n,s,r,k=args.n,args.s,args.r,args.letters;t=n-r;m=n-s
    if args.span_cover_h is not None:assert args.span_cover_h>=1
    assert 1<=r<s<n and (args.no_flag or s%2==1) and 2<=k<=26 and t<=(m+2)*(m+1)//2
    if args.no_flag:
        assert r==1 and args.protected_state is not None
    pairs=list(combinations(range(n),2));P=len(pairs)
    solver=z3.Tactic('sat').solver()
    F=[[[z3.Bool(f'f_{ell}_{q}_{u}') for u in range(n)] for q in range(n)] for ell in range(k)]
    for letter in F:
        for row in letter:solver.add(z3.PbEq([(v,1) for v in row],1))
    if args.protected_state is not None:
        assert r==1 and s>=4 and 0<=args.protected_state<n
    assert 0<=args.protected_isolation_depth<=s-r-1
    if args.protected_isolation_depth:assert args.protected_state is not None
    if args.protected_predecessor_size is not None:
        assert args.protected_state is not None
        a=args.protected_state
        predecessor=[z3.Bool(f'protected_predecessor_{q}') for q in range(n)]
        solver.add(z3.Not(predecessor[a]))
        if args.protected_predecessor_size:
            solver.add(z3.PbEq([(v,1) for v in predecessor],args.protected_predecessor_size))
        else:
            # This <=3 slice is complete only when P1<=4 is proved below.
            assert 0<=(m+2)*(m+1)//2+1-t<=m and (m+2)*(m+1)//2+1-t<=4
            solver.add(z3.PbGe([(v,1) for v in predecessor],1),z3.PbLe([(v,1) for v in predecessor],3))
        fixed_type=[z3.Bool(f'protected_fixed_type_{ell}') for ell in range(k)]
        solver.add(z3.Or([z3.Not(v) for v in fixed_type]))
        for ell in range(k):
            for q in range(n):
                solver.add(F[ell][q][a]==z3.Or(z3.And(fixed_type[ell],z3.BoolVal(q==a)),
                                             z3.And(z3.Not(fixed_type[ell]),predecessor[q])))
        if args.fixed_predecessor is not None:
            chosen={int(q) for q in args.fixed_predecessor.split(',')}
            assert chosen and chosen<=set(range(n)) and a not in chosen
            solver.add([predecessor[q]==(q in chosen) for q in range(n)])
            # A moving letter with |B|>=2 is singular, and may be named first.
            if len(chosen)>=2:solver.add(z3.Not(fixed_type[0]))
    else:assert args.fixed_predecessor is None
    if args.second_predecessor:
        # PROOF.md#problem4-second-entrance-fiber: valid for singleton equality and s>=5.
        assert s>=5 and args.fixed_predecessor is not None
        a=args.protected_state;B={int(q) for q in args.fixed_predecessor.split(',')}
        second=[z3.Bool(f'second_predecessor_{q}') for q in range(n)]
        solver.add(z3.Not(second[a]))
        solver.add(z3.Or([second[q] for q in range(n) if q not in B and q!=a]))
        solver.add(z3.Or([z3.Not(second[q]) for q in B]))
        types=[[z3.Bool(f'second_type_{ell}_{j}') for j in range(3)] for ell in range(k)]
        solver.add(z3.Or([typ[2] for typ in types]))
        for ell,typ in enumerate(types):
            solver.add(z3.PbEq([(v,1) for v in typ],1))
            for q in range(n):
                pre_B=z3.Or([F[ell][q][u] for u in B])
                solver.add(pre_B==z3.Or(z3.And(typ[0],z3.BoolVal(q==a)),
                                      z3.And(typ[1],z3.BoolVal(q in B)),
                                      z3.And(typ[2],second[q])))
        if (n,s,r)==(13,9,1) and args.span_cover_h==5:
            solver.add(z3.PbLe([(v,1) for v in second],3 if len(B)==1 else 4))
            solver.add(z3.PbLe([(second[q],1) for q in range(n) if q not in B],5-len(B)))
            # C is a clique in P2, so the normalized P5 cover meets
            # every pair of C. At most one C-point lies outside it.
            solver.add(z3.PbLe([(second[q],1) for q in range(m-1,n)],1))
        if args.fixed_second_predecessor is not None:
            C={int(q) for q in args.fixed_second_predecessor.split(',')}
            assert C and C<=set(range(n)) and a not in C and not B<=C and not C<=B
            solver.add([second[q]==(q in C) for q in range(n)])
    else:assert args.fixed_second_predecessor is None
    immediate={}
    for pair in pairs:
        x,y=pair;v=z3.Bool(f'kernel_{x}_{y}');immediate[pair]=v
        solver.add(v==z3.Or([z3.And(letter[x][u],letter[y][u]) for letter in F for u in range(n)]))
    # A synchronizing alphabet has a singular letter; normalize one to first.
    solver.add(z3.Or([z3.And(F[0][x][u],F[0][y][u]) for x,y in pairs for u in range(n)]))
    T=(m+2)*(m+1)//2;cap=T+1-t
    if 0<=cap<=m:solver.add(z3.PbLe([(v,1) for v in immediate.values()],cap))
    if args.fixed:
        fixed=json.loads(args.fixed.read_text(encoding='utf-8'))
        assert len(fixed)==k and all(len(row)==n for row in fixed)
        solver.add([F[ell][q][u]==(fixed[ell][q]==u) for ell in range(k)
                    for q in range(n) for u in range(n)])
    if args.synchronization_rank:
        # A strictly decreasing unsigned rank certifies a route to a
        # collision. Actual pair distances minus one fit in these bits.
        width=P.bit_length()
        rank={pair:[z3.Bool(f'sync_rank_{pair[0]}_{pair[1]}_{j}') for j in range(width)] for pair in pairs}
        for pair in pairs:
            x,y=pair;choices=[immediate[pair]]
            for other in pairs:
                if other==pair:continue
                u,v=other
                less=z3.Bool(f'sync_less_{x}_{y}_{u}_{v}')
                solver.add(less==z3.Or([z3.And(z3.Not(rank[other][j]),rank[pair][j],
                                                *[rank[other][l]==rank[pair][l] for l in range(j+1,width)])
                                       for j in range(width)]))
                for letter in F:
                    choices += [z3.And(letter[x][u],letter[y][v],less),
                                z3.And(letter[x][v],letter[y][u],less)]
            solver.add(z3.Or(choices))
    if args.cover_by_images:
        assert args.span_cover_h is not None and not args.cycle_five
    edges={}
    if not args.cover_by_images:
        for x,y in pairs:
            for u,v in pairs:
                edge=z3.Bool(f'edge_{x}_{y}_{u}_{v}');edges[(x,y),(u,v)]=edge
                solver.add(edge==z3.Or([z3.And(letter[x][u],letter[y][v]) for letter in F]+
                                       [z3.And(letter[x][v],letter[y][u]) for letter in F]))
    short=dict(immediate)
    depth_needed=max(args.span_cover_h or 1,5 if args.cycle_five else 1)
    if args.span_cover_h:
        h=args.span_cover_h
        assert (m>=2 and n>=2*m and t>2*m-1+h) or (m>=4 and n>=2*m and t>=2*m-1+h)
        # The equality boundary for m>=4 uses the symbolic odd-cycle
        # refinement in PROOF.md#problem4-odd-cycle-span-refinement.
    for depth in range(1,1 if args.cover_by_images else depth_needed+1):
        if depth>1:
            current={pair:z3.Bool(f'merged_{depth}_{pair[0]}_{pair[1]}') for pair in pairs}
            for pair in pairs:
                solver.add(current[pair]==z3.Or([short[pair]]+
                          [z3.And(edges[pair,other],short[other]) for other in pairs]))
            short=current
        if args.span_cover_h==depth:
            solver.add([z3.Not(v) for (x,y),v in short.items() if x>=m-1])
    if args.cycle_five:
        assert m==4 and t>=12 and n>=8
        cycle=(0,3,1,4,2,5,6)
        C={tuple(sorted((cycle[i],cycle[(i+1)%7]))) for i in range(7)}
        solver.add([short[pair]==(pair in C) for pair in pairs])
    # Exact graph connectivity, with no pair-distance rank or array theory.
    for reverse in (False,True):
        prior=[z3.BoolVal(q==0) for q in range(n)]
        for depth in range(1,n):
            current=[z3.Bool(f'reach_{reverse}_{depth}_{q}') for q in range(n)]
            for q in range(n):
                solver.add(current[q]==z3.Or([prior[q]]+
                   [z3.And(prior[p],z3.Or([letter[q][p] if reverse else letter[p][q]
                                          for letter in F])) for p in range(n)]))
            prior=current
        solver.add(prior)
    holes=[z3.Bool(f'hole_{q}') for q in range(n)]
    solver.add(z3.PbEq([(v,1) for v in holes],m))
    S=[z3.Not(v) for v in holes]
    def image(source,ell,name):
        result=[z3.Bool(f'{name}_{q}') for q in range(n)]
        for q in range(n):
            solver.add(result[q]==z3.Or([z3.And(source[p],F[ell][p][q]) for p in range(n)]))
        return result
    def size_set(values):solver.add(z3.PbEq([(v,1) for v in values],s))
    def fiber_counts(values,depth):
        # Literal consequences of the first/second entrance proofs;
        # not asserted at later, possibly unsafe, depths.
        if args.protected_predecessor_size is not None and depth<=t-2:
            solver.add(z3.PbEq([(z3.And(values[q],predecessor[q]),1) for q in range(n)],1))
        if args.second_predecessor and depth<=t-3:
            solver.add(z3.PbEq([(z3.And(values[q],second[q]),1) for q in range(n)],1))
    if args.protected_predecessor_size is not None:
        solver.add(z3.PbEq([(z3.And(S[q],predecessor[q]),1) for q in range(n)],1))
    if args.second_predecessor:
        solver.add(z3.PbEq([(z3.And(S[q],second[q]),1) for q in range(n)],1))
    if args.local_prefix_depth:
        assert args.local_prefix_depth<t
        def equal(x,y):return z3.And([u==v for u,v in zip(x,y)])
        T=[z3.Bool(f'local_first_image_{q}') for q in range(n)];size_set(T)
        solver.add(z3.Not(equal(S,T)))
        first=[image(S,ell,f'local_S_image_{ell}') for ell in range(k)]
        for values in first:
            size_set(values);solver.add(z3.Or(equal(values,S),equal(values,T)))
            fiber_counts(values,1)
        solver.add(z3.Or([equal(values,T) for values in first]))
        if args.protected_state is not None:solver.add(T[args.protected_state])
        if args.local_prefix_depth==2:
            family=[S,T]+[image(T,ell,f'local_T_image_{ell}') for ell in range(k)]
            for values in family:
                size_set(values)
                fiber_counts(values,2)
                if args.protected_state is not None:solver.add(values[args.protected_state])
            def paired_sum_equal(x,y,z,w):
                return z3.And([(z3.And(a,b)==z3.And(c,d)) for a,b,c,d in zip(x,y,z,w)]+
                              [(z3.Xor(a,b)==z3.Xor(c,d)) for a,b,c,d in zip(x,y,z,w)])
            for four in combinations(family,4):
                x,y,z,w=four
                duplicates=[equal(a,b) for a,b in combinations(four,2)]
                solver.add(z3.Or(duplicates+[paired_sum_equal(x,y,z,w),paired_sum_equal(x,z,y,w),paired_sum_equal(x,w,y,z)]))
    if args.protected_isolation_depth:
        a=args.protected_state
        frontier=[([z3.BoolVal(q==a) for q in range(n)],
                   [z3.BoolVal(q!=a) for q in range(n)],'')]
        for depth in range(1,args.protected_isolation_depth+1):
            next_frontier=[]
            for protected,others,word in frontier:
                for ell in range(k):
                    next_word=word+'abcdefghijklmnopqrstuvwxyz'[ell]
                    left=image(protected,ell,'isolated_protected_'+next_word)
                    right=image(others,ell,'isolated_others_'+next_word)
                    solver.add([z3.Not(z3.And(x,y)) for x,y in zip(left,right)])
                    next_frontier.append((left,right,next_word))
            frontier=next_frontier
    if args.cover_by_images:
        # A cover contained in 0..m-2 is exactly absence of a short
        # collision in I={m-1,...,n-1}. Literal image cardinalities encode it.
        cover_size=n-m+1
        frontier=[([z3.BoolVal(q>=m-1) for q in range(n)],'')]
        for depth in range(1,args.span_cover_h+1):
            next_frontier=[]
            for source,word in frontier:
                for ell in range(k):
                    next_word=word+'abcdefghijklmnopqrstuvwxyz'[ell]
                    values=image(source,ell,'cover_word_'+next_word)
                    solver.add(z3.PbEq([(v,1) for v in values],cover_size))
                    next_frontier.append((values,next_word))
            frontier=next_frontier
    basis=[S]+([] if args.no_flag else [[z3.Bool(f'basis_{i}_{q}') for q in range(n)] for i in range(1,t)])
    for values in basis:size_set(values)
    if args.protected_state is not None:
        solver.add([values[args.protected_state] for values in basis])
    if args.independent_flag and not args.no_flag:
        for i in range(1,t):
            dual=[z3.Bool(f'dual_{i}_{q}') for q in range(n)]
            for j in range(i+1):
                dot=reduce(z3.Xor,[z3.And(dual[q],basis[j][q]) for q in range(n)],z3.BoolVal(False))
                solver.add(dot==(j==i))
    common=[z3.And([values[q] for values in basis]) for q in range(n)]
    solver.add(z3.PbGe([(v,1) for v in common],r))
    for i in range(0 if args.no_flag else t-1):
        images=[image(basis[i],ell,f'basis_image_{i}_{ell}') for ell in range(k)]
        solver.add(z3.Or([z3.And([basis[i+1][q]==values[q] for q in range(n)]) for values in images]))
        for ell,values in enumerate(images):
            size_set(values) # required for set images to equal trajectory rows
            coeff=[z3.Bool(f'coeff_{i}_{ell}_{j}') for j in range(i+2)]
            for q in range(n):
                solver.add(values[q]==reduce(z3.Xor,[z3.And(coeff[j],basis[j][q]) for j in range(i+2)],z3.BoolVal(False)))
    words={'':S};safe=set();traps=[];blocked=[];rejected=[]
    def require_safe(word):
        if not word or word in safe:return
        require_safe(word[:-1]);ell='abcdefghijklmnopqrstuvwxyz'.index(word[-1])
        words[word]=image(words[word[:-1]],ell,'word_'+word);size_set(words[word]);safe.add(word)
        if args.no_flag:solver.add(words[word][args.protected_state])
        fiber_counts(words[word],len(word))
    def escape(trap):
        trap=set(trap)
        outside=[other for other in pairs if other not in trap]
        if args.cover_by_images:
            leaving=[z3.And(letter[x][u],letter[y][v]) for x,y in trap for u,v in outside for letter in F]
            leaving += [z3.And(letter[x][v],letter[y][u]) for x,y in trap for u,v in outside for letter in F]
        else:
            leaving=[edges[pair,other] for pair in trap for other in outside]
        solver.add(z3.Or([immediate[pair] for pair in trap]+leaving))
        traps.append(sorted(trap))
    def block(rows):
        solver.add(z3.Or([z3.Not(F[ell][q][rows[ell][q]]) for ell in range(k) for q in range(n)]))
        blocked.append(rows)
    resume_metadata=None
    if args.resume:
        prior=json.loads(args.resume.read_text(encoding='utf-8'))
        for key,value in dict(n=n,s=s,r=r,alphabet_size=k,span_cover_h=args.span_cover_h,
                              cover_by_images=args.cover_by_images,no_flag=args.no_flag,
                              protected_state=args.protected_state,
                              protected_predecessor_size=args.protected_predecessor_size).items():
            assert prior[key]==value,(key,prior.get(key),value)
        # Only necessary short-word and pair-trap cuts are replayed here.
        # Row exclusions would require repeating their exhaustive image audit.
        assert not prior['blocked_rows']
        for word in prior['safe_constraints']:
            assert 0<len(word)<t and all(ch in 'abcdefghijklmnopqrstuvwxyz'[:k] for ch in word)
            require_safe(word)
        replay=prior['trap_cuts']
        if args.resume_trap_limit is not None:
            assert args.resume_trap_limit>=0
            replay=replay[:args.resume_trap_limit]
        for trap in replay:
            assert trap and all(tuple(pair) in pairs for pair in trap)
            escape([tuple(pair) for pair in trap])
        resume_metadata=dict(file=str(args.resume),sha256=hashlib.sha256(args.resume.read_bytes()).hexdigest(),
                             previous_source_sha256=prior['source_sha256'],
                             safe_words=len(safe),trap_cuts=len(traps),
                             previous_trap_cuts=len(prior['trap_cuts']))
    started=time.monotonic();status='iteration_limit';witness=None;iteration=0
    for iteration in range(1,args.iterations+1):
        remaining=args.total_seconds-(time.monotonic()-started)
        if remaining<=0:status='total_time_limit';break
        solver.set(timeout=min(args.timeout_ms,max(1,int(remaining*1000))))
        answer=solver.check()
        if answer==z3.unknown:status='unknown: '+solver.reason_unknown();break
        if answer==z3.unsat:status='uncertified_unsat_encoding';break
        model=solver.model()
        rows=[[next(u for u in range(n) if z3.is_true(model.eval(F[ell][q][u])))
               for q in range(n)] for ell in range(k)]
        initial={q for q in range(n) if not z3.is_true(model.eval(holes[q]))}
        assert strong(rows)
        distances=pair_distances(rows);trap=set(pairs)-set(distances)
        if args.synchronization_rank:assert not trap
        if trap:
            if args.minimal_traps:
                def orbit(pair):
                    queue=[pair];seen={pair}
                    for x,y in queue:
                        for row in rows:
                            other=tuple(sorted((row[x],row[y])))
                            assert other in trap
                            if other not in seen:seen.add(other);queue.append(other)
                    return seen
                small=min((orbit(pair) for pair in sorted(trap)),key=lambda T:(len(T),sorted(T)))
                assert small and small<=trap
                escape(small)
            else:escape(trap)
        else:
            bad,_=bfs(rows,initial,lambda U:len(U)<s or (args.no_flag and args.protected_state not in U))
            assert bad is not None
            if len(bad)<t:require_safe(bad)
            else:
                z=certificate(rows,initial,r)
                if z is not None:assert z['value']>=t
                if z is None:
                    _,actual=bfs(rows,range(n),lambda U:False)
                    for U in actual:
                        if len(U)!=s or min(distances[p] for p in combinations(sorted(U),2))<t:continue
                        alt=certificate(rows,U,r)
                        if alt is not None and alt['value']>=t:z=alt;break
                if z is not None:
                    assert verify(z);witness=z;status='witness_verified';break
                rejected.append(dict(rows=rows,S=sorted(initial),reason='chosen subset unreachable, no actual equality image'))
                block(rows)
        if iteration%10==0:
            print(json.dumps(dict(iteration=iteration,seconds=time.monotonic()-started,
                                  safe_words=len(safe),trap_cuts=len(traps),blocked=len(blocked))),flush=True)
    result=dict(n=n,s=s,r=r,target=t,alphabet_size=k,status=status,iterations=iteration,
                seconds=time.monotonic()-started,z3_version=z3.get_version_string(),
                span_cover_h=args.span_cover_h,cycle_five=args.cycle_five,
                independent_flag=args.independent_flag,
                cover_by_images=args.cover_by_images,
                protected_state=args.protected_state,
                protected_predecessor_size=args.protected_predecessor_size,
                fixed_predecessor=args.fixed_predecessor,
                second_predecessor=args.second_predecessor,
                fixed_second_predecessor=args.fixed_second_predecessor,
                local_prefix_depth=args.local_prefix_depth,
                protected_isolation_depth=args.protected_isolation_depth,
                no_flag=args.no_flag,
                synchronization_rank=args.synchronization_rank,
                resume=resume_metadata,
                minimal_traps=args.minimal_traps,
                safe_constraints=sorted(safe,key=lambda w:(len(w),w)),trap_cuts=traps,
                blocked_rows=blocked,rejected=rejected,witness=witness,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope=('Ordinary avoid-or-compress CEGIS without a span flag; exact one-hot rows and graph connectivity. ' if args.no_flag else 'Full F2 flags with exact one-hot rows, graph connectivity and short-pair closures; synchronization and compression CEGIS. ')+
                      'Negative output not a certified upper.')
    args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key not in
                     ('safe_constraints','trap_cuts','blocked_rows','rejected','witness')}),flush=True)
    if witness:print(json.dumps(witness),flush=True)


if __name__=='__main__':main()
