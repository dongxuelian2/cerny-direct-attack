# Independent audit: exact uniform averaging pays quadratic word cost

Date: 2026-10-01. **PROVED (paper)** as an obstruction to a proposed
averaging method. The bounded checks below are **COMPUTATIONALLY VERIFIED**.
Publication priority is **OPEN**; no novelty or **FORMALLY VERIFIED** claim
is made. This does not prove or refute the unrestricted Cerny conjecture.

The current PERMUTATION_AVERAGING_WORD_COST.md is mathematically sound,
including its explicit adjacent-OUTPUT-value sorting and reversed-word
construction. The averaging support must use actual original permutation
letters. Group membership and abstract inverses never have zero cost.
The exact optimum proved here concerns EXPECTED cost; it does not determine
the optimum MAXIMUM support cost or a minimum refutation state size.

## 1. A precise lower bound for every nonnegative uniform average

On Q={0,...,n-1}, n>=2, take the adjacent transpositions tau_i swapping
i and i+1. They generate the transitive group S_n. For a right-action
word w define its displacement

    F(w)=sum_(q in Q) |qw-q|.

At each step exactly two original trajectories are at output positions
i and i+1. Right multiplication by tau_i moves each one unit. The triangle
inequality gives F(w)<=2|w|. This remains true for a nonshortest word,
including cancellation pairs; redundant original letters cannot lower cost.

Let nonnegative weights p_w give the exact row-transition-matrix average

    sum_w p_w M_w=J/n.

If normalization was not separately required, summing any matrix row
already forces sum_w p_w=1. Every q consequently has uniform final image,
so

    E F(w) = (1/n) sum_(q,r) |q-r|
           = (2/n) sum_(d=1)^(n-1) d(n-d)
           = (n^2-1)/3.

Thus EVERY such distribution satisfies

    E |w| >= (n^2-1)/6.                                (1)

The argument also covers countable support. An infinite expected cost
satisfies the inequality; if the expectation is finite, the same
nonnegative sums and termwise bound apply. No uniform distribution on
the whole group and no independence of different states is assumed.

