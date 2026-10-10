# Binary fourth fiber E={2,4} is impossible

9 October 2026. Conditional on the established equality flag at
(13,9,1), with B={0},C={1,4},D={5},E={2,4}. This is a binary-only
fourth-profile exclusion outside the article. It neither excludes the
whole third/joint case nor gives a new F value.

## Necessary row description

Use the proved common-fourth space of B1_PARTIAL_COVER_FOURTH.md.
K={1,2} covers P5, where P_h consists of pairs merged within h letters.
States0,3 are isolated in P6, and5 is isolated in P4. Thus any pair
incident to U={0,3,5} is isolated in P4. All images through seven
contain U, meet C once and meet E once; they are collision-free
characteristic nine-sets. In particular S,SF,SF^2 meet E once and L
is injective on S. Original reachable-image requirements remain in
force, although reachability is not needed in the exclusion.

Some letter F has pre_F(5)=E, while another letter L has pre_L(0)=C.
They are distinct because4 belongs to C and E. There are exactly two
letters. F has protected inputs0,3 permuting those states: pre_F(0)
cannot be C, which intersects E. The common first/second preimage
descriptions force the two protected singleton inputs to supply0,3.
Its preimage of C is consequently D={5}. Write gamma=F5 in C.

L's preimage of C is a singleton u in U; write delta=Lu in C.
The other input among5 and the protected point not supplying3 maps
to5. Let J={6,...,12}, T={2} union J. L maps its eight T inputs into
T, with J injective by the K-cover. It is either bijective there or
has exactly one extra kernel {2,q},q in J. F maps {1} union J into
T, with J injective, and is either bijective there or has exactly one
extra kernel {1,r},r in J. No outside-C injectivity is asserted.
Strong connectivity requires both C targets to have incoming edges,
so {delta,gamma}=C. No higher-layer edge-count cap is used.

## gamma=4, delta=1

If F has a predecessor x of2, the protected pair {5,x} follows F^2
to a singleton, since F5=4 and F2=F4=5. This contradicts isolation
of5. Therefore F omits2. Its seven J outputs are distinct and are
exactly J, so F1=Fq for a unique q in J.

If L has a predecessor x ofq, the protected pair {u,x} follows L F
to a singleton, because Lu=1 and F1=Fq. Hence L omitsq. Its J outputs
are exactly T minus {q}; L2=Lr for a unique r in J. If r differs from
q, both2 andr have distinct L-predecessors in J. That outside-K pair
follows L^2 into a singleton, contradicting the K-cover. Thus r=q.

Only the following hard profile remains:

    L(J)=T minus {q}, L2=Lq; F(J)=J, F1=Fq.

L omits4,q, while F omits1,2. Their immediate kernels together are
the four-cycle G with edges14,24,1q,2q. Every G edge joins {1,2}
to {4,q}. Each letter image omits one whole side, hence contains no
G edge. No distinct pair maps into G under either letter, and each
immediate kernel is contained in G. Therefore G is backward closed:
the only mergeable pairs are its four edges. The automaton cannot
synchronize (for example pair03 is never merged). This covers all
ordinary permutations in this hard profile without fixing their labels.

## gamma=1, delta=4

If L has a predecessor x of2, {u,x} follows L F into a singleton,
because Lu=4 and F4=F2=5. Thus L omits2 and maps J bijectively to J,
with L2=Lq for a unique q in J.

The seven distinct F(J) outputs form T minus {z}, for some z in T.
If z is neither2 norq, the distinct outside-K F-predecessors of2,q
follow F L into a singleton. Hence z is2 orq.

If z=2, incoming coverage of state2 forces F1=2 (L already omits2).
F permutes J. Choose x in J with F^2 x=q. The protected pair {5,x}
follows F^2 L to a singleton, since F^2 5=2 and L2=Lq. Contradiction.

Now z=q, so F(J)=T minus {q}. If F1=q, let r be the J-predecessor
of2 under F. For r different fromq, choose x in J with Fx=r; then
{5,x} follows F^2 L into a singleton, since F^2 5=q and F^2 x=2.
If r=q, the port values are F1=q,Fq=2. Here a short actual-image
argument replaces a pair shortcut: pre_F(E)={q},pre_(F^2)(E)={1}.
The one-count conditions on SF and SF^2 force q,1 into S. Since S
meets C={1,4} once,4 is absent; since it meets E={2,4} once,2 is
present. But L2=Lq then collides two S states in one letter. This
contradicts safety. No guessed reachability path or multiplicity is used.

Otherwise F1=Fr for a unique r in J. If r differs fromq, a J input
x with Fx=r exists because r belongs to T minus {q}. The protected
pair {5,x} follows F^2 into a singleton: its first images are1,r and
F1=Fr. Therefore r=q. The final hard profile is

    L(J)=J, L2=Lq; F(J)=T minus {q}, F1=Fq.

Again the immediate kernels are exactly G={14,24,1q,2q}. L omits1,2,
and F omits4,q; each image is independent in G. Thus no pair maps
into a G edge under either letter and the same backward-closed
four-cycle obstruction prevents synchronization. All cases have failed.

## Complete independent audit and scope

The exact kernel inventory preserves all six earlier E24 field pairs:
96 row patterns (including unused rows retained from the original
admission) and384 compatible kernel pairs. The checker independently
reconstructs their partitions using the earlier independent outside-K
block insertion, not the generator.

Complete over-approximate literal row controls at n=7,8,9 have512,
10,368,294,912 pairs. They retain every possible ordinary output system
under the local row/cover templates, including two harmless protected
variants not admitted by the earlier strong-connectivity condition.
No equality claim at smaller n is inferred. Every short word above
is evaluated directly, and hard cases have their literal inverse
graphs checked. The initial-image exception is checked with all sixteen
Boolean assignments of states1,2,4,q; no assignment satisfies its
one-count and safety conditions.

Complete individual thirteen-state hard-profile controls cover all
seven labels of q and423,360 full letters, with all ordinary permutations
and protected variants. Both orientations of the hole sets are included.
The symbolic four-cycle argument covers arbitrary pairs of such letters;
this is not a full n13 transition-pair enumeration. All392 initial
nine-set controls (56 per q) confirm the one-count exception's
incompatibility. No solver timeout or ordinary-label representative is
used to establish any exclusion.

All six E24 fourth-field pairs are discharged. After this cut, before
the separate E16 exclusion, the B0/C14/D5 branch has three remaining
binary fourth geometries E={6},{1,6},{2,6},
21 labelled E choices and88 field pairs. They still cover all fourteen
original D={5} typed third pairs. Unrestricted retains its six fourth
geometries; the binary incoming argument is not extended. Joint23
binary/42 unrestricted, third binary152/784 and unrestricted349,
and both F intervals[11,12] remain unchanged. The accepted article
and109-file supplementary package are unchanged.

Run enumerate_b1_partial_cover_e24.py then check_b1_partial_cover_e24.py
with Python>=3.10, assertions enabled. A separate auxiliary certificate
reproduces the inventory and independent audit byte-identically.
