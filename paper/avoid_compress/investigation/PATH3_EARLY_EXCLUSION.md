# Path early-type-3 exclusion at codimension three

**Claim.** For n>=6, a strongly connected synchronizing automaton cannot
have an (n-3)-set of shortest compression length ten and

    P1={01}, P2={01,02}, P3={01,02,23}.

The alphabet is arbitrary finite, and reachability of the set is not needed.
SHORT_PAIR_STRUCTURE.md supplies the credited short-pair reduction. Let
C={0,1,2,3}. Three-hole sets covering P3 form the family H consisting of
the four triples in C and 02x,03x,12x for x outside C.

As in PATH2_EARLY_EXCLUSION.md, every image reached within six letters
has holes in H. Distinct reachable images grow strictly until compression,
so |R_i|>=i+1 through depth nine. For tests of maximum length L, their
common H-preserving domain must contain R_(6-L), hence have at least 7-L
vertices. Exiting that domain gives compression after at most L+3 further
letters. These length charges always use original letters.

## Compatible letters

Every letter is a permutation or a rank-(n-1) map with common kernel 01.
Its inverse pairs of 01 belong to P2, and those of 02 belong to P3.
The permutation templates are:

    A: (0,1,2,*) on C;
    B: (0,2,1,*) on C;
    T: (1,*,0,2) on C.

A,B are closed when their last core image is 3; T is closed when T1=3.
Otherwise that image is outside C. Singular letters either omit 0,
with f0=f1=c, f2=t, f3=z distinct and nonzero, or omit 1 with one of

    D0: (c,c,0,2),  D2: (c,c,2,0),  c>=3.

These last letters are closed when c=3, otherwise mixing. To check
completeness, a singular missing output is 0 or 1 by the inverse-pair
01 test. If it omits 1, its kernel image cannot belong to 02: that would
create both 0x and 1x as inverse pairs, which cannot both lie in P3.
The inverse pair of 02 must therefore be the disjoint pair 23, giving
the two displayed orientations. The permutation templates follow by
intersecting the inverse pairs of 01 and 02. Growth from P1 to P2
requires B or T; growth from P2 to P3 requires T or D0 or D2.

## A mixing T permutation

Put a=T1 outside C and v=T^-1(3). Test T and TT. If v!=a, their common
domain is contained in {02v,12v,03v,03T^-1(v)}, of size at most four,
contradicting |R4|>=5. If v=a, the domain is exactly

    D={013,123,02v,12v,03v}.

All its five images are reached by depth four; every letter sends each
of them to an H-image. Relabel v=4. Complete projection of compatible
letters gives 24 profiles. As synchronization requires every vertex
to exit D, a first exit of length five requires the five exit distances
to be a permutation of 1,...,5. For every such vector d, include ALL
profiles p with d(i)<=1+d(p(i)), d(EXIT)=0, and check that every vertex
can exit. Exactly one of the 120 vectors survives: (4,1,5,3,2).
Every underlying partial row of every allowed profile preserves the
five-state set C union {v}. This contradicts strong connectivity for
n>=6. Otherwise first exit has length at most four and a failed T/TT
test followed by a P3 merging word compresses within 4+2+3=9.

The finite projection is complete for every n. Only the five distinguished
input states matter. For singular missing-0 rows the three domain tests
013,123,02v (and 03v) force both 2 and 3 among their four distinct
nonzero outputs: if only one were present it could not meet all the
requirements on (c,z),(t,z),(t,fv),(z,fv). At most two fresh outside
labels are needed. Singular missing-1 rows already use outputs 0,2;
their two other distinct outputs need at most two fresh labels.
Thus labels 0,...,6 suffice, including represented v=4. Permutations
use the A,B,T templates. No alphabet-size bound is imposed.

path3_mixing_actions.py uses structural templates and reverse exit
closure; audit_path3_mixing.cpp independently enumerates all literal
forward partial rows, checks inverse pairs, and searches forward from
each domain vertex. Every profile and row-closure flag matches. The
reports are path3_mixing_actions.json, path3_mixing_independent.json and
path3_mixing_audit.json. ASan/UBSan also pass with identical output.

The n=5 boundary is real. Rows (1,1,2,3,4), (1,4,0,2,3), S={1,3}
are strongly connected and synchronizing, with reaching word abbabba
and reset word abbbbabbbbabbbba. Ordinary BFS gives projected exit FIVE
and actual compression TEN. The invariant five-state set is then all
of Q; consequently the claimed exclusion retains n>=6.

