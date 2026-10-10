# A compression-bound floor for short-pair covers

9 October 2026. This is a direct use of the known Frankl--Pin bound,
not a new compression theorem or a new value of F. It excludes the
whole joint B={0},C={1} at (13,9,1), for every finite alphabet.

Let P_h have as edges pairs merged by words of length at most h in
a strongly connected synchronizing n-state automaton. Suppose Z is
a vertex cover of P_h, |Z|=k and n-k>=2. The auxiliary set Q minus Z
has no pair merged within h, hence no word of length at most h
compresses it. But the Frankl--Pin theorem compresses every subset T
of size at least two in at most binomial(n-|T|+2,2) letters. Thus

    binomial(k+2,2) <= h  implies that Z cannot cover P_h.       (1)

The case k=0 is included: synchronization needs a singular letter.
The restriction n-k>=2 is essential; singleton subsets do not compress.
Strong connectivity and synchronization are retained throughout,
matching the cited theorem's hypotheses. The auxiliary set Q minus Z
need not be a reachable image: the known theorem applies to every
subset. This does not relax the paper's requirements on the original S.

For example, tau(P3)>=2 when n>=3. In the thirteen-state investigation
tau(P5)>=2, tau(P6)>=3 and tau(P10)>=4. These lower bounds concern
vertex cover size, not the earlier retracted edge-cardinality caps.

The precise source is Szykula (STACS2018), Theorem1, p.56:2, which
restates the Frankl--Pin theorem for arbitrary finite alphabets:
https://drops.dagstuhl.de/storage/00lipics/lipics-vol096-stacs2018/LIPIcs.STACS.2018.56/LIPIcs.STACS.2018.56.pdf
The formula and subset-size hypothesis were independently checked
against that primary PDF on9October2026. There is no priority claim
for (1), an immediate consequence of this existing theorem.

## Stripping protected points from the thirteen-state H-cover

Assume ac(S,{a})=12, |S|=9, n=13. The established compression
dichotomy supplies a cover H of P5 with at most three states, enlarged
to H={0,1,2}; a=3 is outside H. The first and second entrances meet
all images once through depths ten and nine, respectively.

If B={b}, every safe image through ten contains b. If C={c}, every
safe image through nine contains c. These states are distinct from a
and, when both are singletons, distinct from each other. For any
protected set X contained in every image through depth nine,

    ac(S,X)>=10, ac(S,X)<=4+d_X,

where d_X is the shortest merging length of a pair incident to X.
The second inequality is ENTRY_FIBER_FLAG.md's protected-pair bound.
Consequently d_X>=6: X is isolated in P5. This argument does not assume
equality of ac(S,X) unless it follows separately from its upper bound.

Remove from H every singleton B point and singleton C point. All
those points are isolated in P5; the remainder is still a cover.
If its size is at most one, (1) contradicts that cover, since the
compression bound for a twelve-set is three, and three<=five.

## Whole joint B={0}, C={1}

Here X={3,0,1} is protected through depth nine, so 0,1 are isolated
in P5. The H-cover reduces to {2}. Apply the known compression bound
to Q minus {2}, of size twelve. It compresses within three letters,
giving an edge of P3 outside {2}; this is an edge of P5 as well,
contradicting the claimed one-point cover. This excludes the whole
joint b1_in_c2, independently of every third/fourth entrance and
independently of alphabet size. Initial reachability is unnecessary.

In particular the original third profiles D={2},{4},{2,4} are all
excluded. There is also a separate immediate obstruction in D={2}:
the four singleton states 3,0,1,2 are protected through eight and
therefore isolated in P4. Every immediate collision must touch H,
but all H states are isolated, so every letter is a permutation.
Synchronization is impossible. The whole-joint argument above is
stronger and avoids separate row or kernel classifications.

An independent labelled audit of the intact43 joint orbits strips
protected singleton points and applies (1). Only b1_in_c2 is newly
excluded this way: six labelled ordered pairs (B,C) inside H. It
preserves all other joint records; in particular a two-point cover
of P5 is not rejected, since its Frankl--Pin bound is six, above five.

## Scope and verification

The symbolic argument uses the known compression theorem and the
previously proved protected isolation and H-cover. Finite controls
check (1) on complete small binary and ternary row domains, selected
larger alphabets, and all290 verified frontier examples. They also
compare cover tests with shortest pair and actual-subset compression
search. These controls supplement the proof; they are not a complete
thirteen-state automaton scan or a new all-parameter formula for F.

Counting only the whole-joint exclusion, binary joint cases are23 and
unrestricted42; binary third admission would be158 orbits /842 pairs.
Both extrema at(13,9,1) remain[11,12]; no numerical alphabet separation
or complete answer follows. The accepted paper and release are unchanged.

## Further third-profile exclusions from actual-image intersections

For a fixed admitted B,C,D, let T be the family of all nine-sets
containing3 and meeting B,C,D once, and let X be their intersection.
Every actual image through eight belongs to this family, so contains
X. Each point of X is therefore isolated in P4: apply ac(S,{x})>=9
and ac(S,{x})<=4+d_x to get d_x>=5. Since H covers P4 as well as
P5, H minus X is a cover of P4. If at most one H point remains,
(1) gives a contradiction. This uses P4, not P5: the D one-count
condition is only guaranteed through eight. Possible additional
Boolean fibers merely restrict T and cannot invalidate this necessary
intersection condition; none is assumed absent.

The intact235 third orbits for the B1/B2 inventory have eleven such
exclusions. Three belong to the whole joint already excluded above.
The other eight are:

| ID | B | C | D | Forced H points |
|---|---|---|---|---|
| b1_out_c2_third1 | 4 | 0 | 1 | 0,1 |
| b1_in_c1_third1 | 0 | 4 | 1 | 0,1 |
| b1_in_c3_third1 | 0 | 14 | 2 | 0,2 |
| b2_mixed_c2_third1 | 04 | 1 | 2 | 1,2 |
| b2_mixed_c7_third2 | 04 | 124 | 01 | 0,2 |
| b2_mixed_c9_third10 | 04 | 01 | 124 | 0,2 |
| b2_in_c4_third10 | 01 | 04 | 124 | 0,2 |
| b2_in_c6_third4 | 01 | 024 | 14 | 1,2 |

Digits in the table denote sets of state labels. The first four
rows force the displayed points directly by singleton fibers. In
the fifth and sixth rows, x0+x4=x0+x1=x1+x2+x4=1 implies x1=x4
and x2+2x4=1; Boolean coordinates give x0=x2=1. The seventh row
has x0+x1=x0+x4=x1+x2+x4=1, forcing the same conclusion. In the
last row x0+x1=x1+x4=x0+x2+x4=1 gives x4=x0 and x2+2x0=1,
so x1=x2=1. These are literal characteristic coordinates of safe
images, not multiplicities after an unchecked collision.

The independent bit-mask audit computes each actual-family intersection
and repeats the cut on every labelled D choice within its original
stabilizer orbit. The negative property is invariant under relabelling
preserving H and3. It leaves all other third geometries admitted by
this particular cut, without claiming their automata exist.

Including these eight additional exclusions, binary residual third
admission is152 typed orbits /784 earlier pairs. Binary geometric
admission after previous joint exclusions and this cut is197. For
unrestricted alphabets,224 of the original235 B1/B2 third geometries
remain under this cut alone (the inventory does not include B3).
Joint counts remain23 binary /42 unrestricted; neither F value changes.
