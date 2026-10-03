# Sharp avoid-or-compress bounds on the first two cardinality faces

Date: 2026-10-01. **PROVED (paper)** for the parameter ranges below.
Priority is **OPEN**. No **FORMALLY VERIFIED** claim is made.

For nonempty A properly contained in S, define

    ac(S,A)=min{|w|: A is not contained in S w OR |S w|<|S|}.

All words use ORIGINAL letters, with right actions. Szykula's known
avoid-or-compress lemma gives ac(S,A)<=n-|A| when some state of A is
avoidable. It applies to every strongly connected synchronizing DFA.
See [Szykula 2026, Lemma 3 and Open Problem 4](https://arxiv.org/pdf/2608.24245),
which attributes the lemma to the STACS 2018 paper. Its question about
tightness as a function of both cardinalities motivates this result;
the general upper bound is NOT claimed as new.

## Exact extremal statement, with actual reachable images

Among n-state strongly connected synchronizing DFAs, even requiring
S=Qv for an original word v, the following maxima are exact:

* |S|=|A|+1: maximum ac(S,A)=n-|A|, for every 1<=|A|<n.
* |S|=|A|+2 and S properly contained in Q: maximum ac(S,A)=n-|A|,
  for every 1<=|A|<=n-3.
* S=Q: maximum ac(Q,A)=1, for every nonempty proper A. A synchronizing
  DFA must have an original singular letter, which immediately compresses Q.

The lower bounds have BINARY strongly connected synchronizing examples.
The upper bounds are the known lemma and the elementary last observation.
Thus the second face includes |S|=3, |A|=1 for every n>=4, and neither
face is limited to isolated-state extensions of a pair. The two faces
do NOT settle all of Open Problem 4. The subsequent
[third-face continuation](AVOID_COMPRESS_THIRD_FACE.md) proves equality
when |S|-|A|=3 and n-|A| is even and at least6. The general remaining
cardinality problem is OPEN.

The subsequent [all-gaps theorem](AVOID_COMPRESS_ALL_GAPS.md) proves
sharpness at infinitely many n for EVERY fixed cardinality pair with
gap>=3. Exact maxima at the remaining state counts are still OPEN here.

## First face: one moving point and an anchored core

Put k=|S|>=2, L=n-k+1>=1. The states are 0,...,n-1. Letter a advances
0,...,L-1 by one and fixes L,...,n-1. Set

    S={0,L,L+1,...,n-1},       A=S\{0}.

Letter b cycles S in the displayed order, and sends every other state
to L. Hence Q b=S: the subset is an actual image. Strong connectivity
follows by taking the a-path from0 to L, then the b-cycle through the
anchored states and back to0.

For 0<=j<L write S_j=A union {j}. The only safe transitions before
compression are

    S_j a=S_(j+1)   (j<L-1),       S_j b=S_0.

At j=L-1, a maps the moving point into L in A. Every word of length
less than L therefore has image S_j for j<L, contains A and has size k.
The ORIGINAL word a^L compresses S. Thus ac(S,A)=L=n-|A|.

Synchronization is not assumed: c=a^L acts on S as the unit 0->L and
fixes all other core states, while b acts as a k-cycle. The standard
cycle/unit word

    c (b^(k-1) c)^(k-2)

resets S and also Q, since Q c=S c=A. Its ORIGINAL length is

    (k-1)L+(k-2)(k-1)=(k-1)(n-1)<=(n-1)^2.

No exact reset-threshold claim is required for the extremal statement.

## Second face: two moving points and an alternating timer

Put r=|A|>=1, M=n-r>=3, s=r+2. Write the states as

    A={p_0,...,p_(r-1)},       U={u_1,...,u_M},
    S=A union {u_1,u_2}.

Letter a fixes A. Both constructions below have

    p_i b=p_(i+1) for i<r-1,      p_(r-1) b=u_1.

If M is ODD, a cycles u_1,...,u_M, and

    u_j b=p_0 for odd j,         u_j b=u_2 for even j.

If M is EVEN, necessarily M>=4, and

    u_1 a=u_2;  u_j a=u_(j+1) (2<=j<M);  u_M a=u_2;
    u_1 b=u_2;
    u_j b=p_0 for even j>=2,     u_j b=u_2 for odd j>=3.

In either case Q b=S. The protected b-path reaches u_1, and a then
reaches every u_j; a suitable u_j b returns to p_0. This proves strong
connectivity, including the transient state u_1 in the even case.

The two points in S a^j remain distinct for EVERY j>=0. For
0<=j<=M-2 their b-images are the two different states p_0,u_2.
At j=M-1 they have the SAME b-image p_0:

* Odd M: the pair at that layer is {u_M,u_1}, both with odd index.
* Even M: the pair is {u_M,u_2}, both with even index.

Because A b=(A\{p_0}) union {u_1}, the safe b-transition returns
S a^j to S, and the first exceptional b-transition compresses it.
Every a-run of fewer than M-1 letters followed by b is safe. Every
shorter word can be split into such a-runs; a trailing run is also
safe because a fixes A and keeps the two moving points distinct.
Consequently ALL words of length less than M are safe, while

    h=a^(M-1)b

compresses S. Therefore ac(S,A)=M=n-|A|, as claimed. Avoidance and
compression are BOTH included in this lower bound; it is not only a
claim about the first rank drop of a preferred word.

## A charged synchronization certificate for the second face

Let t=a b for odd M, and t=b for even M. On S, t is the full cycle

    p_0,...,p_(r-1),u_1,u_2.

On S, h agrees with t except that u_1 h=p_0 instead of u_2; both
u_1,u_2 map to p_0. Let g be the core unit u_1->u_2. Thus h=g t
on S (equivalently t followed by the unit u_2->p_0).
The original-word macro

    h (t^(s-2) h)^(s-2)

acts on S as g (t^(s-1)g)^(s-2)t, and resets it. To verify the
standard unit/cycle identity directly, after g the missing point is
u_1. Applying t^(-1)g successively shortens the remaining cyclic
interval by one, until only u_2 remains. The final t keeps it a singleton.
Prepending ORIGINAL b gives a whole-Q reset, of charged length

    1+(s-1)M+2(s-2)^2     when M is odd,
    1+(s-1)M+  (s-2)^2    when M is even.

These are explicit upper bounds, not exact rt formulas. They certify
synchronization for ALL parameters; some of these upper bounds exceed
the Cerny square, so they are NOT alleged square proofs for this family.
All occurrences inside a macro are counted as ORIGINAL letters.

## Verification and research consequence

avoid_compress_sharp_faces.py produces the rows, a reaching word,
an attaining word, and a charged reset program. The independent
check_avoid_compress_sharp_faces.py uses ordinary set transitions and
an independent construction in core/cycle coordinates. It checks
ALL safe subset/letter edges before the first successful BFS layer,
strong connectivity in both graph directions, Q b=S, the complete
original-letter macro rows, and the composed whole-Q reset. Small
scopes additionally have exact ordinary full-image reset BFS.
Explicit reset words are literally checked where retained. The finite
scope and corruption counts are recorded in the generated check report.
This is COMPUTATIONALLY VERIFIED in those scopes, not a formal kernel.

The saved scope has 381 parameters through n1025, 26992 subset vertices,
53222 subset/letter edges, 17305572 original macro state/letter controls,
and 109418 literal reset letters. All cardinalities at n2..18 are covered
on the stated two faces, with selected larger parameters. There are 73
exact full-image reset BFS controls at n<=10 (9926 vertices), and nine
corruptions are rejected. Checkpoint109/193 preserves the previous108
captures and appends only the present generation/replay/check; it is
NOT a full109 rerun. None of these finite counts proves the all-n result;
the preceding timer and charged-core proof supplies that result.

The known local bound cannot be improved strictly merely by using
either of these cardinality relations, actual-image reachability,
strong connectivity, synchronizability, or a binary alphabet.
A proof strategy may still exploit the relation BETWEEN successive
successful steps. These examples do not show that every step in one
reset construction simultaneously incurs its worst local bound. That
missing cost coupling remains the central Cerny obstacle. Cerny OPEN.
