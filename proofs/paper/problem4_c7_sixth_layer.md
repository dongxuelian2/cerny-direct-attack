# Excluding a seven-cycle at the sixth short-pair layer

10 October 2026. AI-assisted continuation; priority OPEN. This is a new
computer-assisted branch exclusion, with a uniform mathematical reduction
and two independent finite checking approaches. It is not Lean verified.
All lengths are original-letter lengths; all alphabets are arbitrary finite.

**P4-C7-SIXTH — PROVED ON PAPER (computer-assisted).** Let n>=8. In a
strongly connected synchronizing n-state automaton with an (n-4)-subset S
satisfying c(S)>=12, P6 cannot be C7 plus n-7 isolated vertices. Initial
subset reachability and a protected set are not required.

This excludes one further graph branch. It neither proves tau(P6)<=3 nor
determines F_bin(13,9,1) or F(13,9,1). The earlier repository theorem rules
out C7 at P5; the statement here concerns the later layer P6.

## 1. A uniform reduction to seven subset positions

Assume P6 is a seven-cycle C, with isolated vertex set J. The independent
(n-4)-sets are precisely

    F = {J union T : T is a maximum independent triple of C}.

There are seven triples: their cyclic gaps are 2,2,3. For every |w|<=5,
Sw belongs to F; otherwise w already compresses S or its image contains a
P6 edge, yielding compression within eleven letters. In particular S is
one member of F. Let R_i consist of its images through depth i.

Strong connectivity and synchronization imply the trajectory span has
dimension at least min(i+1,n): a plateau is invariant under every letter,
and reset words followed by state paths span all coordinate rows. Thus
R4 spans dimension at least five and contains at least five distinct sets.
Each letter maps these into F, preserving cardinality.

By the rank-transfer argument in
[the short-pair note](problem4_short_pair_peeling.md), every letter has
rank at least n-2. Its kernel pairs belong to C, so its nontrivial fibers
are disjoint cycle edges, at most two of them. Every J input is a singleton
fiber, distinct also from every core input fiber.

At most one J input can map into C. Indeed, two such inputs have distinct
images x,y in C, and the images of all R4 sets contain x,y. At most two
maximum independent triples of C7 contain a fixed pair. To check this
last fact, adjacent pairs occur in none; pairs at cyclic distance two
have two choices of a third vertex, and pairs at distance three have one.
Their characteristic rows, even after adjoining J, span dimension at
most two. But a map with nullity at most two sends a space of dimension
at least five to one of dimension at least three. Contradiction.

If no J input maps into C, the letter permutes J and maps C into C.
If exactly one does, say j0 maps into C, the other |J|-1 inputs have
|J|-1 distinct outputs in J. The remaining J output j1 must be supplied
by exactly one core fiber, since every output member of F contains J.
All other core fibers map injectively to distinct core outputs different
from the image of j0.

Therefore the action on F and on pairs whose two outputs lie in C is
represented exactly by a map on C union {j}: identify the *input* j0 with
j and the *output* j1 with j, and discard the other isolated coordinates.
For the no-crossing case fix j. This is a projection of one letter's
relevant data, **not** a conjugacy of its transformation. In particular,
powers of a projected map need not agree with powers of the real map;
no such power-based cut is used in either checker.

The eight-state representative has rank at least six, with kernel a cycle
matching of size zero, one, or two, and maps at least five of the seven
sets {j} union T back into that family. Conversely, we enumerate every
map satisfying these conditions, allowing extra maps if necessary.
This is a superset cover for every n>=8, not a finite-n extrapolation.

## 2. Complete letter domain

Label C as 0,1,...,6,0 and j as 7. Order the seven independent triples
by their integer bit mask:

    21, 37, 41, 42, 74, 82, 84.

Adjoin bit 128 to each. Each action has a seven-entry profile, with value
7 denoting EXIT (failure to lie in the family). There are

    8! + 7*(8P7) + 14*(8P6) = 604800

maps with a permitted kernel: the empty matching, seven one-edge
matchings, and fourteen two-edge matchings. Exactly 1484 maps preserve
at least five members. Their relevant signatures number 896.

A signature records the subset profile; the image of each cycle edge
(a collision, another cycle edge, or a pair outside C); and every cycle
edge that has a non-cycle input pair as a preimage. These are all the
facts used in the next stage. No assumptions about a common kernel,
permutation letters, binary alphabets, or a chosen early-layer chain
are imposed.

