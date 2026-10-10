# Four binary paired seventh exclusions in E6/F7/G8

9 October 2026. Conditional at n=13, |S|=9, ac(S,{3})=12,
B0,C14,D5,E6,F7,G8. Binary H12,H19,H24,H129 are excluded.
State9 represents any of the four fresh ordinary labels. This is
a local exclusion, not an exact F value or a whole G8 exclusion.

## Complete necessary row normalization

B1_SEVENTH_ENTRANCE.md proves common pre(G) after explicitly rejecting
the uncovered Boolean remainders. Put P={0,3,5,6,7,8}, J={9,...,12},
T={2} union J, C={1,4}, K={1,2}. Every actual image through four
contains P. MANDATORY_CORE_ISOLATION.md therefore isolates every point
of P in P7. K covers P5, so a pair outside K cannot merge in five letters.

Let X supply H as its preimage of G, and L merge C to B={0}.
Both letters exist by strong connectivity and the earlier reductions.
Because H meets C, their roles are distinct: preimages of distinct
output fields are disjoint. With a binary alphabet these are all letters.
The parent field pairs force X to permute0,3 and give

    X5=gamma in C, X6=5, X7=6, X8=7, X(H)=8.

For L, pre(C)={u}, u in {0,3,5}. Its singleton preimages of A,C,D,E,F,G
use all six inputs of P, and Lu=delta in C. Thus L maps T into T,
injectively on J, with only a possible ordinary kernel {2,q}, q in J.
Its remaining four P inputs biject to5,6,7,8 in every possible order.
No assignment involving protected8 is dropped. The two singleton
pre(C) fields and strong connectivity require {gamma,delta}=C.

All ordinary input fields below have the same size as T, except H129,
where there is one fewer input. The outside-K inputs are injective by
the K-cover. These are consequences of the literal field capacities,
not a general outside-C injectivity assertion or an edge-count cap.

## H12 and H129: two-letter contradictions

For H12, X maps I={4} union J bijectively to T. If gamma=1, an
ordinary predecessor x of2 makes {5,x} merge under X^2, since
X1=X2=8. Hence gamma=4,delta=1. If L has an ordinary predecessor
x of2, {u,x} merges under LX. Otherwise L omits2 and L2=Lq for
some q in J. Distinct outside-K X predecessors of2,q merge under XL.
All these contradict either P7 isolation or the K-cover of P5.

For H129, X maps I={4,10,11,12} injectively into the five-set T.
Its four distinct outputs include2 or9. If gamma=1, a corresponding
ordinary input x makes {5,x} merge under X^2, since X1=X2=X9=8.
Thus gamma=4,delta=1. L(T) has at least four points, so contains
2 or9. Its ordinary predecessor x makes {u,x} merge under LX.

## H19: short words or a backward-closed four-cycle

Now X maps I={2,4,10,11,12} into T, injectively outside2, with at
most one extra kernel {2,r}, r in I minus {2}.

If gamma=1,delta=4, any ordinary X predecessor x of9 makes {5,x}
merge under X^2. Thus X omits9 and its outside-K ordinary inputs
map bijectively to T minus {9}, with X2=Xr. For r different from4,
outside-K X predecessors of2,r merge under X^2. Hence r=4.
Any ordinary L predecessor x of2 makes {u,x} merge under LX.
Otherwise L omits2, L(J)=J and L2=Lq. If q differs from9,
outside-K X predecessors of2,q merge under XL. Hence q=9.

The remaining immediate kernels are14,19,24,29. L omits1,2 and
X omits4,9. Each image is independent in this four-cycle between
{1,2} and {4,9}. No distinct pair maps into an edge, and every
immediate kernel is an edge. Backward closure puts every mergeable
pair in this four-edge graph, contradicting synchronization.

If gamma=4,delta=1, any ordinary L predecessor x of9 makes {u,x}
merge under LX. Thus L omits9, L(J)=T minus {9} and L2=Lq.
For q different from9, outside-K L predecessors of2,q merge under
L^2, so q=9. Write X(I minus {2})=T minus {z}. If z is neither
2 nor9, outside-K X predecessors of2,9 merge under XL.

For z=9, incoming coverage of9 forces X2=9. Let r be the outside-K
X predecessor of2. It has an outside-K X predecessor x: x=5 if
r=4, otherwise x is ordinary. The distinct outside-K pair {r,x}
merges under X^2L.

