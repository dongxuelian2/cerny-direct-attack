# B1/C3 mixed three-point-overlapping-third-entrance certificate

This auxiliary package excludes binary equality at (13,9,1) with
B={4}, C={0,1,5}, D={0,2,6}. Initial-set reachability is unnecessary
for this negative. No unrestricted-alphabet exclusion is made.

With Python 3.10+ and the standard library, run:

```sh
python check_b1_mixed_c3_three_point_third.py
```

The checker must report pass after the n=7,8,9 controls. It enumerates
the complete thirty split-kernel patterns and 24 raw F core maps / 36
(delta,F) cores. Both R partition inventories have 4,140 elements;
322,560 output assignments are checked for each letter's eight distinct
admitted partitions. The 123 universal graph configurations use conservative
sets of every unspecified thirteen-state output.

The F-only count-form lemma covers all 13,680 parameterized rows, all
342,000 nine-set controls, and every ordinary J permutation. Another
8,640 rows check the zero-reachability step. The paper proof includes
a complete form-transition table and the separate five-cycle averaging
case. Small complete normalized row controls have 1,440, 18,792 and
393,984 assignments; they verify explicit words and graphs and use
independent forward pair and subset-prefix BFS. The fast pair BFS also
agrees with the original set BFS on the first 64 rows of each family.

The negative result uses the proved |P1|<=4 budget, H-cover of P5,
protected a,b isolation through P6 and one-count entrance conditions
on actual nine-set images. Earlier premise certificates remain separate
prerequisites. The smaller normalized controls need not derive those
entrance conditions from their smaller subset sizes. Neither these
controls nor the parameterized F lemma are a full thirteen-state row
scan, an all-n F upper bound or an alphabet separation.

The intact admission inventory now retains only D={2,6} in B1/C3 mixed.
Its disjoint third-entrance geometry still has fourteen letter-profile
pairs and is not excluded by this proof. The total residual binary
admission is 164 typed third orbits / 915 letter-profile pairs; these
count necessary profile admissions, not automata. Joint cases stay
26/43 and both extrema stay [11,12]. Cumulative counts use preceding
independently audited exclusions.

CHECKSUMS.txt authenticates every distributed byte. This standalone
checker regenerates b1_mixed_c3_three_point_third_audit.json byte for
byte. The accepted article and its 109-file release are unchanged.
