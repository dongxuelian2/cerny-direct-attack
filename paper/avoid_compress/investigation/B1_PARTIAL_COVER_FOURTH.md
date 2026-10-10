# The fourth entrance when B={0}, C={1,4}, D={5}

9 October 2026. Conditional on ac(S,{3})=12, |S|=9, n=13 in a
strongly connected synchronizing automaton. The statements about the
fourth entrance hold for any finite alphabet. Binary field-pair counts
are separate necessary admission, not a sufficient transition model.
No new F value or numerical alphabet separation is claimed.

## The effective cover is K={1,2}

The previously established H={0,1,2} cover of P5 loses state 0,
which is isolated in P6 because B={0} is mandatory through ten.
Thus K={1,2} covers P5. C={1,4} is an immediate collision pair:
a letter with preimage of B equal to C maps both C points to 0.
This does NOT supply outside-C injectivity. The earlier proof for
C={1,2} cannot be copied with the ordinary state 2 silently removed.
Here immediate extra collisions involving 2 are retained.

The intact third inventory has seven D geometries for this B,C.
D={2} was already excluded for every alphabet by the known-cover
intersection test. Its row/kernel admission is retained as a control,
not reinstated as an active geometry. For all seven profiles the
complete K-cover/protected kernel over-approximation has 646 row
patterns and 6,555 compatible pattern pairs over 54 original typed
pairs. It imposes neither C-cover nor higher-layer edge-count caps.
The independent checker reconstructs these partitions without
importing the generator.

## A common fresh fourth fiber exists in the singleton-D geometry

Assume the fresh third fiber is D={5}. Every image through eight
contains 3,0,5 and meets C once. For every letter ell, pre_ell(5)
meets every image through seven once. A preimage containing 3,0 or5
must be that singleton: otherwise its one-count condition omits
another point from every such image. Strong connectivity gives a
word from S to that point of length at most n-|S|=4, a contradiction.
Distinct one-count fibers are incomparable by the same argument.

Some preimage E of 5 is not one of {3},B,C,D. If all were among
these, U={3} union B union C union D would be backward closed under
every letter: the established first, second and third preimages are
already contained in U. U has only five states, is nonempty and proper,
contradicting strong connectivity. E is therefore outside {3},
incomparable with B,C,D and disjoint from the singleton sets B,D.

Local equality gives dim V7=8 and an annihilator of dimension five.
Writing h_X=9*chi_X-1, its restriction to O=Q minus {3} contains
1_O,chi_B,chi_C,chi_D,chi_E. The first four are independent. A Boolean
column in their span that meets S once has constant coefficient zero:
the remainder outside B union C union D meets S at least five times,
so it cannot belong to such a one-count fiber. On their three private
cells the other coefficients are Boolean, and their sum is one.
Thus only B,C,D are possible. Fresh E supplies a fifth independent
column, so these columns form a basis of the restricted annihilator.

Consider any other outside preimage R of 5. Its indicator is in this
five-column span. On the remainder outside B,C,D,E it is the constant
coefficient. At least four S points are in that remainder, so that
coefficient must again be zero. B,D are private singleton cells;
C minus E and E minus C are both nonempty. On these four private
cells the four remaining coefficients are Boolean. Since S meets
B,C,D,E once, their sum is one. Therefore R is one of B,C,D,E.
Every letter's preimage of 5 is consequently one of {3},B,C,D,E.
This common-E conclusion is proved for this geometry; it is not an
assumption about other third or fourth entrance configurations.

Each E is an immediate collision clique, because a letter maps E to
the singleton 5. The K-cover of P1 therefore implies |E minus K|<=1
and |E|<=3. All the ordinary-label permutations remain admitted.

## Exact fourth admission and one known-bound cut

Under permutations preserving K,B,C,D and3, precisely seven fresh
E geometries occur, with 31 labelled E choices. Exact rational rank
and all actual-family one-count equations are checked. There are no
additional covered Boolean preimage fibers in any of these geometries.

| E | labelled choices | binary fourth-field pairs | known-cover cut |
| --- | ---: | ---: | --- |
| {2} | 1 | 41 | excluded |
| {6} | 7 | 41 | retained |
| {1,2} | 1 | 6 | retained |
| {1,6} | 7 | 6 | retained |
| {2,4} | 1 | 6 | retained |
| {2,6} | 7 | 41 | retained |
| {1,2,6} | 7 | 6 | retained |

For E={2}, every image through seven contains 2. The singleton
protected-pair inequality ac(S,{2})<=4+d_2 and ac(S,{2})>=8 imply
d_2>=4; hence 2 is isolated in P3. Strip it from K, which covers P3.
The remaining singleton {1} would cover P3, contrary to three-letter
compression of the twelve-set Q minus {1}. This uses the existing
Frankl--Pin theorem for arbitrary subsets. The original S remains an
actual reachable image as required, though that property is not needed
for this conditional exclusion.