## A closed T permutation

Now T on C is (1,3,0,2). Its outside action is a permutation. For an
additional letter g, let D2(T,g) be the domain preserving H under all
words of length at most two on T,g. Direct substitution gives:

| Mixing g | Domain is contained in | Definition of v,u |
| --- | --- | --- |
| A | 123,03v,12u | v=g^-1(3), u=T^-1(v) |
| B | 012,03v,12u | same |
| D0 | 013,03u,12v | same |
| D2 | 023,123,12u | same |

For A, the tests g,gT,Tg remove respectively core 013,023,012;
for B they remove 023,013,123. Their outside constraints require
gx=3 for 03x and g(Tx)=3 for 12x. In the D0 case gg removes 023,123
and g removes 012; its 013 survives only if g(g0)=3, equivalently g0=v, while
the outside restrictions give the displayed unique preimages. In D2,
g removes 013, Tg removes 012, and gg removes every possible 03x.
These observations verify all four rows. Every domain has size at
most three, contradicting |R4|>=5. Thus every permutation and every
missing-1 letter preserves C. Strong connectivity requires a mixing
missing-0 letter f with core images c,t,z.

Call a core output good if it is 2 or 3. If at most one of c,t,z is
good, D2(T,f) has at most four vertices. With none good there are no
core holes, and each outside type 03x,12x has at most the two outside
preimages of 2,3. With only c good, there is at most core 012 and one
outside choice for each type. With only t good, core holes are among
023,123, with at most 03v,12T^-1(v); with only z good they are among
013,123, with at most 12v,03T^-1(v). Here v is the outside preimage
of the other good output. These counts are at most four.

If c and one of t,z are the two good outputs, the remaining core image
is outside C (otherwise f is not mixing). All outside holes are removed
by f and Tf. At least one core hole is removed by fT: if c=2 it is
013 when z is outside, or 012 when t is outside; if c=3 the holes
023,123 are removed. The domain then has size at most three.

It remains that c is outside and {t,z}={2,3}. Set v=f^-1(1) and
u=T^-1(v), both outside C. Compute D3(T,f), the domain preserving H
under all words of length at most three:

    t=2,z=3: D3={013,123,03u};
    t=3,z=2: D3={023,123,03v}, plus 12u iff f(u)=v.

For completeness the two-step domains before the last tests are

    t=2,z=3: {013,023,123,12v} union {03x: x outside C};
    t=3,z=2: {012,023,123,03v} union {12x: x outside C}.

Requiring their T- and f-successors to remain in those domains gives
the displayed D3 sets directly. Their sizes must be at least four
because |R3|>=4. Only t=3,z=2 and f(u)=v survive. Since f(v)=1,
u!=v. Relabel u=4,v=5 and order the remaining domain as

    D={023,123,124,035}.

All four images are reached by depth three, so every letter maps them
to H. The complete projection has 19 profiles. A first exit at length
four requires one of the 24 permutations of distances 1,...,4. None
allows every vertex to exit. The first exit therefore has length at
most three; a failed test of length at most three and a P3 merging
word compress within 3+3+3=9. This excludes closed T as well.

This second finite projection also has parameter-independent coverage.
Permutations use the closed A,B,T core rows, missing-1 letters the two
closed D rows. A missing-0 row has five distinct nonzero outputs from
six inputs. The domain tests on 023/123,124,035 force both 2 and 3
among those outputs. Thus at most three fresh labels are needed and
labels 0,...,8 cover every partial row. path3_closed_T_actions.py and
audit_path3_closed_T.cpp independently give the same 19 profiles and
24 negative distance checks. audit_path3_closed_T_domains.py verifies
every stated domain reduction by literal subset actions at n=6,7.

## No T permutation

There must now be a B permutation and a D0 or D2 letter. A closed D0
is impossible even alone: its common domain for D0,D0D0 is precisely
the four core holes, fewer than |R4|>=5. A mixing D0 together with B
also has a two-step domain of size at most four. To see this write
v=D0^-1(3). The D0 and D0D0 tests leave at most core 013, only if
D0(v)=3 with v=D0(0), and outside holes 12v,02v,03x with x=v or
x=D0^-1(v). If B is closed it removes 02v; if core 013 is present,
D0^-1(v) is not outside, giving at most three vertices. If B is mixing,
its test forces x=B^-1(3) for 03x and for 02x. There are then at most
one core hole and three outside holes. Both counts are at most four.
Thus no D0 letter exists, and a D2 letter is necessary.

