# Independent adversarial audit of the terminal-kernel continuation

Date: 2026-10-01. Audited starting HEAD
`c05a8c49b286bb5cc8c6a5ff468a9636052c89fa` on
`research/cerny-direct-attack`. This audit changes no existing source or
ledger. Its own script, report, and finite data are confined to
`direct_attack/`. No historical expensive search was replayed.

**PROVED (paper audit):** the terminal-wedge bound, generic single-kernel
independence, complete-partite weak-saturation equality, conditional
uniform lift, and stated state-minimal-counterexample consequences have
valid arguments under their explicit hypotheses. I found no mathematical
counterexample or missing substantive step. **COMPUTATIONALLY VERIFIED**
below refers only to the separate finite tests and their stated scopes.
Publication priority is **OPEN**. No novelty, Lean, or **FORMALLY VERIFIED**
claim is made. The unrestricted Cerny conjecture remains **OPEN**.

## 1. A minor quantifier repair

The section-2 instruction to split a rank-at-most-t kernel into exactly
t nonempty subfibers requires `t<=s`. Its substantive application on a
decreasing-size quotient edge satisfies this automatically. For the
full written range `t>=k-1`, add the case `t>s`: then `q=0,u=s` in the
balanced-fiber formula, so `K_0(s,t)=0` and the claimed lower bound is
trivial without splitting. At `t=s` splitting into singletons works.
This is an exposition repair, not a refutation of the lower bound or any
downstream profile consequence. The root agent was informed before this
report was written.

The generic-vector argument should be understood over an infinite field,
for example the real numbers. An unrestricted finite field need not admit
arbitrarily many state vectors in the required general position. The
paper argument can choose real vectors, and its DFAs have no field
restriction.

## 2. Independent derivation of the terminal-wedge argument

Fix a shortest compression word of length L for a k-set S. Its images
before the last letter all have size k. Pull a pair merged by the last
letter back through the injective prefixes, obtaining P_i in S_i. If
`j<i` and `P_i subset S_j`, the prefix of length j followed by the suffix
after position i compresses S in `j+L-i<L` letters. Hence every later
witness pair avoids every earlier image, including earlier visits to
the same class separated by visits elsewhere.

For `L>b`, retain exactly `i=0,...,L-b-1`. If S_i contained a pair
merged by a word of length at most b, that word after the prefix would
compress S in at most `i+b<L` letters. Thus every retained image avoids
the entire short-terminal graph, not just a selected letter kernel.

In a class D of size s, put `d=s-k+2` and `B_i=D\S_i`. Wedge with the
`d-2` state vectors indexed by B_i, followed by a fixed volume form,
defines a functional on `wedge^2 R^d`. Its value on the wedge of P_i is
nonzero because the d involved vectors are independent. For `j<i`, P_i
meets B_j, making the jth functional zero on the ith pair wedge. The
resulting square evaluation matrix is triangular with nonzero diagonal,
so the functionals are independent. Each B_i hits every short-terminal
edge, so every functional annihilates that edge span. There are therefore
at most `binom(d,2)-tau_D(b)` retained indices in D. Summing over the
classes and charging the omitted b indices proves the displayed bound.
The case `L<=b` is immediate. No representation of the letter actions by
these vectors is used.

This also explains why b cannot be silently subtracted without its
charge, and why terminal pairs from several letters cannot have their
counts added without a union-rank calculation.

## 3. Generic independence and exact weak saturation

For one kernel partition into r fibers, give every fiber center e_0 and
give each remaining vertex its own `e_0+e_j`. Each center-leaf wedge has
a unique `e_0 wedge e_j` coordinate. After subtracting those coordinates,
each leaf-leaf wedge has a unique `e_i wedge e_j` coordinate belonging to
that fiber. This explicitly proves independence of all K kernel wedges
in dimension `1+s-r`, and hence in any larger dimension.

Take a K-minor nonzero at this configuration. It is a nonzero polynomial
in the vector entries. Each determinant requiring independence of a
d-subset is another nonzero polynomial. Their finite product is nonzero,
and consequently has a real point where all these conditions hold
simultaneously. This proves kernel independence together with general
position; it does not assume the displayed center configuration itself
has general position. For `r>=k-1`, the required dimension inequality is
`s-k+2>=s-r+1`.

For a rank at most t with `k-1<=t<=s`, split actual fibers until there
are t. Convexity of `binom(x,2)` makes the balanced sizes minimize the
total pair count. Those subfiber edges are still genuinely merged by
the letter. The preceding independence result applies with rank t.

