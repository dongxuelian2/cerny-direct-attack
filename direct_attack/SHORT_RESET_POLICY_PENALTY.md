# A global shortest-image-policy penalty with reset threshold three

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

**PROVED on paper.** For every even n>=6, the ternary strongly connected
DFA below has exact rt=3 and global best shortest-image-policy cost P=n.
Every proper actual image has e<=n-1, with equality attained. Thus the
policy's ratio to the true optimum is n/3, unbounded. This refutes EVERY
fixed-factor and fixed-additive approximation P<=C rt or P<=rt+C.
It does not refute P<=(n-1)^2, the universal e<=2n target, or Cerny.

A second DFA differing in ONE transition has the same full actual image
family and the same rt=3 but P=3. The change modifies eligible shortest
phase parents, not the existence or ordinary length of a short reset.
Priority of the precise parameter obstruction remains OPEN. No new Lean
theorem or general n-only reset upper bound is claimed.

## Construction and complete image family

Use right actions on Q={0,...,n-1}. Define

    a(q)=1 if q mod 4 is 1 or 2, and 0 otherwise;
    b(q)=q+1 mod n;
    c(q)=q mod 2 except c(n-2)=1 and c(n-1)=2.

Both a and c fix 0,1; a sends 2 to 1. The word aba resets Q to 1.
No word of length <=2 resets: Qa={0,1}, Qc={0,1,2}; applying a or c
to either preserves at least 0,1, and applying b preserves cardinality.
A leading b preserves Q. Thus rt=3, and the cycle b supplies SC.

Write A_i={i,i+1}, B_i={i,i+2}, C_i={i,i+1,i+2}, with indices modulo n.
The full image family is

    R={Q} union all singletons union {A_i,B_i,C_i: i in Z_n},
    |R|=4n+1.

Reachability is explicit: Qa=A_0, Qc=C_0, Qa b^(n-1)c=B_0, and Qaba={1};
rotations by b reach every listed image. The family is closed: a maps into
{0,1}, c into {0,1,2}, and every nonempty subset of either belongs to R.
The n>=6 guard makes the n rotations in each of the two pair orbits distinct.

## Rank-three transport: a full lower proof into the critical triple

Let T=C_(n-3). Q is the only actual image of size greater than 3, so
G(T)=W(T)=e(T)=delta(Q,T). The word cb^(n-3) maps Q onto T in n-2 letters.
Suppose a shorter word of length ell<n-2 transported Q into ANY nonempty
subset of T. It has a last nonpermutation letter x in {a,c}; write it
v x b^r, with t=|vx|>=1. Its image J after x is a nonempty subset of
{0,1,2}. Since r<=n-4, translating J by r cannot wrap around the cycle.

For t=1 or 2, J contains 0: the one-letter images are A_0,C_0; aa,ac,ca,cc
have image A_0, and ba,bc have image A_0,C_0. Hence r>=n-3 and ell>=n-2.
For t>=3, min J<=2, so r>=n-5 and ell>=3+n-5=n-2. Both contradict
strict shortness. The proof includes strict subset and singleton arrivals,
not only words reaching the triple exactly. Therefore G(T)=W(T)=n-2.

## Exact shortest rank-two parents

No cyclic triple is monochromatic under a: the period 0110, including the
even-cycle boundary when n mod 4 is 2, has no cyclic run of three equal
values. The triples' c-images are

    C_i c=A_0 for 0<=i<=n-4;
    C_(n-3)c=A_1;
    C_(n-2)c=C_(n-1)c=C_0.

Thus no triple is merged by a single letter, and kappa=2. The rank-two
first-drop boundary consists EXACTLY of A_0 and A_1. A_0 has Q as a
parent (via a) and every triple as a parent (via a); A_1's ONLY larger
parent is T=C_(n-3), via c. Permutation b has no boundary edge.

For a rank-two target S, let d_j(S)=delta(A_j,S), j=0,1. If S!=A_0,
then d_0(S)=1+d_1(S): a,c preserve A_0, so any shortest successful word
starting there must begin with its first effective b, which sends A_0 to
A_1. Removing preceding neutral letters proves the lower equality;
prepending b proves its upper equality.

