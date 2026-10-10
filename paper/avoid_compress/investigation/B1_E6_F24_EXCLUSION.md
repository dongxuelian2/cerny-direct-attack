# Binary fifth F24 after E6 is impossible

9 October 2026. Conditional at n=13, |S|=9,
ac(S,{3})=12, B0,C14,D5,E6,F24; binary only. No whole E6/third/
joint exclusion or new F value is asserted.

## Necessary rows

Use B1_FIFTH_ENTRANCE.md and put P={0,3,5,6}, K={1,2},
J={7,...,12}, T={2} union J. K covers P5, and0,3,5,6 are
isolated in P6,P7,P4,P3. Every image through six meets F once.
In particular S,SX,SX^2 are collision-free nine-sets meeting F
once, and L is injective on S.

Choose X with pre_X(6)=F={2,4} and L with pre_L(0)=C={1,4}.
They are distinct. Disjoint preimages make X permute0,3,
pre_X(C)=D={5}, pre_X(D)=E={6}, X6=5, and X2=X4=6.
Write X5=gamma in C. Its ordinary inputs {1} union J map into
T, injectively on J, with at most an extra kernel {1,r}, r in J.

For L, pre(C)={u}, u in {0,3,5}; write Lu=delta in C. Its
four singleton preimages of A,C,D,E use all P inputs. L maps T
into T, injectively on J, with at most an extra kernel {2,q},
q in J. These are K-cover consequences, not outside-C injectivity.
Since only two letters supply the C targets, strong connectivity
requires {delta,gamma}=C.

## gamma=4, delta=1

If X has an ordinary predecessor x of2, {5,x} follows X^2 to
a singleton, since X5=4 and X2=X4=6. Thus X omits2 and maps
J bijectively to J, with X1=Xq for a unique q in J. If L has
a predecessor x ofq, {u,x} follows L X to a singleton. Hence
L omitsq, maps J bijectively to T minus {q}, and L2=Lr for
a unique r in J. For r different fromq, outside-K L predecessors
of2,r follow L^2 to a singleton. Therefore r=q.

The remaining kernels are G={14,24,1q,2q}, a four-cycle between
{1,2} and {4,q}. L omits4,q and X omits1,2. Both letter images
are independent in G, so no distinct pair maps into G and every
immediate kernel lies in G. Backward closure prevents synchronization.

## gamma=1, delta=4

If L has a predecessor x of2, {u,x} follows L X to a singleton.
Thus L omits2, maps J bijectively to J, and L2=Lq for a unique
q in J. The distinct X(J) outputs form T minus {z}. If z is
neither2 norq, outside-K X predecessors of2,q follow X L to
a singleton. Hence z=2 orq.

If z=2, incoming coverage of2 forces X1=2. X permutes J.
Choose x in J with X^2 x=q. Then {5,x} follows X^2 L to a
singleton: X^2 5=2 and L2=Lq.

If z=q and X1=q, let r be the J predecessor of2. For r different
fromq, choose x in J with Xx=r; {5,x} follows X^2 L to a
singleton. If r=q, then X1=q and Xq=2. Here pre_X(F)={q}
and pre_(X^2)(F)={1}. The one-count conditions on SX and SX^2
force q,1 into S. As S meets C once,4 is absent; as S meets F
once,2 is present. But L2=Lq then collides two S states in one
step, contradicting safety. This uses actual image coordinates,
not a guessed reaching path or transformation multiplicities.

Otherwise X1=Xr for a unique r in J. If r differs fromq, choose
x in J with Xx=r. The protected pair {5,x} follows X^2 to a
singleton. The last possibility r=q again has kernels G. L omits
1,2 and X omits4,q, so the same backward-closed four-cycle
prevents synchronization. Every case fails.

## Independent checks and scope

The joint overlap-fifth checker independently reconstructs every
kernel partition and keeps all12 original F24 field pairs. It
checks every normalized row pair at n=8,9,10 and every proof word
literally. All16 Boolean assignments of1,2,4,q verify the actual
one-count exception; full n13 nine-set controls retain the extra
mandatory state6. Complete individual n13 hard letters include
all six q labels and every ordinary permutation/protected variant.
The graph proof covers arbitrary coupling, without a full n13
row-pair scan. Length-three protected words touch5, which is
isolated in P4; no unproved higher-layer edge count is used.

Run enumerate_b1_e6_overlap_fifth.py and check_b1_e6_overlap_fifth.py
with Python>=3.10, assertions enabled. This is auxiliary work
outside the unchanged accepted109-file article supplement.
