# Unrestricted B0/C4/D15/E25 exclusion

Conditional at (13,9,1), equality ac(S,{3})=12, B={0}, C={4},
D={1,5}, E={2,5}, with K={1,2} covering P5. This fourth geometry
is impossible for an arbitrary finite alphabet. It does not exclude
the whole D15 third type or determine an extremal value.

Set H={0,3,4}, O=Q-(H union D), R=Q-K. Here 2 belongs to O.
The mandatory core H is isolated in P7. The complete Boolean
classification has twelve individual fields and no additional covered
companions. Exact disjointness gives three exhaustive letter classes:

* F: preD=D, H is permuted, D maps into D and O into O.
* M: preD is one point p of H, preC=D, and O maps into O.
* T: preD=E, H is permuted, 5 and 2 map into D, and 1 maps into O.

For each letter, injectivity outside K makes its ordinary inputs
O-{2} map injectively into O. Let h be the unique omitted O output,
and let d be the unique D output of R. Its free image is exactly

    Rl = H union {d} union (O-{h}),   d in {1,5}.

For F and T this output comes from 5; for M it comes from the entering
point p in H, while 5 maps to C. These inputs are all outside K.

There are suppliers M0 with preC=D and T0 with preD=E. Thus {1,5}
merges under M0 and {2,5} under T0M0. If d=5 and h!=2, Rl contains
2 and 5, contradicting the P3 cover by lifting the latter seed.
Therefore every first R image is R, B1=Q-{5,2}, or
C_h=Q-{5,h} with h in O-{2}.

## No kernel pair inside O

Any such kernel pair of a letter L must be {2,x}, x in O-{2},
because L is injective on R. Consider the T0 ordinary-output hole h.
If h is different from 2 and x, RT0 contains 2,x, which immediately
lifts this kernel to a free pair merged in two. Hence h is 2 or x.
Put v=1T0. If v!=h, an ordinary input y in O-{2} has yT0=v,
giving {1,y} in P1. If v=h, the preimages of outputs 2,x under T0
are 1 and one ordinary y, giving {1,y} in P2 via T0L. The input y
need not differ from x; no such assumption is made.

Every B1 first image contains 1,y and is forbidden. A C_h first image
can avoid both seed pairs {2,x} and {1,y} only if h=x=y. If x!=y,
every letter maps R onto R, contradicting synchronization. If x=y,
all four K-{5,x} pairs lie in P2: {1,5}, {2,5}, {2,x}, {1,x}.
SATURATED_TWO_GUARD_TRAP.md applies using the P4 cover and likewise
contradicts synchronization. These alternatives exclude every kernel
inside O. In particular each F and M letter permutes O.

## Mandatory isolation and strong connectivity

Every M must send its protected entering point p to 1. Otherwise
pM=5; choose q in O with qM=2. The word MT0M0 merges p,q in three.
Fix p0 in H with p0M0=1. The full image QM0 is Q-{5}.

No F can send 1 to 5: choose q in O with qM0F=2, using the two
O permutations. Then M0FT0M0 merges p0,q within four. All M outputs
in D are 1, and exact preD=D allows no F predecessor of 5 except
5 after excluding 1F=5. Strong connectivity therefore forces a T
with 2T=5; otherwise no state outside {5} can enter 5.

For this T let h again be the omitted ordinary output. If 1T!=h,
some ordinary y has yT=1T. Since QM0 covers O, M0T already merges
a pair touching p0 in two. Hence 1T=h.

If 5T=5, the free-image restriction above forces h=2. The image
QM0T contains 5 and takes p0 to 2; appending T0M0 merges a pair
touching p0 within four. If 5T=1, T is a permutation. At h=2 the
same contradiction applies. Otherwise h is ordinary and v=hT is in
O-{h}. The exact missing-set identities are

    RT^2 = Q-{1,v},       QM0T^2 = Q-{h}.

If v!=2, RT^2 contains 2,5, yielding a free pair merged by T^2T0M0
within four. If v=2, p0M0T^2=2 and QM0T^2 contains 5, yielding a
mandatory pair merged by M0T^2T0M0 within five. Both are forbidden.
Thus the transition required for strong connectivity is impossible.

This proves the conditional exclusion for arbitrary alphabet size.
Synchronization is essential in the saturated-image subcase; SC
alone is not substituted there. The argument uses only the P4 cover
after outside-K injectivity, mandatory isolation through five, exact
fields and suppliers, SC and synchronization. The accepted P5/P7
premises imply the required bounds. No binary capacity assumption,
higher-layer edge-count cap, or initial-reachability shortcut is used.

The accompanying two independent row enumerators and literal-word
checker test complete small supplier domains and seeded larger
alphabets. Sampling supports the paper argument and proves no upper
bound. Nonsynchronizing image-closure certificates are checked against
independent reverse pair BFS; boundary controls are not F witnesses.
