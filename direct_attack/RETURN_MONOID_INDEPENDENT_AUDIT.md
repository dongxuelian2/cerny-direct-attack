# Independent return-monoid audit and local-rank continuation

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-10-01. Audited the paper statements and their two implementations
at the supplied checkpoint `c05a8c49b286bb5cc8c6a5ff468a9636052c89fa`.
No audited claim below was refuted. This report, its separate checker, and
its separate JSON are the only files added by this audit. Existing ledgers,
reproduction lists, historical captures, and the frozen baseline were not
edited by this agent. No Git commit was made.

**PROVED (paper)** below means a complete mathematical argument is supplied.
**COMPUTATIONALLY VERIFIED** means only the exact bounded scopes in section 7.
No **FORMALLY VERIFIED** claim is made. Publication priority is **OPEN**.
The unrestricted Cerny conjecture, general quotient hereditariness, and
universal linear image-extension bounds remain **OPEN**.

## 1. Adversarial audit of the existing return statements

### Actual first returns and the full monoid

For an equal-size congruence and strongly connected bijective-edge graph J,
choose shortest J-paths p_D:C->D and r_D:D->C, with empty paths at C.
A shortest p_D has no internal visit to C, and a shortest r_D has no
internal visit to C. Thus every `p_D a r_(Da)` is a genuine first return:
if Da=C, the a-step is the final return; otherwise the suffix first enters
C at its end. This also covers D=C and an immediate return letter. Every
nonempty `p_D r_D` is likewise a genuine first return. All lengths are
at most 2m-1; the latter loops have length at most 2m-2.

Composition must be read in the repository's right-action convention.
Let `f_(D,a)=p_D a p_(Da)^(-1)` as an abstract coordinate transformation.
The actual generator is `g_(D,a)=f_(D,a) ell_(Da)`, where
`ell_E=p_E r_E` is an actual permutation return. Its inverse is in the
generated finite transformation monoid: if its order is t, its inverse
is its `(t-1)`st power. Therefore every f_(D,a) belongs to that monoid.
The f's telescope along any quotient path beginning and ending at C.
Conversely, every generator is an actual C-return. This proves the claimed
monoid equality, including the identity, without synchronization or base
strong connectivity assumptions.

The inverse argument is exclusively a membership argument. It cannot be
used to shorten original words. An explicit obstruction is the unary
automaton on two h-fibers in which a maps the first fiber identically to
the second and maps the second back with the h-cycle. Then J is strongly
connected, `ell=a^2` has order h, and its inverse has shortest original
return length exactly `2(h-1)`. This can exceed 2m-1 arbitrarily far.
Section 7 independently checks h=3,...,12. The unary example need not
synchronize, because the membership theorem makes no such assumption.

The statement that the generated alphabet synchronizes iff C is resettable
in A also holds: a word resetting C to a singleton in a different class
can be followed by a J-path back to C. That routing is used only for the
equivalence, not supplied as a free word in any length bound.

### Sharpness and the equal-two-class boundary

In the R,L,c sharp family, any singular C_0-return must first reach class
m-1, use R there, and then reach class zero again. The necessary lengths
are m-1, one, and m-1, even if identity loops are inserted. The first
singular return is consequently at length 2m-1. At that cutoff, the only
nontrivial short return actions are the cycle c and the unit collapse
`(h-1)->0`. Their macro reset threshold is the usual `(h-1)^2`; this is
a macro statement, and the original costs are unequal. The explicit
full-Q word displayed in the existing paper indeed resets. No exact
original threshold is implied.

For the nonbijective two-class family, put h=2t+1 and B={0,t}. The two
points of B+s have different x-colors for 0<=s<=2t-1: in the first half
their colors are 0,t, and in the second half they are t,0. At s=2t the
points are 2t,t-1, both with color zero. First returns through length h
are identity or x followed by those first h-1 shifts. Their rank-two
images remain in the same pair family after any further short return.
Therefore no product synchronizes. At length h+1 the exceptional pair
appears and ab merges it. The full-Q reset `b a^h b a` is valid.
The failure concerns the return cutoff, rather than the original reset
threshold or Cerny. It shows that removing bijective connectivity cannot
leave a cutoff depending only on m.

### General short returns and the quotient lift

