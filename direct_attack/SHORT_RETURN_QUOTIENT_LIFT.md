# Short first returns, compression of a block, and a stronger quotient lift

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. **PROVED on paper**, for arbitrary finite alphabets and
arbitrary state sizes under the stated hypotheses. The exact publication
priority is **OPEN**. The stationary-span ingredient and the Frankl
renewing-sequence bound are known; no novelty claim is made for them.
There is no **FORMALLY VERIFIED** or Lean claim. Independent finite checks
are **COMPUTATIONALLY VERIFIED** in their explicitly sampled scope.

The unrestricted Cerny conjecture, universal `e(S)<=2n`, existence of any
universal linear image-extension constant, and the best-policy square
remain **OPEN**. This is a general block/compression mechanism with
conditional quotient consequences, not an upper bound in `n` alone.

The later PROFILE_CLASS_COMPRESSION.md strengthens first compression
for a minimum class, repairs the two h=6 profile gaps below, and raises
the current minimal-counterexample class floor to seven. It also
excludes nontrivial congruences below n22 in a state-minimal counterexample.

## 1. A short-return reduction valid for every congruence class

Let A be a strongly connected synchronizing n-state DFA. Let C be a
congruence class, `h=|C|<n`, and `d=n-h`. A **first-return word** w is
nonempty, satisfies `Cw subset C`, and satisfies `Cv intersect C=empty`
for each nonempty proper prefix v of w. A length-one letter mapping C
into C is included. Define B on the h states C, with one letter for each
distinct transformation of C induced by a first-return word of length
at most `d+1`. Then

    B is synchronizing.                                      (1)

Its alphabet may contain many words, but there is a synchronizing
subalphabet of at most `h^2` actual first-return transformations. Every
macro letter is charged at its original word length, at most `n-h+1`.
For h>=2, synchronization of B forces a nonpermutation macro letter.
Consequently a particularly direct compression theorem is

    c(C) <= n-h+1,                                         (2a)

with a compressing word that RETURNS the whole C into C. More generally,
for EVERY k-subset S of C, 2<=k<=h, apply the established Frankl
compression bound in the h-state B and expand its macro letters:

    c(S) <= (n-h+1) binom(h-k+2,2).                        (2b)

These are all-n, arbitrary-alphabet compression theorems under the
congruence hypothesis; S itself need not be Q-reachable. They are not
universal bounds for arbitrary subsets in arbitrary DFAs. The family in
section 2 makes (2a) sharp at unbounded n, already for h=2.

If H(h) is ANY proved reset upper bound for arbitrary h-state DFAs, then
EVERY subset of C can be reset in A within

    (n-h+1) H(h).                                            (2)

In particular the entire class C can be compressed/reset within that
budget. Neither a reset word for the quotient nor an arbitrary reaching
word is repeated inside (2).

### Complete proof of (1)

Use row transition matrices `M_a`, and order coordinates as `C,O=Q\C`.
Let `E_a=(M_a)_(C,O)`, `D_a=(M_a)_(O,O)`, `R_a=(M_a)_(O,C)`, and
`I_a=(M_a)_(C,C)`. A congruence ensures every word sends the WHOLE
current class into one class. Thus a path starting in C either returns
with all its original trajectories together, or keeps them all outside;
there are no partial returns.

Fix ANY row g on C. The rows `g E_a` span a subspace `U_0` of R^d.
Put

    U_j = span{g E_a D_v : |v|<=j}.

If `U_0=0`, every outside excursion is zero. Otherwise `dim U_0>=1`.
As usual `U_j=U_(j+1)` implies invariance under all `D_a`, hence
stabilization forever. Therefore `U_(d-1)` spans EVERY outside excursion:
there are at most d dimensions, and a nonstabilized chain grows at each
step. Applying `R_b` shows that the output row of ANY first return of g
lies in the span of its outputs under first returns of length at most
`1+(d-1)+1=d+1`, together with immediate returns `g I_a`.

Products with an intermediate return are zero after the restriction to
O. Every nonzero restricted product corresponds to an actual first
return: the congruence rules out partial survival. Thus the spanning
rows are induced by legal actual words, rather than artificially gated
partial maps. Zero products do not change the span.

For a stochastic row g on C, let L be its orbit span under B. L is
invariant under every short first return by definition. Apply the
preceding argument separately to EACH row in L: it follows that L is
invariant under EVERY first return, of any length. An arbitrary word
mapping C into C factors at its consecutive class returns into such
first returns, so L is invariant under that word as well.

Strong connectivity and synchronization of A give, for every q in C,
an actual reset word z_q ending at q. It maps C into C and hence
`g M_(z_q)=[q]` lies in L. Consequently

    span{g M_w : w a B-word}=R^h
    for EVERY stochastic g on C.                           (3)

