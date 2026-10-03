# Inclusion-maximal seeds and antitone policy tails both fail

**REFUTED with paper-proved state minima over every finite alphabet.**
The best-policy square conjecture remains OPEN; these are failures of
stronger selection and potential rules. All sets below are actual images.
Seed selection statements assume n>=2; the n1 empty-reset base has no seed.

## Policy tails need not decrease under inclusion: minimum n4

Let a=[1,2,0,0] and b=[3,2,0,1]. For S={0} and T={0,3}, exact
G(S)=5 but G(T)=6, despite S being a proper subset of T. Every e/G/W and
forward distance, actual reach word and best policy word is independently
checked. Thus G cannot serve as an antitone potential on actual images.

At n<=3, any nontrivial proper inclusion of nonempty actual images has
singleton S and rank-(n-1) image T. Q is the only larger image than T,
so G(T)=delta(Q,T). A G(S) policy constructs an actual word from Q into S,
and therefore into T, giving G(T)<=G(S). Inclusions into Q are immediate
from G(Q)=0. This proves the arbitrary-alphabet minimum n4.

## Even allowing every fiber's inclusion-maximal seed loses optimality

For a letter x and state p, consider actual images U with |U|>=2 and
Ux={p}. Call U maximal for (x,p) if no strictly larger actual image V
containing U is merged by that SAME letter to that SAME state. Let M be
the UNION of these maximal images over all (x,p), and put

    F_max=1+min_(T in M) G(T).

A seed maximal for one of its merge labels is eligible. This definition
does not discard it merely because it has another nonmaximal label.
Every maximum-cardinality seed is maximal, so P<=F_max<=F_kappa.
Nevertheless F_max=P is false. A state-minimal example is n5:

    a=[0,3,1,4,2], b=[0,1,0,4,3], c=[1,3,3,1,1].

Here P=rt=3 but F_max=4. All maximal sources are {0,2}, {1,2},
and {0,3,4}; their masks are 5,6,25. Full actual image membership and
every merge label are independently checked. Explicit best global and
best restricted policy chains attain the claimed budgets.
A second n5 example has P=5 and F_max=7:

    a=[1,3,2,0,0], b=[1,2,4,3,0], c=[0,1,0,3,0].

Its maximal sources have masks 21 and 24. It is a larger finite gap,
not a stronger minimality result or an infinite approximation obstruction.

## Why n<=4 is excluded for every alphabet

Choose an optimal one-letter seed U using the universal first-drop normal
form: 1+G(U)=P. Among actual images containing U in that same merge fiber,
extend it to an inclusion-maximal T. If U=T there is nothing to prove.
If T=Q, its merging letter is constant and P=F_max=1. Otherwise |U|>=2
and U is strictly contained in proper T. At 2<=n<=4 this forces |T|=n-1.
Hence Q is its only larger image and G(T)=delta(Q,T)<=G(U), by the actual
word from Q into U constructed by a G(U) chain. Therefore
F_max<=1+G(T)<=P, proving equality. This establishes arbitrary-alphabet
state minimum n5 independently of the search. No binary minimum is claimed:
complete binary covers through n5 have no inclusion-maximal failure.

The n5 counterexample necessarily uses a smaller actual seed whose cheap
tail is lost when replacing it by a containing merged image. Shortest
phase selection on that larger image chooses a different future tail.
This is compatible with the inclusion monotonicity of the unrestricted
distance delta(Q,T); it concerns the shortest-phase policy G instead.

## Computational boundary

The frozen ternary n5 adaptive search uses seed 20261024 and 200000
mutations, with 185268 SC synchronizing scores, and finds gaps 1 and 2.
Sampling does not establish absence of other failures. The exact same
mutation stream, counters and both retained full arrays are replayed.
All saved arrays and maximal-source memberships have a separate ordinary
per-target reverse BFS check; explicit words additionally use the older
inverse-set checker. Complete binary inputs n2..5 are independently
enumerated, with no F_max>P. Three corrupted certificates are rejected.
Original exploratory counts are retained with their explicitly narrower
provenance; the frozen search has literal argv and stdout/stderr.

There is no new n-only upper bound, no Lean addition, and no priority claim.
F_max<=(n-1)^2 is still OPEN, as are P's square bound and Cerny.
