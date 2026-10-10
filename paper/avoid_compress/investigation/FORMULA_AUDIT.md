# Audit of the conjectural exact formula

8 October 2026. This note concerns only the current Open Problem 4
avoid-or-compress invariant. The proposed formula is refuted for both
binary and arbitrary finite alphabets: at every n>=11, s=n-3,
1<=r<=n-10, both maxima are nine whereas the proposed minimum is ten.
CODIMENSION_THREE_UPPER_PROOF.md supplies the all-state-count upper;
ordinary-set binary certificates supply the reachable-image lower.

The accepted exact region, with m=n-s,q=n-r, is: m=0 gives one;
1<=m<=3 gives min(q,3m); m>=4,q<=3m-1 gives q. The first two faces and
the every-n cofinal range n>=2s-r-1 are also proved. All 286 triples
through n=12 and four additional n=13 triples have matching proofs
and independently checked binary witnesses. DFA enumeration is not
asserted at n=8,...,12.

The region unclassified as a whole remains m>=4,q>=3m. The first unknown
is (13,9,1), with both alphabet-class maxima in [11,12]. No all-parameter
replacement formula or alphabet separation is established. The article
remains a partial answer, with the requested title and seven-page PDF.
The actual supplement has 109 files, listed in ../reproducibility/README.md,
inside ../release/reproducibility.zip. Auxiliary research is outside it.
CURRENT_FRONTIER.md and active_research.json give the current research
state. Older package counts and intervals below are historical only.

## Archived binary-only update (superseded)

Two completed independent finite decision covers prove F_bin(11,8,1)=9,
below U=10. BINARY_OBSTRUCTION_PROOF.md gives the reduction, completeness
argument and an elementary reachable-image lower example. The Python audit
checks the witness, short-image table, pairs and saved count agreement.
Unrestricted F remains in [9,10]. Earlier failed searches and intervals
below are historical diagnostics, not the proof of this negative result.
The final five-page paper includes this computer-assisted theorem.
Its actual supplement is ../release/reproducibility.zip, with the 26 files
listed in ../reproducibility/README.md. This local investigation directory
and the larger construction notes are not the submission supplement.

## Definition and the established upper bound

Use the manuscript's definition of F(n,s,r): maximize ac(S,A) over strongly connected synchronizing n-state complete automata, with S an actual image of Q, |S|=s and |A|=r. The alphabet is unrestricted in this definition. Write F_bin for the same maximum restricted to binary automata, and put

```
U(n,s,r) = min(n-r, (n-s+2)(n-s+1)/2).
```

For every 1 <= r < s <= n,

```
F_bin(n,s,r) <= F(n,s,r) <= U(n,s,r).
```