For clarity, the known stationary-span synchronization criterion used
to finish the proof can be derived directly. Choose a stationary
distribution alpha for the uniform random walk on B. Equation (3)
forces alpha to be positive: a zero coordinate of alpha stays zero
under every letter, by stationarity and positivity of letter weights,
and therefore under every word, contradicting (3). The ascending-chain
argument makes the orbit rows through B-length `h-1` span R^h.
For any proper nonempty X subset C, not all those rows have the same
mass on X; otherwise their span would satisfy the nontrivial homogeneous
equation `row(X)=alpha(X) row(C)`. Averaging equally over word lengths
0..h-1, and uniformly over letters at each length, gives alpha again.
Hence some such word has mass on X STRICTLY GREATER than alpha(X).
Its preimage of X has strictly greater alpha mass. Iterating this
inverse extension terminates at C, since only finitely many subsets
exist. This constructs a reset word for B and proves (1).

To obtain an alphabet of at most `h^2` words, choose a matrix basis from
the short first returns. Its span equals the original letter-matrix
span, so its orbit spans are the same; (3) and the preceding argument
still apply. Selecting a basis does NOT assert equality of the two
transition monoids or equality of their reset thresholds.

There is a polynomial construction of such a matrix basis. In the
space of `h by d` matrices, retain a basis of all restricted exit
products of depth at most d, with an actual representative word for
each basis member. Extend the basis by the matrices `D_a`, truncating
at that depth. Apply all final `R_b`, add the immediate-return matrices,
and choose a basis of the resulting `h by h` matrices. Both spaces
have polynomial dimension (`hd` and `h^2`), and d rounds suffice.
Unlike the row proof, the matrix space need NOT stabilize at depth
`d-1`; the construction is explicitly truncated. Every nonzero retained
representative is a legal first return. This distinction is audited by
exact rational arithmetic in `check_return_word_lift.py`.

The same proof holds for any nonempty proper C satisfying
`Cw subset C OR Cw intersect C=empty` for EVERY word w. We use a
congruence class as a readily certified instance of this nonsplitting
condition. In fact this semantic condition introduces no additional
scope: define p~q if, for every word w, `pw in C iff qw in C`.
This is a congruence, and the nonsplitting condition makes C exactly
one of its classes. When h>=2 and C is proper, the congruence is
nontrivial. Thus the mechanism cannot reach simple automata through
a different choice of a nonsplitting proper set.

The complementary linear separation fact is a reconstruction of DFA
partition refinement. If C is NOT nonsplitting, some word of length
at most `n-h` has both an inside and an outside image of its members.
Start refinement with the two classes C and Q\C. Before the first
split of C, there are at most n-h+1 blocks. A stable refinement never
splits later, so each earlier depth increases the block count. A first
split at depth T therefore has T+1<=n-h+1, proving T<=n-h. This is a
short membership-separation word, not a compressing or extending word.

## 2. The return cutoff is sharp; a shorter universal repair fails

For each odd `t>=3`, let C={0,1}, O={2,...,t+1}, n=t+2. Let

    a(0)=2, a(1)=3, a(2+j)=2+(j+1 mod t);
    b(0)=0, b(1)=1, b(2+j)=j mod 2.

The two-class partition C|O is a congruence. A is SC: a cycles O,
b reaches both members of C, and a exits C. The word `b a^t b`
resets A, so it synchronizes.

Every first return is either b or `a^(k+1) b`. For k<=t-2, the two
outside trajectories have indices k,k+1 without wrapping and have
different b-colors. These return maps are permutations of C. At
k=t-1, the indices t-1 and 0 both have color zero, and `a^t b`
is constant. Therefore the cutoff `n-h=d=t` yields a nonsynchronizing
reduced automaton, whereas `n-h+1=t+1` first admits a constant letter.

Thus replacing the cutoff in (1) by `n-h` is **REFUTED** at arbitrarily
large n. These are not image-extension counterexamples: C=Qb has e(C)=1.
The lower obstruction concerns the whole return alphabet, not a claim
that every individual long return word must be shortened to the same map.

The cutoff refutation has an even smaller general-class witness, proved
directly: at n=3 take a=[2,2,0], b=[1,0,0], C={0,1}, O={2}.
The partition is a congruence, the DFA is SC, and baa resets Q. The only
length-one return is the transposition b; aa is a constant return of
length two. Thus cap n-h=1 fails, while n-h+1=2 works. This n3 witness
is state-minimal for the general class statement, since h>=2 and h<n.
C is not a MINIMUM class here. For a minimum-class witness at its own
state minimum n4, take a=[2,3,2,2], b=[1,0,0,1], classes {0,1}|{2,3}.
It is SC and baab resets Q. The first returns of length at most two
are b and ab, both permutations; aab is constant at length three.
These small witnesses concern the return cutoff. Their whole-class
compression costs are 1 and 2, respectively, so they do not attain
the n-h+1 compression upper bound. The infinite odd-t family does.
These additional minima have direct paper proofs; the 53-record matrix
certificate count above refers to the separate sampled/control corpus.

