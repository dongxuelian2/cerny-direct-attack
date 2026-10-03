# Rank-loss saturation preserves optimal histories under permutation augmentation

Date: 2026-10-01. The general transfer and cut-gap lemmas are
**PROVED (paper)**. The particular low-dimensional inputs are
**COMPUTATIONALLY VERIFIED at n7 and n15 ONLY**. There is no arbitrary-d
construction, **FORMALLY VERIFIED** result or general Cerny proof.
Priority is **OPEN**; elementary rank inequalities are not claimed novel.

Subsequent ALL_OPTIMAL_LOG_COUNTER_HISTORY.md supplies a DIFFERENT
explicit all-d unit/carry family and refutes every optimized positive
linear coefficient, even with Eulerian simple complete reachability.
The finite inputs and general transfer/slack lemmas here remain valid.
Earlier arbitrary-d/positive-fraction OPEN labels below are superseded;
expensive-phase tradeoffs remain OPEN.

## General rank bound and a transfer theorem

For a transformation f define its corank c(f)=n-|Qf|. For EVERY subset
S, |Sf|>=|S|-c(f). Thus a reset word w must pay total corank at least
n-1. If every original letter has corank at most c>=1, the reset
threshold is at least

    L0=ceil((n-1)/c).

**PROVED.** Suppose a reset word of length L0 exists. Adjoining ANY
additional ORIGINAL permutation letters preserves the reset threshold
AND the entire collection of shortest ORIGINAL reset words. Indeed a
word of length at most L0 containing one added permutation has at most
L0-1 positive-corank positions, and can lose at most c(L0-1)<n-1
points. It cannot reset. A shorter word consisting of old letters is
also excluded by the same lower bound. Every shortest word is therefore
an old shortest word, with identical labeled indices, image histories,
full inverse histories and their exact dimensions.

Every shortest word at this lower bound strictly reduces its current
image at EACH step. A neutral step would leave only L0-1 possibly
reducing steps, with the same insufficient corank budget. Every forward
prefix image is actual; reading these strict drops backwards yields a
compatible actual-image chain of ORIGINAL one-letter phases. Each such
phase has exact e=1, because a zero-letter word cannot transport a
strictly larger set into a smaller one. Consequently P=rt=L0. This
argument proves existence of an optimal policy; it does not identify
EVERY optimal policy when c>1 and there is rounded corank slack.

This hypothesis is lower-bound attainment, not a way of asserting that
an arbitrary DFA attains that bound. In particular it does not imply
an unrestricted quadratic reset construction.

## Actual images and full inverse cuts: an exact general slack lemma

**PROVED.** For ANY reset word w=u v to q, put

    C(w)=sum_(letters f of w) c(f), delta=C(w)-(n-1).

Let S=Qu be its actual prefix image and T={q}v^-1 its full suffix
preimage. Then S is contained in T, and

    0 <= |T|-|S| <= delta.

The lower subset-image bound gives |S|>=n-C(u). The fiber bound
|Xf^-1|<=|X|+c(f), obtained by summing all fiber excesses and subtracting
missing target points, gives |T|<=1+C(v). Subtraction proves the claim.
It also proves delta>=0 for every reset word. This applies to arbitrary
alphabets and strict arrivals, without actual-image heredity.

When delta=0, S=T at EVERY cut, so every full inverse cut is actual.
This equality alone does NOT prove that a multiletter phase is locally
shortest or that greedy choices are globally compatible. Permutation
letters may still cost positive length with zero corank. The next
specialization removes that problem by saturating ORIGINAL LETTER COSTS.

## Corank-one specialization: all optimal policy cuts are forced

**PROVED.** If every original letter has rank n or n-1 and rt=n-1,
every shortest reset has n-1 strictly reducing rank-(n-1) letters.
The total corank is n-1. By the cut-gap lemma, EVERY forward prefix
equals the corresponding full inverse suffix preimage. Those sets are
actual, with cardinalities n,n-1,...,1, and every inverse stage has e=1.
Thus P=rt=n-1.

Moreover EVERY optimal actual-image policy has one-letter phases and
these same letter-level cut histories. Compose its phase words to a
length-(n-1) reset word. For each nominal edge T->S of length ell,
the corank bound implies |T|-|S|<=ell. Summing over the chain gives
n-1<=sum ell=n-1, forcing equality on every edge, exact arrivals and
one-point loss at every original letter. At the singleton end, the first
inverse letter's full preimage is actual by the preceding cut lemma,
so e=1. Its parent must equal this one-point-larger preimage. Repeating
forces each subsequent one-letter cut. Therefore adjoining permutations
preserves ALL optimal endpoint-set policy histories too, despite changing
the ambient actual-image family. This is a precise restricted invariance;
general image-policy monotonicity under adding letters remains REFUTED.

