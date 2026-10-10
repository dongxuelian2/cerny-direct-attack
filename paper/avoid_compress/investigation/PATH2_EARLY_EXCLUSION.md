# Path early-type-2 exclusion at codimension three

**Claim.** For n>=6, a strongly connected synchronizing automaton cannot
have an (n-3)-set of shortest compression length ten and early merging
pairs P1={01}, P2={01,02}, P3={01,02,13}. The alphabet is arbitrary finite;
reachability of the set is not needed for this necessary exclusion.

The short-pair refinement and its hypotheses are in
SHORT_PAIR_STRUCTURE.md and EARLY_PAIR_TYPES.md. They force every letter
to be a permutation or a rank-(n-1) transformation with common kernel 01.
Every inverse pair of 01 lies in P2 and every inverse pair of 02 lies in
P3. Write C={0,1,2,3}; an outside state means a state outside C.

## Images, domains and the accounting of lengths

The three-hole sets covering P3 are exactly the four triples in C and
01x,03x,12x for outside x. Let H be this family. Every image of the initial
set reached within six letters has holes in H; otherwise a further word
of length at most three compresses the initial set within nine letters.

Let R_i be the distinct images reached within i letters. Until compression
occurs this family grows strictly: equality R_i=R_(i+1) would make it
invariant under every letter, and a reset word could not compress any
member. Thus |R_i|>=i+1 for i<=9.

For a finite list W of test words of maximum length L, let D(W) consist
of H in H for which every test word preserves the set size and produces
holes again in H. Then R_(6-L) is contained in D(W). Consequently
|D(W)| must be at least 7-L. Failure of a test from D(W) gives compression
in at most L+3 further letters (or already compresses during the test).
Hole actions below always mean complements of actual images, not
preimages of subsets.

## Compatible letters

Every singular letter omits 0. Indeed its missing output must be 0 or 1,
because otherwise inverse pairs of 01 either are disjoint from 01 or
contain both 0z and 1z, incompatible with P2. If it omitted 1, inverse
pairs of 02 would similarly either be disjoint from 01 or contain both
0z and 1z. Neither possibility belongs to P3. Write such a letter f as
f0=f1=c, f2=t, f3=z, where c,t,z are distinct and nonzero.

Permutations fall into three classes, by their specified core rows:

* A: (0,1,2,*) on C;
* B: (0,2,1,*) on C;
* T: (*,*,*,*) with T0=1, T1=0, T3=2.

The free image in B is 3 or outside C; that in T is T2=3 or outside C.
Call these closed and mixing respectively. There is a B permutation:
the new inverse pair 02 of 01 must arise from a permutation, and class
T has inverse pair 01 instead. There is also a T permutation: only it
has inverse pair 13 of 02. Singular letters omit 0, so create neither
of those new inverse pairs. The classification follows directly by
intersecting the inverse pairs of 01 and 02; their common inverse
endpoint is the preimage of 0.

## Permutation mixing

Direct hole substitution gives the following domain bounds. Juxtaposition
of letters is right action, so TB means first T, then B.

| Letters | Tests W | L | Maximum | Core holes and outside restrictions |
| --- | --- | ---: | ---: | --- |
| B mixing, T mixing | B,T | 1 | 5 | 012,023; at most one outside choice for each of 01,03,12 |
| B mixing, T closed | B,TB | 2 | 5 | 023,123; 01v,03v,12u, where v=B^-1(3), u=T^-1(v) |
| B closed, T mixing | B,T,TT | 2 | 4 | At most three core holes and one outside hole, or two core holes and two outside holes |
| B,T closed, A mixing | A,B,TA | 2 | 4 | 012,013; at most 03v and 12T^-1(v), v=A^-1(3) |

In the first row v=B^-1(3) fixes the outside choice for 01 and 03,
and T^-1(3) fixes it for 12. The bound five contradicts |R5|>=6.

In the second row, membership of 01v further requires T(v)=v. Equality
five therefore forces u=v, and its domain is exactly

    D={023,123,01v,03v,12v},  v outside C, T(v)=v.

If its size is smaller than five, |R4|>=5 gives a contradiction. The
equality case is treated by the complete finite projection below.

For the third row put a=T2 outside C and v=T^-1(3). If v=a, the
possible core holes are 012,013,023 and the only outside hole is 12v:
T^-2(3)=2 is in C. If v!=a, only 012,013 remain among core holes,
and at most 12v,03T^-2(3) remain outside. Both give the stated four.
In the last row A preserves 012 and sends 3 outside. The B test deletes
all 01x; the A and TA tests restrict the other two types to the listed
unique preimages. These two rows contradict |R4|>=5.

## Complete five-image projection

