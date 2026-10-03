# Exact weighted returns and larger-cycle class-reset pressure

Date: 2026-10-01. The unrestricted proposal

    reset_A(C) <= (|C|-1)(n-1)

remains **OPEN**. This continuation gives an exact scorer for the fixed
two-class schema and fresh finite evidence at much larger n. It does not
establish the proposal, a new unrestricted reset bound, publication
priority, or a **FORMALLY VERIFIED** result.

## Exact weighted identity: PROVED on paper

Fix C={0,...,h-1}, O={h,...,h+t-1}, with h>=2 and t>=h. Letter a
injects C into O and is the full t-cycle on O. Letter b permutes C and
maps O onto C. This is a congruence; every candidate is strongly
connected. From a C-state, a enters O; from any O-state its a-orbit is
all of O, and b reaches every C-state.

Consider the h-state alphabet of actual C-return transformations

    B_0 = b|C,             weight(B_0)=1,
    B_j = (a^j b)|C,       weight(B_j)=j+1,  1<=j<=t.

On the nonempty subsets of C, let d_weight(C) be the minimum total
weight of a path from C to a singleton, or infinity if no such path
exists. Then, exactly,

    reset_A(C) = d_weight(C).

Proof. Every image of C is wholly in C or wholly in O. On either class,
a preserves cardinality, because its restriction to C is injective and
its restriction to O is a permutation. Thus every **shortest** resetting
word from C ends in b. (An arbitrary resetting word need not end in b:
one may append a after reaching a singleton.) Its unique decomposition
at successive b letters is a concatenation of blocks b or a^j b,
j>=1. After the first a of a positive block, the image lies in O;
therefore on C the block a^j b has the same transformation as

    a^(1+((j-1) mod t)) b.

Replacing a longer block by this representative preserves every
successive C-image and never increases length. Every shortest ordinary
reset therefore produces a weighted path of cost no greater than its
length. Conversely, every weighted path expands to its literal blocks
and produces an ordinary word of exactly that path's cost. The two
inequalities give equality, including equivalence of nonsynchronization.

If two return blocks have the same transformation on C, retaining the
cheapest weight preserves every subset transition and can only shorten
an expanded word. There are at most h^h distinct transformations and
at most 2^h-1 nonempty subset vertices. Unlike the previous full-state
64-bit subset scorer, the state count n=h+t can exceed 64 without
affecting subset mask width. The new native implementation uses only
h<=6 in its large-cycle stream and h<=3 in its exhaustive stream; no
unbounded-size implementation claim is made.

The already proved full-reset relation also applies:

    rt(A) = 1 + reset_A(C).

Indeed the first b in any full reset maps its pre-b image, either Q
or O, onto C. Removing any preceding a-prefix saves letters; an a-only
word cannot reset Q. Starting with b and a shortest C-reset attains the
displayed value. Hence weighted synchronization is full synchronization
for this schema, rather than merely pair or first-drop compression.

## Fresh adaptive pressure

weighted_class_reset_pressure.cpp uses the exact identity above. It
deduplicates return transformations in increasing literal block cost,
then runs Dijkstra on all reachable nonempty C-subsets. Every stored
word expands to the actual original binary word. No subset vertex cap,
approximate score, or heuristic distance enters an accepted score.

Seed 20261021 proposes 1000000 candidates in 21 profiles:

| h | t values |
|---|---|
| 3 | 25,49,97,193,385,769,1537,3073 |
| 4 | 33,65,129,257,513 |
| 5 | 41,81,161,321 |
| 6 | 49,97,193,385 |

These profiles and this stream are distinct from the previous 1120000
proposals at h3..10,t<=28. The new search mutates O colors, C injections
and the C permutation, and permits occasional score decreases. Its
seven structured restart types include modular colors, long monochromatic
blocks, a dominant color with rare other colors, two alternate modular
periods, random colors with enforced surjectivity, and shuffled balanced
colors. Randomized injection/permutation variants accompany the restarts.
Surjectivity rejects are counted before scoring.

Of 1000000 proposals, 999995 are synchronizing accepted evaluations,
none is nonsynchronizing and five are nonsurjective. There are no budget
violations. The mutation/restart counts and per-profile proposal/acceptance
counts are in data/weighted_class_reset_pressure.json. Repeated candidates
are possible: these are evaluation counts, not distinct automaton counts
or an isomorphism cover.

The 21 retained maxima happen to have the finite observed values

    class_rt = (h-1)(t+1),
    target - class_rt = (h-1)(h-2).

This pattern is an observation about the saved maxima, not an all-n
upper bound. In particular h3,t3073,n3076 gives

    reset_A(C)=6148 < 6150=(h-1)(n-1),   rt(A)=6149.

Its weighted C-graph has seven vertices. All saved profiles collectively
have 507 weighted vertices, while their ordinary complete subset graphs
have 65827 vertices. The earlier adaptive streams are not rerun or
superseded. Their h3,n10 equality certificate remains a control: its
value 18 still refutes the strict version at h>=3.

## Focused equality lifts: no all-n family obtained

weighted_class_equality_lifts.py fixes the ten-state certificate's
O-color word [0,2,2,2,1,0,1] and injection indices [5,4,1]. A designated
extension inserts one contiguous color word into one of its eight
linear gaps, remaps each original injection coordinate past the gap,
and tries every C permutation. Equal resulting automata are deduplicated.
At t10 and t13, EVERY inserted color word of length three/six is covered.
At t25,49,97,193, the inserted word repeats EACH of the 27 length-three
color words. The latter are complete designated periodic-insertion
covers, not arbitrary inserted-word covers at those lengths.

