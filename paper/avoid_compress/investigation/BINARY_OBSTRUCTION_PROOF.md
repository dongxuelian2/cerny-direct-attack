# The binary sharpness requirement at (11,8,1)

This note distinguishes the manuscript's unrestricted-alphabet F from its binary restriction F_bin. The result below concerns F_bin only. It cannot alone refute the unrestricted F formula or solve Open Problem 4 completely.

Two independently implemented completed decision covers give F_bin(11,8,1)=9, whereas the proposed minimum is 10. The lower bound has the following elementary proof.

## An explicit lower bound 9

Let T={x_0,x_1,x_2,x_3,x_4,z} and K={v,y,c,t}, and add d. Letter b cycles T in the displayed order, cycles v,y,c,t, and fixes d. Letter a interchanges z,y and c,d, sends t to z, and fixes the other states. Its only non-singleton fiber is {y,t}, mapping to z. Put S=T union {v,t}, A={x_3}.

The b-cycles together with the two a-interchanges prove strong connectivity. Direct application of the letters gives Q(abbbabaabb)=S. For completeness, the successive holes along this reaching word are

```
{t}, {v}, {y}, {c}, {t,d}, {v,d}, {v,t,c}, {v,t,d}, {v,y,d}, {y,c,d}.
```

The last hole set is the complement of S.

Here is the complete short-image table. A row records the three holes of an eight-state image. The two successors are valid eight-state images for every row with level less than eight. No successor is needed from a level-eight row.

| Row | Holes | Level | a | b |
| --- | --- | ---: | --- | --- |
| 0 | y,c,d | 0 | 1 | 1 |
| 1 | t,c,d | 1 | 1 | 2 |
| 2 | v,t,d | 2 | 3 | 4 |
| 3 | v,t,c | 3 | 2 | 5 |
| 4 | v,y,d | 3 | 3 | 0 |
| 5 | v,y,t | 4 | 6 | 7 |
| 6 | z,v,t | 5 | 5 | 8 |
| 7 | v,y,c | 5 | 2 | 9 |
| 8 | x_0,v,y | 6 | 10 | 11 |
| 9 | y,t,c | 6 | 12 | 3 |
| 10 | x_0,v,t | 7 | 10 | 13 |
| 11 | x_1,y,c | 7 | 14 | 15 |
| 12 | z,t,d | 7 | 9 | 16 |
| 13 | x_1,v,y | 8 | - | - |
| 14 | x_1,t,d | 8 | - | - |
| 15 | x_2,t,c | 8 | - | - |
| 16 | x_0,v,d | 8 | - | - |

Every listed successor has level at most one more than its source. Induction therefore shows that every word of length at most eight stays in this table; a level-eight row cannot occur earlier. None of the hole sets contains x_3. Thus every word shorter than nine is safe. The word ababbbab reaches row 16, whose image contains both y and t, so ababbbaba compresses at length nine. Equivalently abababbbb omits x_3 at length nine.

To prove synchronization, note that e=a^2 is the global unit t -> y, and b^12 is the identity. Its conjugates b^(12-i)e b^i, for i=0,1,2,3, merge every opposite pair of K. Any pair {d,q} with q in K can be rotated to {d,v}; applying a gives {c,v}, an opposite pair. Thus all d--K pairs merge. The pair {c,z} maps under a to {d,y} and merges. The pair {d,z} maps under b^4 a b^8 to {c,z}, since z b^4=x_3, a fixes x_3, and c b^8=c. Consequently every d--T pair merges after rotating its T-point to z.

Adjacent pairs in K can be rotated to {c,t}; a sends this to {d,z}. For a T--K pair, rotate the K-point to c; if the T-point is z use the preceding {c,z} case, and otherwise apply a to obtain a d--T pair. Finally a T--T pair can be rotated until one point is z, then a sends it to a T--K pair. Every pair merges. Successively merging two points of an image gives a reset of Q, proving synchronization. All conjugates and rotations are words in the original binary alphabet.

The JSON witness supplies the two transition rows, actual reaching word, attaining word and literal reset word. `check_binary_obstruction.py` recomputes exact ac by ordinary subset BFS and checks the table and every stated structural condition.

## Reduction of the upper-bound decision to one kernel pair

We use the Frankl--Pin set-pair bound: an s-subset Frankl--Pin sequence on n states has length at most T=binom(n-s+2,2). A sequence consists of s-sets S_i and pairs E_i subset S_i with E_i not contained in S_j for any j<i.