For a congruence class C and d outside states, the row exit-span chain
stabilizes by outside depth d-1. Restrictions to the outside kill a
trajectory after a return. The congruence condition ensures every
surviving product is an actual first return, because an entire class
returns together. Hence all first-return outputs of each row lie in the
span of the outputs of actual returns of length at most d+1.

Applying this fact to each row of the short-return orbit span establishes
invariance under every return. Base strong connectivity and synchronization
then supply all reset singletons in C. The stationary-span argument is
sound: stationarity with positive letter weights makes the support of a
stationary row invariant under every letter; full orbit span forces full
support. Uniform averaging of words of lengths 0 through h-1 then supplies
strict inverse expansion for every proper subset. Strictly increasing
stationary mass on a finite set of subsets must terminate at C.

The matrix-basis algorithm truncates exit products at original exit length
d. It does not assume the h-by-d matrix space stabilizes after d-1 rounds.
The code's `range(1,len(O)+1)` and its depth guard implement that truncation.
Choosing an actual matrix basis preserves orbit spans, not transition
monoids. The stated h^2 basis bound is safe; the elementary row-sum
constraints would also give the optional sharper bound h^2-h+1.

The nonsplitting-set interpretation and its canonical membership
congruence are valid. An arbitrary reachable image cannot be substituted
for a class. The C_3 example gives the advertised failure even for
all-length first returns.

Both quotient lifts correctly pay the quotient reset and class routing
once. A macro square requires a square bound for the smaller h-state
return automaton; quotient square alone is insufficient for arbitrary h.
State minimality supplies the smaller-state hypotheses in the
minimal-counterexample deductions, with no circular n-state assumption.

### Permutation transitivity

Every permutation letter's inverse is a positive power of that same
letter, so it also preserves the congruence. Hence a permutation sends
an entire class bijectively onto an entire class, not merely into it.
Class transitivity forces equal sizes and strong connectivity of J.
State transitivity implies class transitivity for every congruence.
Thus the stated exclusion and the conclusion that a state-minimal
counterexample with a state-transitive permutation subgroup is simple
are valid. Group primitivity does not follow: a block system of the
permutation subgroup need not be preserved by other letters.

## 2. Exact confined monoids for every bijective-edge SCC

**PROVED (paper).** Let theta be any congruence, potentially nonuniform,
and let K be a strongly connected component of its bijective-edge graph.
Its k classes have a common size h, since each bijective edge preserves
size. Fix C in K. A K-confined C-return is an original word whose quotient
path starts and ends at C and never leaves K. Define p_D and r_D as
shortest J-paths within K. Form the actual return alphabet

    p_D a r_(Da)      for D in K and Da in K,
    p_D r_D           for D in K\{C}.

There are at most k|Sigma|+k-1 generators, all genuine first returns, all
of length at most 2k-1. Their monoid is EXACTLY the restrictions to C of
all K-confined C-returns, including identity. The alphabet may be empty
at an isolated one-class SCC; then both monoids are the identity monoid.

Proof: use exactly the coordinate construction in section 1, but only for
edges with both endpoints in K. The loops ell_E have positive-power
inverses in the generated monoid. The coordinate maps telescope on every
K-confined quotient path. Every generator itself stays in K, proving the
reverse inclusion. This proof does not use any properties of outside
classes or an actual inverse letter.

If this confined monoid synchronizes, a quotient reset u ending at T,
followed by a quotient path from T to C, and then a macro reset gives

    rt(A) <= |u|+dist_quotient(T,C)+(2k-1)H(h).

Here A must synchronize, the quotient must allow the route, and H(h)
must be a proved reset bound for arbitrary h-state DFAs. For a uniform
congruence, k<=m, so the existing strict square comparison applies with
the larger coefficient 2m-1. Consequently a state-minimal counterexample
with a uniform congruence has a NONSYNCHRONIZING confined return monoid
in EVERY bijective-edge SCC. Requiring only that J is not strongly
connected is a weaker necessary condition.

This statement does not claim that an SCC's confined monoid equals its
all-length return monoid when returns leave K. The nonbijective boundary
is an explicit obstruction to that replacement. Nor does global
synchronization imply synchronization within some SCC.

## 3. A general charged local-word/profile lift

**PROVED (paper).** Let A synchronize and let its congruence quotient
be strongly connected, with class sizes s_1,...,s_m. The base DFA need
not itself be strongly connected. Let u reset the quotient to T, let D
be ANY class, and let v be ANY actual word, of original length L, whose
restriction to D has rank r. Define

    Phi_r(s_1,...,s_m)
      = sum_i sum_(k=2)^min(r,s_i) binom(s_i-k+2,2).

