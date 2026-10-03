# Exact barrier to terminal-window and rankwise worst-case budgets

Date: 2026-10-01. **PROVED (paper)**. This is a reconstruction on
the classical Cerny family and an audit of the NEW terminal-window
method. No novelty or **FORMALLY VERIFIED** claim is made. The
unrestricted Cerny conjecture remains **OPEN**.

Let C_n have Q={0,...,n-1}, a:q->q+1 modulo n and b:n-1->0,
with b fixing all other states. Assume n>=2. For a pair P let
d(P) be its exact shortest merging length.

## 1. Exactly one pair at every distance

Put N=binom(n,2). For r=1,...,floor(n/2) set

    E_r={r-1,n-1},
    ell_r=n, except ell_(n/2)=n/2 when n is even,
    P_(r,j)=E_r a^(-j),  0<=j<ell_r.

These are the distinct a-orbits, classified by their shorter
circular separation r. They partition all unordered pairs. Exactly,

    d(P_(r,j))=(r-1)n+1+j.                              (1)

Here negative powers only specify states; the resetting words below
use positive a powers. To prove (1), assign the displayed value D
to each pair and zero to singletons. For j>0, a sends P_(r,j) to
P_(r,j-1), lowering D by one. For j=0, a sends it to the last
pair of its SAME orbit, so D(P)<=1+D(Pa) still holds.

Letter b fixes pairs not containing n-1. If it acts on E_r, then
r1 collapses and for r>=2 the result {0,r-1} is the last pair of
orbit r-1. Its value is (r-1)n, exactly one below D(E_r).
The only other n-1-containing pair in orbit r is {n-1-r,n-1},
at j=r. It is distinct from E_r unless r=n/2. Its b-image is
{0,n-1-r}. If r<floor(n/2), this is in orbit r+1 at j=r,
with larger D. The same is true for r=n/2-1 with n even.
If n=2r+1 and r is the last orbit, the b-image is the last pair
{0,r} of that SAME orbit, with value rn, again not smaller than
D(P)-1. Therefore

    D(P)<=1+D(Pa),  D(P)<=1+D(Pb)

for every pair. Telescoping along any merging word proves the lower
bound d(P)>=D(P). Conversely apply a^j b, then recursively merge
the last pair of orbit r-1; its length is j+1+(r-1)n. For r1
the pair collapses directly. This proves the upper bound and (1).

Consequently the exact pair distances are a permutation of
1,2,...,N. In particular the terminal graph F(b) of pairs merged
within b letters has

    |F(b)|=min(b,N).                                    (2)

## 2. Optimizing the new terminal-wedge window gives NO improvement

Use the trivial congruence with the single class Q. At rank k set
d=n-k+2 and T=binom(d,2), as in TERMINAL_KERNEL_FRANKL.md.
For any allowed general-position vectors and any b>=1, the span
rank tau(b) of the terminal-pair wedges is at most |F(b)|<=b.
Hence its guaranteed compression budget satisfies

    b+T-tau(b) >= T.

At b=1 there is exactly one terminal pair, whose wedge is nonzero
in general position; its rank is one. Therefore, for EVERY rank
2<=k<=n, even optimizing the window and the vector choice,

    min_(b>=1) [b+T-tau(b)] = T.                         (3)

Summing these independent rank budgets gives exactly

    sum_(k=2)^n binom(n-k+2,2)=binom(n+1,3).

This exceeds (n-1)^2 at EVERY n>=4. Indeed the difference is
(n-1)(n-2)(n-3)/6. The refinement can strengthen congruence-profile
bounds, but even its best window does not improve the ordinary
Frankl rankwise bound on C_n. This statement concerns the wedge
method, not every possible use of the whole terminal graph.

## 3. Even exact terminal graphs cannot rescue separate worst-rank sums

Define R_k=max{c(S):S is a reachable k-image of C_n}. Every nonempty
subset is reachable: the conjugate unit sending i to i+1 and fixing
the others is a^(n-1-i) b a^(i+1). For any target S, delete each
run of states in Q\S in circular order toward its succeeding state
in S. Every deleted state maps into a still-present successor, so
each unit reduces the image by one. Their product maps Q onto S.
These are existence words, not a claimed short reaching bound.

In fact the exact maximum has a closed form. Set g=floor(n/k),
e=n-gk and t=k-e. Then

    R_k = g(n-k+e+1) = g(n-t+1).                        (4a)

For k=2 this equals binom(n,2), already proved in section 1.
For k>=3, a set with minimum circular gap d<g has compression
at most dn<=(g-1)n, strictly below the displayed value. For a set
with minimum gap g, at most e of its k gaps can exceed g, so at
least t gaps equal g. Their starting labels x, in increasing
ordinary order, are separated by at least g. Thus their maximum
label is at least (t-1)g. From (1), the pair corresponding to a
gap starting at x has phase n-1-x, so its distance is gn-x.
All other pairs have separation at least g+1 and larger distance.
The set therefore compresses in at most gn-(t-1)g. Attain this
by the circular gap sequence consisting of t gaps of length g
followed by e gaps of length g+1, starting at zero. Its tight-gap
starts are exactly 0,g,...,(t-1)g, proving (4a).

The half-orbit ambiguity occurs only at k=2 and was handled above.
At e=0 the same expression is n(g-1)+g, so no extra exception
is needed. A set compresses exactly when some pair in it merges.
In particular

    R_k >= n(floor(n/k)-1)+1.                           (4)

Even before the asymptotic consequence, (4a) gives
R_k>=2(n-k)+1: at g=1 this is equality; at g>=2 the difference
is (g-1)[(g-2)k+2e+1]>0. At n>=4, k2 has g>=2, so

    sum_(k=2)^n R_k > sum_(k=2)^n [2(n-k)+1]
                   = (n-1)^2.                          (4b)

Thus separate rankwise worst-case budgets already exceed the square
at EVERY n>=4, not merely at an asymptotically large size.

Thus any method which proves separately valid budgets B_k for ALL
reachable k-images and then pays every rank must have

    sum_(k=2)^n B_k >= n sum_(k=1)^n floor(n/k)
                        -2n^2+2n-1
                     >= n^2(H_n-3)+2n-1.               (5)

The last inequality uses floor(n/k)>=n/k-1. H_n>=log(n+1), so
this is Omega(n^2 log n). Already for every n>=32, H_n>4,
and the lower bound exceeds the square. A finite check of smaller
n can sharpen that threshold, but is unnecessary for the all-n
barrier. Replacing the wedge allowance by exact graph sequence
capacities still gives valid all-image budgets and cannot evade (5).

This does NOT forbid a square proof using terminal information,
rank jumps or adaptive budgets. The obstruction is the sum of
independent worst phases; the equally spaced worst sets at different
ranks need not occur together in a shortest reset. A successful
general proof needs their compatibility or a different global invariant.

## Verification boundary

check_terminal_window_barrier.py independently recomputes original
pair-graph distances, verifies the entire Bellman/word certificate,
counts terminal layers and checks the rank sums. For small n it
enumerates ordinary reachable images and computes every R_k exactly.
The all-n conclusions (1)--(5) rest on the proofs above, not the
finite calculations. This is separate from the earlier circular
rank-area barrier: (3) tests the new optimized terminal-window bound;
(5) excludes EVERY independently valid worst-rank sum on actual C_n.
The exact formula (4a) and both barriers received an independent
adversarial derivation in TERMINAL_KERNEL_INDEPENDENT_AUDIT.md.