The displacement is the established Spearman footrule statistic. The
relation of footrule to inversion distance is classical; see
[Diaconis--Graham, 1977](https://doi.org/10.1111/j.2517-6161.1977.tb01624.x).
The original-word inequality used above has been proved directly here.
This source supports the attribution, not a priority claim for this
particular averaging obstruction.

## 2. Exact attainment, with the right action checked

Take g_k(q)=q+k mod n, k=0,...,n-1. Its one-line row is
`[k,k+1,...,n-1,0,1,...,k-1]`. It has k(n-k) inversions and displacement
`2k(n-k)`.

Here is a literal positive-word algorithm valid with right actions.
For a nonidentity permutation row g, choose adjacent output values i,i+1
whose preimages satisfy `g^(-1)(i)>g^(-1)(i+1)`. Such an i exists because
the preimage list is a nonidentity permutation and therefore has an
adjacent descent. Right multiplication by tau_i swaps these VALUES.
Comparisons with every other value are unchanged, so the inversion count
falls by exactly one. Repeat until identity. If the sorting word is
`tau_(i_1)...tau_(i_L)`, the reverse sequence
`tau_(i_L)...tau_(i_1)` realizes g starting from identity, and has the
SAME actual cost L. Each inverse letter is literally itself; none is
removed or charged for free. In particular g_k has an actual word of
length k(n-k). Inequality F/2 also proves that no shorter word realizes it.

Choose those n words with weights 1/n, including the empty identity word.
For each q, the images g_k(q) run through Q exactly once, so the average
matrix is J/n. Their mean original cost is

    (1/n) sum_(k=0)^(n-1) k(n-k)=(n^2-1)/6.              (2)

Equations (1)--(2) prove the exact minimum expected cost. The cyclic
construction has maximum support cost floor(n^2/4); the lower bound on
every possible maximum support cost is only ceil((n^2-1)/6). These two
quantities are not asserted to be equal.

For n>=6, the expected optimum is greater than n-1, since the difference
is `(n-1)(n-5)/6`. Therefore exact uniform averaging supported entirely
on permutation words of original length at most n-1 is **REFUTED** for
every n>=6 in this family. No state-minimum statement is inferred for
other alphabets or from the inconclusive smaller cases.

## 3. An exact six-state separating functional

At n=6 use the coefficient matrix H_(q,r)=|q-r|. Every word of length
at most five has `sum_(q,r) H_(q,r) (M_w)_(q,r)=F(w)<=10`. Therefore
the same upper bound holds for every convex mixture of these matrices.
The proposed uniform average has functional value

    sum_(q,r) H_(q,r)/6 = 35/3 > 10.

This is an exact rational separation certificate, requiring no numerical
optimization. Independent whole-group BFS finds 169 distinct permutation
actions obtainable through five adjacent transpositions; their largest
F is ten. The cyclic-shift certificate has lengths `[0,5,8,9,8,5]`, mean
35/6, and exact matrix average J/6. The functional excludes every allowed
short-word mixture, including arbitrary repeated words and zero weights.

## 4. Strongly connected synchronizing embedding

Adjoin the singular unit letter e taking n-1 to zero and fixing other
states. Adjacent permutations already make the base state graph strongly
connected. An explicit literal full-Q reset word is

    product_(j=n-1,n-2,...,1) (tau_j tau_(j+1)...tau_(n-2) e),

where the permutation part is empty at j=n-1. Before its j-stage the
current image is `{0,...,j}`. The permutation part sends j to n-1 and
fixes every smaller live state; e then merges that point with zero.
The resulting image is `{0,...,j-1}`. The total original cost is
`n(n-1)/2`. This is an upper-bound witness, not an exact threshold claim.
The checker supplies separate literal transition-row validation through
n=32.

The averaging support remains permutation-only. A word containing e
cannot act as a permutation: its full-Q rank drops and subsequent letters
cannot restore it. Thus the lower bound applies also if "permutation
support" is interpreted semantically as words whose resulting actions
are permutations. Averages using singular actions, a uniform image for
only ONE starting state, signed linear combinations, target-dependent
transport, and weaker stationary averaging conditions are outside the
assertion. Those methods are not refuted here.

## 5. Independent bounded audit

New checker: `check_permutation_averaging_word_cost_audit.py`.
New data: `data/permutation_averaging_word_cost_audit.json`.
It imports none of the existing research solvers and uses exact integers
and rational arithmetic throughout.

Reproduction:

    python direct_attack/check_permutation_averaging_word_cost_audit.py

Default scopes, **COMPUTATIONALLY VERIFIED**:

* Complete adjacent-transposition permutation BFS for n=2,...,8:
  46232 group elements. For every element, BFS word distance equals
  inversion count and satisfies the displacement bound. Independently
  constructed reversed sorting words are literally checked, charging
  623482 original letters in aggregate.
* The exact short-word separating functional at n=6,7,8. There are
  respectively 169,602,2191 actions through n-1 letters, with maximum
  displacement 10,12,14 and uniform target values 35/3,16,21.
  At n<=5 this functional gives no refutation; no stronger claim is made.
* All cyclic-shift averages for n=2,...,64: 63 exact balanced averages,
  with 720720 literal original letters checked. Every row/column matrix
  entry of each unnormalized n-word sum is exactly one. A second ordinary
  transition-row evaluator agrees through n=12. Full words are retained
  for n<=12 and n in {16,24,32,48,64}; other sizes retain exact summaries.
* Thirty-one synchronizing embeddings, n=2,...,32, with literal whole-Q
  reset words and stage images checked. No reset threshold is claimed.
* Four deliberately corrupted fields are rejected: an original word,
  a matrix-sum entry, expected cost, and maximum-support lower bound.

The theorem for all n follows from sections 1--2; finite enumeration
does not establish its scope. No old or expensive historical pipeline
was rerun. Existing return-audit files, ledgers, and frozen baseline were
not edited by this audit. No Git commit was made.
