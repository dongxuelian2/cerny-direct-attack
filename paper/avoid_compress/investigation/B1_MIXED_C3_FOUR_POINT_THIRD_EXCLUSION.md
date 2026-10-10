# Four-point third entrance in the B1/C3 mixed joint

9 October 2026. Conditional binary exclusion at (13,9,1), outside the release.

Suppose ac(S,{a})=12, |S|=9, in a binary strongly connected synchronizing
automaton. Normalize H={0,1,2}, a=3, b=4, B={4}, C={0,1,5}. We exclude
D={0,1,2,6}. Write U={0,1}, J={7,...,12}, R={2,6} union J,
and O={5,6} union J. Established premises are |P1|<=4, H covering P5,
the entrance flags and isolation of a in P7. Also b is isolated in P6:
all images through depth ten contain a,b, so ac(S,{a,b})>=11; the
avoid-or-compress upper gives equality 11, and ENTRY_FIBER_FLAG.md's
protected-pair inequality gives the asserted isolation. No reachability
of the initial set is needed for this negative.

## Complete row and kernel cover

The third fiber is common in this geometry. Any other outside preimage
of C has indicator alpha+beta chi_B+gamma chi_C+eta chi_D. The remainder
outside B,C,D meets S at least five times, so alpha=0. The private cells
{4}, {5}, {2,6} make beta,gamma,eta Boolean. Its count on S is their sum,
which must be one. Thus the only outside fibers are B,C,D. Since D
overlaps C, the unique C-merging letter L has pre_L(B)=C and pre_L(C)
a protected singleton p in {a,b}. Put pL=delta in C. The other protected
input maps to a. The second letter F permutes {a,b}, has pre_F(C)=D,
and maps all its other inputs (5 and J) to R. L maps R to R.

The C triangle consumes three immediate pairs. Four D inputs must map
to the three C outputs. A triple kernel block would add at least two
pairs outside the C triangle. Thus F has one two-point block, one
of 01,02,06,12,16,26, or the two blocks 01 and 26. In the last case
F uses two C outputs and delta must be the remaining point. In the
other cases F uses three distinct C outputs. F is injective on {5} union J because these inputs
are all outside H. Its seven R outputs miss exactly one point nu of R,
and every used R output has an outside-H predecessor.

L is either bijective R to R, or has just one pair {2,q}, q in R minus
{2}, and seven R blocks injecting into eight R outputs. In the latter
case all blocks contain an outside-H point. Its missing R output mu
is in {2,q}, or pulling this kernel pair under L gives an outside-H
two-step pair. Only when the F block is 01 can q be arbitrary; when
it is 26 the L pair must be 26, and the other F blocks force L bijective.

D is a collision clique in P2 (F followed by L). If F used both R
outputs 2,6, its two outside predecessors would merge by F^2 L.
Therefore nu is 2 or 6. At least one of 2,6 has an outside L predecessor:
for bijective L there is only one H input in R, and for singular L all
used R blocks contain outside points. If delta were in U, pulling
{delta,d} subset D, for such an L-used d in {2,6}, would give an
outside pair merged by L F L. Hence delta=5.

Similarly F has an outside predecessor of its used output d in {2,6}.
If F6 were in U, the outside pair consisting of 6 and that predecessor
would follow F into D and merge by F L. Hence F6=5. The double-block
case is now impossible: delta=5=F6 would leave one C point without
any incoming transition. The complete core
cover consequently has twelve maps: two for each of the six kernel
blocks. Write G0=binomial(H,2). The words below are concatenations in
the usual left-to-right action order.

## F2 in U: blocks 01,02,12,06,16

First suppose nu=6. Let x be the outside F predecessor of 2 and let
y be an outside F predecessor of x. Such y exists: x is either 5,
whose outside predecessor is 6, or in J, every point of which is used.
The pair {x,y} follows F to {2,x}, then to {F2,2} subset D, and merges
by F L. Word F^3 L has length four. Thus nu=2.

Now F permutes O, and x=F^(-1)(6) is in O minus {6}. If L is bijective
on R, pulling the D pair {2,6} forces L2 in {2,6}. If L2=6, choose
outside L predecessors of 2 and x (the latter is p when x=5).
They follow L F to {F2,6} subset D and merge by F L. Thus L2=2.
If L is singular, using both 2 and 6 would pull the D pair to an
outside pair merged by L F L, so mu is in {2,6} as well as {2,q}.
If mu is not 2, necessarily q=6 and mu=6; L uses both 2 and x with outside
predecessors (x is never 6), giving the same word L F^2 L. Thus mu=2.

For blocks 01,02,12, F maps H into H. If L is bijective and L2=2,
neither letter has a predecessor of H outside H, contrary to strong
connectivity. In the singular case use

  G = G0 union { {h,o}: h in H, o in O }.

