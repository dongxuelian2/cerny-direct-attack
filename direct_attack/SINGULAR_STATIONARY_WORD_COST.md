# A short stationary mixture cannot use singular words in Cerny automata

Date: 2026-10-02. **PROVED (paper), EVERY n>=2.** A method obstruction,
not a general reset theorem. Publication priority **OPEN**; novelty is
not claimed. General Cerny **OPEN**. No **FORMALLY VERIFIED** claim.

Later continuation WEAK_STATIONARY_LINEAR_COST_COUNTERFAMILY.md shows
that maximum support n is NOT universal: an SC sync fast-reset family
has exact maximum singular stationary-support cost ceil(3n/2)-1 for
EVERY n>=4. The Cerny-family statement below remains valid. No general
cost-n theorem should be inferred from this particular family's optimum.

Use Q={0,...,n-1}, a(q)=q+1 mod n, and b(n-1)=0 with b fixing all
other states. Words act on row vectors on the right. Let h be the column

    h(q)=n-2-q for 0<=q<=n-2,    h(n-1)=n-1.

For EVERY literal original word w with |w|<=n-1, let r_b(w) be its
number of maximal nonempty consecutive b-runs. Then

    ([Q] M_w-[Q]) h = -r_b(w).                           (1)

Thus a nonnegative probability mixture of words of length at most n-1
satisfying ONLY

    [Q] sum_w p_w M_w = [Q]                              (2)

has zero weight on every word containing b. Its positive-weight support
therefore consists entirely of permutations, so cannot itself generate
a synchronizing semigroup. This includes singular words in the allowed
search: their weights are forced to zero by an exact separating functional.
The condition in (2) is much weaker than asking for matrix average J/n.

## All-word proof, including redundant words

For ANY word w=a_1...a_L, deterministic row matrices give the exact
telescoping identity

    [Q](M_w-I) = sum_i [Q](M_(a_i)-I) M_(a_(i+1)...a_L).

An a term is zero; a b term is (e_0-e_(n-1)) M_v for its literal suffix v.
When L<=n-1, this suffix has length<=n-2. Until the first a in v,
an initial b merges the pair0,n-1 and its term becomes zero. If the suffix
is empty, the two outputs are0,n-1 and their h difference is -1.
Otherwise if its first letter is a, let k>=1 be its number of a's.
There are at most n-2 such letters. Its two trajectories are k,k-1:
no later b acts on either, since neither has reached n-1. Their h
difference is again -1. Hence a b occurrence contributes -1 exactly
when it is the last letter or is immediately followed by a; it contributes
zero when immediately followed by b. These are precisely the final
letters of the b-runs. Summing proves (1). Redundant b's and arbitrary
initial a's are allowed; no shortestness assumption enters the proof.

Applying h to (2) gives sum_w p_w r_b(w)=0. Every term is nonnegative,
so no word containing b has positive weight. Such a word is always
singular, and a word without b is a permutation, because rank cannot
increase after the first b. This proves the stated support obstruction.

## Exact optimum for maximum support word length

Consider all nonnegative probability mixtures on actual words which
satisfy (2) and assign POSITIVE mass to at least one singular word.
Their minimum possible maximum support length is exactly

    n.                                                  (3)

The lower bound is (1). For the upper bound use the n words

    w_k=b a^k, k=0,...,n-1,     p_(w_k)=1/n.

For every starting state q, the n outputs (b(q)+k) mod n run through Q
once. In fact the entire matrix average is J/n, implying (2). All support
words are singular and their largest cost is n. The support semigroup
is strongly connected and synchronizing. Strong connectivity follows
already from b and b a: repeatedly applying b a follows0,1,...,n-1,
and b sends n-1 back to0. The literal word

    (b a^(n-1))^(n-2) b

is reset and belongs to the support-generated semigroup; it costs
n(n-2)+1=(n-1)^2. After j copies of b a^(n-1), j>=1, the whole-Q
image is {0,...,n-j-2} union {n-1}; the final b completes the collapse.
At n=2 the repeated factor is empty and b already resets.

The optimum in (3) is a MAXIMUM support-cost statement. There is no
positive lower bound on EXPECTED cost under these weak assumptions:
mix an arbitrarily small positive amount of the displayed distribution
with the empty word. It stays stationary, and still has synchronizing
support. The cost is never silently charged as an expectation instead
of a worst-case original word.