Before the binary-only cuts below, the other six geometries have 106
binary fourth-field pairs. Together
they cover all fourteen original D={5} typed pairs. No entire third
profile or joint is removed. A surviving field pair is necessary data,
not an automaton existence claim. Binary joint admission remains23,
binary third admission152/784, unrestricted joint admission42 and
unrestricted third geometry349. Both F values remain in [11,12].

## Binary E={1,2} and E={1,2,6} are also excluded

This subsection requires exactly two letters. Write F for a letter
with pre_F(5)=E, and L for a C-merging letter. They are distinct,
since E contains1 while L sends1 to0. For F, pre(B) cannot be C;
its protected inputs therefore permute0,3. Its pre(C) cannot use a
protected input or C (which overlaps E), so pre_F(C)=D={5}.
Write gamma=F5 in C. Its ordinary inputs are {4,6,...,12} for
E={1,2}, or {4,7,...,12} for E={1,2,6}. They all lie outside K,
and map injectively into T={2,6,...,12}. Their counts are eight
and seven, respectively.

For L the preimage of C is a protected singleton or D; call its
unique input u and its output delta in C. The other input among
that protected singleton and5 maps to5. All T inputs map into T,
injectively except for a possible single extra kernel {2,q}, q in
T minus {2}. At least seven distinct T outputs are attained. These
facts follow from K-cover, without an outside-C injectivity claim
or a higher-layer kernel budget. Strong connectivity requires both
C targets to have incoming transitions; L and F each have singleton
preimages of C, so {delta,gamma}=C. The point u is in {0,3,5}, all
isolated in P4 (0,3 are isolated even in P6).

For E={1,2}, F maps its eight ordinary outside-K inputs bijectively
onto T. If gamma=1, choose x outside K with Fx=2. The protected pair
{5,x} follows F^2 into a singleton, since F5=1 and F1=F2=5. This
contradicts isolation of5. Hence gamma=4 and delta=1. If L has an
ordinary predecessor x of2, the protected pair {u,x} follows L F
to a singleton, since Lu=1 and F1=F2=5. Otherwise L omits2 from T,
so its eight T inputs cannot be injective: its extra kernel is {2,q}
for some q in T minus {2}. Choose the distinct outside-K F-predecessors
of2,q. Their pair follows F L to a singleton, contradicting the K-cover
of P5. These alternatives exhaust every ordinary permutation and
every allowed extra {2,q} kernel.

For E={1,2,6}, the seven outside-K ordinary F outputs in the eight-set
T include at least one of2,6. If gamma=1, choose an outside-K input x
whose F output is that state. Then {5,x} follows F^2 into a singleton,
contradicting isolation of5. Thus gamma=4 and delta=1. The at least
seven L outputs in T also include at least one of2,6; choose its input
x in T. The protected pair {u,x} follows L F into a singleton, because
F1=F2=F6=5. Again this violates isolation. No pair of full thirteen-
state permutations is fixed in either proof.

These two binary fourth geometries have six earlier field pairs each,
all discharged. Binary fourth admission in this D={5} branch becomes
four geometries,22 labelled E choices and94 field pairs, still covering
all fourteen original third-field pairs. For arbitrary alphabets the
six geometries /30 labelled choices remain: a third letter could supply
an additional C target, so the binary incoming argument is not extended
to that class. No whole third or joint orbit is removed.

The independent word audit checks every normalized pair of these row
templates at n=7,8,9:256,3,456 and73,728 pairs per E profile. Smaller
controls impose the same local pair premises; they make no equality
claim at those sizes. Every protected or outside-K witness has length
two and is evaluated literally. Complete thirteen-state individual port
controls enumerate both40,320 ordinary F-output systems and all322,560
ordinary L-output systems. Symbolic image-cardinality arguments above
cover every coupled output choice; the controls are not a full n13
transition-pair scan. The separate audit imports neither generator.

## Independent checks and a guard against a false C-cover shortcut

The checker independently enumerates all K-cover kernel partitions
by placing each outside-K input into a distinct initial block, then
inserting the K inputs. This is a complete partition construction
because no two outside-K inputs can collide. It verifies every old
row/pair, every fourth-field pair, all31 labelled E choices and every
covered Boolean R candidate, using literal masks and rank modulo1009.
The matrices have at most six Boolean columns, whose square minors
have absolute value at most6^3=216<1009 by Hadamard; the modular
rank test is exactly rational rank. The source uses no floating ranks.

A full thirteen-state single-letter control has kernels14 and26,
pre(3)={3},pre(0)=C,pre(C)=B,pre(5)=D, and no other mergeable pair
at any depth for that single letter. It satisfies the K-cover and
protected isolation but fails outside-C injectivity on pair26.
This is a control for letter-level admission, not a strongly connected
synchronizing automaton or an equality witness. It prevents deleting
the extra ordinary collisions from a row template merely by treating
K as if it were C.

Run enumerate_b1_partial_cover.py, enumerate_b1_partial_cover_fourth.py,
and check_b1_partial_cover_fourth.py with Python>=3.10, assertions enabled.
The auxiliary certificate reproduces both inventories and the independent
audit byte-identically, outside the unchanged109-file accepted supplement.
