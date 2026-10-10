# Exclusion of the binary three-point entrance with one new overlap point

9 October 2026. Complete conditional computer-assisted proof, outside
the paper release. No new extremal value or alphabet separation.

At (n,s,r)=(13,9,1), a binary strongly connected synchronizing automaton
with ac(S,{a})=12 cannot have |B|=3, overlapping first and second entrances
B,C, and |C minus B|=1. Initial-set reachability is not required for
this exclusion. Other C shapes and unrestricted alphabets are not covered.

The five-pair endpoint argument in SINGLETON_THREE_KERNEL_EXCLUSION.md
gives |P1|<=4. The localized moving-kernel and first-level equality
arguments reduce the rows to the six complete cases in
OVERLAP_THREE_KERNEL_NORMALIZATION.md. All permutations on the seven
unforced moving inputs and all three first-level F actions are admitted.
No long-cycle type, reachability bound or SAT answer is imposed.

## Complete row cover and counts

For each moving conjugacy type and first-level action, F is a nine-set
bijection fixing a and mapping its unique C input to its unique B output.
There are 7! free-output permutations. The remaining four inputs give
the following tail counts, in the action order FU=U, FU=T, FT=U:

| Shape | Moving orbits | Tail counts per free-output permutation | Row assignments |
|---|---:|---|---:|
| inside1 | 60 | (2,0,2) | 1,209,600 |
| inside2 | 60 | (6,4,6) | 4,838,400 |
| outside1 | 60 | (2,0,2) | 1,209,600 |
| outside2 | 60 | (6,4,6) | 4,838,400 |
| common1 | 180 | (6,0,6) | 10,886,400 |
| absent2 | 60 | (12,8,12) | 9,676,800 |

The tail counts depend only on C membership, the selected input kernel
blocks, two unused B outputs and two unused non-B outputs. Relabeling
the seven distinct free outputs changes none of these equality/type
relations. They therefore do not depend on the actual free permutation.
The independent typed-function checker exhausts every tail and verifies
each action count for every free permutation in the n=9 controls.

All 32,659,200 assignments are examined by ordinary reverse pair BFS
and direct strong-connectivity checks. Protected-point pair distances
must be at least eight, as established in ENTRY_FIBER_FLAG.md. The
retained strong, synchronizing, protected-isolated assignments number
24,410, 48,820, 16,762, 0, 0, 0 in the six shapes respectively. Ordinary
subset BFS tests their specified initial sets: all 89,992 have
avoid-or-compress value four, strictly below twelve. None is removed
by a test of initial-set reachability; no equality candidate survives.
The program has no search time limit, sampling or unchecked solver.

## Independent audit and boundary

check_overlap_three_kernel.py independently enumerates all 10,080
moving rows and classifies their conjugacy types by marked cycle words,
checking the native representative lists against the complete orbit
cover. It verifies the closed row counts above. It additionally
re-enumerates all 4,320 n=9 control assignments by full typed functions
on the unspecified inputs, literal sets and forward pair BFS. Every
aggregate count and complete delay histogram agrees with the native
program. Full n=9 and n=13 scans under AddressSanitizer and
UndefinedBehaviorSanitizer reproduce all inventories and counts.

The shared native graph/pair/subset helper is copied exactly from the
previous audited kernel probe without its entry point; the independent
checker also verifies this provenance. The finite histograms are not
an n-uniform upper of four. Neither the auxiliary proof nor its package
is included in the unchanged 109-file article supplement.

This excludes b3_mixed_c4,c5,c6,c8,c9,c10 in the original joint inventory.
Together with the prior exclusions, 32 binary and 43 unrestricted
joint cases remain. The B3 mixed-cover branch still permits c3,c7,c11,
all with two new C points. Both extremal intervals at (13,9,1) remain
[11,12]; this is not a complete answer to Open Problem 4.
