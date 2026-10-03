# Exact extremal profiles: what survives comparison

**COMPUTATIONALLY VERIFIED**, for the stated finite binary scope only.
First-letter functional-digraph representatives cover all distinct-letter binary automata,
including pairs conjugated from any original first letter. They overlap:
automata with different choices of first letter can appear multiple times.
Full state/alphabet canonicalization is applied to retained extremal classes.
Repeated identical letters reduce to a unary automaton. Such an automaton
cannot be both strongly connected and synchronizing on n>=2 states, so its
omission loses no classes in this extremal search. Partition searches also
include nonsc automata; their unary cases are audited separately through n=5.
Covering-occurrence counts are never reported as isomorphism-class counts.

| n | Retained threshold range | Exact retained classes | Distribution |
|---|---|---|---|
| 4 | >=9 | 2 | two at 9 |
| 5 | >=14 | 16 | one at 16, four at 15, eleven at 14 |
| 6 | >=23 | 4 | two at 25, two at 23; none at 24 |

The complete six-state binary covering pass tests 6,065,150 distinct-letter
ordered representatives. Its strongly connected part has 1,165,941 covering
occurrences, not that many unique classes. Random larger-state experiments
are explicitly separate from this exhaustive covering.

## Concrete distinctions at the same maximum threshold

For C6 and the other six-state square extremal, rt=25 in both cases, yet:

| Profile | C6 | Other saved extremal |
|---|---|---|
| permutation letter cycles | (6) | (3,3) |
| other letter cycles | (1,1,1,1,1) | (1,1,1,2) |
| proper-rank gaps | (1,3,3,5,13) | (1,3,5,8,8) |
| maximum pair distance | 15 | 11 |
| reachable subsets by rank 1..6 | (6,15,20,15,6,1) | (6,15,19,12,3,1) |
| best forward greedy | 27 | 26 |
| best inverse greedy | 25 | 27 |
| minimal phase bottleneck | 6 | 8 |
| exact transformation monoid size | 2742 | 17265 |

Neither a full-cycle letter nor maximum possible pair diameter nor full
reachability of all nonempty subsets is necessary for square extremality.
Equal rt also does not imply similar rank-gap allocation or monoid size.
The two four-state square extremals likewise have the same rank thresholds
and pair-distance spectrum but distinct phase bottlenecks (4 versus 5),
monoid sizes (128 versus 145), and opposite advantages of the two orientations.

All four saved six-state near-extremals have letter ranks (5,6), and all 22
retained four-/five-/six-state classes have trivial state/alphabet
automorphism groups. These are observed finite constraints, not necessary
conditions for a minimal counterexample. The five-state near-extremals even
include letter-rank pattern (4,4), so a permutation letter is not universal
over this near-extremal corpus.

The semigroup enumerations in this table terminated completely. Elsewhere a
profile with semigroup_complete=false records only a truncated enumeration;
its stored size is not the full monoid size. Independent distance/profile
checkers do not independently re-enumerate every monoid or automorphism group.

The mathematical return from this comparison is rejection of several simple
rigidity guesses. No new asymptotic extremal characterization is established.

An additional exact congruence scan of these same 22 retained binary
classes finds that all are simple, including the five square-extremals.
It enumerates all proper nontrivial state partitions and independently
checks simplicity through pair-generated congruence closure; ordinary
subset BFS rechecks every saved reset threshold. This is finite evidence
consistent with Rodaro--Venturi's proposed simplicity of all extremals,
not evidence that near-extremality forces simplicity at arbitrary n.
QUOTIENT_FIBER_LIFT.md separately proves a conditional strict exclusion
of bounded-fiber congruences for square-extremal automata.