The partition/injection generator enumerates all 604800 maps once.
An independent generator enumerates all 8^8=16777216 literal transition
rows and filters by rank and pairwise kernel membership. The sorted
1484 retained rows agree byte for byte. Their displayed subset images
and all signature fields are independently reconstructed by Python.

## 3. Two interacting exact-distance requirements

Let d_i be the shortest EXIT distance from family member i in the actual
alphabet. Synchronization makes all seven values finite, between one
and seven. Every integer from one to max(d_i) occurs along a shortest
exit path. Relabel the cycle so that S is position zero; rotation is
transitive on the seven triples. Since EXIT in at most five letters
would compress S within eleven, d_0>=6. There are exactly 3960 possible
vectors satisfying these elementary constraints.

Let e_k be the actual shortest merging length of cycle edge k. Each lies
in {1,...,6}; every other distinct pair has merging length at least seven.
For a letter with subset profile a, its compatibility conditions are:

1. d_i <= 1+d_(a(i)), with d_EXIT=0.
2. If edge i collides immediately, e_i=1.
3. If edge i maps to cycle edge k, e_i<=1+e_k.
4. If a non-cycle pair maps to cycle edge k, e_k=6.

Condition 4 follows from 7<=1+e_k and e_k<=6. When a cycle edge maps
outside C, this relaxation imposes no extra upper-distance condition.
Immediate kernels are already constrained to C by the letter domain.

Exact finite distances also require a first-letter witness for each
position and each edge: for every i, some compatible letter has

    d_i = 1+d_(a(i)),

and for every k, some compatible letter either merges it with e_k=1 or
maps it to an edge l with e_k=1+e_l. The same alphabet must supply both
kinds of witness. For fixed distance vectors, include all compatible
signatures; this can only make finding the required witnesses easier.
Every genuine alphabet is contained in this pool, so failure of witness
coverage disproves that distance vector without limiting alphabet size.

## 4. Exact rejection and independent check

Ignoring pair distances, only fourteen of the 3960 subset-distance
vectors admit all their required first-letter witnesses. Their compatible
signature pools have respectively 3 to 23 elements. The C++ checker then
exhausts all 6^7=279936 pair-distance assignments for each of those
fourteen vectors: **3919104 joint vectors, zero survivors**.

The independent Python audit generates the subset vectors as multiset
permutations and uses reverse breadth-first search to identify the same
fourteen. It searches the full pair-distance domain by depth-first
assignment, pruning only when a partially specified vector has no
compatible supplier for some required descent. It visits **4946 partial
nodes**, including its candidate roots, and finds zero complete solutions.
Every pruned branch fails a necessary local inequality or an explicitly
required supplier; this is exhaustive arithmetic, not a solver status.

Both checkers accept an artificial positive control with subset profile
(1,2,3,4,5,EXIT,EXIT), pair action (1,2,3,4,5,MERGE,MERGE), no forced-six
constraints, and both distance vectors (6,5,4,3,2,1,1). The control tests
that the distance rejection is not caused by a blanket rejection bug;
it is not claimed to be an automaton letter.

The empty intersection of the necessary conditions contradicts the
hypothetical automaton. This completes the computer-assisted proof.
The normalized-action reduction in Section 1 supplies the all-n coverage.

## Reproduction

From the repository root, with Python 3.10+ and a C++17 compiler:

```sh
mkdir -p .reproduction/problem4
g++ -std=c++17 -O2 computations/src/problem4_c7_profiles.cpp -o .reproduction/problem4/profiles
.reproduction/problem4/profiles > .reproduction/problem4/profiles.txt
.reproduction/problem4/profiles --literal > .reproduction/problem4/literal.txt
cmp .reproduction/problem4/profiles.txt .reproduction/problem4/literal.txt
g++ -std=c++17 -O2 computations/src/problem4_c7_distances.cpp -o .reproduction/problem4/distances
.reproduction/problem4/distances < .reproduction/problem4/literal.txt
python computations/src/problem4_c7_audit.py .reproduction/problem4/literal.txt
```

No generated binary, cache, SAT output, or regenerated action table is
committed. Sources and exact counts suffice to regenerate the small table.
The initial SMT reconnaissance gave UNSAT, but is not a proof dependency.
