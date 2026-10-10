# B1/C3 mixed one-new-6 overlapping-third-entrance certificate

This auxiliary package proves that binary equality at (13,9,1) with
B={4}, C={0,1,5} cannot have D={0,6} or D={0,1,6}. The proof treats
the outside-kernel partner equal to 6 and distinct from 6 separately.
It retains every ordinary injection/permutation; initial reachability
is unnecessary for this negative. No arbitrary-alphabet exclusion is made.

With Python 3.10+ and the standard library, run:

```sh
python check_b1_mixed_c3_one_new6.py
```

The checker must report pass, 50,574 F kernel partitions, 282,240 complete
F output assignments, 80,640 L output assignments, 240 core ports and
26 critical cores. It verifies backward closure using conservative
sets of all unspecified thirteen-state outputs. Three independently
completed small normalized row families have 360, 3,240 and 7,128
assignments; forward pair BFS and strong connectivity independently
discharge them. Explicit words in the symbolic case cover are checked
on each literal row. These finite controls are not a full thirteen-state
transition-table scan or an extrapolated extremal bound.

The included proof notes establish the H cover, |P1|<=4 budget, entrance
fibers and necessary outside-C kernel; their earlier larger certificates
remain separate prerequisites. Cumulative frontier counts include the
previously audited exclusions. The original inventory is intact. The
remaining B1/C3 mixed D shapes are {2,6},{0,2,6},{0,1,2,6}; the residual
binary admission has 166 typed third orbits and 921 letter-profile pairs.
These count necessary profile admissions, not automata. Joint cases
stay 26 binary / 43 unrestricted and both extrema stay [11,12].

The paper and its accepted 109-file supplement are unchanged. CHECKSUMS.txt
authenticates every distributed byte; the standalone checker regenerates
b1_mixed_c3_one_new6_audit.json byte for byte. No new F value, complete
answer, solver negative or numerical alphabet separation is claimed.