Dropping the nonsplitting assumption is even more decisive. In C_3 take
`a=[1,2,0]`, `b=[0,1,0]`, and the actual image C=Qb={0,1}.
Its a-image {1,2} partially meets C, so no first return can start with a.
The b-image is C and b acts there as the identity, so the ONLY first
return is b. The all-length first-return alphabet is nonsynchronizing,
although `b a a b` resets A in four letters. Thus the assertion that
arbitrary reachable images have a synchronizing return alphabet is
**REFUTED**, even with no word-length cutoff. It is state-minimal because
a proper set of size >=2 first exists at n=3.

## 3. General conditional quotient lift

Let theta have m>=2 classes, let h be its smallest class size, and let
u reset the quotient into a class T. Choose a smallest class C and a
shortest quotient-state path from T to C, of length at most m-1. The
concatenation sends all Q into C. Then (2) gives the general bound

    rt(A) <= |u| + dist_(A/theta)(T,C) + (n-h+1) H(h).         (4)

This theorem applies to ANY SC synchronizing DFA and any finite alphabet;
it pays the quotient reset and class routing exactly once. With a square
quotient, and any h for which its square is established, it yields

    rt(A) <= m(m-1) + (n-h+1)(h-1)^2.                       (5)

For h<=5 the small-state square used here is known; no new finite
small-state theorem is claimed. For a state-minimal counterexample,
the h-state reduced automaton is smaller than A, so the square in (5)
also follows from minimality itself, for arbitrary h. No circular
assumption about the n-state square is used.

## 4. Every class of a state-minimal counterexample has size at least six

The conditional square lifts STRICTLY when h<=5, for EVERY class-size
profile and every n. This improves the repository's former h<=3 exclusion.

For h=1 the quotient reset and routing already reset A. For h=2,3,4,
compare (5) with the square at the smallest possible n=hm. The gaps are

    h=2: 3m^2-5m+2;
    h=3: 8m^2-17m+9;
    h=4: 15m^2-43m+28.

Each is strictly positive for m>=2 (the h=4 gap is 2 at m=2).
The gap only increases with n>=hm: its increment when n increases by
one is `2n-1-(h-1)^2>0` in these ranges.

For h=5 and m>=3 the minimum-n gap is `24m^2-89m+65`, positive at
m=3 (14) and increasing thereafter. At m=2, (5) is already strict
for n>=14. It remains to cover the profiles `(5,t)`, t=5,6,7,8.

Here use a fiber version of the standard Frankl argument. A shortest
word compressing a k-set within a congruence class has a renewing
sequence of pairs and k-sets. Split that sequence by its current class.
Within a class of size s, Frankl bounds its length by
`binom(s-k+2,2)`. The original renewal condition holds on each
subsequence. Thus EVERY k-set inside a class compresses within

    sum_(classes D, |D|>=k) binom(|D|-k+2,2).               (6)

More explicitly, along a shortest compressing word, all preterminal
images S_i have size k. Pull back its final merged pair uniquely along
the injective prefixes to obtain P_i subset S_i. If P_i were contained
in an earlier S_j, that earlier prefix followed by the suffix at i
would compress the initial set sooner. This is exactly the renewing
condition needed for each class subsequence. Summing the bounds proves
(6), including paths that move to other classes.

After routing Q into a smallest h-class, apply (6) at most once per
rank k=h,h-1,...,2. With `J_h(s)=sum_(k=2)^h binom(s-k+2,2)`, this gives
another general bound

    rt(A) <= |u|+dist(T,C)+sum_D J_h(|D|).                  (7)

For the four leftover profiles, the coarse bound `2+J_5(5)+J_5(t)` is
42,56,74,96, respectively, strictly below 81,100,121,144. This completes
the all-profile h<=5 proof.

Consequences: a state-minimal Cerny counterexample cannot have a
nontrivial congruence with ANY class of size <=5. A square-extremal SC
automaton also cannot have such a congruence when its quotient obeys
the square. Simple automata, larger classes, and unrestricted
hereditariness are not settled.

