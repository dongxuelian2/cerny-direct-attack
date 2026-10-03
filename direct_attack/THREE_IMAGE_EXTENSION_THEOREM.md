# A sparse rank-three family with exact maximum image extension 2n-4

**PROVED on paper for every n>=4.** This gives an asymptotic coefficient
obstruction 2, even with additive O(1) or o(n) slack. It is not a counterexample
to a universal 2n bound, a new general reset upper bound, or Cerny. Priority
of the precise family and image-capacity conclusion remains OPEN.

Put L=n-2, C={2,...,n-1}, and use right actions:

    0a=0, 1a=1, ca=2+(c-1) mod L for c in C,
    0b=1, 1b=2, cb=1 for 2<=c<n-1, (n-1)b=0.

Thus a cycles C and fixes 0,1; b has rank 3. Write P={0,1,2} and
S={0,n-1}. The automaton is strongly connected: 0 ->1 ->2 via b, C is
an a-cycle, and n-1 ->0 via b. Its full-Q reset word is

    b b a^(L-1) b b,

of length L+3=n+1.

## The whole image family is explicit

The nonempty reachable images are exactly

    {Q}, all singletons, {0,1},
    {0,1,c}, {0,c}, {1,c} for each c in C.                 (R)

There are 4n-4 such images. Qb=P, and a rotations reach all triples.
Pb={1,2}, so rotations reach all {1,c}. The last such pair satisfies
{1,n-1}b={0,2}, whose rotations reach all {0,c}; then {0,n-1}b={0,1}.
For c!=n-1, {0,c}b={1}; paths from 1 reach every state, giving all
singletons. Conversely the displayed family is forward closed. On triples,
b gives P if c=n-1 and {1,2} otherwise. On pairs, b gives

    {1,c} -> {1,2} (c!=n-1),  {1,n-1} -> {0,2},
    {0,c} -> {1}   (c!=n-1),  {0,n-1} -> {0,1},
    {0,1} -> {1,2}.

This proves (R), reachability and synchronization without treating any
ordinary subset as an image for free.

## A reachable pair with exact image-extension cost

Every image larger than S is Q or one of the triples. Before its first
rank drop to <=2, it remains a triple (after Q's first b). That first drop
is necessarily b and its image is ALWAYS {1,2}. A triple with c!=n-1
attains this drop in one letter. Hence

    e(S)=1+min{|v|: {1,2}v subset S}.                     (1)

Starting from {1,2}, any rank-two arrival at {0,n-1} must first enter the
{0,c} family. This can happen only through {1,n-1}b={0,2}. Before this
entry at least L-1 a's are needed, and the entry b costs one. From {0,2},
another L-1 a's are necessary to reach {0,n-1}. Applying b earlier would
merge the pair, so no rank-two shortcut occurs. The exact pair arrival
cost is 2L-1, attained by a^(L-1)b a^(L-1).

Any singleton arrival has a first merge. The only pair merge is
{0,c}b={1} with c!=n-1. It takes at least L+1 letters to produce this
singleton from {1,2}: first enter {0,2} in L letters, then merge. From 1
the shortest state path into S has length L: b to 2 followed by L-1
a's to n-1. Every earlier b from C returns to 1, and reaching 0 requires
passing n-1 first. Thus singleton arrivals cost at least 2L+1, two more
than the pair arrival. Equation (1) proves

    e({0,n-1})=2L=2n-4.

The actual larger image P and word b a^(L-1)b a^(L-1) attain this cost.
Loss of intermediate cardinality and partial-target arrivals were both
included in the lower bound.

## This is the maximum over ALL proper images

For c=2+r, 0<=r<L, the following actual larger-image transports give
upper bounds (the source P is a triple):

* Q b a^r = {0,1,c}, cost 1+r<=L;
* P b a^r = {1,c}, cost 1+r<=L;
* P b a^(L-1)b a^r = {0,c}, cost L+1+r<=2L;
* P b a^(L-1)b b = {1} subset {0,1}, cost L+2<=2L.

Singletons use the reachable pair {0,2} as source: b reaches 1, bb a^r
reaches c, and bb a^(L-1)b reaches 0, with costs at most L+2<=2L.
Together with the exact lower bound this proves max_S e(S)=2n-4.
Consequently e(S)<=Cn+d for all such automata forces C>=2 for ANY fixed
d; the same follows with an o(n) additive term. This is stronger than a
single finite obstruction to a literal Cn envelope. It does not refute C=2.

## Reset and best-policy costs are only n+1

Q needs at least two letters to first drop to {1,2}: its first b has rank
3, and the first triple-to-pair drop always yields that pair. The earliest
pair-to-singleton merge then costs L+1 as above. Thus rt>=L+3, matching
the displayed reset word. In particular the long extension is local.

The singleton 1 has e=1 via {0,2} and b. The pair {0,2} has e=L+1:
the proof above requires L letters from {1,2} to first reach {0,2}, whereas
a singleton in that target costs at least L+2; prepend the first triple
drop. P is an allowed endpoint of this shortest extension. Finally P has
e=1 via Q and b. This exact policy chain costs 1+(L+1)+1=L+3. Since
rt<=P_best, it follows that P_best=rt=n+1 for every n>=4. No policy
square counterexample follows from max e=2n-4.

## Ordinary cardinality extension misses the image deficit

For n>=5, S has ordinary inverse-cardinality extension cost exactly n-1.
Read inversely: a^(L-1) brings S to {0,2}, b brings it to {1,n-1}, and
another b gives X={0} union (C\{n-1}), of cardinality L>2. An earlier
first b yields only {n-1}; it then needs L-1 a's, b to {1}, and b to X,
costing at least L+2 instead. Before that first b a alone preserves size.
Thus n-1=L+1 is minimal. The forward word is bb a^(L-1).

However rho(X)=2 by (R), because X omits 1 and contains no triple. Its
image deficiency is |X|-rho(X)=n-4, unbounded. So a short ordinary
extension is not an image extension here. At the excluded boundary n4,
L=2 gives no cardinality growth at X; ordinary extension cost is 4.

## Verification and attribution boundary

The sparse multi-source native algorithm and an independent ordinary-set
ALL-SOURCE forward algorithm agree on EVERY e/G/worst/forward entry for
all 60 saved cases n4..63. The full closed image family, exact words, rt
and maximum e are independently checked. Three corruptions are rejected.
The arbitrary-n conclusions rest on the complete proofs above, not those
finite computations. No new Lean theorem.

Ordinary extension is a different problem with known larger lower bounds;
the image-extension formulation itself is known from
[Kisielewicz--Szykula, Section 3.1](https://arxiv.org/pdf/1608.01268).
Search results for ordinary 2n-4 extension/avoiding bounds do not establish
priority for the present reachable-image capacity statement. Novelty remains
OPEN; no exhaustive literature-priority conclusion is asserted.
