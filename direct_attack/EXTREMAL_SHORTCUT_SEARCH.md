# Exhaustive single-shortcut attack on retained near-extremal bases

The n4 and infinite shortcut obstructions show why ordinary alphabet
monotonicity cannot filter a global policy counterexample. We therefore
exhausted ALL generated transformations as individual new unit-cost labels
for the 16 retained binary n5 classes with rt>=14 and the four n6 classes
with rt>=23. Original base rows and source hashes are frozen in each record.

There are 22,136 n5 additions and 54,540 n6 additions, 76,676 total.
Every resulting DFA remains SC and synchronizing with the same monoid and
image family. None has P larger than its original base. The two n5 maximum
policy values are 16 (one base has rt=15); the n6 maxima are 25,25,23,23.
Full histograms of exact (P,rt) values, monoid sizes, peak transformations,
actual peak words and captured generation argv/stdout are retained.

These are **COMPUTATIONALLY VERIFIED finite negative results**, not a
new monotonicity theorem, characterization or unrestricted square proof.
They cover every SINGLE generated-map addition to these 20 specific bases.
They do not cover all ternary automata, larger states, or simultaneous
multi-shortcut additions. Since P is nonmonotone, individual robustness
does not justify a sequence of alphabet additions.

The checker independently enumerates each entire transformation closure
and replays every score histogram with the audited unrestricted native
solver. Forty base/peak policy certificates have independent ordinary-set
inverse BFS and Bellman checks. All 76,676 scores are not individually
recomputed with the ordinary-set checker; that narrower boundary is explicit.
No Lean result or priority claim.

## Two permutation/unit-defect shortcuts

The follow-up uses the same 20 bases and adds every pair of DISTINCT
generated transformations of rank >=n-1, excluding the original two labels
and the identity. These are simultaneous four-letter alphabets; the two
extras have actual base-word representations. There are 676466 n5 pairs
and 1767876 n6 pairs, 2444342 total. No policy increase or square violation
is found. The n6 maximum policies are 21,21,20,21, all strictly below the
respective bases 25,25,23,23; the n5 maximum across these pairs is 15.
Original single-shortcut data remain preserved in their own directory.

check_extremal_shortcuts --pairs independently reconstructs the closures,
selects the eligible transformations, and replays every pair's score
histogram. Forty additional base/peak certificates have ordinary-set policy
checks. The full pair scores still use the audited native kernel; the
ordinary-set checker does not recompute all 2444342 entries. No unrestricted
four-letter enumeration or arbitrary rank/multi-shortcut guarantee follows.
