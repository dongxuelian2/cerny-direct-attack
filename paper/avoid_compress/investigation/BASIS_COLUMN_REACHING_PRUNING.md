# Prefix-column consequences of strong connectivity

This note supplies necessary conditions, not a new value of F. Its intended
application is the remaining equality flags at (n,s,r)=(13,9,1), target 12.
It does not assume two letters or require the initial subset to be reachable.

Let an n-state complete automaton be strongly connected and synchronizing.
Fix S of size s>=2, set m=n-s, and let c(S) be its shortest compression length.
For distinct p,q let d(p,q) be their shortest merging length.

## Reaching and cooccurrence

Every state q can be reached from some state of S in at most m letters:
take a shortest directed path from S to q. Its vertices after its initial
vertex are distinct and outside S, so there are at most n-s of them.

If p in Su implies q in Su for every word u of length at most m, then

    d(p,q) >= c(S)-m.

Indeed choose such a prefix reaching p. It also puts q in the image. If
that prefix has already compressed S, then c(S)<=m and the assertion is
immediate. Otherwise append a shortest merging word for p,q. The result
compresses S and has length at most m+d(p,q). This proves the inequality.
The implication hypothesis is a statement about actual images, not about
an arbitrarily chosen list of test subsets. Synchronization ensures the
finite distances used here exist; the reaching argument uses strong
connectivity. No optimality claim or priority claim is made for this lemma.

## Exact column identities of a full prefix span

Use right actions and the transformation matrix D_w defined in the paper.
The row x_w=chi_S D_w counts trajectories and has total s even after
collisions. Let V_i=span_R{x_w: |w|<=i}, and let R_0,...,R_t be any basis
consisting of actual prefix rows and spanning V_i, with i>=m.

* A zero column in every basis row would be zero throughout V_i. Reaching
  that state from S by a word of length at most m contradicts this. Hence
  every column occurs in at least one basis row.
* Equal distinct columns p,q throughout the basis are equal throughout
  V_i. Equal nonnegative trajectory counts imply simultaneous membership
  of p,q in every actual image through m. Thus d(p,q)>=c(S)-m.
* If column j is 1 in every basis row, then x_j=(sum_q x_q)/s throughout
  V_i, since every basis row has total s. Every actual prefix through m
  consequently contains j. For ANY q!=j choose a prefix reaching q;
  j is also present. The same argument gives d(j,q)>=c(S)-m. This is
  precisely the previously audited mandatory-core isolation lemma.

These deductions use only linear equalities. Columnwise inequalities on
basis rows do NOT extend to their real linear span. For example the
weight-two rows 1100,0110,0011 all satisfy p=>q for p=0,q=1, but their
linear combination 1100-0110+0011=1001 does not. Do not add implication
rules inferred only from basis inequalities.

## Letter-domain consequences at the remaining parameter

At (13,9,1) and ac(S,{3})=12, c(S)>=12 and m=4. Thus the equal-column
pairs and all pairs touching a constant-one column have merging distance
at least eight. Let G be any verified subgraph of P3 (pairs merging within
three letters). For every actual letter f:

1. An equal-column pair p,q has f(p)!=f(q) and {f(p),f(q)} not in G.
   Otherwise it merges in one letter, or in at most 1+3=4 letters.
2. For a constant-one column j and every other input q, the same conditions
   hold. Equivalently f(j) is distinct from all other input images and
   isolated in the induced G graph on the FULL output set Qf.

Therefore each equal-column class has an injective G-independent image,
and every constant-one column obeys full-output isolation. These are
necessary restrictions on EACH letter of an arbitrary finite alphabet.

A dynamic mandatory point in the existing P5 cover H can also be stripped:
it is P7-isolated, hence incident to no P5 edge. If the remaining cover
has size at most one, the previously proved compression-cover floor
excludes the branch. A program applying this additional rule must bind
and check that earlier floor proof independently; it is not implemented
merely by asserting that a cover looks small.

Apply column deductions only to a basis spanning the entire actual V_i,
not just independent safe rows. The audited equality-flag theorem gives
dim V_i=i+1 for i<=11. A complete staircase branch that establishes its
i+1 actual independent prefix rows and constrains all preceding row
images to the branch span meets this premise. No safety or characteristic
row assumption at depth 12 is made. All finite tests are controls of this
paper proof; they are not extrapolated to an all-parameter formula.
