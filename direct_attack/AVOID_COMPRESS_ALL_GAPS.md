# Sharp avoid-or-compress examples for every fixed cardinality gap

Date: 2026-10-01. **PROVED (paper)** for every r>=1, g>=2, k>=2.
Priority **OPEN**; no **FORMALLY VERIFIED** claim; general Cerny **OPEN**.

## The result and the remaining scope

Put M=kg+1, n=r+M+1, s=r+g+1. There is a BINARY strongly connected
synchronizing n-state DFA and an ACTUAL image S with |S|=s, together
with A properly contained in S, |A|=r, such that

    ac(S,A)=n-|A|=M+1=kg+2.

Consequently for EVERY fixed pair of cardinalities 1<=|A|<|S| with
|S|-|A|>=3, the known n-|A| bound is sharp at INFINITELY MANY state
counts n. The first two faces are covered separately in
[AVOID_COMPRESS_SHARP_FACES.md](AVOID_COMPRESS_SHARP_FACES.md). The g2
specialization is exactly [AVOID_COMPRESS_THIRD_FACE.md](AVOID_COMPRESS_THIRD_FACE.md).
This is stronger than adding isolated states to a pair: every example
is binary, SC and synchronizing, and S is an actual original-word image.

The upper bound is Szykula's KNOWN avoid-or-compress lemma, attributed in
[the 2026 survey, Lemma3/Open Problem4](https://arxiv.org/pdf/2608.24245).
It is NOT claimed as new. This resolves sharpness for every fixed
cardinality pair along the stated infinite arithmetic progressions;
it does NOT give the exact maximum for every triple (n,|S|,|A|).
The remaining state-count ranges and general Cerny are OPEN.

## Construction and actual reachability

Take P={p_0,...,p_r}, U={u_1,...,u_M},

    A=P\{p_r},                S=P union {u_1,...,u_g}.

Letter a fixes P and cycles U. Letter b is

    p_0 b=u_1; p_i b=p_(i-1) for 1<=i<=r;
    u_j b=p_r                 if g divides j;
    u_j b=u_(j+1)             if g does not divide j and j<M;
    u_M b=u_(g+1).

On S, b is the cycle p_0,u_1,...,u_g,p_r,p_(r-1),...,p_1.
Every outside state reaches this cycle within g+1 b's: each ordinary
block advances to its multiple of g and then p_r; u_M takes the path
u_(g+1),...,u_(2g),p_r. M>=2g+1 guarantees this last path is valid.
Therefore Q b^(g+1)=S. The two cycles and p_r routes prove SC.
Only the states u_g,u_(2g),...,u_(kg) collide under b. Every other
fiber has size one. Letter a is a permutation.

## Linear propagation proves ALL short words safe

Partition the state coordinates into the r+1 SINGLE protected states P
and g color cells: u_j has color j mod g, with color g representing0.
Let C be the n-by-s cell-incidence matrix. On the s cell coordinates,
define permutations T_a,T_b by

* T_a fixes P and cycles colors1,...,g.
* T_b cycles p_0,1,...,g,p_r,...,p_1.

These cells are NOT a congruence. For BOTH original letters, the only
departure from the indicated cell action occurs at u_M, of color1:
its actual image has color1, whereas the permutation prescribes color2.
In row-matrix notation the exact identity is

    M_l C=C T_l+e_(u_M)^T (e_1-e_2),     l in {a,b}.        (1)

Here e_(u_M)^T is a column and e_1-e_2 is a row on the CELL coordinates.
Initially chi_S C is the all-ones row on those coordinates. Both T's
preserve that row. For ANY original word w=l_1...l_t, iterating (1) gives

    chi_S M_w C=1_s+sum_i mu_i (e_1-e_2) T_(l_(i+1)...l_t), (2)
    mu_i=(chi_S M_(l_1...l_(i-1)))_(u_M)>=0.

The vectors chi_S M_w count initial-S trajectories with MULTIPLICITY;
(2) remains valid even after a collision. Their positive coordinates
are exactly the ordinary image S w.

The argument is a GENERAL delay principle. Suppose a cell projection
has an initial transversal S, its prescribed letter maps are permutations,
and each actual error is a nonnegative source column times e_p-e_q.
Suppose an error source cannot be reached from S before h letters,
every colliding original-letter fiber lies wholly inside one designated
cell in B, and all A-points are singleton cells. If permutation-cell
distance p->B is d_plus and q->A is d_minus, the same expansion proves

    ac(S,A)>=h+1+min(d_plus+1,d_minus).                     (3)

Indeed no positive error can reach a collision cell before h+1+d_plus
steps, so a first collision needs one more letter. No negative error
can reach A before h+1+d_minus steps. This is a conditional paper
theorem about the stated exact matrix identities and fibers, not an
assertion that an arbitrary DFA admits such a projection. In the present
family h=M-g, d_plus=g-1 and d_minus=g, yielding M+1. The finite checker
verifies those hypotheses directly rather than treating cells as a
genuine quotient or selecting one successful trajectory.

Starting in S, reaching u_M costs at least M-g letters: the initial
maximum U-index is g, and each letter increases an index by at most
one; all jumps from P or wraps go to smaller indices. Thus mu_i can
be nonzero only at positions i>=M-g+1.

In the CELL permutation graph, color1 cannot reach color g in fewer
than g-1 letters, and color2 cannot reach ANY state of A in fewer
than g letters. Before entering P one must traverse the intermediate
colors, and then take b from color g to p_r and b again into A.

For a prefix of length <=M-1, no POSITIVE correction in (2) has yet
reached color g. Therefore its total trajectory count in that cell is
at most1. All colliding b-sources belong to this cell. A first collision
at a word position <=M is therefore impossible; a has no collisions.
This proves |S w|=s for EVERY |w|<=M.

For a prefix of length <=M, no NEGATIVE correction in (2) has yet
reached any A-coordinate. Each such coordinate still has count>=1.
Thus A is contained in S w for EVERY |w|<=M. Taken together these
two conclusions give ac(S,A)>=M+1, without selecting a preferred word,
ignoring other original letters, or assuming images preserve the cells.

## The attaining original word and synchronization

The word a^(M-1)b^2 has length M+1 and final image

    {p_0,...,p_(r-2)} union {p_r,u_1,...,u_g,u_(g+2)}.

It misses p_(r-1) from A and STILL has cardinality s. Hence ac=M+1
exactly, with avoidance and no rank drop for this attaining word.

Synchronization is certified independently of that lower bound.
Let c=a^(M-1)b^s. On S it fixes P and sends

    u_1 c=p_0;       u_j c=u_(j-1) for 2<=j<=g.

The exceptional u_M branch takes g+1 b's to p_r, then s-(g+1) b's
to p_0. Ordinary u_(j-1) are on the s-cycle, so b^s fixes them.
Thus c^g maps all u_1,...,u_g to p_0 and fixes P.
The ACTUAL word v=c^g b has unique fixed root u_1 on S, and maximum
rooted height r+1: p_r walks down P and then into u_1; all moving
core points go directly to u_1. Therefore

    b^(g+1) v^(r+1)

resets Q. Its fully charged ORIGINAL length is

    g+1+(r+1)[g(n+g-1)+1].

This word may exceed the Cerny square, and is NOT alleged shortest or
a new square proof. It establishes synchronizability for all parameters.
The matrices in (1) are bookkeeping, not free word generators.

## Post-proof continuation toward a compatible cost bound

Two shorter ORIGINAL core macros are available:

    tau=a b^(g+1),              h=a^(M-g)b^(g+1).

Both return S into S. On the core, tau is a PERMUTATION: it is the
g-cycle R on u_1,...,u_g (fixing P), followed by b^(g+1). To check the
last moving point, u_g a=u_(g+1) takes g b's to p_r and one more to
p_(r-1), exactly the image u_1 b^(g+1) prescribed by R.

The second macro has corank ONE on S and satisfies

    h=e tau,       e: u_g->p_0, all other core states fixed.

For j<g, u_(M-g+j) takes g-j b's to p_r and then j+1 further b's,
giving the same target as u_j tau. The exceptional u_M takes all g+1
b's to p_r=p_0 tau. Thus the only changed
core source is u_g, and the kernel is {p_0,u_g}.
The charged lengths are |tau|=g+2 and |h|=M+1=n-|A|.

This is a paper algebra continuation, NOT an additional registered
computational claim. A read-only 192-parameter calculation agreed with
these identities, but that exploratory control is not in the independent
seal and is not used as proof. The preceding paper calculation is complete.

These macros expose a local unit paired with a short permutation, but
the unit e itself is h tau^(-1). In the ORIGINAL alphabet that inverse
needs an actual positive word, with its length counted. Treating it as
free would repeat an already failed cost shortcut. No bound here shows
that a sequence of these operations stays within (n-1)^2. The all-gaps
theorem remains a sharp LOCAL obstruction and an exact signed-error
delay result, with the global reset-cost coupling OPEN.

## Independent verification and implications

The independent checker constructs the core cycle first, verifies EVERY
state/letter instance of (1), and computes the two cell distances by
ordinary graph BFS. It runs ordinary set BFS for exact ac, checks actual
reachability and SC, evaluates complete ORIGINAL c/v rows, verifies the
root graph and the whole-Q reset, and literally checks retained words.
Small scopes also have independent full-image rt BFS. No negative random
search is used to prove the general claim. The g2 family was already
sealed at checkpoint110; the new finite scopes focus on g>=3.

The new scope has48 parameters, g3..11, throughn1025,542068 safe BFS
vertices,732192 subset/letter edges,12234 exact cell-identity controls,
26538765 ORIGINAL macro state/letter controls,5694 rooted states and
20894 literal reset letters. Five n<=12 full-image BFS controls use10719
vertices, and9 corruptions are rejected. Checkpoint111/195 preserves110
captures and appends only this generator/replay/check, not a full111 run.

The construction rules out improving n-|A| strictly for all state counts
using only a FIXED pair of cardinalities, SC, synchronization, actual-image
reachability or a binary alphabet. A pointwise improvement at the remaining
arithmetic ranges is still possible. More significantly, a quadratic reset
proof still needs to control how successful LOCAL steps fit into ONE word;
sharpness of each individual step does not prove that all those costs must
be incurred successively. This compatibility/cost question remains OPEN.