| t | distinct designated inputs | maximum class reset | target |
|---|---:|---:|---:|
| 10 | 1080 | 15 | 24 |
| 13 | 29160 | 21 | 30 |
| 25 | 1080 | 16 | 54 |
| 49 | 1080 | 16 | 102 |
| 97 | 1080 | 16 | 198 |
| 193 | 1080 | 16 | 390 |

All 34560 inputs synchronize. A separately reconstructed designation
generator and ordinary subset BFS independently check EVERY input and
these exact designated maxima, in 4033582 ordinary vertices. All 70
stored records (six peaks, 63 family controls and one equality seed)
also pass full schema/SC/word/weighted checks, in 33928 ordinary vertices.
Three additional saved-record corruptions are rejected.

A natural alternating-tail extension for p>=2 has

    t=3p+1,
    colors = [0] + [2]^(2p-1) + [1,0,1,0,...]_(p+1 terms),
    injection = [2p+1,2p,1],   b|C=(01).

It equals the old certificate at p2, so it is a concrete candidate for
an all-n equality family. Its intended equality is **REFUTED**, and the
failure has an all-p proof: for EVERY p>=4, the word a^(p+3)b resets C
in p+4 letters. After its a-prefix, the three O-indices are

    (2p+1+p+2) mod (3p+1)=2,
    (2p+p+2) mod (3p+1)=1,
    1+p+2=p+3.

All lie in the monochromatic interval 1..2p-1 when p>=4, and b maps
them to state 2. Thus reset(C)<=p+4<6p+6=2(n-1). At p3 an independent
exact check instead gives reset(C)=11<24; the word a^4 b a^5 b attains
11. Exact controls for p2..64 are stored. The explicit p>=4 upper bound
is **PROVED (paper)**; no all-p exact-distance claim is needed.

These failures are limitations of the specified extensions. They do
not prove absence of a different all-n h3 equality family or imply an
improved general class-reset bound. The original equality certificate
remains valid. Data/checks are weighted_class_equality_lifts*.json;
replay_weighted_class_equality_lifts.py deterministically replays only
this new designated cover and its independent check, with literal
argv/stdout/stderr and generator/checker/data/report SHA256 captures.

## Independent checks and exact scope

check_weighted_class_reset_pressure.py imports no native scoring code.
It recomputes all 21 retained maxima using ordinary frozenset forward
BFS on the original n-state two-letter automaton and compares a separately
implemented weighted Dijkstra. It verifies the original words, return
blocks, transformation counts, full-reset relation and schema. Strong
connectivity is checked with one forward and one reverse traversal from
one state, in O(n), rather than BFS from every state.

The native tiny mode enumerates each labeled injection, C permutation
and surjective O coloring exactly once for h2..3 and h<=t<=4. The checker
independently reconstructs the complete expected designation set and
rejects duplicate or missing entries. There are 5816 inputs, of which
5336 synchronize. Independent ordinary subset BFS visits 111128
vertices; weighted graphs contain 36840. Their distances, synchronization
decisions and saved words agree on every input. This is a complete cover
of those designated tiny profiles, not of larger n or arbitrary DFA.

Seven independent corruptions are rejected: class distance, full reset
distance, weighted vertex count, transformation count, ordinary word,
return block and O-cycle row. The exact check report is
data/weighted_class_reset_pressure_checks.json.

weighted_class_reset_native.py uses g++ 4.9.2 with literal flags
-O3 -std=c++11 -static-libgcc -static-libstdc++. Its separate build and
generation captures record literal argv, cwd, stdout, stderr, elapsed
time, source/binary/output SHA256 values and compiler version. A separate
2000-proposal pilot is saved and is not included in the million-proposal
count above. Its 21 saved peaks also pass the independent checker,
visiting 75204 ordinary vertices. Thus all 42 saved main/pilot records
are checked, in 141031 ordinary vertices total; these records need not
be distinct. capture_weighted_class_reset_checks.py saves literal checker
argv, stdout/stderr and source/checker/report hashes in
data/weighted_class_reset_check_captures.json. Seven corruption types
are rejected for each source file. replay_weighted_class_reset.py replays only the two new
main streams and compares the entire parsed JSON with the frozen files;
its exact child captures are in data/weighted_class_reset_replays.json.

Reproduction from the repository root with the bundled Python runtime:

    python -m direct_attack.weighted_class_reset_native --trials 1000000 --seed 20261021 --out direct_attack/data/weighted_class_reset_pressure.json
    python -m direct_attack.weighted_class_reset_native --mode tiny --out direct_attack/data/weighted_class_reset_tiny.json
    python -m direct_attack.check_weighted_class_reset_pressure
    python -m direct_attack.capture_weighted_class_reset_checks
    python -m direct_attack.replay_weighted_class_reset
    python -m direct_attack.weighted_class_equality_lifts
    python -m direct_attack.check_weighted_class_equality_lifts
    python -m direct_attack.replay_weighted_class_equality_lifts

Use the configured runtime path rather than the broken default python
on this host. All new files are confined to direct_attack/. Existing
native scorers, replay ledgers and the frozen baseline are unchanged.
The exact saved checks and tiny cover are **COMPUTATIONALLY VERIFIED**;
the weighted identity is **PROVED (paper)**. The general class-reset
proposal and the unrestricted Cerny conjecture remain **OPEN**.
