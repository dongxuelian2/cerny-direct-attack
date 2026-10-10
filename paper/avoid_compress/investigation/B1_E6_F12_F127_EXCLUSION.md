# Two binary fifth-cover exclusions after E6

9 October 2026. Conditional on n=13, |S|=9,
ac(S,{3})=12, B0,C14,D5,E6, and a binary alphabet. Fresh fifth
F={1,2} and F={1,2,7} are excluded. No unrestricted exclusion,
whole E6 exclusion or new F value is asserted. State7 represents
any of the six fresh ordinary labels.

Write K={1,2}, T={2,7,8,9,10,11,12}, P={0,3,5,6}. K covers P5;
each point of P is isolated in at least P2. The first five
preimages have the descriptions proved in B1_FIFTH_ENTRANCE.md.
There are no additional fifth Boolean fibers for these two F.

Choose a letter X with pre_X(6)=F and a letter L with
pre_L(0)=C. They are distinct because1 belongs to F and C.
For X, pre(B) cannot be C. Its pre(A),pre(B) therefore are
the two singleton inputs0,3 in some order. Since F meets C,
pre_X(C) cannot be C, so it is D={5}. All pre(D) choices except
E={6} now overlap an assigned input, so X6=5. Consequently
X5=gamma in C, and X maps F to6. Its other inputs are

  I={4,7,...,12} for F12,
  I={4,8,...,12} for F127.

They map into T injectively, because they are outside K.

For L, pre(C) is a singleton {u}, u in {0,3,5}, since C is
already used as pre(B). Write Lu=delta in C. The four singleton
fields pre(A),pre(C),pre(D),pre(E) use all four inputs of P:
pre(D) is one of A,B,D,E and pre(E) is one of A,B,D,E, since
C and F overlap the assigned pre(B). Every T input consequently
maps into T. L is injective there outside the point2; its only
possible nontrivial ordinary kernel is a pair {2,q}, q in T minus
{2}. Its T-image has at least six points. These facts follow
from the K-cover, without asserting outside-C injectivity.

Only two letters exist and each has a singleton pre(C).
Strong connectivity requires both C outputs to have incoming
transitions, so {gamma,delta}=C.

For F12, the seven ordinary X inputs are outside K and map
bijectively onto T. If gamma=1, choose x in I with Xx=2.
The protected pair {5,x} follows X X to a singleton, since
X5=1 and X1=X2=6. Thus gamma=4 and delta=1.
If L has a T input x with Lx=2, then the protected pair {u,x}
follows L X to a singleton. Otherwise L omits2 from T. Its seven
T inputs cannot be injective, so its ordinary kernel is {2,q}
for some q in T minus {2}. The distinct X predecessors of2,q
in I give an outside-K pair merged by X L, contradicting the
K-cover of P5. Every extra ordinary kernel is retained.

For F127, the six ordinary X outputs in the seven-set T include
at least one of2,7. If gamma=1, a corresponding ordinary input
x makes {5,x} merge under X X, because X1=X2=X7=6. Hence
gamma=4 and delta=1. The at least six L outputs in T also include
one of2,7. Choose its input x in T. The protected pair {u,x}
then follows L X to a singleton, a contradiction. All witnesses
have length two and use only the isolation depths already proved.

The independent checker reconstructs the normalization of every
one of the twelve admitted field pairs per F from literal input
sets. It then checks every coupled normalized transition pair at
n=8,9,10, including all protected assignments and every ordinary
permutation/extra {2,q} kernel. These smaller controls test the
same local premises, not equality or an F value at those sizes.
Complete individual n13 port checks cover all5,040 ordinary X
systems per F and35,280 ordinary L systems, including4,320
systems omitting2. The symbolic counting above covers arbitrary
coupled n13 choices; no thirteen-state pair scan is claimed.

Run check_b1_e6_fifth_pair_exclusions.py with Python>=3.10 and
assertions enabled. F12 removes12 binary field pairs and F127
removes12. Together with the all-alphabet singleton F2 exclusion,
E6 retains F7,F17,F24,F27:four geometries,19 labelled choices,
268 binary field pairs, still covering all14 original third pairs.
The all-alphabet F12/F127 geometries remain. This is auxiliary
work outside the unchanged109-file accepted article supplement.
