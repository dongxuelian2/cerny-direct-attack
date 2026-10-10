# Excluding third entrances with sole new point 2 in the B1/C3 mixed case

9 October 2026. Symbolic binary exclusion at (13,9,1), outside the release.

Assume binary strongly connected synchronizing equality ac(S,{3})=12,
|S|=9. Normalize H={0,1,2} covering P5, B={4}, C={0,1,5}. The established
five-pair endpoint argument gives |P1|<=4. We exclude the four third
profiles D={0,2},{2,5},{0,1,2},{0,2,5}. D={2} was excluded earlier.
No initial-set reachability assumption is used.

Put a=3,b=4,q=6, J={7,...,12}, O={q} union J, R={2} union O.
The label q will denote the outside partner of a necessary extra kernel
pair, not a new point of D. Write U=D intersect C and V=C minus D.
Here U is nonempty proper and D=U union {2}.

## Complete kernels and R-output blocks

BINARY_SINGLETON_FIRST_SECOND_COVER.md proves a common third fiber and
the complete binary row cover for this one-new-point geometry. The unique
C-merging letter L satisfies pre_L(B)=C, pre_L(C)={p}, p=a or b, and
pre_L(A)={the other protected point}; let delta=pL in C. The other letter
F permutes {a,b}, has pre_F(C)=D, and has a protected singleton as
preimage of B. Its remaining inputs map into R.

The same proposition proves that L is not injective outside C. Its C
triangle already contributes three immediate pairs. An outside-C pair
must meet H at 2. L2 belongs to R, whereas La,Lb belong to {a} union C;
so its other endpoint is ordinary, normalized to q=6. Consequently the
full immediate-pair set is exactly

  K = binomial(C,2) union {{2,q}}.

L has precisely the C block, the {2,q} block and all other points as singletons.
Its seven R-input blocks are {2,q} and the six J singletons, injected
into the eight R outputs. It misses exactly one R point mu. Every used
R output has an outside-H L predecessor. If both 2 and q were used,
pulling the pair {2,q} back under L would give an outside-H pair merging
in two steps. Thus mu is 2 or q. Likewise, if a short mergeable pair
joins delta to a used R output, pulling it under L gives an outside-H
pair: delta has the outside-H singleton predecessor p in {a,b}.

The R-inputs of F are V union O. Any F kernel pair must belong to K.
Since 2 is not among these inputs, only pairs inside V can occur.
For V of size two there are nine inputs into eight R outputs; the sole
permitted collision is the V pair, so its blocks map bijectively to R.
For singleton V there are eight inputs and no permitted collision,
again bijective to R. These assertions exhaust the abstract kernels;
no guessed cycle type or unproved higher-layer edge cap is used.

If U={0} or {0,1}, V contains 5. Every F R-input block then has an
outside-H point (5 or an ordinary point). The two R outputs 2,q both
have outside-H F predecessors, so an outside-H pair merges by F L.
This excludes D={0,2} and D={0,1,2}.

It remains to treat U={5} or {0,5}. Then V is {0,1} or {1}. Its F
kernel block consists entirely of H points and has some R output e;
all other R-output blocks have ordinary predecessors. Pulling {2,q}
under F forces e in {2,q}; otherwise an outside-H pair merges by F L.
The restriction F:O -> R minus {e} is bijective.

## The exceptional output e=2 is impossible

If mu=2, both letters preserve the proper nonempty ordinary set O:
LO=O and FO=O. This contradicts strong connectivity. Hence mu=q.
If delta belongs to U, {delta,2} is a pair in D and merges by F L;
pulling it under L gives an outside-H pair in at most three steps.
Therefore delta belongs to V.

Let x be the unique ordinary F predecessor of q. The pair {delta,x}
merges by F L, because Fdelta=2 and Fx=q. If x differs from q, its
L output-preimage block exists since L misses only q, so pulling this
pair under L gives an outside-H pair in three steps. If x=q, Fq=q
and L has no predecessor of q. Thus q has no incoming transition
except its self-loop, again contrary to strong connectivity. This
excludes e=2 for both remaining U shapes.

## Exceptional output q: a complete finite core cover

