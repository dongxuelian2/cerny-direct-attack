# Symbolically excluding the binary three-point overlap c7

9 October 2026. Conditional exclusion at (13,9,1); no new extremal value.

There is no binary strongly connected synchronizing automaton with
ac(S,{3})=12, |S|=9, normalized H={0,1,2} covering P5,
B={0,1,4}, C={0,2,5}. No initial reachability is needed.

The third-entrance proof forces D={2,6} as the common preimage of C.
The five-pair Frankl--Pin endpoint argument gives |P1|<=4. The complete
necessary row cover is proved in C7_THIRD_PROFILE_NORMALIZATION.md.
In its notation, M(B)={3}, M3=beta in {1,4}, M2,M6 in {2,5},
and M maps W={5,7,...,12} bijectively to X={6,7,...,12}.
Also F3=3, F2=0, F0,F5 in {1,4}, F6 in {2,5}.
On R={1,4,7,...,12}, F has precisely one pair block, either {1,4}
or {1,h} with h>=7; its other blocks are singletons and its blocks
map bijectively onto X. If F0=F5, that R block must be {1,4}.
Every F-preimage of an X point therefore contains a point outside H:
its only possible H input is 1, which is paired with an outside point.

We will contradict even the weaker assumption that H covers P4,
using backward pair preimages. If a pair merges within l steps,
every distinct pair whose images under one letter form that pair
merges within l+1 steps. All instances below involve distinct points.

First M2 and M6 must differ. If both equal 2, {2,6} merges in one
step, and its M-preimages include {6,w} where w in W is the unique
M-preimage of 6. This outside-H pair merges within two steps. If
both equal 5, strong-connectivity indegree forces F6=2, as M then
misses 2. The F-preimages of the one-step pair {2,6} include {6,r}
with r outside H in R, again merging within two steps.

Next {2,6} always merges within three steps. If F6=2, choose
v=F0 in {1,4}. The pair {0,v} is in the one-step B triangle;
its F-preimages include {2,0}. Taking another F-preimage gives
{6,2}. If F6=5, then {0,5} merges within two steps: directly when
F0=F5, or as an F-preimage of the one-step pair {1,4} otherwise.
Its F-preimage {2,6} merges within three steps.

If M6=2, its M-preimages include the outside-H pair {6,w} above,
now merging within four steps. Hence M2=2 and M6=5. If F6=2,
its F-preimages include {6,r} with r outside H, also merging within
four steps. Hence F6=5. In particular M^(-1)(2)={2} and
F^(-1)(2) is empty.

Suppose first the R block is {1,4}. Define G0 to consist of the
B triangle, {0,5}, and every pair containing 2. G0 contains all
one-step merged pairs. It is backward closed under both letters:
under M all pairs with endpoint 0 have empty preimage, the pair
{1,4} has empty pair preimage since only beta is an M output, and
preimages of pairs containing 2 still contain 2. Under F those last
pairs have empty preimage; preimages of {0,1} and {0,4} contain 2,
preimages of {1,4} are either empty or {0,5}, and the preimage of
{0,5} is {2,6}. These descriptions use the actual pair preimage,
not a Cartesian product permitting equal inputs. Thus every pair
merged by any word belongs to G0. For example {3,4} is not in G0,
so the automaton cannot synchronize.

It remains that the R block is {1,h}, h>=7, and F0 differs from F5.
If beta=1, the M-preimage of this one-step pair includes {3,w_h}
where w_h in W maps to h, an outside-H pair merging in two steps.
Therefore beta=4. If F5=1, its F-preimages include {5,r} with
r outside H in R, another outside-H pair merging in two steps.
Therefore F0=1, F5=4. Enlarge G0 to G1 by adding {1,h} and every
pair {0,r}, r in R. Again all one-step merged pairs belong to G1.
The new pair {1,h} has no M-preimage, because M misses 1; its
F-preimages are of the form {0,r}, r in R. A pair {0,r} has no
M-preimage, and all its F-preimages contain 2. Hence G1 is backward
closed. It still excludes {3,4}, contradicting synchronization.

Every case gives either a pair outside H merging by depth four or
a nonsynchronizing automaton. Since H covers P5, the c7 branch is
excluded. This proof uses no first-level flag computation, subset
enumeration, SAT result, timeout, or numerical histogram. Native and
independent literal controls check the necessary row cover and the
pair dichotomy, as auxiliary audits rather than a substitute for proof.

This excludes b3_mixed_c7 only. The disjoint c3 branch, B1/B2 branches
and unrestricted alphabets remain open. The first unresolved extrema
at (13,9,1) remain in [11,12]; this is not a complete answer to Problem 4.