Then

    rt(A) <= |u|+dist_quotient(T,D)+L+Phi_r(s_1,...,s_m).   (A)

Proof of the compression ingredient: for a shortest word compressing a
k-set within a congruence class, all preterminal images S_i are k-sets
inside classes. Pull back a final merged pair along each injective
prefix to P_i subset S_i. If P_i were contained in an earlier S_j,
that earlier prefix followed by the suffix beginning at S_i would
compress sooner. Within a size-s class the standard Frankl renewing
sequence theorem bounds this subsequence by binom(s-k+2,2). Sum over
classes of size at least k. A synchronizing A guarantees compressibility
of every such set, so these bounds apply at each actual remaining rank.

Now u followed by the quotient route sends Q into D. Applying v sends
that image to rank at most r within one class. Compress at each rank
k=r,r-1,...,2, skipping ranks that do not occur. The displayed positive
rank budgets sum to Phi_r, proving (A). All routing, v, and compression
words are charged original words. No return condition is imposed on v.

If the quotient satisfies the square, coarsening only its reset and route
costs gives

    rt(A) <= m(m-1)+L+Phi_r.                              (B)

Thus in a state-minimal counterexample every actual local rank-r word
must satisfy the necessary condition

    L > (n-1)^2-m(m-1)-Phi_r.                            (C)

This is useful only when its right side is nonnegative; no unconditional
quadratic bound follows for arbitrary ranks or profiles.

## 4. All-n exclusion of low class-restriction rank

**PROVED (paper).** Let A synchronize and its quotient be strongly
connected. Suppose its congruence is uniform with m>=2 classes of size
h>=2, and the quotient satisfies the square. If ANY letter has
a singular restriction of rank r<=2m+1 on ANY class, then

    rt(A) <= m(m-1)+1
             +m[binom(h+1,3)-binom(h-r+2,3)] < (mh-1)^2. (D)

The graph J can be disconnected. The restriction rank is measured on
one h-class, and is not the letter's rank on the full mh-state DFA.

The non-strict bound is (B) with L=1 and the telescoping binomial sum.
It remains to prove strictness for all integers m,h. The budget increases
with r. If h<=2m+2, use r<=h-1; its maximum is
`(m-1)^2+m binom(h+1,3)`. Its square gap equals

    m(h-1)[(h+1)(6m-h)-12]/6.

For 2<=h<=2m+2, the concave product `(h+1)(6m-h)` is bounded below
by the smaller of its two endpoint values, `18m-6` and
`8m^2+8m-6`. Both exceed 12 for m>=2. The gap is strictly positive.

If h>=2m+2, use r<=2m+1. Direct summation gives

    sum_(k=2)^(2m+1) binom(h-k+2,2)
       =m h^2-2m^2 h+m(4m^2-1)/3.

The square gap in (D) at this maximal r is

    2m(m^2-1)h+m-(4m^4+2m^2)/3.

It increases with h. At h=2m+2 it is
`m(8m^3+12m^2-14m-9)/3`, strictly positive for m>=2. This proves
(D) for every size, with no finite size assumption.

In particular, EVERY singular letter restriction in a state-minimal
counterexample with a uniform congruence must have rank at least
2m+2. This adds a local-rank barrier to the existing h>=6m restriction
and the SCC conditions. For m=2 it prohibits all singular ranks 1,...,5
on either class, regardless of how large h is. Equation (C) is the
stronger length-sensitive constraint for actual words, including those
that leave and revisit a bijective-edge SCC.

The counterexample corollary uses the complete strong-connectivity
reduction in MINIMAL_COUNTEREXAMPLE.md: state minimality forces the base
DFA to be strongly connected, so every quotient is strongly connected.
A square quotient without the routing hypothesis is not sufficient for
the arbitrary-source-class theorem.

This rank barrier covers alphabets whose full-DFA letters have large
rank. In the equal-two-class boundary family, both letters have full
rank h, but a has rank two on C; J is disconnected and (D) still applies.
For example h=13 gives n=26 and full letter ranks 13, despite local rank
two. The saved boundary controls explicitly check this distinction.

