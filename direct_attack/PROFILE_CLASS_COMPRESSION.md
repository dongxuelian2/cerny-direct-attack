# Sharp profile-sensitive compression of a minimum congruence class

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Continuation notice: TERMINAL_KERNEL_FRANKL.md strengthens the tail
bound at every rank, repairs the four nonuniform n22 gaps, and routes
a uniform quotient reset to a singular class. Thus all congruences
are excluded from a state-minimal counterexample at n<=22, and a
uniform profile must have h>=6m. The older bounds and arithmetic
gaps below document the original checkpoint, not the current boundary.

Date: 2026-09-30. **PROVED on paper**, for arbitrary finite alphabets and
all state sizes under the hypotheses below. Publication priority is
**OPEN**. No Lean or **FORMALLY VERIFIED** claim. The finite sample and
independent exact certificate checks are **COMPUTATIONALLY VERIFIED**
only in their stated scope.

This continues SHORT_RETURN_QUOTIENT_LIFT.md. It strengthens first
compression of a minimum class, rather than claiming a smaller cutoff
for a synchronizing first-return alphabet.

## Theorem

Let A be an n-state DFA with a congruence theta having m>=2 classes.
Assume its QUOTIENT is strongly connected. Let C be a smallest class,
of size h>=2, and assume C is compressible in A. The base DFA need not
be strongly connected or synchronizing. Define

    rho = max_D dist_(A/theta)(D,C),
    N = sum_D (|D|-h+1) = n-m(h-1).

Then

    c(C) <= N+rho <= n-m(h-2)-1.                         (1)

Both are bounds on literal original-letter word length. There is also
a singular word returning C into C of length at most N+2rho. At least
one singular FIRST-return word has length at most N+2rho, by factoring
this return at consecutive returns to C. This last statement supplies
one nonpermutation macro; it does not assert that the entire alphabet
below that smaller cutoff synchronizes.

If C is not a minimum class, a shortest quotient path to any smaller
class already gives c(C)<=m-1. Thus the difficult whole-class case is
precisely the minimum-class case of (1).

### Proof

Set g=[C]/h, the uniform stochastic row on C. For each class D, choose
a shortest quotient-state word r_D sending D into C; r_C is empty.
All these words have length at most rho. Put T=N+rho. Since every
class has at least h states, N>=m.

Suppose no word of length at most T compresses C. For each D, a
quotient-state path from C to D has length at most m-1. Concatenate
it with r_D. Its length is at most m-1+rho<T. The resulting h-set
must still have h states and lie in C, so it is all of C. In particular
the restriction of r_D to D surjects onto C.

Write C={c_1,...,c_h}. On rows x in R^n define h-1 forms supported
in D, one for each j<h:

    F_(D,j)(x) = sum_(p in D, p r_D=c_j) x_p
                 - (1/h) sum_(p in D) x_p.

Surjectivity of D r_D onto C makes these h-1 forms independent.
Different D have disjoint supports, so all m(h-1) forms together are
independent. Their common kernel K therefore has dimension N.

For ANY word w of length at most N, Cw lies in one congruence class D.
The word w r_D has length at most N+rho=T, so by the supposition it
maps C bijectively onto C. Consequently (g M_w) M_(r_D)=g.
Every form supported in D vanishes on g M_w; the forms supported in
other classes vanish because g M_w has no coordinates there. Therefore

    V_N = span{g M_w : |w|<=N} subset K.

Let V_i be these ascending orbit spans. Starting from dim(V_0)=1,
N strict increases would give dim(V_N)>=N+1, which is impossible.
Thus V_i=V_(i+1) at some i<N. Such an equality makes V_i invariant
under every letter matrix. Its span then contains every later orbit
row, all of which must lie in K.

Now use the assumption that C IS compressible: let z compress it,
with Cz contained in D. Appending r_D still leaves fewer than h
states, all in C. But its row g M_(z r_D) belongs to K and is
supported in C. The h-1 equations for C, together with total mass
one, require this row to be g, whose support is all h states. This
contradiction proves (1).

Appending the appropriate r_D to a compressing word from (1) proves
the N+2rho return claim. If every first-return factor were a permutation
of C, their composition would be a permutation of C, contradicting
its smaller rank. This proves the singular first-return corollary.

The proof uses a standard ascending-chain span argument, but includes
one independent family of h-1 balance equations for EVERY quotient
class. Its dimension budget is N, rather than the n-h outside-state
budget in the short-return theorem. It concerns the full initial class.

## Sharp infinite family, at every class size h>=2

