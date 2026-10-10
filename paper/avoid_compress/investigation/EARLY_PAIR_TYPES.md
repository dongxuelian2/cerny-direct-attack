# Necessary early-pair types for tight compression

Put m=n-s>=3 and T=binom(m+2,2). If a synchronizing automaton has an
s-set of shortest compression length T, SHORT_PAIR_STRUCTURE.md gives
|P_h|<=h for h<=m. Conversely P_1 is nonempty and the closures P_h grow
strictly until all pairs are present. A plateau would be an inverse-closure
fixed point and persist forever, contrary to synchronization. Therefore
|P_h|=h for h<=m. In particular there are ordered distinct pairs E_1,E_2,E_3
with P_h={E_1,...,E_h} for h=1,2,3.

Every letter is a permutation or a rank-(n-1) transformation with the common
kernel E_1. Write E_1={0,1}. Up to simultaneous state relabeling the ordered
three pairs, for n>=6, have precisely these nine types:

| type | E_2 | E_3 |
| --- | --- | --- |
| 0 | {0,2} | {1,2} |
| 1 | {0,2} | {0,3} |
| 2 | {0,2} | {1,3} |
| 3 | {0,2} | {2,3} |
| 4 | {0,2} | {3,4} |
| 5 | {2,3} | {0,2} |
| 6 | {2,3} | {0,4} |
| 7 | {2,3} | {2,4} |
| 8 | {2,3} | {4,5} |

Proof of completeness: E_2 shares one endpoint with E_1 or is disjoint.
In the first case normalize it to {0,2}; the ordered pair stabilizer fixes
0,1,2, and E_3 can be the remaining old edge, an edge from each of those
three vertices to one new vertex, or an edge on two new vertices.
In the disjoint case normalize E_2 to {2,3}. Its stabilizer independently
swaps the endpoints of the first two pairs. Thus E_3 joins the pairs,
joins either pair to a new point, or uses two new points. These give the
five and four types above. No missing-state or alphabet-size assumption
is used in this classification.

## Type 1 is incompatible with strong connectivity

Suppose P_1={01}, P_2={01,02}, P_3={01,02,03}. For every letter f,
preimages of 01 are in P_2, and preimages of 02 are in P_3.

If f is a permutation, f^{-1}(01) is 01 or 02, and f^{-1}(02) is a
different edge of the three-edge star. Their intersection is {0}.
Since 01 and 02 also intersect at {0}, bijectivity gives f^{-1}(0)=0.
In particular no other state maps to 0 under f.

If f is singular, let d be its unique missing output and c the common
image of 0,1. If d is not in 01 and c is in 01, the preimages of 01 are
the two distinct pairs {0,z},{1,z}, for z outside {0,1}; both cannot lie
in P_2. If d and c are both outside 01, its unique preimage pair is
disjoint from {0,1}, again impossible in P_2. Hence d is 0 or 1.
If d=1, examine 02. When c is in 02, its two preimages {0,z},{1,z}
cannot both belong to P_3. When c is outside 02, its unique preimage
pair is disjoint from {0,1} and cannot belong to P_3. Thus d=0.
No state therefore maps to 0 under a singular letter.

Every letter either fixes 0 with no other incoming edge, or omits 0
entirely. State 0 is unreachable from every other state, contradicting
strong connectivity. The argument works for any alphabet size and any n
where this type is defined; it gives only a necessary exclusion.