The threshold 2m+1 is the largest FIXED r for which this unsaved Frankl
budget can give an all-h exclusion. At r=2m+2 its h^2 coefficient is
`m(r-1)/2=m^2+m/2`, exceeding the square's m^2 coefficient. The saved
large-h controls show this budget failure. This is a limitation of the
bound; it is not a realizable automaton counterexample and does not
refute a stronger theorem using several terminal kernels or actual
trajectory restrictions.

## 5. All nonuniform profiles: local rank at most three lifts the square

**PROVED (paper).** Let A synchronize, let its quotient be strongly
connected, and let theta be ANY nontrivial congruence, with m classes
of positive sizes s_1,...,s_m and `2<=m<n`. Assume the quotient satisfies
the square. If a word v of original length L has rank at most three on
ANY class, then

    rt(A) <= m(m-1)+L+Phi_3
          = sum_i s_i^2-2n+m^2+L.                         (E)

In particular a LETTER of class-restriction rank at most three gives
`rt(A)<=(n-1)^2`. The displayed budget is strictly below the square
except possibly for the profile (1,2), where equality suffices to
exclude a counterexample. Neither uniform class sizes nor bijective
connectivity is assumed.

Proof. The identity

    Phi_3(s_1,...,s_m)=sum_i(s_i-1)^2

holds also for singleton classes: s=1 contributes zero, s=2 contributes
`binom(2,2)=1`, and s>=3 contributes
`binom(s,2)+binom(s-1,2)=(s-1)^2`. Formula (E) follows from (B) and
`Phi_r<=Phi_3` for r<=3. Its gap below the square is

    K+1-L, where K=n^2-sum_i s_i^2-m^2.                  (F)

If all s_i>=2, then

    K=2 sum_(i<j) s_i s_j-m^2
       >=4m(m-1)-m^2=m(3m-4)>0.

For arbitrary positive class sizes, put s_i=1+x_i, with x_i>=0 and
sum_i x_i=t=n-m>=1. Since `sum_i x_i^2<=t^2`,

    sum_i s_i^2=m+2t+sum_i x_i^2 <= m+2t+t^2,
    K >= 2t(m-1)-m >= m-2 >= 0.

Thus L=1 always gives a nonnegative square gap. It can vanish only
when m=2,t=1, hence for the profile (1,2). All other nontrivial profiles
give a positive gap. This proves the letter conclusion without relying
on a separately established singleton-class exclusion. The routing
hypothesis remains necessary; quotient square alone does not provide
a path to an arbitrary source class.

For a state-minimal counterexample, base strong connectivity supplies
the routing, and state minimality supplies the square for its smaller
quotient. Consequently EVERY letter restriction on EVERY class of
EVERY nontrivial congruence has rank at least four. This includes
nonsingular restrictions on small classes: no class of size at most
three can occur. More strongly, EVERY actual word of local rank at
most three must satisfy

    L > n^2-sum_i s_i^2-m^2+1 = K+1.                    (G)

These ranks concern one class, not the full DFA. The rank-two/rank-one
specializations of (C) may give still stronger length constraints.
The identity congruence m=n and the universal congruence m=1 are excluded
from this theorem; their substitution would invalidate the profile-gap
argument or the smaller-quotient interpretation.

### A family separating local rank three from whole-letter rank three

For h>=4 and j>=1 put t=jh+1. Use classes C={0,...,h-1} and O indexed
0,...,t-1. Let a send local states 0 and 1 of C to indices 0 and 1 of O,
and all other states of C to index h of O; let a cycle O. Let b fix C
and map index q of O to q mod h in C. Both letters have full-DFA ranks
t and h, respectively, while a has rank THREE on C. The base DFA is
SC: O cycles, b reaches every C-state, and every C-state exits under a.
The graph J has two isolated one-class SCCs.

The literal word `b a^t b a b` resets Q. The initial b sends Q onto C.
After a^t the three O-indices are `{t-1,0,h-1}`; b maps them to
`{0,h-1}`, a maps those to O-indices `{0,h}`, and b merges them at zero.
Its length is t+4; no exact reset threshold is claimed.

This family makes the scope difference explicit: neither full-DFA
letter has rank at most three. For h=13,t=27, n=40, full letter ranks
are 27 and 13, while (E) with L=1 gives 823<1521. The twelve saved
controls use h in {4,7,13,21} and j in {1,2,3}; their full transitions,
literal resets, local ranks, SC properties, and disconnected J are
checked separately. The family illustrates the theorem; it is not
claimed to attain its reset bound.

