# Binary rigidity at the balanced-hyperplane counting limit

Date: 2026-10-02. **PROVED (paper), arbitrary n>=5**. This is a
necessary structural condition, not a general reset upper bound.
General Cerny and ALL/SOME shortest-history cost/rank remain **OPEN**.
No publication priority or **FORMALLY VERIFIED** claim.

Let alpha=(1,1,-1,-1,0,...,0), W=ker alpha and V=W intersect {0,1}^n.
There are6*2^(n-4) vertices and c=n-4 singleton directions. Suppose
W is the FULL inverse-history span of ANY globally shortest reset w,
and its length attains the refined bound

    L=6*2^(n-4)-(n-4)-1.                               (1)

Assume the alphabet has TWO original letters a,b, neither preserving W.
For a row transformation matrix M_f, put beta_f=alpha M_f. For an
inverse target vector x in W, M_f x belongs to W exactly when beta_f x=0.
Also beta_f Q=0, because deterministic row matrices fix the all-ones
column. Nonpreservation means beta_f restricted to W is nonzero.

Then, after possibly exchanging a,b, their restricted guards are

    beta_a|W = lambda*(x_0-x_2),
    beta_b|W = mu*(x_0-x_3), lambda*mu != 0.             (2)

In particular EVERY free-coordinate coefficient of BOTH beta rows
vanishes. This is stronger than merely counting one intersection space.
At n6/d5 it constrains the still-open L21 saturation case to two
opposite pair-match guards, unless at least one letter preserves W.
It neither constructs such an automaton nor excludes the constrained
case. Larger alphabets are not covered by the binary conclusion.

