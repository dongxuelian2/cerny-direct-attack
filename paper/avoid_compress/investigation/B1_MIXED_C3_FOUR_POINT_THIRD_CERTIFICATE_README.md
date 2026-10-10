# B1/C3 mixed four-point-third-entrance certificate

This auxiliary package proves that binary equality at (13,9,1) with
B={4}, C={0,1,5} cannot have D={0,1,2,6}. The argument permits the
C-merging letter to be injective outside C and includes the double
F kernel 01+26. It uses |P1|<=4, the P5 cover H={0,1,2}, and isolation
of the two protected states in P6, derived in the included proof from
the established entrance and protected-pair bounds. Initial-set
reachability is unnecessary for this negative. No arbitrary-alphabet
exclusion or all-n statement is made.

With Python 3.10+ and the standard library, run:

```sh
python check_b1_mixed_c3_four_point_third.py
```

The checker must report pass after all three row controls. It covers
15 D partitions, 4,140 L R partitions, 877 F R partitions, 42 raw F
core maps and 114 (delta,F) cores. The six distinct extra-pair constraints
have 564,480 L output assignments; F has 40,320 R injections. Universal
backward-graph checks use conservative sets of all unspecified outputs
at thirteen states, covering 312 configurations and 48,672 pair checks.
The independent normalized row controls have 1,872, 18,792 and 331,776
assignments at n=7,8,9, including every ordinary injection/permutation
in those small families. Every explicit proof word or obstruction is
checked. Integer forward pair BFS independently checks all rows; it
also agrees with the original set-based BFS on the first 64 rows of
each family. The two-ordinary-point n=9 control covers the distinct
x,y graph branch. Allow roughly a minute on a typical desktop.

These controls support a symbolic n=13 proof; they are not a full
thirteen-state scan or an extremal upper extrapolated from small rows.
Earlier premise certificates remain separate prerequisites. Cumulative
frontier counts include their previously audited exclusions. The intact
inventory retains D={2,6},{0,2,6} in B1/C3 mixed, and 165 residual binary
typed third orbits / 918 letter-profile pairs in total. These count
necessary admissions, not automata. Joint counts stay 26/43 and both
extrema stay [11,12]. No numerical alphabet separation is established.

CHECKSUMS.txt authenticates every distributed byte. The standalone
checker regenerates b1_mixed_c3_four_point_third_audit.json byte for
byte. The accepted manuscript and its 109-file release are unchanged.
