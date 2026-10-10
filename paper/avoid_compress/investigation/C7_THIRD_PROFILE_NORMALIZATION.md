# Complete row cover for the binary c7 third-entrance profile

9 October 2026. Independently audited necessary row cover; not a new F value.

At (n,s,r)=(13,9,1), normalize H={0,1,2}, protected a=3,
B={0,1,4}, C={0,2,5}. BINARY_THIRD_ENTRANCE_CROSSING.md proves
M^(-1)(C)=F^(-1)(C)=D={2,6}. Together with the first two entrance
identities this forces M(B)={3}, M3=beta in {1,4}, M2,M6 in {2,5},
F3=3, F2=0, F0,F5 in {1,4}, and F6 in {2,5}.

Write J={7,...,12}, X={6,...,12}, W={5} union J and V={1,4}.
The seven W inputs under M must go to X. No collision among them
is possible: the B triangle already consumes three of the at most
four P1 pairs, and a further pair must touch H; W is disjoint from H.
Thus M maps W bijectively onto X. Its only possible additional
collision is {2,6}. Every bijection W -> X is, up to permutation of
J fixing states 0,...,6, a path from 5 through k ordinary points to 6
and disjoint permutation cycles on the other 6-k ordinary points.
There are sum_{k=0}^6 p(6-k)=30 types, where p is the partition
function. With beta and the two new-point outputs this gives 240
moving rows, covering all 8*7!=40,320 labelled moving rows.

The remaining F inputs R=V union J (eight points) go to X (seven).
The collision-pair budget permits exactly one pair block in R:
either {1,4}, inside B, or {1,h} for h in J, since 1 is its only H
point. Other blocks are singletons, so their seven output blocks
map bijectively to X. If F0=F5 the outside-B pair {0,5} has already
used the budget, forcing the R block to be {1,4}. A three-point
R block would create at least two pairs outside B and is forbidden.
If F0 differs from F5, all seven pair choices are possible.

Strong connectivity requires the other point gamma in V minus
{beta} to be an F output of 0 or 5, since it is not an M output.
It also requires F6 to be the other new point if M2=M6. These are
only indegree necessities; no stronger graph property is assumed.
The resulting complete row count is

  30 * 2 * (2+2*2) * (1+2*7) * 7! = 27,216,000.

This is a complete necessary row cover, possibly a strict superset:
when M2=M6, its outside-B pair may already exhaust the shared budget,
but the generator conservatively retains the F choices justified by
the weaker triangle-plus-F budget. Such extra rows cannot invalidate
a negative result. No claim that every generated row meets all equality
conditions is made.

Every safe initial nine-set meets B,C,D once and contains 3. There
are exactly fifteen: U={0,3,6} union J; X_j={j,2,3} union J for
j in V; and Y_{j,h}={j,3,5,6} union (J minus {h}) for j in V,h in J.
These follow by splitting its unique C point into 0,2,5. No other
initial sets are dropped and no reachability assumption is needed
for a negative result.

The native scan uses only necessary filters before ordinary subset
BFS: the safe one-count conditions on B,C,D through depth two;
the first two exact real equality-flag constraints (at most two
first-level Boolean points, and coplanarity at depth two); every
pair touching a has merging distance at least eight; H covers P5;
ordinary strong connectivity and pairwise synchronization. All
fifteen initial sets are checked wherever they survive these filters.
A pairwise synchronizing finite deterministic automaton is synchronizing.
Reachability from Q is tested only for positive local equality candidates.

The same enumerator at 9<=n<13, with |J|=n-7, supplies small controls,
not exclusions of those parameters. The full equality structure or
the H cover need not be attained there. Its closed row count is

  12 * (sum_{k=0}^{n-7} p(n-7-k)) * (2(n-7)+3) * (n-6)!.

C7_THIRD_PROFILE_EXCLUSION.md gives a symbolic exclusion independent
of the first-level filters and finite counts. check_c7_third_profile.py
independently audits every labelled moving row's cycle type, all possible
initial sets, literal typed-function assignments at n=9, forward pair BFS
and the seven paper-proof cases, including both backward-closed graphs.
Complete ordinary and sanitized native pair scans agree at n=9 and n=13.
The disjoint c3 branch, all B1/B2 branches and unrestricted alphabets
are outside this cover.