For an arbitrary graph G, the exact translation
`M_k(G)=|E(G)|-wsat(G,K_k)` has the correct sequence orientation. Given
a renewing sequence, delete all its distinct witness edges. Restore them
in sequence order: later witnesses are absent from the current witness
clique, while earlier witnesses have already been restored. Each step
therefore completes a clique. Conversely, in a weak-saturation addition
sequence, the witness clique for an added edge cannot contain a future
missing edge, exactly the renewing condition. Both directions are needed
to get equality.

For a complete r-partite G with `r>=k`, coarsen its parts to k nonempty
groups, choose a base vertex per group, and start from the base clique
minus one edge. Give each nonbase vertex k-2 neighbors among the bases
outside its own coarse group. The initial edge count is

    binom(k,2)-1+(k-2)(s-k)
      =binom(s,2)-binom(s-k+2,2).

Restore the base edge, then each nonbase vertex's remaining base neighbor.
Restore all remaining edges between coarse groups using the other k-2
bases. Finally restore edges between original parts in the same coarse
group using any k-2 other coarse-group bases. Every stated witness is a
literal k-clique in the target graph. At k=2 the witness uses zero other
vertices, and the construction still works. This gives the attaining
weak-saturation bound. The wedge argument with the K independent
within-part edges gives the converse renewing bound, so

    M_k(G)=binom(s-k+2,2)-K.

Thus one cannot improve the one-kernel barrier by a sharper argument that
uses only the allowed set-pair sequences. A claim of DFA realizability of
the attaining sequence would require additional work and is not present.

## 4. Profile and uniform-lift quantifiers

On a simple quotient path from a largest class to a minimum h-class,
select kernels only at decreasing-size edges. Each source class is used
at most once. Since `binom(a,2)>=a-1` for `a>=1`, its balanced subfiber
kernel contributes at least the source-target size drop. The sum of all
positive drops is at least `s_max-h`. At every remaining rank `k<=h`,
all these classes have size at least k and all selected target sizes are
at least h, so the same savings apply. If all classes have equal size,
synchronization implies a singular class restriction somewhere: otherwise
every word would remain injective on each class. This supplies the one
terminal wedge needed for `K_*=max(1,s_max-h)`.

For exactly two classes, a shortest quotient path from the larger to the
smaller consists of a single letter. The direct balanced-kernel count is
therefore legitimate. For more classes this direct-letter assertion is
not used.

The full-class first-compression theorem also checks out independently.
Under its contradiction assumption, each return map r_D surjects D onto
C because a short C-to-D path followed by r_D maps the whole C bijectively
onto C. The h-1 balance forms on each D are independent: all h fibers are
nonempty, and evaluating a linear relation on the last fiber first forces
the sum of its coefficients to zero, then evaluation on the other fibers
forces each coefficient to zero. Supports in different D are disjoint.
The common kernel has dimension N. The orbit span through length N lies
there, so some ascending-span step must stabilize and make every later
orbit row lie there. A compressed C-return row has mass one but support
smaller than h; the balance equations on C require it to be uniform on
all of C, a contradiction. This uses quotient strong connectivity and C
compressibility, and does not need strong connectivity or synchronization
of the whole base DFA.

After this first drop, compression at each actually visited remaining
rank gives the stated tail sum. Skipped ranks can be omitted because every
displayed rank budget is at least one: it is b plus a sum of annihilator
dimensions. Formula (5) additionally assumes a square quotient and pays
both the quotient reset and its one subsequent route.

For a uniform profile, choose a class D carrying a singular restriction;
one exists by synchronization. Reset the quotient, route its endpoint to
D in at most m-1 letters, and pay one singular letter. All h-classes are
minimum classes, so this choice does not conflict with the first-drop
argument. The unrefined Frankl tails total
`m[binom(h+1,3)-1]`, including the empty h=2 tail. This gives

    rt(A)<=(m-1)^2+m binom(h+1,3).

The square gap is exactly
`m(h-1)[(h+1)(6m-h)-12]/6`. On the integer interval
`2<=h<=6m-1`, the concave factor `(h+1)(6m-h)` is minimized at an
endpoint. Its smaller endpoint is 6m, which is at least 12. Equality
requires exactly `(m,h)=(2,11)`. Hence a state-minimal counterexample
with a uniform congruence must have `h>=6m`; using `n=mh`, the stated
square-root equivalents follow. A quotient-square hypothesis suffices
for this uniform lift; the argument does not claim an unrestricted
n-only bound.