By the universal first-drop theorem, A_1 is the UNIQUE winning boundary
image for EVERY rank-two target S!=A_0. Its only larger parent is T. Hence

    e(S)=1+d_1(S), G(S)=W(S)=e(S)+n-2 for S!=A_0;
    e(A_0)=G(A_0)=1.

These equations preserve all shortest-word ties; they do not select one
convenient extension word and ignore other winning parents.

## Global optimum of the policy

Every actual one-letter merge source has size 2 and is different from
A_0, which a,c preserve and b permutes. Therefore EVERY such source S
has G(S)>=n-1. The general one-letter-seed normal form gives P>=n.
The source A_1 is merged by a and has e(A_1)=1, so G(A_1)=n-1 and P=n.
A concrete optimal policy word is cb^(n-3)ca, of length n: it first
reaches T, c transports T onto A_1 in its shortest phase, and a merges A_1.

The contrast with aba is precise. Transporting Q into A_1 by ab costs 2,
but the policy forbids that phase because T c=A_1 costs 1. The compulsory
shorter local phase chooses a parent whose full transport costs n-2.
The singleton initial phase alone cannot repair this future-tail loss.

All images have e<=n-1. For triples, ab^i gives e(C_i)<=i+1 for
0<=i<=n-2, and Qa is contained in C_(n-1). For pairs S!=A_0, a sends
A_1 to 1. Choose a positive q in S with q<=n-2 to obtain d_1(S)<=q,
so e(S)<=n-1. The only remaining pair is {n-1,0}, reached from A_1 by
b^(n-2), again giving e<=n-1. The singleton seed targets are exactly 0,1;
every nonpermutation letter is nonincreasing in the ordinary state index,
while b increases it by at most one. Hence seed distance to q>=1 is q-1,
and e({q})=q, e({0})=1. In particular e({n-1})=n-1, proving exact maximum.

## The single-transition control and excluded odd parameters

Replace c(n-2)=1 by c(n-2)=0, leaving every other transition unchanged.
The resulting c_0 still fixes 0,1, still has image C_0, and has the SAME
complete R by the same reachability/closure words. Its rank-two boundary
is A_0 and B_0: the special triple C_(n-2) maps to B_0, and there is no
larger image mapping in one letter into A_1. No triple is a-monochromatic.
Therefore e(A_1)>=2, and Qab=A_1 attains 2 with Q as an eligible parent.
So G(A_1)=2, and rt<=P<=1+G(A_1)=3 proves P=rt=3.

For odd n>=5, the construction's assignment c(n-2)=1 changes nothing in
the parity map; triple c-images are only A_0 or C_0. The only possible
a-monochromatic cyclic triple (when n mod 4 is 1) maps to 0, which is
outside A_1. Thus again no one-letter larger-image transport into A_1
exists, Qab attains e=G=2, and P=3. Saved odd controls delimit the even
obstruction. The n4 boundary has 15 images rather than 4n+1 and is handled
as a separate finite check, not silently included in the image-count proof.

## Verification boundary

The family certificates contain both transition versions at every even
n6..62, odd controls n5,n7,n9,n11, and the separate n4 case. Every saved
e/G/W/forward entry is independently recomputed using ordinary ALL-SOURCE
forward BFS. Complete image closure, the rank-two boundary, critical triple
lower cost, reset and policy words, parity/transition controls and corruption
rejection are checked. Arbitrary-n claims follow from the proof above.
The four adaptive short-reset searches are separate sampled evidence;
no absence of a policy square counterexample is inferred from them.

The four frozen searches n6/8/10/12 contain 400000 mutations plus 512 scored
seeds, all 400512 exact. Maxima P are 6,10,14,14 while rt remains 3.
All 27 retained search arrays and all 63 family/control arrays have independent
ordinary ALL-SOURCE checks; three corruptions are rejected. Every search
counter, full P histogram, retained array and seed byte is replayed. Replay
advances the mutation RNG through the deterministic construction of all 128
initial seeds even when loading frozen rows, retaining the original stream.

SHORT_RESET_SEED_BUDGET.md then settles this regime in advance: whenever
an existing reset has ell<=(n+1)/2, EVERY one-letter seed and every future
tie satisfies the square budget. Therefore further rt=3 square attacks at
n>=5 would repeat a proved conditional result. The infinite P/rt penalty
is retained as a structural obstruction, and future global-policy attacks
must leave this short-reset regime.