In the equality case all five images of D are reached by depth four.
Every letter must send every one of them to an H-image, because depth
five is still at most six. Relabel v as 4 and order D as displayed above.
Project each compatible letter to its five successor indices, using
EXIT=-1 when its successor belongs to H but not D.

This is a parameter-independent finite enumeration. A permutation has
one of the three core templates above and arbitrary injective remaining
images. A singular row has form (c,c,t,z,u), with c,t,z,u distinct and
nonzero. Images of 023 and 123 require t or z to be 1 or 3; that of
014 requires c or u to be 1 or 3. These are disjoint groups of distinct
outputs, so both 1 and 3 must occur among the four outputs. At most two
additional fresh labels are needed. Thus output labels 0,...,6 represent
every possible partial row, for every n; extra labels not in C union {4}
are interchangeable. Rows that do not extend at a particular small n
may be included: this only enlarges the candidate action set.

The enumeration gives exactly 22 action profiles, with a separate flag
recording whether EVERY underlying partial row preserves E=C union {4}.
Synchronization forces every D-vertex eventually to exit D. Finite exit
distances are at most five. If the initial vertex has distance five, a
shortest exit path uses all vertices, whose distance vector must therefore
be a permutation of 1,...,5. For each of the 120 vectors d, include all
profiles p satisfying

    d(i)<=1+d(p(i)),  d(EXIT)=0.

If even this enlarged graph does not permit every vertex to exit, an
actual synchronizing alphabet with that vector is impossible. Exactly
one vector survives: (4,3,5,1,2). Its allowed profiles are precisely

    (0,1,2,3,4), (1,0,2,4,3), (2,4,0,3,1), (2,2,0,-1,3).

For every underlying row of these profiles, E is invariant. Since |E|=5
and n>=6, strong connectivity is impossible. Otherwise the first exit
has length at most four. Appending a failed defining test of length at
most two and a merging word of length at most three compresses within
4+2+3=9. Thus mixing B is excluded, and the preceding cases show that
all permutations preserve C.

path2_reduced_actions.py constructs the structural templates and uses
reverse exit closure. audit_path2_actions.cpp independently enumerates
literal forward partial rows, tests inverse pairs and holes directly,
and searches forward from every domain vertex. They agree on every
profile, every underlying-row closure flag and the candidate vector.
The C++ implementation also passes ASan/UBSan with an identical report.
The reports are path2_reduced_actions.json, path2_actions_independent.json,
codimension_three_upper_audit.json. No alphabet-size cutoff is used.

## Singular mixing once permutations preserve C

Choose a closed B and T. Strong connectivity requires a singular f that
does not preserve C. Retain f0=f1=c, f2=t, f3=z. Say t or z is good when
it belongs to {1,3}. Direct substitution gives:

| Good images among t,z | Tests | L | Domain bound |
| --- | --- | ---: | ---: |
| neither | B,f | 1 | 4 |
| exactly one | B,f,Tf | 2 | 4 |
| both | B,fB,TfB | 3 | 4 |

For the first row B excludes 01x. The holes 023,123 fail f. If c is
1 or 3, the two other core holes may remain, but only the other member
of {1,3} has an outside preimage; each of 03x and 12x has at most that
one choice. If c is neither, no core hole remains and each outside type
has at most two choices. Both counts are at most four.

In the second row T swaps 012 with 013, so the tests f,Tf retain either
both of these holes or neither. The holes 023,123 are similarly paired.
Each outside type has at most the unique outside preimage of the other
member of {1,3}. If all four core holes remain, c must be that other
member, so this outside preimage does not exist. Thus again the count
is at most four. The first two rows contradict respectively |R5|>=6
and |R4|>=5.

In the last row {t,z}={1,3}; mixing forces c outside C. Let v=f^-1(2),
u=T^-1(v), both outside C. The domain has exactly FOUR holes:

    t=1,z=3: D={023,123,12v,03u};
    t=3,z=1: D={023,123,03v,12u}.

It is not a two-image domain. Both 023 and 123 have f-image holes 013,
which is outside D, so two distinct vertices have exit distance one.
Every vertex must exit under synchronization. In a four-vertex graph
with two distinct distance-one vertices, maximum exit distance is at
most three: a shortest distance-four path would use distinct vertices
of all four levels, leaving only one vertex at level one. The initial
vertex is in D. Its exit takes at most three letters; a failed defining
test takes at most three more, and a P3 merge at most three more. Thus
compression has length at most nine. This excludes the last singular
mixing possibility and contradicts strong connectivity.

audit_path2_domains.py independently computes ordinary subset actions
for every compatible letter at n=6 and n=7 (137 and 791 letters). It
checks every row of the domain tables, the five-image equality case,
the exact four-image last domain and its two immediate exits. These
are finite controls of the symbolic proof, not extrapolation to larger n.
The saved report is path2_domain_audit.json.