Fix h>=2 and t=jh+1 with any integer j>=1. Let

    C={0,...,h-1}, O={h,...,h+t-1}, n=h+t,
    a(q)=h+q                     for q in C,
    a(h+k)=h+(k+1 mod t)         for 0<=k<t,
    b(q)=q                       for q in C,
    b(h+k)=k mod h               for 0<=k<t.

The partition C|O is a congruence, with h as its minimum size and
rho=1. The DFA is strongly connected: a cycles O, b reaches every
member of C, and a exits C into O.

Every first return is b or a^k b, k>=1. For k<=t-h+1 the h outside
trajectories are a contiguous nonwrapping window and b maps them
bijectively onto C. At k=t-h+2 the window wraps for the first time.
The induced colors are 2,3,...,h-1,0,0 (for h=2 they are 0,0), so
that return loses one state. Before it, every returning factor is a
permutation and a acts injectively on the outside trajectories. Hence

    c(C)=t-h+3=n-2h+3=N+rho.                           (2)

The DFA is synchronizing, not merely compressible. The short return
a^2 b is an h-cycle on C. Compose the first singular return a^(t-h+2)b
with (a^2 b)^(h-2) to obtain the map fixing 0,...,h-2 and sending h-1
to h-2. This adjacent collapse and the h-cycle are a conjugate of the
Cerny alphabet, hence reset C. Prepending b sends the whole Q into C.
For h=2 the h-2 exponent is zero and the singular return is constant.

Thus (1) is SHARP at infinitely many n, for every fixed h>=2,
already for binary SC synchronizing DFAs with two classes. The h=2
case includes the earlier n-h+1 sharp cutoff family. These examples
still have e(C)=1, since Qb=C; they do not refute a linear extension
bound.

## Counterexample-first computation and verification boundary

class_compression_pressure.py proposes 20000 deterministic adaptive
alphabets with injective class maps where sizes permit, over fourteen
fixed profiles. It retains 18 improving SC synchronizing inputs and
35 sharp-family controls (h=2..8, j=1..5). Of the proposals, 3588 are
SC synchronizing. This is a sample, not an exhaustive automaton cover.

check_class_compression_pressure.py uses a separate reverse-subset
distance computation and a separate forward quotient-distance BFS.
It verifies all 53 retained certificates, 30727 subset vertices,
literal compression/reset/routing words, all 35 equality cases, and
rejection of four deliberately corrupted fields. The generator and
checker are distinct implementations; neither replaces the proof.
The weaker theorem hypotheses (quotient SC and class compressibility)
are justified by the proof, not by claiming that the SC synchronizing
sample exhausts them.

Reproduce with:

    python -m direct_attack.class_compression_pressure --trials 20000 --seed 20261014 --out direct_attack/data/class_compression_pressure.json
    python -m direct_attack.check_class_compression_pressure

## A stronger all-profile minimal-counterexample reduction

Now assume A is SC synchronizing. Once the first word from (1) drops
the whole class below h, the fiber-Frankl bound from
SHORT_RETURN_QUOTIENT_LIFT.md applies at each remaining rank. With
J_(h-1)(s)=sum_(k=2)^(h-1) binom(s-k+2,2), this proves

    reset_A(C) <= N+rho+sum_D J_(h-1)(|D|).               (4)

There is a useful elementary refinement at the final pair step. Let
P=sum_D binom(|D|,2) be the number of pairs lying within classes,
and let K be the number of those pairs merged by at least one letter.
A shortest pair-compressing path cannot visit a pair of this terminal
kind before its last transition: at such a pair it could merge in
one step. The earlier pairs are distinct. Hence ANY synchronizable
pair inside a class compresses within P-K+1 steps.

In a synchronizing DFA K>=1. Also K>=s_max-h: follow a simple quotient
path from a largest class to a smallest one. On every decreasing-size
edge D->E, its letter collapses at least |D|-|E| pairs in D. Distinct
source classes have disjoint pairs, and the sum of positive size drops
on the path is at least s_max-h. With exactly two classes of sizes
(h,t), strong connectivity forces some letter to map the t-class
directly into the h-class. Writing t=qh+r, 0<=r<h, gives the stronger
balanced-fiber lower bound

    K >= K_0=max{1, r binom(q+1,2)+(h-r)binom(q,2)}.

For arbitrary profiles use K_0=max{1,s_max-h}. For h>=3, replacing the
rank-two term in (4) consequently proves

    reset_A(C) <= N+rho+sum_D J_(h-1)(|D|)-(K_0-1).      (5)

