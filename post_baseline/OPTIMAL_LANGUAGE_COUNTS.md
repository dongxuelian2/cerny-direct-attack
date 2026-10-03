# A normalized integer-array model at the end of each dyadic regime

Status: **PROVED** paper theorem. Counting constants remain largely OPEN.

Fix L>=2,p=2^L. Then the three relaxed optimal languages

    W_(2p-2), W_(2p-1), W_(2p)

are in explicit bijection, and hence have the same cardinality C_L.
The words themselves have different lengths. This explains the final
three-value plateaus observed at r6..8 and r14..16.

## The common finite model

Use variables z_i for 1<=i<p. Set z_(2^d)=0. Within each binary-index
level [2^d,2^(d+1)-1] they are nondecreasing nonnegative integers. For
i=2^d+a<p require

    z_i <= z_(2i)+2a,

interpreting every z_j with j>=p as0. These conditions define a finite
set Z_L independently of r. For each of the three r values, map it to
clocks

    s_i=d*r+2(i-2^d)+z_i,  2^d<=i<2^(d+1), i<p;
    s_i=Lr+2(i-p),         p<=i<=r+1.

This gives the bijection Z_L -> W_r.

### Proof

For i<p, the earliest relaxed clock is d*r+2(i-2^d). The global optimum
forces every dyadic event and the tail from p, so each admissible clock
has the displayed form with z>=0 and power-index z=0. Spacing within a
level is precisely monotonicity of z. Even release to child2i is precisely
z_i<=z_(2i)+2a. All children 2i with i<p exist because r+1>=2p-1.

The remaining boundary spacing from 2^(d+1)-1 to2^(d+1) says

    z_(2^(d+1)-1) <= r-2^(d+1).

It is automatic at these three r. Iterating the child inequality yields

    z_(2^d+a) <= 2a*(2^(L-d)-1).

At the last index of its level this is at most

    2p-2^(d+1)-2^(L-d+1)+2
      <= 2p-2-2^(d+1) <= r-2^(d+1),

because d<=L-1. All tail spacings hold; any even release whose parent is
already in the tail has difference2i>=r when that child exists. Odd
releases follow from spacing. Thus every Z_L array is feasible and all
feasible clocks give exactly one array. The child upper bound also proves
finiteness. This establishes the bijections without enumeration.

## A simple growth bound

Let N=p/2-1. Set all upper-level z values to0. On the bottom level choose
arbitrary bits b_1,...,b_N and put z_(p/2+a)=sum_(j<=a) b_j.
This is nondecreasing, satisfies z<=a<=2a, and all upper-level child
inequalities remain valid. The 2^N choices are distinct. Consequently

    C_L >= 2^(2^(L-1)-1).

There are p-1-L free coordinates; the iterated bound makes each at most2p,
so C_L<=(2p+1)^(p-1-L). Thus the stabilized optimal-word language can be
exponentially large in the anchor count, despite its simple distance and
single canonical greatest schedule.

Complete finite enumeration gives C_2=3,C_3=279. These numerical constants
are **COMPUTATIONALLY VERIFIED**, not asserted from the paper inequalities.
An exact count/recurrence for arbitrary C_L and a normalized model for every
interior r in the dyadic regime remain **OPEN**. No claim is made that this
integer-array system or its isolated counting problem is new in the
combinatorics literature.