Here is the compression refinement from Kisielewicz, Kowalski and Szykuła, *Experiments with Synchronizing Automata*, CIAA 2016, Theorem 1, with the needed argument. Let P be a set of pairs each merging within h letters, and let p be the maximum length of such a sequence over P. If a shortest compressing word for S has length L>h, take its first L-h prefix images. For each choose a pair merged by the corresponding suffix of that word. The pair chosen at a later prefix is absent from every earlier image, since otherwise a shorter compressing word would result. No pair of P occurs in these prefix images either, since appending its h-letter merge would shorten the word. Appending a length-p sequence over P gives L-h+p<=T, hence L<=T-p+h.

If two distinct pairs merge under letters, take those two pairs as P, h=1. Since 2<=s<n they admit a sequence of length two: choose the first s-set to contain the first pair but omit an endpoint of the second not in the first; choose the second s-set to contain the second pair. Thus L<=T-1=9 when n=11,s=8. Every s-subset is compressible in a synchronizing automaton. Therefore compression length ten is possible only when the union of all letter kernel pairs is a single pair K. After exchanging letters, a is singular of rank n-1; b is either a permutation or a rank-(n-1) transformation with the same K.

## Completeness of the finite cover

A rank-(n-1) transformation has one state of indegree zero, one of indegree two, and every other state of indegree one. Its functional graph is one transient path of length h>=1 entering a cycle of length L>=1, together with disjoint permutation cycles. Indeed a branching tree before the cycle would have at least two leaves. Up to conjugacy, the first component is

```
0 -> 1 -> ... -> h+L-1 -> h,
K={h-1,h+L-1}.
```

The remaining cycle lengths are an integer partition of n-h-L. If h>=4, a^4 has rank n-4=7 and compresses every eight-state subset. Hence only h=1,2,3 are needed. Enumerating all L and partitions gives 209 first-letter forms for n=11.

For a fixed first form, begin with its path-and-cycle component discovered, in its forced a-order. Assign b-successors to discovered sources successively. A successor in an already discovered component is fully labelled. When a successor first enters an undiscovered a-cycle, its rotation can be chosen to make that successor the cycle's first vertex; equal-length undiscovered cycles can be exchanged to select the first unused one. Append that entire cycle in a-order. This normalization uses only automorphisms of a and fixes all previously discovered vertices. Strong connectivity guarantees that every a-component is eventually discovered. Thus the branching procedure covers every strongly connected b, up to conjugacy preserving a.

Permutation b-successors are injective. In the singular case only the two K-sources share a successor; the second is forced to have the first's value. All other successor choices are injective. The K-sources both lie in the initially discovered component, and the first precedes the second. These alternatives exhaust every admissible b.

For a partial b-assignment let G be the graph of pairs that merge in at most nine letters using only the determined transitions. Reverse pair closure computes these edges exactly for the partial transition relation. Completing b can only add such edges. An eight-state subset avoiding compression through length nine would be an independent set of G; its three-point complement would cover every edge. A partial branch may therefore be discarded whenever G has no vertex cover of size at most three.

The first program checks this by a greedy four-edge disjoint matching when available, followed by a complete depth-three vertex-cover recursion. The independent implementation instead enumerates all 165 three-point hole sets and intersects their edge-cover masks, using bitset pair closure instead of inverse-state-fiber BFS. Their graph connectivity tests also differ. At complete branches, strong connectivity and synchronization are tested exactly; actual full-set images are checked if a compression-delayed subset survives. In the n=11 run no complete branch is both strongly connected, synchronizing and compatible with a three-point cover of the short-pair graph. Thus no binary strongly connected synchronizing eleven-state automaton has an eight-state subset of compression length ten. The conclusion holds even without requiring that subset to be a reachable image.

## Audit checklist and results

* The first n=11 cover completed: 209 first-letter forms, 1,415,723,476 successor assignments, 611,559,458 partial prunes and 129,412,072 complete maps; no eligible strongly connected synchronizing map.
* The second n=11 cover also completed. Every assignment, prune and leaf count agrees: 1,415,723,476; 611,559,458; 129,412,072. No eligible strongly connected synchronizing map survives. Its completed n=6,7,8,9 controls also agree with the first implementation in every count.
* The n=5 positive control finds the known compression length ten for a reachable pair. Its ac for a singleton A is smaller; it is not a counterexample to the avoid-or-compress formula.
* `audit_compression_cover.py` independently enumerates labelled first transformations and explicit conjugacy orbits, and repeats all admissible labelled second transformations for n=5,6. Ordinary forward pair BFS agrees with the earlier unpruned C++ cover. This independently checks the first-letter classification and the negative n=6 control.
* Solver timeouts are not used anywhere in this proof. No all-parameter negative statement is inferred from the cover at n=11.

The proposed unrestricted F formula remains a separate question. What this finite obstruction rules out is the requested assertion that its upper bound always has a binary attaining witness.
