# Binary c3 / D={2,6} certificate

This auxiliary package contains the symbolic exclusion of binary
c3 third entrance D={2,6} at (13,9,1). Read C3_D6_BINARY_EXCLUSION.md.
The antecedent notes supply common entrance fibers and equality flags;
their references to other branch exclusions are historical context,
not additional proofs needed for this package's exclusion.

Binary c3 now retains only singleton D={6}; unrestricted c3 retains
four typed profiles. The entire c3 joint orbit is not excluded.
Both extrema at (13,9,1) remain [11,12]. This package is outside the
unchanged article's 109-file supplement and does not assert a numerical
alphabet separation or a complete answer to Problem 4.

Python 3.10+ and its standard library suffice:

```sh
python check_c3_d6.py
```

The checker must report status pass, three binary profile pairs,
42 constant-5 rank-six cases, 1,176 proper-E coordinate cases,
432 quotient configurations, 21 initial nine-sets and one/four
remaining binary/unrestricted c3 third profiles. It computes integer
ranks by fraction-free elimination, independently enumerates the
actual disjoint row types, audits literal core reachability through
the stated short depths, and checks all 5,040 X permutations.

No native row scan, SAT answer, timeout result, numerical rank tolerance,
external library or full-frontier data is used. The exclusion is a
paper proof; the finite checks audit its explicit claims. CHECKSUMS.txt
authenticates the original bytes. The independent audit regenerates
byte for byte from this standalone package.