For h=6 the two bounds (5)/(7) ALONE are inconclusive at `(6,14)` and `(6,15)`.
These are arithmetic gaps, not automaton counterexamples. The remaining
profiles with minimum six are strictly excluded by (5)/(7): for m>=4,
the minimum-n gap is `35m^2-161m+126>0`; for m=3 only n=18..21 require
(7); for m=2 only n=12..21 require (7), leaving those two profiles.
Convexity of J_6 concentrates fixed excess size in one class, so checking
`(6,...,6,n-6(m-1))` bounds every other size profile at that n,m.
These h=6 assertions use `H(6)=25`, as supplied by state minimality (or
a separately known six-state square); they are not derived from a
quotient-square assumption alone. The subsequent profile-sensitive
first-compression theorem repairs both gaps; see PROFILE_CLASS_COMPRESSION.md.

## 5. A growing class-size restriction in ANY state-minimal counterexample

For a state-minimal counterexample, (5) is valid for every h<n by
minimality of A, even if h is arbitrarily large: B is an actual smaller
synchronizing DFA over a finite alphabet. Therefore EVERY nontrivial
congruence, with m classes and minimum class size h, must satisfy

    m(m-1)+(n-h+1)(h-1)^2 > (n-1)^2.                       (8)

There is a useful all-n corollary, independent of the number of classes:

    n <= h^2-3h+3,  and h>=7.                              (9)

Equivalently, every class has size at least

    max{7, ceil((3+sqrt(4n-3))/2)}.

Thus any nontrivial congruence has fewer than about sqrt(n) classes,
and EVERY class has size at least sqrt(n)+3/2+o(1). These restrictions
do not assert that a hypothetical counterexample has a congruence.

Proof of (9). Sizes h<=5 were excluded above; h=6 is excluded by the
subsequent PROFILE_CLASS_COMPRESSION.md. For h>=4, suppose
`n>=n0=h^2-3h+4`. Since m<=n/h, the gap between the square and the
right side of (5) is at least

    D_h(n)=(n-1)^2-(n/h)(n/h-1)-(n-h+1)(h-1)^2.

At n0 this equals `3h-16+28/h-16/h^2`. It is positive for h>=4:
at h=4 it is 2, and its derivative in h is
`3-28/h^2+32/h^3>0`. Its derivative with respect to n at n0 is
`h^2-4h+3+7/h-8/h^2>0` for h>=4, and that derivative increases with n.
Hence D_h(n)>0 for all n>=n0, contradicting (8). Since n is integral,
(9) follows. This is a general conditional reduction for a minimal
counterexample, not a guessed growth law inferred from enumeration.

The exact profile condition (8) is stronger than its n-only corollary.
For example it excludes h=6,m>=4 directly; the additional fiber bound
handles the leftover m=3 cases. The profiles (6,14) and (6,15) are
inconclusive for (5)/(7) alone, but are repaired by the later theorem.
Combining (5) and (7) also excludes every nontrivial congruence when n<20
in a state-minimal counterexample: once h<=5 is removed, the only
profiles to check are twenty two-class profiles with sizes >=6 and
the two three-class profiles (6,6,6), (6,6,7). Their integer bounds are
strict. This is a necessary condition on counterexamples, not a claim
that all automata below twenty states satisfy Cerny.

## 6. Verification, attribution, and the remaining bottleneck

The counterexample-first sample proposes 6000 congruence-respecting
alphabets, with 435 SC synchronizing exact inputs accepted and 53
retained records including controls. This is sampling, not an exhaustive
automaton cover. The controls include reduced Cerny automata with macro
thresholds 4,9,16,25, and the sharp cutoff family through n=65.

The independent checker uses a polynomial exact rational MATRIX basis,
rather than the generator's first-return tuple-orbit BFS. It checks the
equality of the short-return matrix spans, synchronization of the basis
alphabet, reverse-subset Bellman distances, all literal lifted words,
8832 full-image vertices, 3999 minimum-n inequalities, four exceptional
profiles, and rejection of three deliberately corrupted certificates.
The all-n theorems rest on the proofs, not on those finite counts.

The full-orbit stationary criterion is the known mechanism of
[Berlinkov--Szykula, Criterion 1 and Theorem 2](https://arxiv.org/pdf/1412.8363).
Their general low-rank construction appends a fixed rank-h word to
every macro letter. The present return reduction uses a class preserved
by actual return words and charges the quotient transport once.
Frankl's set-sequence bound is also established theory. The quotient
context is [Rodaro--Venturi, Propositions 3.1--3.2](https://arxiv.org/pdf/2509.17992).
Their paper leaves the general hereditary square problem open. Priority
of this precise short-return reduction and h<=5 consequence remains
OPEN after the current comparison; absence in a search is not evidence
of novelty.

The largest unresolved issue remains a target-sensitive compatible
compression/extension mechanism for simple automata, or for arbitrary
reachable images whose trajectories split at a proposed return set.
This proof cannot silently replace a class by such an image: the
restricted products would then describe partially gated maps instead
of actual word actions. No universal image-extension theorem follows.
