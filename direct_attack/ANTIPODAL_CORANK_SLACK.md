# Two neutral singular steps can be unavoidable in a simple circular DFA

Date: 2026-10-01. **PROVED (paper)** for EVERY odd m>=3, n=2m.
Finite exact reset lengths and minimum singular-letter counts have separate
**COMPUTATIONALLY VERIFIED** scopes. General Cerny, any general bound on
neutral-step costs, and formal verification remain **OPEN**. Priority of
this construction and precise lower bound is **OPEN**. The elementary
corank inequalities and the known circular-automaton theorem are not new.

The assertion that one may restrict a general square proof to reset words
whose total original-letter corank is exactly n-1 is **REFUTED**, even for
simple strongly connected binary circular automata. This strengthens the
boundary of OPTIMAL_SATURATION_TRANSFER.md; its sufficient saturation
theorems are unaffected. This is NOT a Cerny counterexample.

## Original letters and a general matching obstruction

On Q={0,...,2m-1} let a(q)=q+1 mod 2m. The only other original letter f is

    f(0)=1, f(1)=f(m+1)=m, f(2)=m+1, f(m)=2,
    f(q)=q at all other states.

It has rank n-1, excluded state 0, duplicate state m, and kernel pair
{1,m+1}. All occurrences of a and f below cost one. Define antipodal
blocks C_j={j,j+m}, with indices j taken modulo m.

For any target S the exact inverse cardinality change is

    |f^-1(S)|-|S| = 1_(m in S)-1_(0 in S).               (1)

Thus every union of whole C_j has zero inverse change. Rotating by a
preserves the family of whole blocks. The first inverse growth from a
singleton, whenever it occurs, has target {m} and gives C_1. Another
growth is impossible until at least one NEUTRAL inverse f occurs.
Consequently every reset word uses at least n copies of f.

This first obstruction is general: if a permutation alphabet preserves
a perfect matching, and every corank-one original letter has its kernel
pair equal to a matching block and its excluded/duplicate states in one
matching block, every reset on n>=4 needs a neutral singular step. There
is no connectivity hypothesis in this conditional statement. It does
not assert synchronization of all such alphabets.

## A second neutral step is necessary for m>=5

**PROVED.** Every reset word uses at least n+1 copies of f for m>=5.
For an inverse singleton-to-Q trajectory write g,u,d for the numbers of
growing, neutral and decreasing f occurrences. Equation (1) gives

    g-d=n-1,        number of f = n-1+u+2d.              (2)

Suppose at most n copies occur. There are no decreases and at most one
neutral occurrence. The preceding matching obstruction consumes that
one neutral at cardinality two; an earlier neutral cannot escape the
block obtained by the first growth.

Directly from the ORIGINAL row,

    f^-1(C_1)={0,2},       f^-1(C_2)={m,m+2};
    f^-1(C_j) is a whole antipodal block for all other j. (3)

To permit a later growth with no neutral budget left, that sole neutral
must therefore produce a pair of cyclic separation two. Its next
growing rotation has target either {m,m+2} or {m-2,m}. The corresponding
preimages are respectively

    C_1 union {m+2},        C_1 union {m-2}.             (4)

In either triple the whole antipodal pair contributes zero to (1).
A subsequent growth must rotate the extra singleton to m; there is
exactly one such rotation. The resulting four-set is respectively

    C_1 union C_(m-1),      C_1 union C_3.               (5)

These are unions of TWO distinct blocks for m>=5. All subsequent
permutation rotations remain balanced, so no fifth inverse growth is
possible without another neutral f. Since n>=10, Q has not been reached.
This contradiction proves the bound. The exceptional m=3 is deliberately
excluded from this second argument: its special row entries overlap the
otherwise fixed states used in (5).

Equivalently, EVERY forward reset trajectory uses at least two f steps
that do NOT decrease its current image rank. Each decreasing f loses
exactly one point and a loses none, so only n-1 f occurrences can decrease
rank over the entire reset. This is a universal statement about ALL
reset words of this family, with no shortest-word or greedy assumption.

## Strong connectivity, simplicity and an explicit square reset

The original a-cycle proves strong connectivity. Every equivalence
invariant under a is a residue partition modulo a divisor d of n.
For each proper nontrivial divisor 1<d<n, necessarily d<=m:

* d=m is broken by the equivalent inputs 0,m, whose f-images are 1,2.
* d=2 is broken by 0,2: m is odd, so f(0)=1 and f(2)=m+1 have different
  parities.
* For 3<=d<m, f(d)=d, whereas f(0)=1; equivalent inputs 0,d split.

Thus every such congruence is broken and the DFA is SIMPLE.

Now take the ACTUAL original word v=f f a^(m-1), of length m+1.
Its row is

    v(0)=v(2)=2m-1,     v(1)=v(m+1)=m+1,    v(m)=0,
    v(q)=q+m-1 mod 2m at all other states.               (6)

The root m+1 is fixed. Since m is odd, the ordinary shift by m-1 has
one cycle on each parity class. In the odd class the row in (6) follows

    2m-1, m-2, 2m-3, m-4, ..., m+2, 1, then root;

