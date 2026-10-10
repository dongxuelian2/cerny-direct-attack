# Uniform codimension-three compression bound

**Theorem.** In every strongly connected synchronizing complete automaton
with n>=6 states, every (n-3)-subset admits a compressing word of length
at most nine. The alphabet is any finite alphabet; the subset need not
be a reachable image.

This proof uses finite, complete action projections after symbolic
reductions. It does not extrapolate an enumeration at small n.

## Reduction to nine ordered early-pair types

The Frankl--Pin compression bound gives ten. Suppose some (n-3)-set
has shortest compression length ten. For h>=1 let P_h contain every
unordered distinct-state pair merging within h original letters.
The refinement of Kisielewicz, Kowalski and Szykuła, CIAA 2016 Theorem 1,
gives compression length at most 10-p(P_h)+h, where p is the longest
(n-3)-subset Frankl--Pin sequence over P_h.

Any q<=4 distinct pairs admit a sequence of length q. Index them
E_0,...,E_(q-1). Choose three holes for its ith subset outside E_i,
hitting an endpoint outside E_i of each later pair E_j, j>i. There
are at most q-i-1<=3 required endpoints, and n-2>=3 available states.
Fill to three holes. Thus E_i is in its own subset and is absent from
every earlier subset, exactly the standard Frankl--Pin convention.
Consequently |P_h|<=h for h=1,2,3. A nonempty synchronizing alphabet
has P1 nonempty. The recurrence adding all letter-preimages of P_h
grows strictly until every pair is present: a plateau is a fixed point
and would contradict synchronization. Since n>=6, it cannot exhaust
all pairs by depth three. Hence |P_h|=h for h=1,2,3.

Write P_h={E1,...,Eh}, E1=01. Each letter is a permutation or has rank
n-1 and common kernel 01. Every two-point inverse image of E1 belongs
to {E1,E2}; every such inverse image of E2 belongs to {E1,E2,E3}.
EARLY_PAIR_TYPES.md proves that the following nine types exhaust all
ordered triples up to simultaneous state relabeling.

## Common image and exit argument

Let H be the three-hole covers of P3. Every image of the initial subset
reached by depth six is uncompressed and has holes in H, or a P3 word
of at most three letters would give compression by depth nine. Let
R_i be the distinct images reached by depth i. These grow strictly
until compression: a plateau is invariant under all letters and cannot
be reset. Thus |R_i|>=i+1 through depth nine.

A domain D defined by H-preservation under test words of length at
most L contains R_(6-L); it must have at least 7-L members. When its
size is exactly 7-L, every member is reached by depth 6-L, and every
letter maps it into H. Project such letters to D and EXIT=H minus D.
Synchronization forces every D-vertex to exit eventually. With k
vertices, finite exit distances are at most k. If an initial distance
equals k, a shortest path visits every vertex, so the distance vector
is a permutation of 1,...,k. For each such vector d enumerate all
profiles p satisfying d(i)<=1+d(p(i)), d(EXIT)=0. Any actual alphabet
is contained in this enlarged graph. If the graph cannot make every
vertex exit, the distance vector is impossible.

Every surviving vector below has the stronger property that every
underlying partial row of every allowed profile preserves a set of
five states. Strong connectivity excludes that for n>=6. Thus maximum
exit distance is at most k-1. The bound is (k-1)+L+3=9 whenever
k=7-L. The second path-2 singular domain instead has k=4 and two
distinct distance-one vertices; its maximum exit distance is at most
three, with the same 3+3+3=9 charge. Type 8 uses its eight covering
images directly, with first exit at most six, hence 6+3=9.

## Complete case table

The cited case notes give the full letter classifications, hole-domain
calculations and fresh-label coverage arguments. Their finite projections
enumerate partial rows on at most six named states. Unnamed output states
are renamed to a bounded supply of fresh labels; this is why the negative
certificates cover every n and arbitrary alphabets. Included extra rows
that fail to extend at a particular small n only enlarge the graph.

| type | E2 | E3 | complete reduction and certificate |
|---|---|---|---|
| 0 | 02 | 12 | TRIANGLE_EARLY_EXCLUSION.md; Case A in TRIANGLE_MIXING_CASE_A.md. Remaining domains: k=4,4,6, with 11,38,61 profiles and 24,24,720 vectors. Only the middle domain has three surviving vectors; all force a proper five-state invariant set. |
| 1 | 02 | 03 | EARLY_PAIR_TYPES.md: every letter fixes 0 with no other incoming edge or omits 0. Strong connectivity is impossible. |
| 2 | 02 | 13 | PATH2_EARLY_EXCLUSION.md: one k=5 domain with 22 profiles and 120 vectors; one surviving vector forces a five-state invariant set. Other domains have insufficient size or the two immediate exits described above. |
| 3 | 02 | 23 | PATH3_EARLY_EXCLUSION.md: k=5,4 domains with 24,19 profiles and 120,24 vectors; only the first has one surviving vector, forcing a five-state invariant set. The no-T branch has a complete symbolic domain count at most four. |
| 4 | 02 | 34 | TYPE4_EARLY_EXCLUSION.md: two k=6 domains, 33,37 profiles, 720 vectors each, no survivors. This case requires synchronization alone. |
| 5 | 23 | 02 | TYPE5_EARLY_EXCLUSION.md: a letter creating 02 necessarily creates the forbidden pair 12 as well, or violates inverse-pair disjointness. No projection is needed. |
| 6 | 23 | 04 | TYPE6_EARLY_EXCLUSION.md: one k=5 domain, 19 profiles, 120 vectors, one survivor forcing a five-state invariant set; all other branches have symbolic domains of size at most four. |
| 7 | 23 | 24 | TYPE7_EARLY_EXCLUSION.md: three k=6 and four k=5 domains, 21,39,37 and 27,23,23,33 profiles. Only C_V has two surviving vectors, each forcing a five-state invariant set. |
| 8 | 23 | 45 | MATCHING_EARLY_EXCLUSION.md: eight images, 177 profiles. All 30,240 possible finite vectors with initial distance at least seven fail. No strong-connectivity hypothesis is needed in this case. |

All cases contradict compression length ten. This proves the theorem.
Binary complete covers at n=11,12,13 are independent historical checks,
not a necessary step of this uniform upper proof.

## Exact reachable-image consequence and its limits

For n>=10 and 1<=r<=n-5, CODIMENSION_THREE_PROOF.md provides binary,
strongly connected, synchronizing witnesses with a reachable (n-3)-image
and local value min(n-r,9). For r=n-4 the first-face theorem provides
the same equality. For 5<=n<=9 every parameter is covered by a literal
binary witness in formula_certificates.json, independently checked by
ordinary subset BFS and original-letter reaching/reset/attaining words.
Since n-r<=8 there, its value U equals min(n-r,9).

Therefore for every n>=5 and 1<=r<n-3,

    F_bin(n,n-3,r) = F(n,n-3,r) = min(n-r,9).

For every n>=11 and 1<=r<=n-10 the conjectured value U is ten, whereas
both maxima are nine. This refutes the proposed formula under the full
binary requirements and for arbitrary finite alphabets. It gives a
partial answer to Open Problem 4; parameters with n-s>=4 are not all
determined. No alphabet separation, priority guarantee or all-parameter
replacement formula follows from this proof.

The hypothesis n>=6 in the compression theorem is necessary for the
five-state-invariant-set arguments. A reachable pair in the strongly
connected synchronizing five-state example in PATH3_EARLY_EXCLUSION.md
has shortest compression ten. Its avoid-or-compress value is bounded
by n-r<=4, so it does not contradict the exact local maximum above.
