"""Finite synthesis by a lower pair potential and an independent sync rank.

Only positive output is mathematical evidence. Unknown/UNSAT is diagnostic.
The encoding admits every genuine witness at its stated alphabet size:
use capped shortest pair distances as the lower potential, and uncapped
shortest pair distances as the decreasing synchronization rank. Reachability
and protected-state delays are checked by independent ordinary BFS.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import z3
from alphabet_check import bfs, certificate, pair_distances, strong, verify


def main():
    ap = argparse.ArgumentParser()
    for name in ("n", "s", "target"):
        ap.add_argument(name, type=int)
    ap.add_argument("--letters", type=int, default=3)
    ap.add_argument("--protected", type=int, default=0)
    ap.add_argument("--kernel", nargs=2, type=int)
    ap.add_argument("--first", type=Path)
    ap.add_argument("--fixed", type=Path)
    ap.add_argument("--free-subset", action="store_true")
    ap.add_argument("--early-pattern", type=int, choices=range(9))
    ap.add_argument("--span-cover-h", type=int,
                    help="Necessary short-pair cover cut; see PROOF.md#problem4-short-pair-span")
    ap.add_argument("--refinement-cuts", action="store_true")
    ap.add_argument("--local-span-prefix", type=int, choices=(1,2),
                    help="Necessary equality flags for target=n-r; see PROOF.md#problem4-local-equality-flag")
    ap.add_argument("--cycle-five", action="store_true",
                    help="Only the C7 P5 branch of PROOF.md#problem4-codimension-four-p5-dichotomy")
    ap.add_argument("--binary-field-flag", action="store_true",
                    help="Full equality flag over F2 for odd |S| and target=n-r")
    ap.add_argument("--timeout-ms", type=int, default=60000)
    ap.add_argument("--total-seconds", type=int, default=180)
    ap.add_argument("--iterations", type=int, default=100)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    n, s, t, k, r = args.n, args.s, args.target, args.letters, args.protected
    assert 2 <= s < n and 0 <= r < s and 2 <= k <= 26
    assert 1 <= t <= (n-s+2)*(n-s+1)//2
    maximum, pairs = n*(n-1)//2, list(combinations(range(n), 2))
    bits, lb, ub = n.bit_length(), (t+1).bit_length(), maximum.bit_length()
    solver = z3.SolverFor("QF_ABV")
    rows = [[z3.BitVec(f"letter_{i}_{q}", bits) for q in range(n)]
            for i in range(k)]
    for row in rows:
        solver.add([z3.ULT(v, n) for v in row])
    if args.kernel:
        p, q = sorted(args.kernel)
        assert 0 <= p < q < n
        for row in rows:
            solver.add([row[x] != row[y] for x, y in pairs if (x, y) != (p, q)])
        solver.add(rows[0][p] == rows[0][q])
    else:
        solver.add(z3.Not(z3.Distinct(rows[0])))
    if args.first:
        first = json.loads(args.first.read_text())
        assert len(first) == n
        solver.add([v == first[q] for q, v in enumerate(rows[0])])
    if args.fixed:
        fixed = json.loads(args.fixed.read_text())
        assert len(fixed) == k and all(len(row) == n for row in fixed)
        solver.add([v == fixed[i][q] for i, row in enumerate(rows)
                    for q, v in enumerate(row)])

    phi = z3.Array("lower_potential", z3.BitVecSort(2*bits), z3.BitVecSort(lb))
    psi = z3.Array("sync_rank", z3.BitVecSort(2*bits), z3.BitVecSort(ub))
    def get(table, x, y):
        x = z3.BitVecVal(x, bits) if isinstance(x, int) else x
        y = z3.BitVecVal(y, bits) if isinstance(y, int) else y
        return z3.Select(table, z3.Concat(x, y))
    for x in range(n):
        solver.add(get(phi, x, x) == 0, get(psi, x, x) == 0)
    for x, y in pairs:
        lower, upper = get(phi, x, y), get(psi, x, y)
        solver.add(lower == get(phi, y, x), upper == get(psi, y, x))
        solver.add(z3.UGT(lower, 0), z3.ULE(lower, t),
                   z3.UGT(upper, 0), z3.ULE(upper, maximum))
        solver.add([z3.ULE(lower, get(phi, row[x], row[y])+1) for row in rows])
        solver.add(z3.Or([z3.ULT(get(psi, row[x], row[y]), upper) for row in rows]))
        solver.add(z3.ULE(z3.ZeroExt(ub-lb, lower), upper) if ub >= lb else
                   z3.ULE(lower, z3.ZeroExt(lb-ub, upper)))

    m = n-s
    if args.cycle_five:
        assert n>=8 and m==4 and t>=12
        cycle=(0,3,1,4,2,5,6)
        cycle_pairs={tuple(sorted((cycle[i],cycle[(i+1)%7]))) for i in range(7)}
        for x,y in pairs:
            if (x,y) in cycle_pairs:
                solver.add(z3.ULE(get(phi,x,y),5),z3.ULE(get(psi,x,y),5))
            else:
                solver.add(z3.UGT(get(phi,x,y),5))
    if args.span_cover_h is not None:
        h = args.span_cover_h
        assert m >= 2 and n >= 2*m and h >= 1 and t > 2*m-1+h
        # A genuine witness has cover(P_h)<=m-1. Relabel that cover inside
        # 0..m-2 and choose capped exact distances as phi. This restriction
        # therefore admits every genuine witness, though a solver failure
        # still is not a certified mathematical upper bound.
        for x, y in pairs:
            if x >= m-1:
                solver.add(z3.UGT(get(phi, x, y), h))
    if args.refinement_cuts:
        T = (m+2)*(m+1)//2
        for h in range(1, m+1):
            cap = T+h-t
            # The universal endpoint construction gives sequences only
            # through m+1 distinct pairs. It justifies this cardinality
            # cut only when cap+1<=m+1; p(P_h) is not |P_h| in general.
            if 0 <= cap <= m:
                solver.add(z3.PbLe([(z3.ULE(get(phi, x, y), h), 1)
                                   for x, y in pairs], cap))

    tight = t == (n-s+2)*(n-s+1)//2
    if tight:
        # Actual short-pair closures grow strictly until all pairs merge.
        # There are therefore at least h pairs with distance <=h. Since phi
        # never exceeds actual distance, <=h together with the refinement cut
        # forces exactly h, even for a nonexact lower potential.
        for h in range(1, n-s+1):
            solver.add(z3.PbEq([(z3.ULE(get(phi, x, y), h), 1) for x, y in pairs], h))
    if args.early_pattern is not None:
        assert tight and n-s >= 3 and n >= 6 and args.kernel == [0, 1]
        sequences = [((0, 1), (0, 2), last) for last in
                     ((1, 2), (0, 3), (1, 3), (2, 3), (3, 4))]
        sequences += [((0, 1), (2, 3), last) for last in
                      ((0, 2), (0, 4), (2, 4), (4, 5))]
        sequence = sequences[args.early_pattern]
        for x, y in pairs:
            if (x, y) in sequence:
                solver.add(get(phi, x, y) == sequence.index((x, y))+1)
            else:
                solver.add(z3.UGT(get(phi, x, y), 3))
    holes = [z3.Bool(f"hole_{q}") for q in range(n)] if args.free_subset else None
    if holes:
        solver.add(z3.PbEq([(v, 1) for v in holes], n-s))
    for x, y in pairs:
        if holes:
            solver.add(z3.Or(holes[x], holes[y], get(phi, x, y) == t))
        elif y < s:
            solver.add(get(phi, x, y) == t)
    if args.local_span_prefix or args.binary_field_flag:
        def set_image(mask,row):
            return z3.Concat(*[z3.If(z3.Or([z3.And(z3.Extract(x,x,mask)==1,
                                                    row[x]==y) for x in range(n)]),
                                    z3.BitVecVal(1,1),z3.BitVecVal(0,1))
                               for y in reversed(range(n))])
        S_mask = (z3.Concat(*[z3.If(holes[q],z3.BitVecVal(0,1),z3.BitVecVal(1,1))
                              for q in reversed(range(n))]) if holes else
                  z3.BitVecVal((1<<s)-1,n))
        first_images=[set_image(S_mask,row) for row in rows]
    if args.local_span_prefix:
        assert 1 <= r < s and t == n-r and args.local_span_prefix < t
        for x,y in combinations(first_images,2):
            solver.add(z3.Or(x==S_mask,y==S_mask,x==y))
        if args.local_span_prefix==2:
            T_mask=S_mask
            for mask in first_images:
                T_mask=z3.If(mask!=S_mask,mask,T_mask)
            masks=[S_mask,T_mask]+[set_image(T_mask,row) for row in rows]
            for a,b,c,d in combinations(masks,4):
                duplicate=z3.Or([x==y for x,y in combinations((a,b,c,d),2)])
                parallelogram=z3.Or([z3.And((x&y)==(z&w),(x^y)==(z^w))
                                    for x,y,z,w in ((a,b,c,d),(a,c,b,d),(a,d,b,c))])
                solver.add(z3.Or(duplicate,parallelogram))
    if args.binary_field_flag:
        assert s%2==1 and 1<=r<s and t==n-r
        basis=[S_mask]+[z3.BitVec(f'flag_image_{i}',n) for i in range(1,t)]
        common=basis[0]
        for mask in basis:
            common=common&mask
            solver.add(z3.PbEq([(z3.Extract(q,q,mask)==1,1) for q in range(n)],s))
        solver.add(z3.PbGe([(z3.Extract(q,q,common)==1,1) for q in range(n)],r))
        for i in range(t-1):
            images=[set_image(basis[i],row) for row in rows]
            solver.add(z3.Or([basis[i+1]==mask for mask in images]))
            for ell,mask in enumerate(images):
                total=z3.BitVecVal(0,n)
                for j in range(i+2):
                    coefficient=z3.Bool(f'flag_coefficient_{i}_{ell}_{j}')
                    total=total^z3.If(coefficient,basis[j],z3.BitVecVal(0,n))
                solver.add(mask==total)
    for direction in ("forward", "backward"):
        ranks = [z3.BitVec(f"{direction}_{q}", bits) for q in range(n)]
        solver.add(ranks[0] == 0)
        for q in range(1, n):
            solver.add(z3.UGT(ranks[q], 0), z3.ULT(ranks[q], n))
            solver.add(z3.Or([z3.And(z3.ULT(ranks[p], ranks[q]),
                                    z3.Or([row[p] == q if direction == "forward"
                                           else row[q] == p for row in rows]))
                             for p in range(n)]))
    start = time.monotonic()
    status, witness, rejected, iteration = "iteration_limit", None, [], 0
    for iteration in range(1, args.iterations+1):
        remaining = args.total_seconds - (time.monotonic()-start)
        if remaining <= 0:
            status = "total_time_limit"
            break
        solver.set(timeout=min(args.timeout_ms, max(1, int(remaining*1000))))
        answer = solver.check()
        if answer == z3.unknown:
            status = "unknown: " + solver.reason_unknown()
            break
        if answer == z3.unsat:
            status = "unsat_encoding_not_certified"
            break
        model = solver.model()
        candidate = [[model.eval(v).as_long() for v in row] for row in rows]
        S = {q for q in range(n) if not z3.is_true(model.eval(holes[q]))} if holes else set(range(s))
        distances = pair_distances(candidate)
        assert strong(candidate) and len(distances) == maximum
        assert min(distances[pair] for pair in combinations(sorted(S), 2)) >= t
        if args.cycle_five:
            assert {pair for pair,d in distances.items() if d<=5}==cycle_pairs
        if args.local_span_prefix:
            from check_local_equality_flag import prefix_images
            from check_short_pair_span import exact_rank
            for depth in range(1,args.local_span_prefix+1):
                masks=prefix_images(candidate,S,depth)
                assert exact_rank([[(mask>>q)&1 for q in range(n)]
                                   for mask in masks],n)<=depth+1
        if args.binary_field_flag:
            masks=[model.eval(mask).as_long() for mask in basis]
            assert all(mask.bit_count()==s for mask in masks)
            common=(1<<n)-1
            for mask in masks:common &= mask
            assert common.bit_count()>=r
            from check_local_equality_flag import image
            from check_short_pair_span import exact_rank
            for i in range(t-1):
                assert masks[i+1] in [image(masks[i],row) for row in candidate]
                assert exact_rank([[(mask>>q)&1 for q in range(n)]
                                   for mask in masks[:i+2]],n)==i+2
            if certificate(candidate,S,r) is not None:
                assert certificate(candidate,S,r)['value']>=t
        if args.span_cover_h is not None:
            assert all(d > args.span_cover_h for (x,y), d in distances.items()
                       if x >= m-1)
        if args.refinement_cuts:
            assert all(sum(d <= h for d in distances.values()) <=
                       (m+2)*(m+1)//2+h-t for h in range(1, m+1)
                       if 0 <= (m+2)*(m+1)//2+h-t <= m)
        # Independently check all claimed inequalities, not only the solver model.
        for x, y in pairs:
            value = model.eval(get(phi, x, y)).as_long()
            assert 1 <= value <= min(t, distances[x, y])
            for row in candidate:
                image = model.eval(get(phi, row[x], row[y])).as_long()
                assert value <= image+1
            rank = model.eval(get(psi, x, y)).as_long()
            assert any(model.eval(get(psi, row[x], row[y])).as_long() < rank
                       for row in candidate)
        z = certificate(candidate, S, r)
        if z is None or z["value"] < t:
            # One poor model subset must not exclude another reachable subset
            # of the same automaton. Examine every actual image before blocking
            # the transition rows; this also makes fixed-row controls reliable.
            _, actual_images = bfs(candidate, range(n), lambda T: False)
            for image in actual_images:
                if len(image) != s or min(distances[pair] for pair in
                                         combinations(sorted(image), 2)) < t:
                    continue
                alternative = certificate(candidate, image, r)
                if alternative is not None and alternative["value"] >= t:
                    z = alternative
                    break
        if z is not None and z["value"] >= t:
            assert verify(z)
            witness, status = z, "witness_verified"
            break
        rejected.append(dict(rows=candidate, S=sorted(S),
                             reason="unreachable" if z is None else "protected_state_delay",
                             value=None if z is None else z["value"]))
        solver.add(z3.Or([v != candidate[i][q] for i, row in enumerate(rows)
                         for q, v in enumerate(row)]))
    result = dict(n=n, s=s, target=t, alphabet_size=k, protected=r,
                  kernel=args.kernel, free_subset=args.free_subset,
                  first_file=str(args.first) if args.first else None,
                  fixed_file=str(args.fixed) if args.fixed else None,
                  tight_refinement_cuts=tight, status=status, iterations=iteration,
                  early_pattern=args.early_pattern,
                  span_cover_h=args.span_cover_h,
                  refinement_cuts=args.refinement_cuts,
                  proved_refinement_caps={str(h):(m+2)*(m+1)//2+h-t
                      for h in range(1,m+1) if args.refinement_cuts and
                      0 <= (m+2)*(m+1)//2+h-t <= m},
                  local_span_prefix=args.local_span_prefix,
                  cycle_five=args.cycle_five,
                  binary_field_flag=args.binary_field_flag,
                  witness=witness, rejected_candidates=rejected,
                  seconds=time.monotonic()-start, z3_version=z3.get_version_string(),
                  scope="Lower-potential finite synthesis; negative output is not an upper bound.")
    args.out.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("rejected_candidates", "witness")}), flush=True)
    if witness:
        print(json.dumps(witness), flush=True)


if __name__ == "__main__":
    main()
