# No fixed additive allowance rescues the three-a extension pool

Date:2026-10-03. **PROVED (paper), infinite two-parameter family.**
Finite controls are **COMPUTATIONALLY VERIFIED**, not FORMALLY VERIFIED.
Every universal three-a root-extension pool of cost n+C, for ANY fixed
constant C, is **REFUTED**. Ordinary RP, SEED, order-two square and general
Cerny remain **OPEN**. No novelty or general reset lower-bound claim.

## Construction

Generalize ORDER_TWO_THREE_A_BARRIER.md from period3 to any p>=3.
Let m>=2, L=2pm, M=4pm, delta=pm, h=2m. Original b cycles the core
and fixes r; a(r)=0, a(0)=a(L)=r. Let G0 be the nonzero multiples
of p among1,...,L-1 and fix both members of these input pairs.

Partition the other input pair indices into p-1 groups G1,...,G_(p-1),
each of size h and invariant under delta modulo L. Require G1 to contain
{delta-2,delta-1,L-2,L-1}. Such a partition exists: those are two
delta-orbits, and each group is filled with m orbits. The required
indices are nonzero mod p, even when p=3. Define

    a(L-2)=1, a(M-2)=1+delta,
    a(L-1)=1+L, a(M-1)=1+delta+L.

Map the other G1 pairs bijectively to output pairs with base1 mod p,
excluding bases1,1+delta. Map each other G_color bijectively to all
output pairs with that color mod p. Either orientation is permitted.
These rows form a bijection on C\{0,L}; exactly TWO opposite pairs
are split. The proved order-two classification gives synchronization.

Take S={r} union {q in C:q mod p !=p-1}. It has |S|=M-4m+1,
least core period p, and is proper and root-present.

## Exact restricted minimum

The leading b-prefix deletion, between-a reductions modulo M and final
power reduction modulo p are exhaustive for all words with at mostTHREE a.
The full defects and root-retention formulas from the period-three proof
apply literally: paired output colors agree modulo p.

Zero, ONE or TWO a letters cannot give rooted positive growth.
For THREE a, a b^j a b^k a b^s, growth is
1-F_s(a(L+j)b^k), while root retention is F_s(a(j)b^k), where

    F_s(x)=chi_S(a(x)b^s),      F_s(r)=chi_S(s).

For every 0<=s<p-1 the zero set modulo L is a nonzero-color group
G_(p-1-s), invariant under delta. All such shifts fail. For s=p-1,
the zero set is G0 while F_(p-1)(0)=1. Thus its ONLY oriented
delta-boundary is0: F(0)=1, F(delta)=0.

Only the four exceptional input indices have different output bases
modulo L. For j=L-2,L-1 their root-side base is1; hence k=L-1 mod L.
The minimum cost is attained at j=L-2,k=L-1,s=p-1 and equals

    3+(L-2)+(L-1)+(p-1) = M+p-1 = n+p-2.

For the upper j=M-2,M-1, k=delta-1 mod L, with cheapest cost
M+delta+p-1, strictly larger. As before there are eight successful
standard triples in the complete ranges. The displayed minimum is
attained and grows by ONE, so the minimum singular count is THREE.

For any constant C choose p>C+2. Then n+p-2>n+C. Already m=2
gives n=8p+1 and restricted minimum9p-1, whose ratio to n tends to9/8.
The additive gap p-2 is linear in this subfamily. This is an objective
failure for a restricted witness pool, not a Cerny threshold lower bound.

## Independent controls and ordinary cost

The separate generator/checker are `periodic_three_a_gap.py` and
`check_periodic_three_a_gap.py`. There are19 structural controls through
n4097 and ten complete canonical controls, covering151056 THREE-a words.
The checker imports no generator. It checks colors, delta invariance,
the actual full words and all zero/one/two/three-a standard forms in
the complete scope, and eight literal small reset witnesses. Seven
corruptions are rejected. Single-letter particle checks total19467444;
the forward particle total includes the separate upper witnesses.

At p4,m2,n33 the unrestricted ordinary minimum is13, versus restricted35.
At p5,m2,n41 it is16, versus restricted44. The ordinary lower certificates
have36308 vertices in total and38680 checked edges; closure induction
covers ALL words below the corresponding minimum, including any a-count.
Literal witnesses attain the minima. These are finite computational
proofs only; the existing Lean n25 minimum10 remains separate.

At p8,n65 and p16,n129, an ordinary BFS reaches its200000-state cap.
That event is explicitly INCOMPLETE, not an absence or lower-bound result.
A separate pruned beam search supplies literal ordinary upper witnesses
of lengths21 and39, respectively, both<=n and both with more thanTHREE a.
The checker independently checks those words but makes NO minimum claim.
No ordinary cost bound is asserted for all p,m or for the largest controls.

The scoped audit preserves the release snapshots, old formal sources and
historical registry. It does not claim a full historical or release rerun.
This refutes a broader short-word shortcut and leaves the actual general
mathematical targets open.