Now e=q and F(V)=q. Let x in O be the F predecessor of 2. If F5 belongs
to U, the outside-H pair {5,x} maps under F into D and merges by F L,
giving a three-step contradiction. Thus F5 belongs to V. If x differs
from q, choose an ordinary F predecessor y of x. The outside-H pair
{5,y} maps under F to {F5,x}, then under F to {q,2}, and L merges it.
Consequently x=q, so Fq=2 and F permutes J.

If delta is in U, pulling {delta,2} in P2 under L forces mu=2.
If delta is in V, pulling {delta,q} in P2 under L forces mu=q.
The predecessor requirements for all C points and the budget K now
leave the following exhaustive cases. Values at a,b merely select
which outside-H protected point is the singleton L predecessor of delta.

For U={5}, write gamma=F5 and eta=F2. The three points delta,gamma,eta
are distinct and exhaust C. Since gamma belongs to V={0,1}:

* If delta=5, both gamma and eta are in V. The outside pair {5,q}
  follows F three times to {2,q}, then L merges it. Word F^3 L has
  length four, a contradiction.
* If delta is in V, eta=5 and mu=q. Let
  G=binomial(C,2) union {{2,q},{2,5},{0,q},{1,q}}.
  It contains every immediate kernel pair and is backward closed under
  F. Under L the only possible G output vertices with predecessors are
  delta and 2; G contains no pair between them. Thus inverse images of
  distinct G pairs under L are empty. G is backward closed under both
  rows and omits {a,b}, so that pair can never merge. Synchronization
  is impossible. This covers both choices of gamma.

For U={0,5}, V={1}, necessarily F5=1. F2 differs from F0 and F5:
collisions involving input 2 would add a pair outside K. Thus F2 is
0 or 5, and F0 is either 1 or the other point of {0,5}.

* If F0=1, F0=F5 is the allowed {0,5} block. Put h=F2 in {0,5};
  delta is its other point and mu=2. The graph
  G=binomial(C,2) union {{2,q},{0,2},{2,5},{1,q}}
  contains all kernels and is backward closed under F. L has only
  delta,q as G output vertices with predecessors, and G has no edge
  between them. Hence G is also backward closed under L, omits {a,b},
  and contradicts synchronization. This covers two core assignments.
* If F0=0 and F2=5, delta may be any C point. For delta=1 or 5, only
  the self-loop 0F=0 enters state 0, contradicting strong connectivity.
  For delta=0, mu=2; choose the protected L predecessor p of 0 and an
  ordinary L predecessor y of q. The outside-H pair {p,y} follows
  L F^2 to {0,5}, then L merges it. Word L F^2 L has length four.
* If F0=5 and F2=0, F cycles 0,5,1,q,2. For every possible delta,
  the outside-H pair {5,q} follows F four times to {0,1}, and L
  merges it. Word F^4 L has length five, a contradiction.

The last three bullets cover respectively two, three and three core
assignments, all eight possibilities for U={0,5}. The two earlier
bullets cover all four possibilities for U={5}. The closure assertions
concern distinct output pairs; direct collisions are separately included
in G. Ordinary J inputs have no F output in these graphs, while under
L their possible outputs cannot form a graph edge with delta. The graph
argument therefore covers every unspecified ordinary permutation or
injection, not only a selected completion.

All four profiles are excluded symbolically, with merging words of
length at most five or a structural contradiction. The independent audit
checks every abstract R kernel, every finite core case, and complete
literal row families with zero and one unmarked ordinary point. Those
small-family controls do not replace the symbolic treatment of six J
points at n=13. No SAT answer or full transition-table scan is claimed.

The B1/C3 mixed joint still remains, but its third entrances are reduced
to {6},{0,6},{2,6},{0,1,6},{0,2,6},{0,1,2,6}. The intact small-first
inventory now has 169 residual binary typed third orbits and 930 letter
pairs. Joint cases remain 26 binary / 43 unrestricted; both extrema at
(13,9,1) remain [11,12]. No new F value or alphabet separation is claimed.

The displayed remaining D labels use the original third-inventory
normalization. Its state 6 is a marked D point and must not automatically
be identified with the kernel partner q of the excluded cases above.