If the alphabet consisted solely of A,B permutations and D2 letters,
the family of holes 12x (x!=1,2, including x=0,3) would be invariant.
A,B preserve the pair 12. A D2 letter sends 120 to 12c and any other
12x to 12D2(x); these are again three distinct holes. This invariant
family of uncompressed (n-3)-images contradicts synchronization.
There is therefore a missing-0 letter f.

Choose one B=b, one D2=d and such an f. Let beta be 1 when b is mixing,
epsilon be 1 when d is mixing. In their common H-domain, 02x has at
most the single outside choice b^-1(3), available only when beta=1;
03x has at most the outside choice d^-1(3), available only when
epsilon=1. Core 023 is absent if beta=1, and core 013 is absent if
epsilon=1. Let c=f0=f1, t=f2, z=f3.

First suppose t is neither 2 nor 3. If neither c nor z is good, all
core holes fail and each outside type 02x,12x requires fx in {2,3};
there are at most two 12x and at most one of each other type, totaling
four. If only c is good, core holes are among 012,013, and all outside
types require the unique outside preimage v of the other good output.
There are at most three outside holes; if all three are present, both
b and d are mixing and core 013 is absent, again totaling at most
four. If only z is good, core holes are among 013,023,123; the possible
02x,03x are paid for by the respective losses of 023,013, leaving at
most three core/outside-extra holes plus the one possible 12x. If both
c,z are good, 02x and 12x are impossible since neither good output
has an outside preimage. The possible 03x is paid for by the absence
of core 013. In each case the one-step domain has size at most four.

Now suppose t=2 or t=3 and use all tests of length at most two on b,d,f.
Define a two-element output-target set V by

    t=2: V={1,b^-1(3)};
    t=3: V={2,w}, w=1 if d is closed, w=d^-1(3) if d is mixing.

The test fb in the first case, or fd in the second, forces fx in V
for every allowed outside 12x. Put a=[c in V], h=[z in V]. The kernel
output c and core output z have no outside preimages, so at most
2-a-h outside 12x survive. The same test requires c in V for core
012, and z in V for core 023,123. Hence the core count is at most

    a + h(2-beta) + (1-epsilon).

The last term bounds core 013, and the beta term removes 023 under
mixing B. The other two outside types contribute at most beta+epsilon.
The total domain size is therefore at most

    a+h(2-beta)+(1-epsilon)+(2-a-h)+beta+epsilon
       = 3+h(1-beta)+beta <= 4.

This also covers the common-kernel issue in fd: when d is closed,
preimages of output 3 are 0,1, but f omits 0, leaving only target 1.
When d is mixing the preimage is the unique outside state d^-1(3).
All targets in V are distinct and neither equals t.

Thus the common two-step domain on b,d,f has at most four images,
contradicting |R4|>=5. This completes the no-T branch and the claim.

audit_path3_no_T.py checks every literal compatible triple from the
complete n6/n7 pools, including all indicators and counts in the last
inequality. audit_path3_no_T.cpp independently generates all full rows
without reading those pools and computes complement-of-subset actions.
Both check 4320 triples at n6 and 414720 at n7, with maximum domain
size four. They also supply controls for mixing D0 with B. The proof
above is uniform; the finite controls are not used for extrapolation.

## Reproduction

From the supplementary directory, with standard-library Python >=3.10
and clang++ (or another C++17 compiler):

    python -B path3_mixing_actions.py
    clang++ -O2 -std=c++17 audit_path3_mixing.cpp -o path3_mix
    ./path3_mix path3_mixing_independent.json
    python -B audit_path3_mixing.py
    python -B path3_closed_T_actions.py
    clang++ -O2 -std=c++17 audit_path3_closed_T.cpp -o path3_closed
    ./path3_closed path3_closed_T_independent.json
    python -B audit_path3_closed_T_domains.py
    clang++ -O2 -std=c++17 audit_path3_no_T.cpp -o path3_no_T
    ./path3_no_T path3_no_T_independent.json
    python -B audit_path3_no_T.py

On Windows add .exe to executable names. The domain checkers use the
complete early_alphabet_pool_n6.json and early_alphabet_pool_n7.json
generated by early_pair_alphabet_pool.py; the standalone native no-T
audit generates all its rows independently of those files. The boundary
checker imports only the independent ordinary-BFS utilities in
verify_certificates.py. Assertions must remain enabled.

## Scope