**Practical limitation, added after attacking this result:** the REAL-
space classification is arbitrary-n, but the DFA saturation hypothesis
(1) is already IMPOSSIBLE at EVERY n>=8 by the classical Pin--Frankl
upper bound T(n)=(n^3-n)/6-1, valid at n>=4; see
[Szykula2026, Section2.1](https://arxiv.org/pdf/2608.24245).
Writing A(n) for (1), A(8)=91>T(8)=83. For n>=8,
A(n+1)-2A(n)=n-4>0, whereas
2T(n)-T(n+1)=n(n+1)(n-4)/6-1>0. Induction proves A(n)>T(n).
Thus this saturation-specific necessary condition cannot deliver a
new large-n automaton bound by itself. No novelty is asserted for
combining the known cubic bound with the exponential space count.
The general near-saturation/common-word cost problem remains OPEN.

## Why saturation forces guard coverage of every vertex

Equation (1), together with distinct history sets, says that the
history visits EVERY vertex of V except zero and the c-1 unused free
singletons. Every nonterminal vertex has an actual next letter with
its guard zero; Q has both guards zero.

If both guards were nonzero at any vertex x in V, they would also
be nonzero at Q-x, since beta_a Q=beta_b Q=0. Neither vertex is zero
or Q. At least one is a nonsingleton, since n>=5, and therefore is
visited by the saturated history. This is impossible. Hence

    (beta_a x)*(beta_b x)=0 for EVERY x in V.            (3)

No assumption that either letter preserves W has been introduced.

## Exact covering classification

More generally, let F,G be ANY real linear functionals on W, both
nonzero, with F(Q)=G(Q)=0. If F(x)G(x)=0 for every Boolean x in W,
then (2) holds for F,G up to exchange and nonzero scaling. Conversely
the two functionals in (2) cover V.

Separate the first four coordinates from the k=n-4 free coordinates.
On a vertex with first four bits zero, the restrictions to free bits
are homogeneous linear forms A,B satisfying A(y)B(y)=0 for ALL
y in {0,1}^k. Evaluating one-hot bits gives A_i B_i=0. If both forms
were nonzero, choose A_i!=0 and B_j!=0. Necessarily i!=j, and the
single-coordinate equations give B_i=A_j=0. At e_i+e_j the product
would be A_i B_j!=0. Thus one free restriction vanishes.

Say A vanishes. The six Boolean first-four patterns span the
three-dimensional core hyperplane. Since F is nonzero and independent
of free bits, some core pattern z has F(z)!=0. For EVERY free y,
F(z)G(z+y)=0, so G vanishes on the entire free cube translated by z.
Subtract the value at y0 from the values at its one-hot successors:
EVERY free coefficient of G is zero. Both forms are now core forms,
and their values on the all-ones core are zero by F(Q)=G(Q)=0.

The four nonconstant, nonzero core patterns are the pair indicators
02,03,12,13. Complementation pairs02 with13 and03 with12, and negates
the values of either functional. Modulo the all-ones direction these
are TWO independent lines: 1111, indicator02 and indicator03 are
independent in the core hyperplane. A nonzero core functional that
vanishes on1111 can vanish on at most one of those two lines.
To cover all four pair patterns, one functional must vanish on the
02/13 line and the other on03/12. Their respective one-dimensional
annihilators are x0-x2 and x0-x3 on W. This proves (2).

For the converse, every balanced first-four Boolean pattern has
x0=x2 OR x0=x3. Indeed when x0=0, one of x2,x3 must be0, and when
x0=1, one must be1. Thus the two guard hyperplanes cover every V.
The result is an exact REAL-space classification, not merely a
bounded integer search.

## Control and continuation boundary

An independent finite checker reconstructs the core from its six
support patterns and classifies canonical exact integer functionals.
It exhausts all pairs in the recorded grids, tests their product at
every Boolean vertex, and separately checks the free one-/two-bit
argument. These are finite controls of the paper proof, not all real
functionals, all DFAs, or a formal verification.
The four grids n5..8 contain176088 ordered form pairs,15756432
Boolean-vertex product controls and176088 separate free-restriction
pair controls; exactly32 ordered pairs cover their grids. Six
corruptions are rejected.

The formerly EXPLORATORY n6 proper-history covering query has NOW
received a complete independent audit. Python verifies ALL46656
first maps are covered by130 disjoint conjugation orbits using93600
literal conjugations. An independently written native inverse-subset
solver replays ALL6065150 distinct-row covering pairs, including NON-SC
inputs, and finds EXACTLY the423 saved records with rt>20, maximum25.
Every retained input is independently conjugated to one of the37
already audited ALL-shortest-prefix cases, with43 nonzero integer
minors. No high-length non-SC input is omitted. Four native input
corruptions are rejected in addition to the earlier three case checks.

Consequently the FULL-history cost/rank inequality is now
**COMPUTATIONALLY VERIFIED for ALL synchronizing six-state DFAs with
at most TWO original letters and ANY globally shortest reset word**.
At L<=20, d<=4 is covered by the general paper capacity theorem,
and d>=5 has target at least20. At L>20, every shortest history has
d6 and L<=25. Duplicate rows give a one-letter synchronizing map,
whose unique fixed root has height at most5; the same low-dimension
paper bound and d>=5 target cover it. Covering counts overlap; they
are not labeled-alphabet counts. This finite stronger-history claim
is not a new ordinary six-state Cerny theorem or an all-n proof.

After checkpoint122, two new negative pressure scopes completed. A
fixed rooted-cycle/one-leaf row at n7 and n8 was paired with EVERY
different second row. The raw counts are823542/16777215 tested and
487769/10183112 synchronizing SC inputs;769 high-length records were
retained. The already-proved capacity bound excludes387, and382 receive
ALL-shortest searches, with no counter. These are designated fixed-row
scopes, not all DFAs; the complete scans/searches are EXPLORATORY.

Adding EVERY different third row to EACH of the37 retained n6 binary
bases tests1726198 designated extensions. High-length records number234;
two repeated labeled alphabets leave232 distinct ones, ALL receiving
shortest-history searches, no counter. Overlap among designated bases
is possible. This does not cover ternary alphabets lacking such a binary
subalphabet; the negative completeness remains EXPLORATORY. The old
37-case independent integer-minor audit stays separate and verified.

The literal explicit Figure3 reset program was also tested at p3..20:
its full inverse-history rank is n3p, already over GF(2), hence over R.
This is a raw exploratory word check, not an all-optimal statement or
an ordinary-threshold proof beyond the previous registered parameters.
That program therefore supplies no low-dimension counterexample.

What remains is a cost theorem for the constrained dual-guard actions,
the one-preserving-letter case, or a different general approach. A
guard is still only a necessary linear condition: it cannot be chosen
freely or used without its actual original letter cost. General Cerny
is still OPEN, with no asserted complete proof to audit.

After the next intermediate commit e0abd74, a NEW exploratory COMPLETE
binary n7 first-map covering query finished343 orbit representatives
and282474906 distinct-row covering pairs, including non-SC inputs.
It finds241140939 synchronizing covering instances, maximum ordinary
rt36. Only12700 high-length inputs remain after the previous proved
d<=4 cut:724 further capacity exclusions and11976 ALL-shortest-path
subspace searches,64325 DFS nodes/13194 dimension cuts, no counter.
The field is101, with every Boolean minor through width7 strictly
smaller by the exact squared Hadamard bound and101 independently
trial-divided. This algebraic fact does NOT independently audit the
whole native search or its input completeness. The negative result
is **EXPLORATORY**, not an upgraded ALL-binary-n7 verified theorem.
Counts overlap under the first-map conjugation cover. The complete
code and raw JSON are archived byte-identically under research_pressure_125.
