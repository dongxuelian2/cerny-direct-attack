# Every single arbitrary letter on the retained near-extremal bases

**COMPUTATIONALLY VERIFIED, finite scope only.** For the 16 retained binary
n5 automata with rt>=14 and four retained binary n6 automata with rt>=23,
EVERY single added transformation is scored exactly: 16*5^5+4*6^6=236624
cases. Identity, constant and duplicated transformations are included.
None raises P over its base value, and none violates the policy square.
This extends the earlier 76676 generated-map additions to arbitrary maps;
it does not reinstate general alphabet monotonicity, refuted already at n4.
Arbitrary multiple additions and all ternary inputs are not covered.

The generator enumerates each map in product(range(n),repeat=n) and uses
the exact sparse full-image solver. Source rows and their summary SHA256,
complete (P,rt) histograms, maxima, added maps and 40 base/peak arrays are
saved. Generation retains literal argv, stdout/stderr and timing.
Adding letters preserves the known base reset, so these inputs cannot be
Cerny counterexamples; the stronger image-policy conjecture is what is
being attacked. Exact rt is independently recorded, not inferred from P.

check_extremal_arbitrary re-enumerates EVERY addition with the separately
audited FULL-CUBE transport kernel, checking each individual (P,rt) against
the sparse kernel before comparing the entire histogram and all maxima/counters.
Forty base/peak e/G/W/forward arrays additionally have
ordinary ALL-SOURCE BFS checks. There is no claim that ordinary BFS scores
every addition. The source hashes and base-membership records are checked.
The short-reset subset count is independently matched; its square guarantee
also follows from SHORT_RESET_SEED_BUDGET.md. No universal theorem, minimum
counterexample result, Lean theorem or novelty claim follows from this run.
