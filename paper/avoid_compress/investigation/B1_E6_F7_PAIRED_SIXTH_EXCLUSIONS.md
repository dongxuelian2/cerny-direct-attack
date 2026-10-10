# Four binary nonsingleton sixth exclusions after E6/F7

9 October 2026. Conditional at n=13, |S|=9,
ac(S,{3})=12, B0,C14,D5,E6,F7. Binary sixth G12,G18,G24,G128
are excluded. State8 represents any of the five fresh ordinary
labels. No whole fifth/third/joint exclusion or F value is asserted.

## Complete necessary row normalization

The common-sixth statement B1_SIXTH_ENTRANCE.md applies. Put
P={0,3,5,6,7}, J={8,...,12}, T={2} union J, K={1,2}.
K covers P5. Points0,3,5 are isolated in at least P4, whereas
6 is isolated in P3 and7 in P2. The length-three protected
witnesses below touch5 or u in {0,3,5}, never rely on7's depth.

For a G-supplying letter X and C-merging letter L, their roles
are distinct because G meets C. Disjoint preimages force X to
permute0,3 and give X5=gamma in C, X6=5, X7=6, X(G)=7.
For L, pre(C)={u}, u in {0,3,5}, with Lu=delta in C.
The singleton preimages of A,C,D,E,F use all five P inputs.
Thus L maps T into T, injectively on J, with only a possible
ordinary kernel {2,q}, q in J. Strong connectivity and the two
singleton pre(C) fields require {gamma,delta}=C.

Every possible assignment of the extra protected inputs6,7 is
retained. All ordinary conclusions come from K-cover, not from
outside-C injectivity or a higher-depth edge-count cap.

## G12 and G128: length-two witnesses

For G12, X maps I={4,8,...,12} bijectively onto T, since I is
outside K. If gamma=1, an ordinary X predecessor x of2 makes
{5,x} merge under X^2, because X1=X2=7. Thus gamma=4,
delta=1. If L has an ordinary predecessor x of2, {u,x} merges
under L X. Otherwise L omits2 and has an ordinary kernel {2,q}.
The distinct outside-K X predecessors of2,q merge under X L.
All alternatives contradict the protected isolation or K-cover.

For G128, the five distinct X ordinary outputs in the six-set T
include2 or8. If gamma=1, the corresponding ordinary input x
gives a protected collision under X^2, since X1=X2=X8=7.
Hence gamma=4,delta=1. L(T) has at least five points, so also
contains2 or8. Its predecessor x makes {u,x} merge under L X.

## G18: short words or a closed four-cycle

Now X maps I={2,4,9,...,12} into T, injectively outside2,
with at most one extra ordinary kernel {2,r}, r in {4,9,...,12}.

When gamma=1,delta=4, any ordinary X predecessor x of8 makes
{5,x} merge under X^2. Thus X omits8 and maps its outside-K
ordinary inputs bijectively to T minus {8}, with X2=Xr. For
r different from4, outside-K X predecessors of2,r merge under
X^2. So r=4. Any L predecessor x of2 makes {u,x} merge under
L X. Thus L omits2, L(J)=J, L2=Lq. For q different from8,
outside-K X predecessors of2,q merge under X L. Hence q=8.

The remaining kernels are14,18,24,28. L omits1,2 and X omits4,8.
Each image is independent in the four-cycle between {1,2} and
{4,8}. No distinct pair maps into a graph edge, all immediate
kernels belong to it, and backward closure prevents synchronization.

When gamma=4,delta=1, any L predecessor x of8 makes {u,x}
merge under L X. So L omits8, L(J)=T minus {8}, L2=Lq.
If q differs from8, outside-K L predecessors of2,q merge under
L^2; hence q=8. Write X(I minus {2})=T minus {z}. If z is
neither2 nor8, outside-K X predecessors of2,8 merge under X L.

If z=8, incoming coverage of8 forces X2=8. Let r be the outside-K
X predecessor of2. It has an outside-K X predecessor x: x=5
when r=4, or x is ordinary otherwise. The distinct outside-K
pair {r,x} merges under X^2 L.

If z=2, X(I minus {2})=J. For X2=2, let r be the outside-K
X predecessor of8. If r=4, {2,5} merges under X^2 L; otherwise
outside-K L predecessors of2,r merge under L X L. If X2 differs
from2, write X2=Xr. For r different from4, outside-K L predecessors
of2,r merge under L X. The final r=4 case has the same four-cycle
kernels14,18,24,28, now with L omitting4,8 and X omitting1,2.
The graph is again backward closed and the automaton cannot synchronize.

## G24: actual one-count in the exceptional case

X maps {1} union J into T, injectively on J, with at most one
extra ordinary kernel {1,r}. When gamma=4,delta=1, any ordinary
X predecessor x of2 makes {5,x} merge under X^2. Thus X omits2,
X(J)=J and X1=Xq. Any L predecessor x ofq makes {u,x} merge
under L X. Thus L omitsq, L(J)=T minus {q}, L2=Lr. If r differs
fromq, outside-K L predecessors of2,r merge under L^2. Hence r=q.
The kernels G={14,24,1q,2q} form a four-cycle; L omits4,q and
X omits1,2. Both images are independent in G, giving backward
closure and nonsynchronization.

When gamma=1,delta=4, any L predecessor x of2 makes {u,x}
merge under L X. Hence L omits2, L(J)=J and L2=Lq. Write
X(J)=T minus {z}. If z is neither2 norq, outside-K X predecessors
of2,q merge under X L.

For z=2, incoming coverage of2 forces X1=2. Choose x in J with
X^2 x=q; {5,x} then merges under X^2 L. For z=q and X1=q,
let r be the J predecessor of2. If r differs fromq, choose x in
J with Xx=r; {5,x} merges under X^2 L. If r=q, then
pre_X(G)={q}, pre_(X^2)(G)={1}. Actual one-count on SX,SX^2
forces q,1 into S. Since S meets C once,4 is absent; since S
meets G once,2 is present. But L2=Lq contradicts safety of L
on S. No multiplicity or guessed reaching word is substituted.

Otherwise X1=Xr. For r different fromq, an ordinary x with
Xx=r makes {5,x} merge under X^2. The last r=q case has the
same graph G, now L omits1,2 and X omits4,q. Backward closure
again prevents synchronization. All cases are exhausted.

## Audit scope

All24 original sixth field pairs per G are retained. The independent
checker reconstructs every kernel partition and role normalization,
including all protected6/7 assignments. Complete smaller normalized
row pairs test every proof word literally and directly check graph
inverse closure. Full individual n13 hard letters retain every fresh
label and ordinary permutation. Actual nine-set and Boolean controls
verify the exceptional G24 one-count argument. These controls do not
assert smaller-n equality or a full n13 transition-pair scan.

Run enumerate_b1_e6_f7_sixth.py and check_b1_e6_f7_sixth.py with
Python>=3.10 and assertions enabled. The accepted109-file article
supplement stays unchanged; this work is auxiliary and conditional.
