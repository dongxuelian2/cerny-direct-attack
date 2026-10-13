"""Exact finite pair-distance synthesis for arbitrary bounded alphabet sizes.

Positive automata are audited with ordinary forward pair/subset BFS.
Unknown and UNSAT outputs are diagnostics, not mathematical upper bounds.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import z3
from alphabet_check import certificate, pair_distances, strong

def main():
    ap = argparse.ArgumentParser()
    for name in ("n", "s", "target"):
        ap.add_argument(name, type=int)
    ap.add_argument("--letters", type=int, default=3)
    ap.add_argument("--protected", type=int, default=0)
    ap.add_argument("--kernel", nargs=2, type=int)
    ap.add_argument("--first", type=Path)
    ap.add_argument("--fixed", type=Path)
    ap.add_argument("--distinct", action="store_true")
    ap.add_argument("--free-subset", action="store_true")
    ap.add_argument("--timeout-ms", type=int, default=60000)
    ap.add_argument("--total-seconds", type=int, default=180)
    ap.add_argument("--iterations", type=int, default=100)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    n, s, target, k, r = args.n, args.s, args.target, args.letters, args.protected
    assert 2 <= s <= n and 0 <= r < s and 2 <= k <= 26
    assert 1 <= target <= (n-s+2)*(n-s+1)//2
    bits, maximum = n.bit_length(), n*(n-1)//2
    hb = maximum.bit_length()
    solver = z3.SolverFor("QF_ABV")
    rows = [[z3.BitVec(f"letter_{i}_{q}", bits) for q in range(n)]
            for i in range(k)]
    for row in rows:
        solver.add([z3.ULT(value, n) for value in row])
    if args.distinct:
        for i, j in combinations(range(k), 2):
            solver.add(z3.Or([rows[i][q] != rows[j][q] for q in range(n)]))
    if args.kernel:
        p, q = sorted(args.kernel)
        assert 0 <= p < q < n
        for row in rows:
            for x, y in combinations(range(n), 2):
                if (x, y) != (p, q):
                    solver.add(row[x] != row[y])
        solver.add(rows[0][p] == rows[0][q])
    else:
        solver.add(z3.Not(z3.Distinct(rows[0])))
    if args.first:
        first = json.loads(args.first.read_text())
        assert len(first) == n
        solver.add([value == first[q] for q, value in enumerate(rows[0])])
    if args.fixed:
        fixed = json.loads(args.fixed.read_text())
        assert len(fixed) == k and all(len(row) == n for row in fixed)
        solver.add([value == fixed[i][q] for i, row in enumerate(rows)
                    for q, value in enumerate(row)])

    H = z3.Array("distance", z3.BitVecSort(2*bits), z3.BitVecSort(hb))
    def get(x, y):
        x = z3.BitVecVal(x, bits) if isinstance(x, int) else x
        y = z3.BitVecVal(y, bits) if isinstance(y, int) else y
        return z3.Select(H, z3.Concat(x, y))
    for x in range(n):
        solver.add(get(x, x) == 0)
        for y in range(x+1, n):
            d = get(x, y)
            solver.add(d == get(y, x), z3.UGT(d, 0), z3.ULE(d, maximum))
            minimum = get(rows[0][x], rows[0][y])
            for row in rows[1:]:
                candidate = get(row[x], row[y])
                minimum = z3.If(z3.ULT(candidate, minimum), candidate, minimum)
            solver.add(d == minimum+1)
    # Paper-backed pruning, valid for any alphabet: a tight Frankl--Pin
    # compression witness has at most h pairs merging within h letters,
    # for h<=n-s. See PROOF.md#problem4-short-pair-structure; not a new upper-bound claim.
    refinement_cuts = target == (n-s+2)*(n-s+1)//2
    if refinement_cuts:
        for h in range(1,n-s+1):
            solver.add(z3.PbLe([(z3.ULE(get(x,y),h),1)
                               for x,y in combinations(range(n),2)],h))
    holes = [z3.Bool(f"hole_{q}") for q in range(n)] if args.free_subset else None
    if holes:
        solver.add(z3.PbEq([(v, 1) for v in holes], n-s))
    for x, y in combinations(range(n), 2):
        lower = z3.UGE(get(x, y), target)
        if holes:
            solver.add(z3.Or(holes[x], holes[y], lower))
        elif y < s:
            solver.add(lower)
    for direction in ("forward", "backward"):
        rank = [z3.BitVec(f"{direction}_{q}", bits) for q in range(n)]
        solver.add(rank[0] == 0)
        for q in range(1, n):
            solver.add(z3.UGT(rank[q], 0), z3.ULT(rank[q], n))
            terms = []
            for p in range(n):
                edge = z3.Or([row[p] == q if direction == "forward" else row[q] == p
                              for row in rows])
                terms.append(z3.And(z3.ULT(rank[p], rank[q]), edge))
            solver.add(z3.Or(terms))
    start = time.monotonic()
    status, witness, rejected = "iteration_limit", None, []
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
        assert all(model.eval(get(x, y)).as_long() == value
                   for (x, y), value in distances.items())
        assert min(distances[pair] for pair in combinations(sorted(S), 2)) >= target
        z = certificate(candidate, S, r)
        if z is not None and z["value"] >= target:
            witness, status = z, "witness_verified"
            break
        rejected.append(dict(rows=candidate, S=sorted(S),
                             reason="unreachable" if z is None else "protected_state_delay",
                             value=None if z is None else z["value"]))
        solver.add(z3.Or([value != candidate[i][q]
                         for i, row in enumerate(rows) for q, value in enumerate(row)]))
    result = dict(n=n, s=s, target=target, alphabet_size=k, protected=r,
                  kernel=args.kernel, free_subset=args.free_subset,
                  first_file=str(args.first) if args.first else None,
                  fixed_file=str(args.fixed) if args.fixed else None,
                  distinct_letters=args.distinct,
                  tight_refinement_cuts=refinement_cuts,
                  status=status, iterations=iteration, witness=witness,
                  rejected_candidates=rejected, seconds=time.monotonic()-start,
                  z3_version=z3.get_version_string(),
                  scope="Finite alphabet synthesis. Negative solver output is not a certified upper bound.")
    args.out.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("rejected_candidates", "witness")}), flush=True)
    if witness:
        print(json.dumps(witness), flush=True)

if __name__ == "__main__":
    main()