F preserves H and O and permutes {a,b}, so G is backward closed under
F. L uses only O as G output vertices, so cannot map a pair onto a
distinct G edge. All direct kernels lie in G; {a,b} does not. Thus
G is also backward closed under L and synchronization is impossible.

For block {u,6}, u in U, let h be the other point of U. L must be bijective,
L2=2, L permutes {6} union J, F u=F6=5, and F maps {h,2} bijectively
to U. If x=5, the protected pair {2,p} merges by L F^2 L, length four.
Therefore x is in J. There are two remaining maps:

* If Fh=h and F2=u, use

    G = G0 union h*O union u*{5,6} union 2*(O minus {5}).

* If Fh=u and F2=h, let y=F^(-1)(x). If y=5, the protected pair
  {2,p} merges by L F^3 L, length five. Thus y is in J. Use

    G = G0 union h*{5,6,x} union u*{5,6} union 2*(O minus {5}).

Here v*T means the set of unordered distinct pairs {v,t}, t in T;
U*T is the union of those stars over v in U.
Both graphs contain all direct kernels and omit {a,b}. Under L,
the only distinct G edges with used output endpoints are 2 paired
with {6} union J; their preimages are again of that form. There is
no edge 25, so the protected L predecessor p of 5 creates none.
Under F, the relevant singleton preimages are pre(2)=empty,
pre(5)={u,6}, pre(6)={x}; in the second graph pre(x)={y} subset J.
The displayed h,u stars pull back respectively into the displayed
2,h,u stars and G0. All other ordinary outputs have arbitrary O
predecessors. This checks backward closure and proves nonsynchronization.

The protected-pair words above contradict isolation of p in at least P6,
even though their other endpoint 2 is in H. They are not claimed to be
outside-H pairs.

## F kernel 26

Here F2=F6=5, F permutes U, and nu is again 2 or 6. Put

  G1 = G0 union U*O union { {2,6} }.

For either nu, G1 is backward closed under F: pre(U)=U,
pre(5)={2,6}, pre(6) is empty if nu=6 and is an ordinary singleton
if nu=2, and pre(2) is empty if nu=2. In the latter case also

  G2 = G1 union 2*(O minus {5})

is backward closed under F. All direct kernels are included.

If L is singular, its pair is 26 and it misses 2 or 6. Among the G1
vertices it uses 5 and at most one of 2,6, together with J; no two of
these form a G1 edge. Thus G1 is backward closed under L as well.

If L is bijective, the D-clique cover forces L2 in {2,6}. For nu=2,
if L2=2 use G2: L permutes {6} union J, so its 2-stars pull back
to 2-stars, and it uses no U output or edge 25. If L2=6, let z be
the ordinary L predecessor of 2. If z is in J, an outside pair follows
L to {2,z}, then L to {6,2}, and F merges it; word L^2 F has length
three. Otherwise z=6, L permutes the pair {2,6} and J, and G1 is
backward closed under L.

For nu=6, let z be the ordinary L predecessor of whichever of 2,6
is not L2. If z is in J, its outside F predecessor and the outside
F predecessor of 2 follow F to {2,z}, then L to {2,6}. Thus F L F merges
that outside pair in three steps. Otherwise z=6, L permutes {2,6}
and J, and G1 is backward closed under L.

Every surviving graph omits {a,b}, hence prevents synchronization.
This completes all six kernel blocks without fixing any ordinary
injection or permutation. D={0,1,2,6} is excluded. No full thirteen-state
scan, new F value, arbitrary-alphabet exclusion or numerical alphabet
separation is asserted.

## Independent audit

The standalone checker enumerates the complete 15 D partitions, 4,140
L R partitions and 877 F R partitions. Its literal C-output enumeration
has 42 F maps and 114 (delta,F) cores, including all six double-block
maps with their necessary delta. It checks 564,480 L output assignments
over the six distinct extra-pair constraints and all 40,320 F R injections.
The universal graph checks cover 312 configurations, using conservative
sets of all unspecified thirteen-state outputs rather than fixed cycles.

Complete small normalized row controls have 1,872 assignments at n=7,
18,792 at n=8 and 331,776 at n=9. Each explicit proof word or obstruction
is checked on each row; independent forward pair BFS also finds an
outside pair through depth five, a protected pair through depth six,
failure of strong connectivity or failure of synchronization. The
n=9 control has two ordinary points and exercises the distinct x,y
graph branch. These are controls, not a full thirteen-state scan or
an extrapolated extremal upper bound. The result leaves only
D={2,6} and {0,2,6} in this B1/C3 mixed joint. Residual binary third
admission has 165 typed orbits and 918 letter pairs. Joint cases remain
26/43 and both extrema stay [11,12].