At `(2,11)`, the complete cost is literally
`1+1+1+2(220-1)=441`. Equality is sufficient to exclude a counterexample,
defined by reset threshold strictly greater than 441. It is not necessary
to prove strictness or assume two letter-merged pairs. If two distinct
letter-merged within-class pairs do exist, their wedges have total rank
at least two at each tail rank: within one class, proportional wedges
would put at least three general-position vectors in one plane, which
is impossible when `d>=3`; across classes ranks add. This validates the
optional 432 bound, without using it in the exclusion.

## 5. Historical class floor and the n<=22 inference

The inference starts with a hypothetical counterexample minimal in
number of states among all synchronizing finite-alphabet DFAs. Its proper
terminal strongly connected component would give a smaller reset problem;
the outside-state routing argument yields the square, so it must be
strongly connected. Its quotient is synchronizing and strongly connected,
and every smaller synchronizing return automaton satisfies the square by
state minimality. Thus both smaller-state assumptions used in the inherited
short-return lift are available. No induction on alphabet size is needed.

I checked the short-return orbit-span and stationary-distribution proof
used by that lift. Restricted excursions span by outside dimension d,
and the congruence ensures nonzero restricted products are actual first
returns. Invariance under short returns implies invariance under all
returns. The base's reset words ending at each member of C force every
stochastic row's return-orbit span to be all of `R^h`. A stationary row
must have positive support; otherwise its zero coordinates remain zero
under every macro word. Averaging the orbit rows then provides a strict
preimage mass increase for every proper subset, and finitely many subsets
force a reset. The resulting short-return alphabet is an actual smaller
synchronizing DFA, making its square use noncircular.

For `h=1`, quotient reset and routing to a singleton suffice. For
`h=2,3,4`, the inherited return-lift square gaps at `n=hm` are positive
for every `m>=2` and increase with n. For `h=5,m>=3` the same is true;
for `m=2,n>=14` it is strict, and the four profiles `(5,5)` through
`(5,8)` have explicit Frankl bounds 42,56,74,96 against squares
81,100,121,144.

For `h=6,m>=4`, the minimum-n gap is
`35m^2-161m+126`, positive at m=4 and increasing thereafter. Its n
increment is `2n-26>0` in that range. For m=3, the return lift is strict
from n=22 onward; for m=2 it is strict from n=22 onward. Only n=18..21
and n=12..21 respectively remain. The integer-convex Frankl sum is
maximized by concentrating all excess size in one class, so the finite
extreme profiles cover every profile in these ranges. The independent
arithmetic below verifies these cases using the old Frankl/return bounds
and the new first-drop bound; the two repaired old gaps are strict.
Consequently every class of every nontrivial congruence of a state-minimal
counterexample has size at least seven.

For n<=22 this leaves only two-class profiles with each size at least
seven, plus `(7,7,7)` at n=21 and `(7,7,8)` at n=22. There cannot be
four classes. Independent integer-profile enumeration covers every one
of these profiles. The new nonuniform n=22 bounds are 423,435,436,439
for `(7,15),(8,14),(9,13),(10,12)`; the triple bound is 202. The
uniform `(11,11)` profile has bound 441. Hence the precise conclusion
is that a state-minimal counterexample at n<=22 cannot have a nontrivial
congruence. It does not prove the square for all n<=22 DFAs and does not
touch simple automata.

## 6. Separate finite adversarial checks

The separate script `audit_terminal_kernel_independent.py` imports no
terminal checker or generator. Its output is
`data/terminal_kernel_independent_audit.json`.

- All 4,306 `(G,k)` instances for every labeled simple graph at n=2..5
  and `2<=k<=n` pass the duality equality. The sequence side uses a
  coverage dynamic program; the saturation side independently enumerates
  initial edge sets and computes clique-completion closure.
- All 2,984 applicable partition/k instances for n=2..7 pass literal
  edge-by-edge checks of the reconstructed complete-partite construction,
  its initial count, and the claimed attained sequence length.
- A deterministic sample of 1,050 congruence-respecting DFAs over the
  profiles `(2,2),(2,3),(3,3),(2,2,2),(3,4),(4,4),(7)` is checked with
  one to four letters. Synchronization is not assumed. Literal subset
  BFS identifies 24,147 compressible class subsets and checks 144,882
  inequalities for `b=1,2,3,4,5,6`. The wedge ranks use distinct
  Vandermonde state vectors and modular elimination, independently of
  the original checker. These are valid ranks with general position,
  not a claim to have maximized the generic ranks.
