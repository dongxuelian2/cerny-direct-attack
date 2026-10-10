# Binary fifth F17 after E6 is impossible

9 October 2026. Conditional at n=13, |S|=9,
ac(S,{3})=12, B0,C14,D5,E6,F17. This excludes a fifth geometry,
not the entire E6, third or joint branch. No F value is asserted.

## Necessary rows, including the extra protected point6

The common-fifth proof B1_FIFTH_ENTRANCE.md applies. Put K={1,2},
P={0,3,5,6}, J={7,...,12}, T={2} union J and I={2,4,8,...,12}.
K covers P5. Points0,3,5,6 are isolated in P6,P7,P4,P3,
respectively. In particular the protected witnesses below touching
5 or u in {0,3,5} may have length three.

Let X supply pre_X(6)=F={1,7} and L supply pre_L(0)=C={1,4}.
They are distinct because1 belongs to both input fibers. Disjoint
preimages force X to permute0,3, with pre_X(C)=D={5} and
pre_X(D)=E={6}. Write X5=gamma in C; X6=5 and X1=X7=6.

For L, pre(C)={u}, u in {0,3,5}; write Lu=delta in C. The
four singleton preimages of A,C,D,E use all P inputs. Thus L maps
T into T, injectively on J, with only a possible extra kernel {2,q}
for q in J. X maps I into T, injectively on I minus {2}, with
only a possible extra kernel {2,r}, r in {4,8,...,12}. The
K-cover proves this; outside-C injectivity is not assumed.
Binary strong connectivity gives {gamma,delta}=C.

## gamma=1, delta=4

If X has an ordinary predecessor x of7, the protected pair {5,x}
follows X^2 to a singleton, since X5=1 and X1=X7=6.
Hence X omits7 and its outside-K ordinary inputs map bijectively
to T minus {7}. X2=Xr for a unique r in {4,8,...,12}.
If r is at least8, outside-K X predecessors of2,r follow X^2
to a singleton. Thus r=4 and X2=X4.

If L has a predecessor x of2, {u,x} follows L X to a singleton,
since Lu=4 and X4=X2. Hence L omits2; L(J)=J and L2=Lq for
a unique q in J. For q different from7, outside-K X predecessors
of2,q follow X L to a singleton. Consequently q=7.

The remaining immediate kernels are14,17,24,27. They form the
four-cycle between {1,2} and {4,7}. L omits1,2 while X omits4,7,
so both letter images are independent in this graph. No distinct
pair maps into any graph edge, and every immediate kernel belongs
to the graph. It is backward closed and prevents synchronization.

## gamma=4, delta=1

If L has a predecessor x of7, {u,x} follows L X to a singleton.
Hence L omits7, L(J)=T minus {7}, and L2=Lq for a unique q in J.
If q differs from7, outside-K L predecessors of2,q follow L^2
to a singleton. Thus q=7 and L2=L7.

The outside-K ordinary X outputs are T minus {z}, z in T.
If z is neither2 nor7, outside-K X predecessors of2,7 follow
X L to a singleton. Therefore z=2 or7.

If z=7, incoming coverage of7, which L omits, requires X2=7.
Let r be the outside-K X predecessor of2. It has an outside-K
X predecessor x: x=5 for r=4, or x is ordinary for r at least8.
The distinct outside-K pair {r,x} follows X^2 L to a singleton.

If z=2, the outside-K ordinary X inputs map bijectively to J.
When X2=2, let r be the outside-K X predecessor of7. If r=4,
the protected pair {2,5} follows X^2 L to a singleton. If r is
at least8, outside-K L predecessors of2,r follow L X L to a
singleton. Otherwise X2=Xr for a unique r in {4,8,...,12}.
For r at least8, outside-K L predecessors of2,r follow L X to
a singleton. The final possibility r=4 has the same kernels
14,17,24,27. Now L omits4,7 and X omits1,2; the same closed
four-cycle prevents synchronization. All cases fail.

## Independent checks and scope

The fifth kernel inventory keeps all12 original field pairs and
every extra ordinary kernel, including unused rows. The checker
reconstructs partitions by outside-K blocks and inserts the K
inputs independently of the generator. Every original field pair
is normalized with all four P inputs retained. Every short witness
is evaluated on all normalized local row pairs at n=8,9,10.
Full individual n13 hard letters include all six labels of the
fresh point, both orientations and every ordinary permutation.
The graph argument covers arbitrary coupling; no n13 row-pair
scan or smaller-n equality claim is made. The proof uses isolation
of5 through four and of u through at least four, so no length-three
word is justified solely by a P2 bound.

Run enumerate_b1_e6_overlap_fifth.py, then
check_b1_e6_overlap_fifth.py, with Python>=3.10 and assertions.
This auxiliary work leaves the accepted article supplement unchanged.