## Charged complete-reachability and simplicity completion

Adjoin the ORIGINAL adjacent transpositions (i,i+1), i=0,...,n-2,
to any such corank-one input. They generate all permutations. The
augmented DFA is SC and simple: any identified pair in a congruence
can be carried to every other pair by a generated permutation, forcing
the universal relation. These permutation words need not be short
reset phases; they cannot appear in ANY minimum reset here.

It is also COMPLETELY REACHABLE. Fix an original rank-(n-1) letter f
and its only collision pair. Given a current k-set with k>=2, an
actual permutation word puts two selected states on that pair; f then
reduces cardinality by exactly one. Iterate and finally permute the
result to the desired nonempty target. If B=n(n-1)/2, any permutation
can be written in at most B ORIGINAL adjacent swaps by sorting. Thus
a concrete target T of size k<n has a membership word of length at
most (n-k)(B+1)+B; Q has the empty word. All conjugations/transport are
charged. No generated permutation is silently declared cost one.

Complete reachability here requires the available rank-(n-1) singular
letter. The general corank-c augmentation theorem above does not claim
complete reachability when all singular ranks are smaller.

## All optimal histories can be small: two finite exact inputs

The fixed original rank-(n-1) rows are retained in
`data/optimal_saturation_inputs.json`. They were found by an ignored
heuristic search; the registered generator reconstructs the exact fixed
certificates, not that search stream or an exhaustive alphabet cover.
No extrapolation to d>=5 is made.

For d=3/4, n=2^d-1, let B_i=[2^i-1,2^(i+1)-2], of size 2^i,
and S_k be the union of B_i whose bits in k are one. Exact inverse
growth and independent forward drop DAGs find that ALL globally shortest
words have the SAME proper endpoint list

    S_2,S_3,...,S_(n-1),

with possible singleton roots as follows:

| n | Original singular rows | rt=P | ALL shortest labeled words | Optimal endpoint chains | Proper stages | Normalized proper rank |
|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 6 | 3 | 3 | 5 | 2 |
| 15 | 14 | 14 | 8 | 1 | 13 | 3 |

At n7 the roots are masks 1,4,8; full letter-level inverse ranks are
3,4,4. At n15 the sole root is mask1; all eight words have full inverse
rank four. Thus counting every intermediate letter or changing the
shortest word cannot produce a large dimension in THESE exact inputs.
There is no suboptimal-history caveat: every word has rt=n-1.

By the general augmentation theorem, adding 6/14 adjacent swaps makes
the inputs SC, simple and completely reachable while preserving EVERY
minimum reset word AND EVERY optimal actual-image policy endpoint chain.
They use 12/28 original labeled letters. The n15 example therefore forces
any proposed universal positive-fraction proper-dimension guarantee to
have coefficient at most 3/13, even in this completed class. It does
NOT refute every positive coefficient. A logarithmic ALL-PARAMETER
optimized-history family remains OPEN. These cheap saturated histories
also do not refute a tradeoff involving expensive phases.

The exact rank is transparent: all proper indicators are block-constant.
They span every block indicator, since chi_(B0)=chi_(S3)-chi_(S2)
and chi_(Bi)=chi_(S_(2^i)) for i>=1. Raw rank with Q is d and centered
rank is d-1. On representative coordinates of B1,...,B_(d-1), the
centered block vectors have determinant n^(d-2), namely 7/225. Including
a singleton from a nonsingleton block adds exactly one raw dimension.

## Independent verification

`optimal_saturation_history.py` uses ALL-SUBSET inverse +1 growth DAGs
and rational Gaussian ranks, retaining every optimal vertex and every
shortest labeled original word. `check_optimal_saturation_history.py`
imports no generator or native solver; it uses ALL-SUBSET FORWARD -1
drop DAGs, literal original-state runs, full inverse reconstruction,
block-cell bounds and integer Leibniz minors. It compares ALL optimum
vertices, roots, labels and histories, not selected traces.

There are 919000 original-label/subset rank controls. Ordinary full-Q
forward closure after augmentation independently reaches all 127/32767
nonempty subsets (32894 vertices total). All eleven shortest base words
are literally checked, paying 130 original letters. Six corruptions
are rejected. The checker verifies the d3/d4 finite claims; the general
transfer and slack statements are paper proofs, not computational
universal proofs or a formal kernel.

Registry106 / regeneration190 preserves the previous105-check record
verbatim and continues only this generator/replay/check. No full106
rerun. General Cerny, compatible-policy square, positive-fraction
optimized dimension and expensive-phase compatibility remain OPEN.