## 6. Proof limitations and attribution

The new consequences use the existing class-sensitive Frankl mechanism
and the elementary finite-semigroup coordinate argument. Exact priority
is not established. The current primary-source records checked for
context are [Rodaro--Venturi, arXiv:2509.17992v2](https://arxiv.org/abs/2509.17992)
and [Berlinkov--Szykula, arXiv:1412.8363v3](https://arxiv.org/abs/1412.8363).
The former describes the general hereditary lifting problem as open;
the latter explicitly studies low-rank-word reset bounds. These facts
support the context, not a novelty claim for (A)--(G).

There is no general theorem that every synchronizing uniform congruence
has a synchronizing bijective SCC. There is no claim that every singular
letter has small LOCAL rank. In particular, near-permutation restrictions
can obey the new rank barrier. Neither the SCC nor local-rank mechanisms
reach simple automata. For nonuniform local ranks above three, the exact
profile bound (A) remains available without an alleged clean all-profile
rank threshold.

## 7. Bounded independent verification

New files:

* `check_return_monoid_independent_audit.py`: ordinary tuples and subset
  BFS; imports none of the existing generators or checkers.
* `data/return_monoid_independent_audit.json`: exact saved controls and
  scope/count report.

Reproduction from this repository, with the supplied Python runtime:

    python direct_attack/check_return_monoid_independent_audit.py

Completed scopes, **COMPUTATIONALLY VERIFIED**:

* Complete fixed-labeled 2+2 congruence cover: all 64 allowed letters and
  all 4096 ordered binary alphabets. Of these 2592 synchronize; 1440
  synchronize with a strongly connected quotient; 568 are SC and
  synchronizing as base DFAs. There are 784 with strongly connected J.
* 1568 original full-return/gauge monoid comparisons on that cover,
  containing 4892 monoid elements. All generator words are independently
  checked to be genuine first returns and to obey the charged cutoff.
* 8192 SCC-confined monoid comparisons, containing 17116 monoid elements.
  The 2k-1 alphabet, the gauge alphabet, and the full confined return
  monoid agree at each designated root, including isolated SCCs.
* 1136 short-return synchronization checks for the SC synchronizing
  base inputs at cap n-h+1=3.
* 86400 exact actual-word lifts of lengths 1 through 4 on the uniform
  cover. The original reset suffix and its literal whole-Q action are
  independently checked against (A), without free inverse operations.
* Complete fixed-labeled binary covers of profiles (2,1) and (3,1):
  12769 inputs total, including 706 synchronizing SC-quotient inputs.
  Their 8472 actual-word lifts of lengths 1 and 2 satisfy the nonuniform
  profile formula. No larger nonuniform cover is asserted.
* 24 sharp controls, h=2,...,7 and m=2,...,5, and nine nonbijective
  controls, odd h=3,...,19. Exact macro subset BFS checks the sharp
  thresholds and the full reset words; all base SC claims are checked.
* Ten unary inverse-cost controls, h=3,...,12.
* 171071 exact arithmetic triples with 2<=m<=30, 2<=h<=200,
  `1<=r<=min(h-1,2m+1)`. The minimum square gap is six at (m,h,r)=(2,2,1).
  Another 396 exact polynomial-identity controls use 2<=m<=100. Nineteen
  r=2m+2 large-h budget failures are saved as METHOD controls only.
* Four deliberately corrupted fields, cutoff, macro threshold, full
  reset word, and transition row, are all rejected.
* 18546 nontrivial nondecreasing profiles with 2<=m<=6 and class sizes
  1,...,12 satisfy the rank-three identity and square gap; 12364 have
  no singleton. The sole zero-gap profile is (1,2). Six selected
  controls also check word-budget equality at L=K+1 and failure of that
  budget at L=K+2, including profiles (7,15), (1,1000), and twelve
  two-state classes. These boundary checks concern the bound, not an
  alleged automaton attaining it.
* Twelve nonuniform SC DFA controls, as specified in section 5, have
  local rank three and full-letter ranks at least four. Their original
  transition arrays and literal full-Q reset words are saved.
* Four additional corrupted profile fields, Phi_3, K, the word-length
  threshold, and a class size, are all rejected. The total corruption
  count in the two independent groups is eight.

The all-n conclusions follow from the proofs in sections 2--5, not from
these bounded counts. No expensive historical audit was rerun.
