# A three-state short-pair cover cannot collapse into an isolated point

This auxiliary statement is independent of alphabet size and initial
subset reachability. It gives no new numerical F value.

## Credited two-cover P4 consequence

In a synchronizing automaton on n>=4 states, a two-state cover of P4
forces |P1|<=2. If three distinct immediate pairs existed, they admit
a length-three Frankl--Pin sequence of (n-2)-sets. For a current pair
e_j omit an endpoint outside e_j from each later pair, then extend
these at most two omissions to exactly two points outside e_j.
This is possible since n>=4. The resulting set T_j contains e_j
and omits at least one endpoint of every later pair. Hence each
later pair is not contained in any earlier set, as required.

The refinement of Kisielewicz--Kowalski--Szykula, CIAA2016,
Theorem1 bounds compression of every compressible (n-2)-set by
binomial(4,2)-3+1=4. The complement of the proposed cover has size
n-2>=2 and is compressible by synchronization, but contains no pair
merged within four letters. This is a contradiction. Strong connectivity
is unnecessary for this credited consequence. For n=3 the complement
is a singleton; the consequence must not be applied there.
The theorem and its convention for sequences/height are documented in
TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md; its primary reference is
https://doi.org/10.1007/978-3-319-40946-7_15.
No priority claim for the refinement or this consequence is made.

## Collapsed-cover obstruction

Let n>=4, synchronization, |P1|<=4, and let a three-state K cover P5.
There cannot be a letter f with f(K)={p} where p is isolated in P4.

The three K inputs give a triangle of immediate pairs. No other input
can join their kernel block: a four-state block would give six pairs,
contrary to |P1|<=4. There can be no other nontrivial block, because
it would give a pair entirely outside K, while K covers P1. Thus f
has exactly this three-state block and all other blocks are singletons.
Its rank is n-2, and its set M of omitted output states has size two.

LETTER_IMAGE_SHORT_PAIR_COVER.md applied at h=4 says f(K) union M
covers P4. Since p is isolated in P4, M itself is a two-state cover
of P4. The credited consequence above gives |P1|<=2, contradicting
the triangle already supplied by f. This proves the obstruction.
Missing outputs are essential; the proof does not assume a permutation
letter or rank-n-1 singular letters. |P1|<=4 is an explicit hypothesis,
not an extrapolated cap on P2,P3,P4.

## Application to equality at (13,9,1)

Suppose ac(S,{3})=12, |S|=9. Existing premises give c(S)>=12, a
cover H={0,1,2} of P5 and |P1|<=4. Every point mandatory through
depth4 is P7-isolated, by MANDATORY_CORE_ISOLATION.md, hence is
P4-isolated. The established first/second/third entrance suppliers
and their one-count depths therefore exclude:

* B=H: its supplier sends H into protected3 (mandatory through11).
  This excludes every B3-in joint, independently of C and D.
* B singleton and C=H: the second supplier sends H into B
  (mandatory through10). This excludes the whole b1_out_c6 joint.
* C singleton and D=H: the third supplier sends H into C
  (mandatory through9). This excludes that whole third geometry,
  while other D geometries in its joint remain unproved.

Incomparability places these singleton targets outside H. All finite
alphabets, all Boolean companion fibers, and simultaneous suppliers
are covered. Initial reachability is unnecessary for the obstruction;
the paper's stronger requirements on any attaining example remain.

## Audit scope

The checker literally tests ordered three-pair sequences on n4..9,
all n4..6 transformations for the covered collapsed-block reduction,
and every ordered labelled binary alphabet on n4 for the two-cover
P4 consequence and collapsed-cover impossibility. A strongly connected
synchronizing boundary without the target-isolation premise is retained.
These controls support the written uniform proof; they are not a
thirteen-state automaton scan. The application audit independently
checks every historical geometry, its labelled D orbit and its required
supplier/mandatory singleton against the immutable checkpoint17 state.
No all-parameter extremal formula or alphabet separation follows.
