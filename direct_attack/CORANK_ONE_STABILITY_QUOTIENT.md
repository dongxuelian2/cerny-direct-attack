# Stable kernels and the canonical group quotient

Date: 2026-10-01. **PROVED (paper)**, arbitrary alphabet, all finite n.
The synchronization assertions are structural, with no general word-cost
bound. Reconstruction/generalization of standard stability arguments;
publication priority **OPEN**, unrestricted Cerny **OPEN**. No formal claim.

## A defect-one kernel is stable

Let A be strongly connected. Other letters may have ANY ranks. If f has
rank n-1, its unique kernel pair K is stable: after EVERY original prefix
v there is an original suffix merging K v.

A rank n-1 functional graph consists of cycles and exactly one nonempty
tail attached to one cycle. There is one missing image state (the leaf)
and one double-image state (the root). If the double-image state were
off a cycle, a further cycle entry would have indegree at least2, which
is impossible. Thus the off-cycle vertices form a single tail. Write
its height h>=1, its leaf l, its height1 vertex t, and the cycle predecessor
of its root c. The kernel pair is {t,c}.

Choose an original minimum-rank image F containing l. Such an image
exists: start from ANY minimum-rank word image and use strong connectivity
to send one of its states to l. Every image of a minimum-rank image again
has minimum size r. In particular its points are pairwise unmergeable.
Then F'=F f^(h-1) has t as its ONLY off-cycle point; its other r-1 points
are cyclic. Let L be a common positive multiple of all f-cycle lengths.
The image F''=F' f^L replaces t by c and fixes all other points. The
point c is not already in F', since f would then lower its minimum rank.

These two minimum-rank images differ by exactly t/c. For ANY prefix v
and ANY fixed minimum-rank word u, both F' v u and F'' v u still have
r points. Their common r-1 points remain distinct, while their two
remaining points must coalesce: the union is mapped inside Q u, which
has only r points. Therefore t v u=c v u for EVERY v. This proves the
claim, even with the SAME u for all prefixes. The construction uses
minimum-rank existence and the possibly large cycle period L; it supplies
no short merging word.