- Every integer size profile with minimum seven, at least two classes,
  and total n<=22 passes the corresponding conditional bound. Separate
  arithmetic checks cover the inherited h=6 finite boundary.
- 30,096 uniform `(m,h)` pairs with `2<=m<=100,2<=h<=6m-1` satisfy
  the exact gap formula, with `(2,11)` the sole equality. The paper
  concavity proof establishes the all-m statement beyond this finite scope.

Reproduction from the repository root:

    python -m direct_attack.audit_terminal_kernel_independent

The audit script uses only Python's standard library. In this session
the explicitly provided bundled Python executable was used. The first
sandboxed attempt completed its calculations but could not save the JSON;
the authorized escalated replay saved the result and exited successfully.
There was no mathematical assertion failure. No pre-existing ledger or
data file was modified by these checks.

## 7. What would constitute genuine additional progress

The exact complete-partite equality closes off a stronger conclusion
derived solely from one letter kernel and unrestricted renewing sequences.
A next general result must use either several short-terminal kernels
with their union rank correctly charged, or constraints of literal DFA
trajectories beyond arbitrary set-pair sequences. Varying b also must pay
its literal b charge and should be audited on the Cerny family before it
is presented as a route to a square bound. The current tail still takes
a separate worst compression budget at every rank; no compatibility
between minimizers at different ranks has been established.

A concrete necessary distinction is that an attaining weak-saturation
sequence only supplies abstract k-cliques and witness pairs. It supplies
neither letters implementing the consecutive set images nor suffixes
pulling every witness back to one final merged pair. A future bound using
those additional constraints would be stronger than the already sharp
one-kernel combinatorial barrier. This audit supplies no such theorem
and does not upgrade finite negative searches to universal claims.

## 8. Independent attack on the subsequent Cerny-family barrier

After the preceding audit, the root agent proposed a separate all-n
obstruction to window optimization and rankwise worst-case summation.
I derived its potential and token arguments independently, and found
both sound under the following precise scope. These are **PROVED (paper
audit)** barriers for the standard Cerny family and the specified bounding
methods; they are not new unrestricted DFA upper bounds.

Write `a(q)=q+1 mod n` and let b fix every state except `b(n-1)=0`.
For `1<=r<=floor(n/2)`, define

    P_(r,j)={r-1-j mod n, n-1-j mod n}.

Its a-orbit period is n, except that the even half-distance orbit has
period n/2. Taking `0<=j<period`, the potential is

    D(P_(r,j))=(r-1)n+1+j.

The pair at `j>0` goes under a to phase j-1, decreasing D by one.
At `j=0,r>1`, b sends the pair to orbit r-1, phase n-1, also decreasing
D by one; at r=1 it merges immediately. These give literal shortest-word
witnesses recursively. The a-transition at phase zero wraps to the last
phase and cannot improve the potential lower bound. Apart from phase
zero, the only b-active phase in a full orbit is j=r. When a further
distance orbit exists, b sends it to orbit r+1, phase r, increasing D
by n. In the final odd orbit it stays in the same orbit at phase n-1,
increasing D by r. In the even half orbit there is no second active
phase among its distinct representatives. All other b-transitions fix
the pair. Thus every letter satisfies `D(P)<=1+D(P letter)`, taking
merged pairs to have potential zero, and the recursive witnesses achieve
equality. The potential is exactly the pair distance.

The intervals of values of D partition `1,...,binom(n,2)`. Therefore
`|F_b|=min(b,binom(n,2))`. For every k and every valid vector choice,
`tau_b<=|F_b|<=b`, so

    b+binom(n-k+2,2)-tau_b >= binom(n-k+2,2).

At b=1 the single terminal pair has a nonzero wedge, giving equality.
Consequently optimizing b, even with the maximal generic wedge rank,
does not improve the ordinary Frankl rank budget anywhere in this family.
This conclusion includes the full rank k=n and the even half orbit;
neither is an omitted edge case.

For the stronger rankwise barrier, choose a k-set whose successive
circular gaps are all at least `g=floor(n/k)`, for instance
`S={floor(i*n/k):0<=i<k}`. Follow its labeled tokens until the first
collision. An effective unmerged b moves exactly one token forward by
one, while a moves all tokens equally. Cyclic order is preserved until
collision. The trailing token of the colliding initially adjacent pair
must therefore have at least g effective b-advances: its excess advances
over the leading token equal their initial gap. Between consecutive
effective b applications to that same token, at least n-1 a letters
are required, since b has just moved it from n-1 to zero and all other
b applications leave it fixed. Hence every compressing word has length
at least

    (g-1)(n-1)+g=n(g-1)+1.