## Relation to the existing route

The earlier PERMUTATION_AVERAGING_WORD_COST_AUDIT.md excludes cheap
simultaneous J/n averages using permutation-only words in a different
adjacent-transposition family, with an exact quadratic expected cost.
It explicitly left singular support and weak stationarity outside scope.
The present theorem attacks that weaker alternative on Cerny's binary
family, allowing ALL original words; it has the distinct sharp lower
bound n for maximum support cost. It is not a claim of quadratic cost
for weak stationarity or a refutation of every averaging argument.

The general method is attributed to
[Steinberg, The averaging trick and the Cerny conjecture, Lemma2](https://arxiv.org/pdf/0910.0410).
His two-factor distributions and their support costs must remain intact.
This obstruction does NOT contradict that lemma: its hypotheses and
total support bounds are different. Nor does it refute an average on a
proper invariant subspace or a subset-specific construction. For the
present a-cycle, however, a letter-invariant column space containing
any singleton already contains every singleton under powers of a and
is the full space. Such a space cannot bypass (1) by projection.

Finite controls check all literal words at n2..16, pair suffixes, exact
stationary attainment at retained larger sizes, and literal common reset
words with actual intermediate images. They are separate from the
all-n proof and do not formally verify it. Any new global square approach
must still account for compatibility, singular support, and actual costs;
one must not substitute this obstruction for a positive general theorem.

## A positive projected-stationarity statement, with its hypotheses paid

**PROVED (paper, a dimension-refined reconstruction of the averaging
lemma):** let A be strongly connected and synchronizing. Suppose a column
space W of dimension d contains1_Q and e_q, is invariant under EVERY
original letter, and some strictly positive probability on ALL original
letters defines P satisfying

    [Q] P x = [Q] x for EVERY x in W.                    (4)

Then there is one actual reset word ending at q with length at most

    (n-1)(d-1).                                         (5)

For a proper nonempty Boolean S in W, put x=chi_S-(|S|/n)1_Q. This
nonzero vector lies in W intersect ker[Q], of dimension d-1. The orbit
span chain starting at x cannot stay in that hyperplane forever: a reset
word ending in S, which exists by strong connectivity, has positive
[Q] M_w x. Before escape the chain grows at every layer, so some word
of length<=d-1 gives nonzero [Q] M_w x. Invariance and (4) give
[Q]P^j x=0 for every j. Average P^j over j0..d-1. Strictly positive
letter probabilities assign positive mass to EVERY word through d-1,
and the mean of that functional is0. Its nonconstant values must include
a positive one. Thus an actual word of length<=d-1 strictly increases
|S| under full inverse image. The new indicator stays in W. Starting
from e_q and repeating at most n-1 times reaches Q. Prepending these
actual extension words constructs one common reset, with every letter
charged; this proves (5). At n1 the word is empty.

The proof fails if W is merely the span of ONE history but is not
letter-invariant, if the probabilities omit required original letters,
or if stationarity is imposed only on a few tested vectors without a
spanning/invariance certificate. No universal W,P satisfying these
hypotheses is asserted. The obstruction (1) excludes a full-space
strictly positive original-letter P already in Cerny's family.

Projected stationarity is actually weaker than full pseudo-Eulerian
stationarity. A five-state example with three ORIGINAL letters is

    f=[4,0,4,0,0], g=[1,2,2,1,4], h=[1,3,3,1,0].

Take alpha=(1,1,-1,-1,0), W=ker alpha, q4, d4. Every alpha M_letter=0,
so W is invariant. The equal-weight average has
[Q]P-[Q]=alpha/3 and therefore satisfies (4). The DFA is SC; f g f
resets it in3 steps. Each one- or two-letter word has rank>=2, so rt=3
exactly. No nonnegative probability on the ORIGINAL letters can make
the full matrix doubly stochastic: columns2 and3 force weights of g,h
to each equal1/2, leaving f weight0, but then column4 sums only1/2.
This small example distinguishes the hypotheses, not a new asymptotic
class result. The finite checker verifies every Boolean S in W and
actual inverse-extension witnesses. The general existence problem for
suitable invariant W and paid P remains **OPEN**.
