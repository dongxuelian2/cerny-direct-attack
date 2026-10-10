# Unrestricted B0/C4/D15/E12 exclusion

Conditional at (13,9,1), equality ac(S,{3})=12, B={0}, C={4},
D={1,5}, E={1,2}, and K={1,2} covering P5. This fourth geometry is
impossible for an arbitrary finite alphabet. It does not exclude the
whole D15 third type, either whole joint, or determine a numerical F.

Put A={3}, H=A union B union C, O=Q-(H union D), R=Q-K. In particular
2 belongs to O. H is mandatory through seven and isolated in P7.
The complete Boolean classification permits exactly the columns
preA in {A,B}, preB in {A,B,C}, preC in {A,B,C,D}, and
preD in {A,B,C,D,E}. There are twelve individual fields and no extra
covered Boolean companions. Both a preC=D supplier M0 and a preD=E
supplier T0 exist. M0 collapses D into the singleton C, so {1,5} is
in P1; T0 maps both 1,2 into D, hence {1,2} merges under T0M0.

Exact disjointness gives three exhaustive letter classes.
F: preD=D; H is permuted, D maps into D and O maps into O.
M: preD is a singleton p in H, forcing preC=D; O maps into O,
   p enters D, and both D inputs map to C.
T: preD=E. Since E meets D, preC is a singleton and H is permuted.
   The inputs {5} union (O-{2}) are outside K and are exactly |O|
   inputs into O. By outside-K injectivity, they map bijectively onto O.
Thus O is contained in R T for every T. We do not assume an F or M
letter permutes O until proving it below.

No letter L can merge a pair {x,y} inside O. The full free-image
coverage O subset R T0 supplies distinct inputs u,v in R with
uT0=x,vT0=y, and T0L merges them within two. This contradicts the
P5 cover. Consequently F and M letters, which map O into O, actually
permute O.

Every M letter sends its protected entering p to 5. If instead pM=1,
choose q in O with qM=2; then MT0M0 merges {p,q} within three,
contradicting H isolation. Fix p0 in H with p0M0=5.

No F letter sends 5 to 1. Such a letter permutes O, so let q in O
satisfy qF=2. If q differs from 2, the pair {5,q} is wholly outside K
and merges under FT0M0 within three. If q=2, then {5,2} merges under
FT0M0; choosing x in O with xM0=2 makes M0FT0M0 merge {p0,x}
within four. The first case violates the cover, the second H isolation.
Therefore 5F=5 for every F.

Strong connectivity now forces some T to send 2 to 1. Otherwise the
only possible predecessor of 1 in every letter would be 1 itself:
M letters have no output1, F has 5F=5 and exact preD=D, and T has
exact preD={1,2}. This backward-closed state contradicts SC.
For such T take q in R with qT=2, using O subset R T. Since H is
permuted, q is either 5 or in O-{2}. The pair {2,q} merges under
TT0M0 in at most three letters. If q=5, lift it by M0 exactly as
above to merge a pair touching H within four. If q is in O-{2},
both endpoints lie in O, so lift them by T0 to a pair wholly outside
K, merged under T0TT0M0 within four. Either conclusion is forbidden.

This excludes E12 for any number of letters. Only the P4 cover and
H isolation through four are needed after outside-K injectivity;
the accepted P5/P7 conditions imply these. Synchronization is not used
beyond the established flag and cover premises. Initial-image
reachability is not an additional condition of this obstruction.
No binary incoming-capacity assumption is used.

Independent generators reconstruct all individual rows at n6..9.
Complete binary supplier alphabets through n9 and complete distinct
three-letter supplier sets through n7 are checked. For larger finite
controls a fixed-seed sample is used only as support. Every SC case
has a directly evaluated short word violating either the free-pair
cover or mandatory isolation, checked by separate reverse pair BFS.
Structural boundary controls are not attaining F witnesses. The
paper argument, not sampled failures, covers arbitrary alphabets.
