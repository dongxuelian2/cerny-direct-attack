# Binary fourth fiber E={1,6} is impossible

9 October 2026. Conditional at (13,9,1), ac(S,{3})=12,
B={0},C={1,4},D={5},E={1,6}; binary alphabet only. Prerequisites are
the common-fourth proof in B1_PARTIAL_COVER_FOURTH.md. K={1,2} covers
P5 and U={0,3,5} is isolated in P4. This excludes a fourth profile,
not the whole third/joint case, and supplies no new F value.

## All necessary ordinary row templates

Let F supply pre_F(5)=E and L merge C to0. They are distinct because
1 belongs to C and E. F permutes0,3 and has pre_F(C)=D={5}, for
the same disjoint-preimage reason used in the E24 proof. Put gamma=F5
in C. L has singleton preimage u in U of C; put delta=Lu in C.
Its other protected/5 input maps to5. Binary incoming coverage gives
{delta,gamma}=C.

Let J={6,...,12}, T={2} union J and I={2,4,7,...,12}.
L maps T into T, injectively on J, with only a possible extra kernel
{2,q},q in J. F maps I into T, injectively on I minus {2}, with only
a possible extra kernel {2,r},r in {4,7,...,12}. The K-cover, not a
C-cover, proves these statements. Every ordinary map and every allowed
extra kernel is retained; no higher-layer edge-count bound is invoked.

## gamma=1, delta=4

If F has an input x with Fx=6, the protected pair {5,x} follows F^2
to a singleton, since F5=1 and F1=F6=5. Therefore F omits6. Its seven
outside-K ordinary outputs are exactly T minus {6}; F2=Fr for a
unique r in {4,7,...,12}. If r is at least7, both2 andr have distinct
outside-K F-predecessors. Their pair follows F^2 into a singleton,
contradicting the K-cover. Hence r=4 and F2=F4.

If L has a predecessor x of2, the protected pair {u,x} follows L F
into a singleton, because Lu=4 and F4=F2. Consequently L omits2;
L(J)=J and L2=Lq for a unique q in J. If q differs from6, both2,q
have distinct outside-K F-predecessors, since F maps its outside-K
ordinary inputs onto T minus {6}. That pair follows F L into a
singleton. Thus q=6.

The only remaining immediate kernels are14,16,24,26. L omits1,2 and
F omits4,6. These kernels form the four-cycle joining {1,2} to {4,6}.
Each letter image is independent in that graph, so no pair maps into
an edge of it; all immediate kernels are in it. The graph is backward
closed, leaving all other pairs unmergeable. Synchronization is impossible.
This covers arbitrary coupled ordinary permutations, not a selected pair.

## gamma=4, delta=1

If L has a predecessor x of6, the protected pair {u,x} follows L F
to a singleton, since Lu=1 and F1=F6=5. Thus L omits6, L(J)=T minus
{6}, and L2=Lq for a unique q in J. If q differs from6, both2,q have
distinct outside-K L-predecessors; their pair follows L^2 to a singleton.
Hence q=6 and L2=L6.

The outside-K ordinary F outputs are T minus {z}, z in T. If z is
neither2 nor6, outside-K F-predecessors of2,6 follow F L to a singleton.
So z is2 or6.

If z=6, incoming coverage of6 (which L omits) requires F2=6. F has
an outside-K ordinary predecessor r of2. State r has an outside-K
F-predecessor x: if r=4, x=5; if r is at least7, x is an ordinary
outside-K input because F maps those inputs onto T minus {6}.
The inputs r,x are distinct, since Fr=2 and Fx=r. Under F^2 they
map to6,2, respectively; L then merges them. This outside-K word
F^2 L has length three, contradicting the cover.

Now z=2. F maps its seven outside-K ordinary inputs bijectively to J.
If F2=2, let r be the outside-K predecessor of6. For r=4, the protected
pair {2,5} follows F^2 L into a singleton: F^2 2=2 and F^2 5=6.
For r at least7, choose outside-K L-predecessors of2,r (both targets
are in T minus {6}). Their pair follows L F L into a singleton,
because Fr=6 and F2=2. Both alternatives contradict the pair premises.

Otherwise F2=Fr for a unique r in {4,7,...,12}. If r is at least7,
outside-K L-predecessors of2,r follow L F into a singleton. Thus r=4.
The remaining kernels are again14,16,24,26; now L omits4,6 and F
omits1,2. The same backward-closed four-cycle prevents synchronization.
All cases are exhausted. No actual-prefix equality claim at another
state count, no solver timeout and no ordinary permutation shortcut is used.

## Independent audit and scope

The generator preserves the six original E16 field pairs. The independent
checker reconstructs every kernel partition, retaining unused rows too.
It evaluates every proof word on complete normalized local row pairs at
n=7,8,9 (512,10,368,294,912 pairs), with no smaller-n equality claim.
It directly verifies the closed graph in every remaining hard pair.
All seven labels of the fresh outside-K E point and all423,360 full
thirteen-state hard-profile letters are checked, including all ordinary
output permutations and protected variants. The symbolic graph proof
covers arbitrary coupling; these controls are not an n13 row-pair scan.

This discharges all six E16 fourth-field pairs. Together with the E24
and earlier E12/E126 exclusions, the binary B0/C14/D5 branch retains
only E={6} and E={2,6}:14 labelled choices and82 fourth-field pairs.
Both geometries still cover all fourteen original third-field pairs.
Unrestricted retains six fourth geometries; neither this binary incoming
argument nor its conclusion is extended to that class. Joint23/42,
binary third152/784, unrestricted geometry349 and both F intervals
[11,12] are unchanged. The accepted paper and its109-file supplement
remain unchanged. This is investigation-only conditional structure.

Run enumerate_b1_partial_cover_e16.py and check_b1_partial_cover_e16.py
with Python>=3.10, assertions enabled. The auxiliary certificate includes
both E16 and E24 complete audits and reproduces them byte-identically.