The avoid-or-compress lemma supplies the first upper bound: a reset word followed by a path outside A verifies the avoidance hypothesis. The Pin–Frankl compression bound supplies the second: s >= 2 and the automaton is synchronizing, so S has a compressing word of that length. A compressing word satisfies the avoid-or-compress predicate regardless of its image's intersection with A. These are upper bounds; taking their minimum establishes no attaining example. Both are explicitly stated in [Szykuła's STACS 2018 paper, Theorem 1 and Lemma 2](https://drops.dagstuhl.de/storage/00lipics/lipics-vol096-stacs2018/LIPIcs.STACS.2018.56/LIPIcs.STACS.2018.56.pdf). The compression theorem is credited there to Pin and Frankl; Frankl's original reference is [An extremal problem for two families of sets (1982)](https://doi.org/10.1016/S0195-6698(82)80025-5).

The target question is [Szykuła 2026, Section 2.2, Lemma 3 and Open Problem 4](https://arxiv.org/pdf/2608.24245v1). The survey asks for tight bounds as a function of both cardinalities, particularly in the strongly connected synchronizing setting. A binary attaining reachable image for every triple would also establish sharpness for arbitrary subsets in that setting, because this upper bound does not require reachability. No such uniform construction is certified here.

## Parameter and boundary audit

* n=1 gives no triples in the stated domain; s>=2 throughout.
* For s=n, U=1, and every synchronizing automaton has a singular letter. This agrees with the manuscript's full-image boundary.
* On s=r+1, put m=n-s. Then n-r=m+1 <= (m+1)(m+2)/2, so U agrees with the first-face theorem.
* On s=r+2<n, m>=1 and n-r=m+2 <= (m+1)(m+2)/2. Thus U agrees with the second-face theorem. At s=n that theorem's proper-image range is excluded and the value is 1.
* In the larger-gap family, m=n-s=(k-1)g+1>=g+1 and n-r=m+g+1<=2m<=(m+1)(m+2)/2. The conjecture therefore agrees with all of the already-proved arithmetic progressions.

This checks consistency only. It does not cover the state counts outside those progressions.

## Exhaustive small cover and independent lower-bound certificates

`exhaust_binary.cpp` exhausts binary automata for n=2,...,7 up to conjugacy of the first transformation, while leaving the second transformation fully labelled. Every unary transformation is marked under every state permutation; the next unmarked transformation represents its entire conjugacy orbit. Simultaneously relabelling the second letter, S and A shows that this cover omits no binary automaton or subset pair. It is an overlapping cover, not a count of binary isomorphism classes.

| n | Transformations | First-letter orbits | Covered representative/labelled pairs | Strongly connected synchronizing pairs in the cover |
| --- | ---: | ---: | ---: | ---: |
| 2 | 4 | 3 | 12 | 4 |
| 3 | 27 | 7 | 189 | 59 |
| 4 | 256 | 19 | 4,864 | 1,240 |
| 5 | 3,125 | 47 | 146,875 | 32,588 |
| 6 | 46,656 | 130 | 6,065,280 | 1,122,529 |
| 7 | 823,543 | 343 | 282,475,249 | 42,605,958 |

For each pair, graph closure tests strong connectivity and full-set subset BFS tests synchronization and enumerates all actual reachable images. For a fixed S, one BFS finds its first compression distance c and each state's first omission distance d_q. Hence ac(S,A)=min(c,min_{q in A} d_q). Choosing the r states with largest min(c,d_q) maximizes ac over all A of size r. Once a known upper bound has an independently checked witness, further searches for that triple cannot improve its maximum and are skipped. Every representative/second-letter pair is nevertheless covered.

`audit_small.py` checks the 56 saved triples for n<=7 using ordinary sets and direct avoid-or-compress BFS, rather than the per-state score reduction. It independently repeats the entire labelled search, with every A explicitly enumerated, for n=2,3,4 (16, 729 and 65,536 labelled pairs). All maxima agree. These finite certificates plus the established upper bound already certify the exact values; they do not depend on treating an unchecked negative search as a theorem.

Structured searches, construction extensions and reuse of the manuscript automata supply attaining witnesses through n=10 as well. `formula_certificates.json` contains all **165 triples for 2<=n<=10**, each with two transition rows, S, A, an original-letter reaching word, an attaining word and a reset word. `verify_certificates.py` independently checks every one and computes exact ac by full ordinary subset BFS. Thus the formula is **certified on all these finite triples**, including all four structural requirements. Automata of sizes 8, 9 and 10 were not exhaustively enumerated. At (10,7,2), a verified Boolean-SAT witness and independent edge-subdivision probes both attain 8. Further checked subdivisions close (11,8,2) and (11,8,3); at n=11 the supplied probes leave (7,1) unresolved; the final cover determines F_bin(11,8,1)=9, while unrestricted F at that point remains in [9,10].

## Adversarial audit of construction extensions

The parameter M=kg+1 in Proposition 5 is substantive. If one retains the transition rules while dropping that restriction, the exceptional state need not have color 1. The signed correction and its distances then change; one cannot reuse the original delay proof.

Two independently checked failures of this attempted extension are recorded in `extension_audit.json`:

* r=1,g=3,M=6 gives n=8,s=5. It is binary, strongly connected and S=Qb^3, but it is **not synchronizing**. Both letters induce permutations on the five cells and S contains one state from each cell, so all words preserve one trajectory in each cell. The proposed attaining value 7 is meaningless in the required class.
* r=1,g=3,M=8 gives n=10,s=5. It satisfies binary, strong connectivity, synchronization and actual-image reachability, but its exact ac is **8**, attained by `aaaaaabb`, instead of the desired 9. Here u_M has color 2, and the end correction is e_1-e_3, not e_1-e_2. The negative term reaches A earlier.

These are counterexamples to a proposed *construction extension*, not counterexamples to F=U. Other automata at those parameters may attain U; at (10,5,1) a different checked witness does attain 9.

A direct chain variant was also checked in 286 finite parameter cases; it does not support a uniform sharpness claim. Its m=1 instances fail synchronization, and valid instances in larger ranges can admit shorter successful words. This variant is diagnostic data only and is not added to the manuscript.

For the compression-dominated test (n,s,r)=(11,8,1), the upper bound is 10. A scan with an arbitrary action on six active states, five other fixed states, and a permutation second letter assembled from paths between the active states covers 23,587,200 structured row pairs. Its maximum is 9. The five-active-state variant also reaches 9. These restricted covers do **not** exhaust all binary automata; they establish a checked lower bound 9 and do not establish a strict upper bound. After the completed cover described above, the supported statement is

```
F_bin(11,8,1) = 9 <= F(11,8,1) <= 10.
```

The previous interval at (10,4,1) is now closed by the cofinal construction below: its value is 9. `unresolved_intervals.json` records the other finite gaps left by the supplied probes. These are unrestricted-alphabet intervals; the binary maximum at (11,8,1) is separately determined.

## Uniform constructions checked on 8 October

`COFINAL_PROOF.md` gives an explicit construction and proof for every r>=1, g=s-r-1>=2 and M=n-r-1>=2g. It treats M>=2g+1 and M=2g separately. Thus F_bin=F=n-r whenever n>=2s-r-1. This includes every residue class of n, rather than only the manuscript's arithmetic progression. The proof bounds trajectory counts in cells and excludes the extra a-collision introduced by the transient path; it supplies original-letter reaching, attaining and reset words. `check_cofinal.py` and `check_boundary.py` independently audit 316 and 33 parameters respectively, through n=39 and n=30, including all color residues. These finite checks do not replace the uniform proof.

`DEFECT_TWO_PROOF.md` proves sharpness 6 for s=n-2 and 1<=r<=n-6. A seven-row hole table proves safety of every word of length at most five; explicit unit macros establish actual reachability and synchronization. `check_defect_two.py` checks all 300 parameters with 7<=n<=30. Combined with the cofinal construction and the existing faces, this determines every codimension-two triple: if n-r<=5, then g=n-r-3<=2, covered by the faces or the M=2g boundary; if n-r>=6, the new construction applies.

The same proof note gives a three-hole-state construction for codimension one, independently checked on 378 parameters through n=30. Together with the full-image boundary this determines every triple with n-s<=2.

The known compression refinement in [Kisielewicz, Kowalski and Szykuła, Theorem 1 (CIAA 2016)](https://kot.rogacz.com/Publications/Kisielewicz2016ExperimentsWith.pdf) gives a necessary condition for attaining the Pin–Frankl bound: if two distinct pairs merge under letters, an s-subset with 2<=s<n compresses in at most binom(n-s+2,2)-1 letters. Indeed the two pairs admit a Frankl–Pin sequence of length two (choose the first s-set to contain the first pair and omit an endpoint of the second), and their synchronizing height is one. Hence compression-bound equality requires a unique immediate kernel pair, with each singular letter of rank n-1. This necessary condition guides `synthesize_boolean.py`; it is not itself a strict universal bound at (11,8,1).

Z3 proposals are independently checked by ordinary-set BFS. The three kernel orbits relative to a canonical S and singleton A at (11,8,1) are outside/outside, protected/outside and unprotected-S/outside; a kernel inside S is immediately unsafe. Current runs for these cases timed out, including a successful positive-control run at (4,3,1). No solver timeout, unverified solver UNSAT, or bounded construction scan is a mathematical refutation. `core_pair_probe.py` exhausts first transformations of rank t-1 on t=4,5,6 states with second letter a fixed point and a (t-1)-cycle. Its pair-delay maxima are 6,9,11. This is another restricted construction diagnostic, not an upper bound for general automata.

`compression_kernel_cover.cpp` supplies a further finite diagnostic: canonical rank-(n-1) first transformations, all permutation second transformations and all second transformations with the same sole kernel pair. For n=5,6,7,8 its maximum compression length for an (n-3)-subset is respectively 10,9,9,9. The first-letter canonical forms consist of one transient chain entering one cycle, with permutation cycles on all remaining states. The recorded witnesses are reachable. The cover's negative conclusions have not received an independent full-cover audit and are not used as refutations or as manuscript claims. They motivate investigating the remaining compression-bound equality case at n=11.

## Proof obligations that remain unmet

An all-parameter proof would need a single consistent specification, for each triple, of two transformations and an actual reachable S. It must establish safety of **every** word shorter than U, and certify strong connectivity and synchronization. An abstract extremal Frankl–Pin set-pair sequence does not by itself realize such transformations. A timer orbit or one long attaining word does not rule out mixed-letter shortcuts. Adding fixed states can preserve a local delay while destroying strong connectivity or synchronization. A binary-only negative result would refute the stronger binary sharpness requirement but would not alone refute the manuscript's unrestricted-alphabet F formula.

The binary-only state described in this archived section has been
superseded by the arbitrary-alphabet codimension-three proof. The current
status, exact region and release counts are those at the top of this file.
No complete answer is asserted. Solver timeouts and restricted-family
failures remain diagnostics, never upper certificates.
