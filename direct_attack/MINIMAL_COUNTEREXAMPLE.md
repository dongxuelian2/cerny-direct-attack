# Necessary conditions, with quantifiers kept explicit

**PROVED (reconstructed reductions and kernel-bridge consequences).
Novelty is not claimed.** Let A be a counterexample with the smallest number
n of states: rt(A)>(n-1)^2. The existence of such an A is not assumed as fact.

Latest original-letter restriction (2026-10-02): EVERY ORIGINAL LETTER
of ANY counterexample has at least TWO functional cycles. This follows
from the reconstructed existing one-cluster upper theorem in
ONE_CLUSTER_UPPER_PROOF_AUDIT.md, attributed to Zhu2026 with the known
Dubuc circular boundary. It does not require state/alphabet minimality.
It is not a statement about arbitrary transformations in the semigroup:
a reset word always has one cycle, but its original-word cost is paid.

The next paid-word continuation gives stronger WORD restrictions, in
PAID_ONE_CLUSTER_WORD_BOUND.md. No counterexample has a rooted word of
length<=n-1. No counterexample has a one-cluster word with cycle size2
and actual length<=floor((n-1)/2). In particular at n>=5 no TWO-letter
word can have a unique two-cycle. More generally every one-cluster word
must fail the explicit conditional square budget there. These follow
from paid reset upper bounds and are not assertions that suitable words
exist universally. The latter formula's proposed universal NONCONSTANT
bridge is separately REFUTED, even at SC n5/rt13.

Latest congruence restrictions (2026-09-30): every class of every
nontrivial congruence has size at least
max{7,ceil((3+sqrt(4n-3))/2)}. A uniform profile with m classes of
size h must additionally have h>=6m, and its graph of bijective
class edges cannot be strongly connected. No nontrivial congruence
is possible at n<=22. These are necessary conditions for a
STATE-MINIMAL counterexample, not a square proof for simple DFAs.
See PROFILE_CLASS_COMPRESSION.md, TERMINAL_KERNEL_FRANKL.md and
BIJECTIVE_FIBER_RETURN_MONOID.md for the complete paper arguments.
The independent continuation in RETURN_MONOID_INDEPENDENT_AUDIT.md
adds: on EVERY congruence class each letter restriction has rank at
least four. In a uniform profile every singular restriction has rank
at least 2m+2, and every bijective-edge SCC's confined return monoid
is nonsynchronizing. The exact charged local-word bound gives a
length constraint for every low-local-rank word, not just letters.

## Strong connectivity is a valid reduction

A synchronizing DFA has exactly one terminal strongly connected component C:
two terminal components could not be mapped to a common state. All states
reach C. Write |C|=m and t=n-m. To send Q into C, let R be the current image
and r=|R\C|. Choose q in R\C of minimum graph distance d to C, and use a
shortest path word sending it into C. The d-1 intermediate outside states
cannot lie in R\C: each has smaller distance to C. They are distinct, so
d-1<=t-r. This word costs <=t-r+1, and reduces r by at least one because C
is invariant under all letters. Summing over the decreasing values of r
costs at most t(t+1)/2. This proof works when ranks are skipped.

The restriction to C synchronizes. If m<n, state minimality gives a reset
word on C of length <=(m-1)^2. Thus

    rt(A) <= t(t+1)/2+(m-1)^2 <= (n-1)^2,

since the difference in the last inequality is t(4m+t-5)/2>=0 for m,t>=1.
For m=1 the reset word on C is empty. This contradicts counterexample status.
Consequently a state-minimal counterexample is strongly connected.

## Alphabet minimality: an existential choice, not a fact about every example

Among state-minimal counterexamples, choose one with the fewest letters.
Deleting a letter can only increase reset threshold. Therefore every proper
subalphabet must be nonsynchronizing. Such a chosen counterexample has no
identity letter, duplicate letter, or letter whose transformation is generated
by the others: removing any of these would preserve synchronization.
We do not conclude that EVERY state-minimal counterexample has this property.

## Uniform compression profile constraint

For lambda_r=min{|u|:rank(u)<=n-r}, the paper kernel bridge proves

    rt(A) <= U(A):=sum_(r=0)^(n-2) min{(r+1)(r+2)/2,lambda_r+r+1}.

Hence U(A)>(n-1)^2 is necessary for any counterexample. This depends only on
proper rank thresholds, excluding lambda_(n-1). It is not sufficient: even
the extremal Cerny family can pass this inequality filter.

If A has a word of rank <=r, length L, 2<=r<=n, repeated kernel bridges give
a rank-at-most-two word of length at most

    2^(r-2)(L+n-r+2)-n.

This follows by Pin's 1978 Proposition 5 recurrence L_(k-1)<=2L_k+n-k+1,
not by treating a reused
suffix as free. The final pair costs at most n(n-1)/2. Therefore a necessary
condition for a counterexample is, for EVERY word of rank r>=2 and length L,

    n(n-1)/2-n+2^(r-2)(L+n-r+2) > (n-1)^2.

For example rank-three letters are excluded for n>=5; rank-four letters for
n>=8. These illustrative deductions are weaker asymptotically than established
small-rank-word results of Berlinkov--Szykula, so they are not new extremal
restrictions. The stronger known low-rank-letter restriction should take
precedence in actual counterexample searches.

Primary source for the recurrence and its logarithmic small-rank corollary:
[Pin 1978](https://www.irif.fr/~jep/PDF/AlgebreLineaire.pdf).

## Charged reflected-return exclusion on arbitrary images

PUBLISHED_COMPRESS_OTHER_FAMILY.md adds an explicit common-word
certificate, not an assumption about all return monoids. If an entering
word of length E has actual image R of size r>=4, and actual return
words c,d act as a cyclic rotation and a reflected adjacent unit of
phase t, then the whole reset budgets are

    E+(r-1)(2|d|+|c|)       if t=1,
    E+(r-2)(2|d|+|c|)       if 2<=t<=r-1,
    E+(r-2)(2|d|+3|c|)      if t=0.

The appropriate quantity must exceed (n-1)^2 in any counterexample.
No congruence is needed, but the precise action hypotheses are essential.
There is no assertion that every synchronizing DFA has such cheap
words; nor is a cycle inverse charged at zero cost. The t0 case uses
the longer actual return c d before forming its rooted composite.

## Conditions that have NOT been proved

- No nontrivial quotient/congruence: still unproved. The fiber-size count in
  QUOTIENT_FIBER_LIFT.md now supplies a conditional lift and excludes every
  congruence whose largest class has at most six states in a state-minimal
  counterexample (using the self-contained rank-truncated 1/2-class lift,
  which reconstructs the published qualitative result). The pair-truncated
  lift additionally excludes every class of size three. With at least
  three classes, the largest must be at least eight. For two classes, the
  mixed-size profiles (3,7) and (4,7) are also excluded. Larger fibers
  remain uncontrolled by this count; letters may move the class.
- A single cyclic permutation letter: six-state extremality already has a
  noncircular example with the same reset threshold 25 as C6.
- No easy pair: literally impossible, since every synchronizing DFA with
  n>=2 has a non-permutation letter and thus a pair of distance one.
- Nearly uniform pair distances: the computed extremal examples have broad
  spectra, and their spectra differ substantially.
- Short avoiding words alone suffice for the exact square: not established.

The first two valid reductions above are standard in spirit. Their complete
proofs are included to prevent misuse of hidden induction or connectivity
assumptions in subsequent work.