For z=2, X(I minus {2})=J. If X2=2, let r be the outside-K X
predecessor of9. For r=4, {2,5} merges under X^2L. Otherwise
outside-K L predecessors of2,r merge under LXL. If X2 differs
from2, write X2=Xr. For r different from4, outside-K L
predecessors of2,r merge under LX. The last r=4 case has the same
four-cycle kernels, now L omitting4,9 and X omitting1,2.
Both images are independent, again preventing synchronization.

## H24: preserve the actual one-count exception

X maps {1} union J into T, injectively on J, with at most one
extra kernel {1,r}. If gamma=4,delta=1, any ordinary X predecessor
x of2 makes {5,x} merge under X^2. Thus X omits2, X(J)=J and
X1=Xq. Any ordinary L predecessor x ofq makes {u,x} merge under
LX. Otherwise L omitsq, L(J)=T minus {q}, L2=Lr. If r differs
fromq, outside-K L predecessors of2,r merge under L^2. Thus r=q.
The graph {14,24,1q,2q} contains all immediate kernels; L omits4,q
and X omits1,2. Independent images imply backward closure and
nonsynchronization.

If gamma=1,delta=4, any ordinary L predecessor x of2 makes {u,x}
merge under LX. Otherwise L omits2, L(J)=J and L2=Lq. Write
X(J)=T minus {z}. If z is neither2 norq, outside-K X predecessors
of2,q merge under XL. For z=2, incoming coverage of2 forces
X1=2. Choose x in J with X^2x=q; {5,x} merges under X^2L.

For z=q and X1=q, let r be the J predecessor of2. If r differs
fromq, choose x in J with Xx=r; {5,x} merges under X^2L. For
r=q, however, pre_X(H)={q} and pre_(X^2)(H)={1}. Actual one-count
on SX and SX^2 forces q,1 in S. Then C one-count forces4 absent,
and H24 one-count forces2 present. Since L2=Lq, L is unsafe on S.
The images SX and SX^2 are collision-free nine-sets; no multiplicity
or conjectured reaching word replaces these actual-image statements.

In the remaining case X1=Xr. For r different fromq, an ordinary
x with Xx=r makes {5,x} merge under X^2. The last r=q case has
the same four-cycle, now L omitting1,2 and X omitting4,q. Backward
closure again prevents synchronization. Every case is exhausted.

## Audit scope and remaining branch

The inventory preserves every original48 field pair per H, every
kernel partition consistent with K and the mandatory P, and unused
rows. The independent checker constructs the partitions by a different
method and verifies the role fields before using any word argument.
It reuses reason17/reason24 from an earlier independent literal-word
auditor with j=9. Those functions evaluate actual transformations;
they do not hard-code the earlier fresh collision target. The changed
target8 and every new protected input assignment are retained.

The Python controls evaluate700,416 complete smaller normalized row
pairs and directly verify the backward-closed graphs. Full individual
n13 ordinary ports retain all four fresh labels and all protected
assignments. Separate forward pair-BFS controls check representatives
of every encountered proof case without using its alleged word.

A separate C++17 implementation uses a different row generation:
inject the outside-guard inputs, then give the guard any remaining
target or any already used target. This enumerates exactly every
permutation or one permitted extra collision, without kernel templates.
Every ordinary system is combined with every protected assignment.
It checks every original-letter proof word, every missing incoming
target, the graph kernels and inverse closure, and the actual one-count
exception. At n13 it exhausts55,296,000 pairs each for H12/H129 and
276,480,000 each for H19/H24,663,552,000 normalized pairs in total.
Its complete proof-case histograms agree with Python at n10,n11.
This covers the four conditional paired geometries, not the other
H9/H29 geometries or the full13-state automaton domain. No smaller-n
equality, unconstrained alphabet classification or exhaustive whole
Problem4 scan is inferred from these controls.

The four binary cuts remove192 field pairs. Together with the earlier
all-alphabet H2 cut, binary E6/F7/G8 retains H9/H29: two geometries,
eight labelled choices,2188 field pairs. Unrestricted seventh admission
still has six geometries/18 labels. No whole G8, fifth, third or joint
branch is removed, no alphabet separation is proved, and both
F(13,9,1) intervals remain[11,12]. The article/release is unchanged.
