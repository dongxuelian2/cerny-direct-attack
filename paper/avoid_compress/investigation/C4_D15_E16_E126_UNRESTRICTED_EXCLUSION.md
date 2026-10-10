# Unrestricted B0/C4/D15/E16 and E126 exclusion

Conditional at (13,9,1), equality12, B={0}, C={4}, D={1,5},
and E={1,6} or {1,2,6}, with residual K={1,2} covering P5.
Both fourth geometries are impossible for arbitrary finite alphabets.
No whole D15 third type or numerical maximum is determined here.

Write H={0,3,4}, O=Q-(H union D), R=Q-K; 2,6 belong to O.
H is isolated in P7. There are exactly twelve individual fields,
with no additional covered Boolean companions. The exact classes are:

* F: preD=D, H is permuted, D maps into D and O into O.
* M: preD={p}, p in H, preC=D, O maps into O.
* T: preD=E, H is permuted. Free input6 maps into D; free inputs
  {5} union (O-{2,6}) inject into O, missing one O output h.

The guard2 is an additional O input for E16, but a D input for E126.
All letters are injective outside K. Suppliers M0 with preC=D and
T0 with preD=E exist. Hence {1,5} merges under M0, and every pair
inside E merges under T0M0 in two.

## E126

The graph consisting of the E triangle and edge15 has exactly two
independent n-2-sets. Its edges lie in P2, so the P4 cover and
FINITE_INDEPENDENT_IMAGE_TRAP.md contradict synchronization. This
case uses no mandatory isolation or strong connectivity after the
exact suppliers and cover are established.

## E16: eliminate O collisions

We have seed edges15 in P1 and16 in P2. A letter kernel inside O
must be {2,x}, x in O-{2}. If x=6 these three edges form the path
5-1-6-2, with three independent n-2-sets. Otherwise they form the
star1-{5,6} plus disjoint edge2-x, with two such sets. All edges lie
in P2, and the finite-image trap contradicts synchronization using
P5. Thus no letter has a kernel inside O; F and M permute O.

Likewise no letter can have immediate kernel25: together with15,16
it gives the path6-1-5-2, with three independent n-2-sets and the
same P5 contradiction.

For every T, free inputs {5} union (O-{2,6}) cover O-{h}. If 2T
does not fill h, it coincides with the image of either5 or an ordinary
O input. These would be the excluded kernel25 or an excluded O
kernel. Thus 2T=h, and these n-5 inputs together cover O bijectively.

## E16: mandatory isolation and the SC-required transition

Every M sends its entering p to5. If pM=1, choose q in O with qM=6;
MT0M0 merges p,q within three. Fix p0 in H with p0M0=5. Then
QM0=Q-{1}, and M0 permutes O.

Every F fixes5. Otherwise 5F=1; take q in O with qF=6. If q!=2,
the free pair {5,q} merges under FT0M0 within three. If q=2, choose
x in O with xM0=2; M0FT0M0 merges p0,x within four. Both are
forbidden. Strong connectivity therefore requires a T with 6T=1:
M has no output1, F has no predecessor of1 outside1, and exact
preD=E16 allows only1 and6 as T predecessors of1.

For this T the free image is H union {1} union (O-{h}). If h!=6,
it contains1,6, lifting their seed to a free pair merged within three.
So h=6 and 2T=6.

If 1T=1, then12 and26 merge under T^2 and16 under T. Together
with15 under M0 this gives triangle126 plus pendant15 in P2. Its
two independent n-2-sets contradict synchronization via the P4 cover.

Otherwise 1T=5, and T is a permutation. Put v=5T in O-{6}.
The missing-set identity is RT^2=Q-{1,v}; also26 merges under T^2M0
in three. If v!=2, RT^2 contains2,6, so T^4M0 merges a free pair
within five. Hence v=2. On {1,2,5,6}, T is then the four-cycle
2->6->1->5->2. Choose q in O with qM0=2. The word M0T^3M0
merges p0,q within five, contradicting mandatory isolation.

This excludes E16 for every finite alphabet. Synchronization is used
explicitly in the image traps and cannot be replaced by SC. All exact
suppliers and all twelve fields are retained; no binary capacity or
retracted pair-count cap is invoked. The source proof, not negative
samples, supplies the arbitrary-alphabet exclusion.

Independent small-domain generators and literal contradiction-word
checkers support both proofs. Closed-frame controls are independently
confirmed nonsynchronizing. Structural boundary examples are not
attaining F witnesses. Initial S reachability is unnecessary for these
conditional obstructions and remains required in every lower example.