This terminal-pair count is a basic shortest-path refinement, not
a novelty claim. It is not applied at h=2, where (1) already resets C.
After quotient reset and routing, a square quotient gives the literal
reset upper bound

    m(m-1)+n-m(h-1)+(m-1)
        +sum_D J_(h-1)(|D|)-(K_0-1),    h>=3.            (6)

Take the minimum of (6), the short-return lift, and the old fiber
bound. The old two bounds already excluded every minimum-h=6 profile
except (6,14) and (6,15). Applying (4), WITHOUT needing a pair saving,
repairs exactly those two gaps:

    (6,14): rt<=337<361;  (6,15): rt<=388<400.

Thus in a STATE-MINIMAL Cerny counterexample every nontrivial
congruence has EVERY class of size at least SEVEN. This is an all-n
statement: for h=6,m>=4 the old minimum-n gap
35m^2-161m+126 is positive and increases with n; m=3 requires only
n=18..21 and m=2 only n=12..21, handled by the convex fiber sum and
the two repairs above. The use of the six-state square is supplied
by state minimality; (6) itself uses only the quotient square.

Combining this with the previous growing-size inequality gives the
stronger necessary condition on EVERY class:

    |D| >= max{7, ceil((3+sqrt(4n-3))/2)}.               (7)

It also excludes all nontrivial congruences at n<22 in a state-minimal
counterexample. After h<=6 is removed, n<=21 allows exactly twenty
two-class profiles with h>=7, plus (7,7,7). Applying (6) gives the
following maximum bounds over the two-class profiles at each n:

| n | maximum bound | square |
|---:|---:|---:|
| 14 | 115 | 169 |
| 15 | 141 | 196 |
| 16 | 171 | 225 |
| 17 | 206 | 256 |
| 18 | 246 | 289 |
| 19 | 291 | 324 |
| 20 | 341 | 361 |
| 21 | 397 | 400 |

The triple profile has bound 176<400. These are all the possible
profiles in that bounded range, not a claim that all automata with
n<22 satisfy Cerny. In particular simple automata are untouched.
At n=22 the combined bounds are still inconclusive for the two-class
profiles (7,15), (8,14), (9,13), (10,12), (11,11), with upper bounds
455,460,454,446,443 against the square 441. They are bound gaps, NOT
automata violating Cerny. Larger profiles remain open as well.

The independent checker verifies the two repaired bounds, 9900 h=6
integer cases, all twenty-one bounded profiles and the n22 arithmetic
gaps. The proof and profile convexity supply the all-n conclusion.

## Why a full class-reset bound remains a major problem

After the first drop, the current image is a proper subset of a class.
Returning it to C no longer forces the uniform row on ALL of C, so
the m(h-1) balance equations above cannot be reused at lower ranks.
The n=3 reachable-image counterexample in SHORT_RETURN_QUOTIENT_LIFT.md
already refutes treating those proper subsets as nonsplitting classes.
Neither (1) nor its equality family supplies a compatible global chain.

One stronger sufficient statement would be

    reset_A(C) <= (h-1)(n-1).                            (3)

This is **OPEN**, with no all-n proof or counterexample supplied here.
If (3) held for every minimum congruence class in every SC synchronizing
DFA, a square quotient would lift strictly for EVERY size profile:
after quotient reset and routing the total would be at most

    m(m-1)+(h-1)(n-1) < (n-1)^2,  n>=mh, h,m>=2.

Indeed the gap is (n-1)(n-h)-m(m-1), increasing for n>=mh, and at
n=mh it is h(m-1)(mh-1)-m(m-1)>0. Singleton classes are handled
directly by quotient reset and routing.

But (3) itself would already give a UNIVERSAL QUADRATIC reset bound.
For any SC synchronizing h-state DFA D, form A on Q(D)x{0,1}. Lift
every original letter diagonally, add a block swap preserving q,
and add a block collapse (q,i)->(q,0). This is SC synchronizing and
has two congruence classes of size h. A word resets Q(D)x{0} exactly
when deleting the two new letters gives a reset word of D: those
new letters never change q. Thus reset_A(Q(D)x{0})=rt(D).
Applying (3) with n=2h would give rt(D)<=(h-1)(2h-1).

This exact reduction is **PROVED**, while (3) stays **OPEN**. It
explains why improving the full class-reset cost cannot be treated
as a routine consequence of having solved its first compression.
No universal e(S)<=2n, universal linear extension constant, or
unrestricted Cerny square is established by this continuation.