All nonempty subsets are actual images: positive-word conjugates of b
give each cyclic adjacent unit `i->i+1`, and applying those units along
each gap outside a desired subset deletes the unwanted states into the
next desired state while fixing every desired state. Thus the spaced
sets above are included even if the budget is restricted to actual
images. Any bound that independently maximizes the compression cost at
every rank and then sums these maxima must be at least

    n sum_(k=2)^n [floor(n/k)-1]+(n-1)
      >=n^2 H_n-3n^2+3n-1
      =Omega(n^2 log n).

This is a method barrier. It does not say that a single reset trajectory
visits all the worst spaced sets, and it does not contradict the square
reset length of the Cerny family. Replacing the wedge rank by an exact
terminal-graph sequence capacity still cannot make such a universal
per-rank budget smaller than an actual subset's compression cost.

The independent script was extended and replayed after this derivation.
It verifies all 20,825 pair distances for n=2..50 against a separate
reverse pair BFS, all 2,035 actual images at n=2..10 by forward image
BFS, and 91 spaced-set lower bounds at n=2..14 by literal compression
BFS. These scopes and counts are recorded in the same audit JSON.
The all-n statements rely on the explicit potential and token proofs,
not on extrapolating those finite checks.

## 9. Independent audit of the exact rankwise maxima

The subsequent stronger root derivation is also valid. It gives an exact
formula at every rank, rather than merely the spaced-set lower bound.
Let

    R_k(C_n)=max_(|S|=k) c(S),
    g=floor(n/k), e=n-gk, m=k-e.

Then for `2<=k<=n`,

    R_k(C_n)=g(n-k+e+1)=g(n-m+1).                 (A)

For any k-set, let d be its smallest circular gap. An arc between selected
vertices is a sum of adjacent positive gaps. Thus the pairs of smallest
circular distance d are precisely the adjacent pairs with gap d. Larger
distances belong to later pair-distance intervals and cannot determine
the first compression. If x is the starting label of a gap d, its phase
is `j=n-1-x`, and its pair distance is `dn-x`. Consequently

    c(S)=dn-max{x : the forward circular gap at x equals d}.  (B)

For the even half-distance case, the two endpoints supply both possible
tight starting labels; taking their maximum automatically restricts the
phase to its distinct half-orbit range. Thus (B) handles that orientation
case as well.

Necessarily `d<=g`. If `d<g`, (B) gives `c(S)<=(g-1)n`. This is strictly
less than the proposed value because `g(m-1)<=g(k-1)<n`. When `d=g`,
the total surplus e over k gaps of size g allows at most e longer gaps.
There are at least m tight-gap starts. In increasing numeric label order
they are separated by at least g, so their largest label is at least
`(m-1)g`. Equation (B) gives the upper bound `gn-(m-1)g`, exactly (A).

For attainment, begin at state zero and use the circular gap vector
consisting of m copies of g followed by e copies of g+1. It sums to n
and has exactly k gaps. Its tight starts are
`0,g,...,(m-1)g`; every other gap is larger. Equation (B) achieves (A).
When e=0 this specializes to the equally spaced set and gives
`n(g-1)+g`. At k=2 the formula gives `binom(n,2)` in both parity cases;
one may equivalently establish that rank directly from the pair spectrum.

The comparison to the square budget is exact:

    R_k(C_n)-[2(n-k)+1]
      =(g-1)[(g-2)k+2e+1].

This is zero for g=1 and positive for g>=2. Summing `2(n-k)+1` over
`k=2,...,n` gives `(n-1)^2`. At n>=4 the pair rank has g>=2, so

    sum_(k=2)^n R_k(C_n)>(n-1)^2       for every n>=4.

Thus summing independent worst-case rank budgets already fails the
square on the Cerny family at every n>=4, even if those budgets are exact
compression times and all sets are required to be actual images. The
harmonic asymptotic barrier remains valid. This does not rule out a
trajectory-dependent argument that selects favorable successive images.

The separate script now enumerates every one of the 32,647 nonsingleton
subsets at n=2..14, using independently computed pair BFS distances.
It checks (B), all 91 exact rank maxima (A), the difference identity,
and the summed strict/equality cases. The JSON retains the complete
rank-sum table for that finite scope. All assertions passed on the saved
replay. The proof above establishes the all-n statement; the table alone
would not.
