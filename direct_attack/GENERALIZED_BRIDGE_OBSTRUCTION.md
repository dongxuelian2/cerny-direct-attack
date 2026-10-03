# Exact quadratic bridge costs for every fixed rank excess

**PROVED (paper); novelty OPEN.** For every k,m,h with 2<=k<m and h>=1,
let n=kmh. In the binary circular Cerny DFA on Z/nZ, put

    qa=q+1 mod n,  (n-1)b=0,  qb=q otherwise;
    S={0,kh,2kh,...,(m-1)kh};
    F_j={jmh,...,(j+1)mh-1},  0<=j<k.

There is an actual rank-k word u with precisely the fibers F_j, and S is
reachable from Q. The exact minimum bridge length is

    min{|v|: |Svu|<k} = (m-k)h*n+kh
                       = (m-k)n^2/(km)+n/m.                 (GB)

This generalizes the k=2,m=3 balanced obstruction. For every fixed k,m,
the length is quadratic. In particular even any fixed positive rank excess
m-k admits no universal linear bridge length. These are not counterexamples
to Cerny; the DFA itself has the familiar square-length reset word.

## Lower bound without an assumption about cyclic order

Track each original q in S through a word v. Let A count its a letters,
and B_q count the b letters applied when that trajectory is at n-1. Then

    qv = q+A+B_q mod n.

Suppose every B_q<=D=(m-k)h. Fix any target block F_j and subtract A from
it modulo n. This gives an interval of mh consecutive positions. Its first
kh positions contain exactly one original state q in S: S has spacing kh,
and kh divides n. Since q lies within the first kh positions and 0<=B_q<=D,
the position q+B_q lies within the same interval (offset at most
kh-1+D=mh-1). Thus qv is in F_j. This holds for every j, so no block is
missing. No order of the final images or distinctness assumption is used.

Every successful v consequently has B_q>=D+1 for some original q. After
each counted b hit that trajectory is at 0. Between successive counted hits
it needs at least n-1 a letters; other b letters leave it fixed. Before the
first hit it needs at least kh-1 a letters, the minimum over the original
states 0,kh,...,n-kh. These disjoint intervals and the counted hits give

    #a >= kh-1+D(n-1),   #b >= D+1,
    |v| >= kh+Dn.

The counting remains valid after trajectories merge: original labels are
still followed, and each B_q counts actual letter occurrences on that label.

## Matching word, including all collision cases

Take v=a^(kh-1)b(a^(n-1)b)^D. After the first b the image is

    {0} union {t kh-1 : 1<=t<m}.

The block a^(n-1)b acts on numerical states as x -> max(x-1,0).
After j blocks the image is

    {0} union {max(t kh-1-j,0) : 1<=t<m}.

At j=D its largest state is

    (m-1)kh-1-D = (k-1)mh-1.

It therefore misses F_(k-1), and hence |Svu|<=k-1. The length is kh+Dn,
matching the lower bound. The max formula handles m>=2k and duplicate images;
a proof based on preserved cyclic order would not cover those cases.

## Actual words and general hypotheses

The local transformation e_i=a^((n-1-i) mod n)b a^((i+1) mod n) sends i to
i+1 mod n and fixes all other states. For each F_j concatenate its internal
e_i in increasing cyclic order. The union of these merges maps F_j to its
last state, giving exactly the required k kernel fibers. The word length is
(n-k)(n+1), not asserted minimal. S is reached by the same local operation
inside the m cyclic intervals ending at the elements of S.

The letter a is a full cycle, so the DFA is strongly connected. The word
b(a^(n-1)b)^(n-2) resets it in (n-1)^2 letters: its image successively is
{0,...,n-2}, {0,...,n-3},...,{0}. All constructions use the original two
letters. In particular u is not treated as a unit-cost added letter.

## What this rules out, and what it leaves open

The linear-excess candidate (m-k+1)(n-k+1) is eventually false for every
fixed m>k>=2. For k=2,m=3 the optimal universal asymptotic order is quadratic:
Pin--Frankl compresses a 3-set within binom(n-1,2) letters and then a pair
within binom(n,2), totaling (n-1)^2; full synchronization of S suffices to
miss a block. The lower family gives n^2/6+O(n). No optimal coefficient is
claimed for arbitrary automata or partitions.

The obstruction controls a PRESCRIBED kernel. It does not rule out choosing
a different rank-k word, a different current image, or a coordinated reset
history that bypasses this bridge. Those choice costs remain the central
uncontrolled part of a general quadratic proof.

## Independent computational audit

generalized_bridge.py stores exact Bellman distance potentials on every
nonempty subset of size at most m, a transition-closed universe. The
independent check_bridges.py verifies the complete universe, all Bellman
inequalities, a matching shortest witness, actual kernel fibers, and Q-to-S
reachability in ordinary set semantics. The finite audit is evidence about
those parameter instances; the all-parameter theorem is the proof above.
No new statement has been Lean-kernel verified.
