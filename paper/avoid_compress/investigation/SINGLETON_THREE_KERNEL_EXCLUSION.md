# The three-point first entrance cannot have singleton second entrance at (13,9,1)

9 October 2026. Complete conditional computer-assisted exclusion only.
This does not determine F(13,9,1) and is outside the article release.

## Statement and reduction

A binary strongly connected synchronizing thirteen-state automaton
cannot have ac(S,{a})=12, |S|=9, first entrance |B|=3 and singleton
second entrance C. The statement does not require S to be reachable;
it therefore excludes the branch under the manuscript's stronger
actual-image requirement as well. No unrestricted-alphabet exclusion
is asserted.

Here is the reduction to |P1|<=4. A Frankl--Pin sequence consists of
nine-sets S_i and pairs E_i contained in S_i such that E_i is not
contained in any earlier S_j. For any five distinct pairs E_1,...,E_5,
construct S_j by omitting one endpoint outside E_j from each later
E_i, then fill its complement to four points outside E_j. Each later
pair is distinct from E_j, so such an endpoint exists; at most four
omissions are required. This gives a length-five sequence. Thus if
|P1|>=5, the refinement of Kisielewicz, Kowalski and Szykula,
Experiments with Synchronizing Automata (CIAA 2016), Theorem 1, gives
compression of every nine-set within

  binomial(13-9+2,2) - 5 + 1 = 11.

This contradicts local value twelve. The cited refinement uses the
maximum admitted sequence length p(P1), not the number of pairs:
the endpoint construction is what permits p(P1)>=5 here. No higher
layer edge-count cap is used. The primary reference is
https://doi.org/10.1007/978-3-319-40946-7_15.

LOCALIZED_BINARY_ENTRANCE_KERNEL.md proves that the unique
moving letter M must have exactly the kernel blocks B, E and
singletons, where E is a two-point set disjoint from B. It also proves
the complete normalization of all rows and initial subsets into the
three first-level actions, and of the moving row into permutation
conjugacy types. There is no fixed cycle length or prescribed cycle
type on the nine-element M-invariant set.

## Complete computation

One of the mixed-cover cases already has a symbolic exclusion: for
H={0,1,2}, B={0,1,4}, the extra pair E outside B must contain 2,
since H covers P1. The two first-level images swap E and both contain
the singleton second entrance, so C is disjoint from E. Therefore
C={2}, the case b3_mixed_c2, is impossible without the computation.
The complete normalized scan below additionally excludes C outside H,
the remaining singleton-C orbit b3_mixed_c1.

probe_singleton_three_kernel.cpp exhausts that normalized row cover.
There are 10,080 labelled moving rows; conjugation fixing the marked
points gives 180 representatives. For each representative the three
first-level actions give exactly

  (5+2+5) * 4 * 7! = 241,920

F assignments, with their respective initial sets. The factors are
the remaining B-output choices forced by strong-connectivity indegree,
the four allowed E/ordinary-output choices, and the seven-output
bijection on the specified initial image. All 43,545,600 assignments
are examined; no sampling, SAT oracle, timeout or search cutoff is used.

Ordinary reverse pair BFS retains 392,531 assignments that synchronize
and have every pair touching a at distance at least eight, a proved
equality requirement. Direct graph reachability leaves 162,091 strongly
connected assignments. Ordinary subset BFS on each specified initial
set finds its avoid-or-compress value strictly below twelve; the
complete tested histogram is 110,327 at four, 44,264 at five and 7,500
at six. Since none has the required delay, no reachability cutoff is
used for this negative result. The existence of an actual reachable
initial set cannot restore equality in this branch.

## Independent checks and exact scope

check_singleton_three_kernel.py independently enumerates the 10,080
moving rows and classifies their orbits using marked cycle words,
rather than the native lexicographic-conjugation procedure. It checks
that the native list includes exactly one representative of every
orbit, and that all assignment totals match the closed count above.
For n=9 it independently enumerates all 3,456 normalized row assignments
using full typed-function assignments on unspecified inputs, literal
sets and forward pair BFS. All aggregate counts and its complete
subset-delay histogram agree. Complete n=9 and n=13 native scans under
AddressSanitizer and UndefinedBehaviorSanitizer also reproduce every
count. n=10,11,12 are additional completed enumerator controls.

The normalization proof is necessary structure under the full equality
hypothesis; the normalized family can contain rows that do not satisfy
every equality flag. Retaining those extra rows makes this exclusion
conservative. The finite histograms assert nothing about larger n or
other entrance fibers. In particular they are not a new uniform upper
bound of six.

Together with the earlier B=H exclusion, this rules out the two further
binary joint orbits b3_mixed_c1 and b3_mixed_c2. Thirty-eight of the
original 43 binary joint cases remain; all 43 unrestricted cases are
still admitted. The first-fiber count stays five binary / six
unrestricted. Both extremal intervals at (13,9,1) stay [11,12].