this visits every odd state other than m, and the distance from 2m-1
to the root is m-1. State m instead goes to 0, then 2m-1, giving height
m+1. In the even class, the ordinary shift cycle is

    0, m-1, 2m-2, m-3, ..., m+3, 2, m+1, then 0.

The modified arrows send 0 and 2 into the odd path and fix m+1.
The longest remaining even segment starts at m-1 and ends at 2,
giving height 2m-3. All states therefore reach the root, with EXACT
rooted height

    H=4 if m=3;       H=2m-3 for odd m>=5.              (7)

Hence v^H resets ALL Q, with fully charged ORIGINAL length

    16 for m=3;       (m+1)(2m-3)=2m^2-m-3 for m>=5.   (8)

At m=3 the square slack is 9. Otherwise the slack is
(2m-1)^2-(2m^2-m-3)=2m^2-3m+4>0. Synchronization and this square
witness are proved directly; no inferred free inverse or added
permutation is used. Circular automata already satisfy Cerny's bound by
Dubuc's established theorem; no new positive class bound is claimed here.

For m=3, f a^3 f^2 a^2 f^2 a^2 f resets to 3. Its prefix-image masks are
63,62,61,59,55,58,44,25,50,40,36,9,18,8. It uses six f's, so the general
matching lower bound proves the exact minimum f-count SIX on paper.
Its unweighted minimum length THIRTEEN is a separate finite BFS result.

## What is and is not established about the slack

The corank slack delta=number(f)-(n-1) is at least one for m=3, and
at least two for every odd m>=5. In complete finite audits at

    n          6    10    14    18
    rt        13    28    45    63
    min #f     6    11    15    19

the two-neutral lower bound is attained at n10/14/18. Minimum f-count
and minimum ORIGINAL length are different objectives: the retained
minimum-f words are longer, and are not asserted shortest in length.
Exact minimum f=n+1 for EVERY odd m>=5 remains **CONJECTURED**; no
all-parameter upper certificate with only two neutral steps is supplied.
Exact arbitrary-m reset threshold and any growing-slack lower bound
remain **OPEN**.

Positive slack does NOT imply a positive prefix-image/suffix-preimage
gap at any particular cut. This result must not be misreported as
refuting the existence of histories whose cuts are actual images.
Nor does it refute a slack-aware quadratic bound. Its obstruction is
the narrower restriction to total corank exactly n-1.

## Independent verification and provenance

antipodal_corank_slack.py builds the direct row, forward shortest-word
BFS and the zero-cost permutation-necklace quotient for minimum f.
check_antipodal_corank_slack.py instead builds a five-cycle permutation
followed by a source overwrite, uses ordinary set preimages and reverse
unweighted/0-1 BFS on FULL subsets, and recomputes every literal word.
It separately searches all inverse trajectories with at most one
neutral f and no decreases. At n10/14/18 their maximum size is four;
with no neutral it is two. These finite checks corroborate the two
paper obstructions rather than supplying the arbitrary-m proof.

Thirty-six parameters through n2050 check 2,881,864 literal macro
state/letter controls, balanced block preimages, both triple-growth
cases, congruence failures and rooted graph heights. The four exact
scopes use 277,186 unweighted and 278,690 weighted reverse vertices,
394 bounded-slack vertices, and reject seven corruptions. This is
**COMPUTATIONALLY VERIFIED**, not **FORMALLY VERIFIED**. The continuation
registry adds one checker and one regeneration command to checkpoint107;
it does not claim a full rerun of every historical check.

Source context: [Szykula 2026, Section 2.8](https://arxiv.org/pdf/2608.24245)
discusses length versus dimension and the transitive corank-one class;
[Zhu 2024](https://arxiv.org/pdf/2407.08135) separates the defect cone
from the escape needed out of its orthogonal space. These explain why
neutral movement must remain available. This source comparison is not
an exhaustive priority audit of the present family.

## Post-commit pressure and the remaining fixed-slack repair

An ignored adaptive cyclic/antipodal rank-one search then maximized the
minimum number of ORIGINAL singular occurrences at n6/8/10/12/14.
It found no required slack above two. This exploration is saved under
native_build/antipodal_slack_maximize.py and its JSON; it has NOT been
independently sealed and establishes no universal upper bound. In
particular a fixed additive slack repair has not been refuted, and
this finite search must not be repeated as if it were a new theorem.

For the explicit family there is also the elementary identity

    f^3: 0->2, 1->m+1, every other state fixed.

Indeed f cycles m,2,m+1 and its two transient states0,1 enter that
cycle. Its third power is therefore a product of two disjoint unit
maps and is idempotent of rank n-2. This may aid an eventual minimum-f
upper construction, but it costs THREE original letters. Replacing f
by two free unit generators would change the problem and erase the
forced-neutral obstruction. No exact arbitrary-m min-f upper, growing
slack, or general length improvement was obtained from this repair.

CORANK_ONE_SINGLETON_OBSERVABILITY.md further proves that this SIMPLE
SC rank-one family has FULL n-dimensional singleton inverse orbit span
when ALL alternative words are admitted. That general paper theorem
does not bound neutral-word costs. It was added after checkpoint108;
the historical108/192 verification boundary is unchanged.