The differing-F-clique argument and almost-group special case are standard;
see [Berlinkov--Nicaud2018, Lemmas1--3](https://arxiv.org/pdf/1805.02154).
The broader unimodal/primitivity consequence is already known from
[Volkov2023](https://arxiv.org/pdf/2306.13317), and stable-vector methods
from [Kari2002](https://pdfs.semanticscholar.org/39e7/64a18388e249f90180ff37ea816d462cdf11.pdf).
None of these known qualitative synchronization results is claimed new.

## All letters of corank at most one

Assume now that EVERY original letter has rank n or n-1. Let sigma be
the stability congruence. It is an equivalence relation: to merge x/y
and y/z after a prefix, first merge x/y, then merge their common image
with z using stability of y/z. Appending a letter preserves stability.

Every quotient by a congruence still has letter corank at most1. Indeed
every missing quotient class contains an original state missing from
the letter image, and different missing classes require different such
states. Strong connectivity also passes to the quotient.

Stability on A/sigma is equality. A stable pair of distinct sigma-classes
would lift to stable original points: after every prefix first merge the
quotient pair into one class, then merge inside that stable class. This
contradicts distinctness of its sigma-classes. By the defect-one lemma,
every letter on A/sigma is consequently a PERMUTATION.

Any pair merged by ANY original word must therefore already belong to
sigma: different quotient states cannot merge under permutations. Thus

    mergeability = stability = sigma.                     (1)

This is special to the stated SC and corank conditions. It need not hold
for general DFAs. Every minimum-rank word u has EXACT kernel sigma.
For one inclusion, if x sigma y but xu!=yu, stability would allow a
further merge inside the minimum-rank image Q u, contradicting minimality.
For the other, xu=yu implies mergeability and hence (1). In particular
ALL minimum-rank words have the SAME kernel and their rank is exactly
the number of stable classes.

Let beta be the least congruence whose quotient letters are permutations.
It can be computed without guessing reset words: start with singleton
classes, pass to the current quotient, join its letter kernels and all
their forward images to a congruence, and pull the joined classes back.
Repeat until every quotient letter is a permutation. Each nontrivial
round reduces the class count; there are at most n-1 rounds. Each stage
is contained in sigma, since the SC corank-one quotient kernel pairs
are stable and stability lifts through classes already inside sigma.
At termination any mergeable original pair lies in beta, by injectivity
of the permutation quotient. Hence

    beta=sigma;  A synchronizes IFF beta has one class.    (2)

This repairs the necessity failure of a SINGLE forward kernel closure:
the common-kernel chain in ORIGINAL_KERNEL_GRAPH_BOUNDARY.md requires
successive ORIGINAL quotient merges. It does not repair its cost problem.
Joining stable pairs or performing quotient rounds does NOT give actual
reset words of those round counts or forest label costs.

## A sharp bound on the stable class-size range

Let s be the number of singular ORIGINAL LETTERS. For every SC input
as above, if m and M are the minimum and maximum stable class sizes,

    M-m<=s.                                               (3)

For a permutation letter, every stable class is carried bijectively to
its target class, so class sizes are preserved. For a singular letter f,
its quotient permutation phi has exactly one kernel-source class X
and one missing-image class Y. Every target class D has a UNIQUE incoming
source class C and contains all its states except the single missing
state when D=Y. Consequently

    |phi(C)|=|C|-1_(C=X)+1_(phi(C)=Y).                     (4)

Summing (4) around each phi-cycle shows that the two distinguished changes
belong to the SAME quotient cycle, or cancel in one step. Other cycles
have constant sizes. The distinguished cycle uses either a single size
or two adjacent sizes. Thus ONE singular letter can cross at most ONE
integer size boundary. A quotient path between a class of size m and
one of size M crosses each of the M-m boundaries, and each boundary
needs a distinct singular-letter type. Strong connectivity proves (3).

The bound is sharp for EVERY s>=1. Use classes C_j of size j for
j=1,...,s+1, with n=(s+1)(s+2)/2. One permutation letter g rotates every
class. The singular letter f_j exchanges C_j and C_(j+1): it sends the
j smaller-class points to the first j larger-class points, the first j
larger-class points back to their counterparts, and the final larger
point to the first smaller point. All other points are fixed. Its rank
is n-1 and its quotient is the adjacent class transposition.

The original automaton is SC because g moves within every class and the
class transpositions connect all classes. No word has rank below s+1,
since its quotient is a permutation. The ACTUAL word u_h=f_(h-1)^2 is
the unit mapping the final point of C_h to its first point, and fixes
every other point. On C_h, v_h=g^(h-1)u_h fixes0 and maps i>0 to i-1.
Thus

    w_h=u_h v_h^(h-2), |w_h|=h(h-1),                       (5)

merges C_h and preserves every class. Concatenating w_2,...,w_(s+1)
gives an original rank-(s+1) word of total charged length
s(s+1)(s+2)/3. By (1), the stable classes are exactly these C_j, and
M-m=s. This is a nonsynchronizing sharpness family, NOT a reset certificate.

## Boundary checks

The SC condition cannot be dropped: on three states take
f=(0,0,2), g=(0,2,2). Both letters have rank2, but the mergeable pair
{0,1} becomes the deadlock {0,2} under g. The two mergeable edges
{0,1}/{1,2} also fail transitivity. States0 and2 are distinct sinks.

The generator compares forward pair-reachability with repeated quotient
kernel joins. The independent checker uses COMPLETE original transformation
monoids on all recorded small SC inputs, reconstructs mergeability and
ALL minimum-rank kernels, and uses a separate bidirectional equivalence
closure for beta. The sharp families are checked from independently
constructed rows and charged class-rooted words. Finite computations
are COMPUTATIONALLY VERIFIED only within their recorded scopes.
No formalization, priority, short minimum-rank word or general square
bound follows from the paper proof. The main remaining problem is still
compatible ORIGINAL word costs.

Completed finite scope:28816 all-corank<=1 binary inputs n2..4,
12551 SC inputs,804310 COMPLETE original monoid transformations and
60426 ALL minimum-rank kernel controls. Separately37358 defect-one /
arbitrary-other binary inputs contain13348 SC cases,661550 monoid
transformations and432756 common-minimum-word/kernel-orbit controls.
The21 sharp parameters s1..16,20/24/32/64/128 reachn8385, with2505120
unit state/letter controls,860228 literal root controls,1556448 whole
rank-word state/letter controls and8 corruption rejections. The two
small exhaustive scopes overlap; their input counts are NOT added as
disjoint automata. Registry116/199 archives115 verbatim, then appends
only this deterministic generator/replay and independent checker.
This is not a fresh full116-check rerun or formal instantiation.
