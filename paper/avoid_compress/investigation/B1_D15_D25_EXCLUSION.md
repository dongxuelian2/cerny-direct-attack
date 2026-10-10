# Whole binary D15 and D25 exclusions

Conditional at (n,s,r)=(13,9,1), ac=12, B={0}, C={1,4},
normalized P5 cover K={1,2}. This does not determine either extremum.

The complete parent fourth classification gives eight E geometries at
D={1,5}, with32 labelled E sets, and seven at D={2,5}, with31 labels.
D15/E2 is excluded by the already proved compression-cover floor:
mandatory2 removes one P5-cover point. Its nine formally compatible
binary fourth pairs are not incorrectly treated as absent. At D25,
E12,E15,E24,E126 have no admissible individual preD tuples in the parent
classification, so are already excluded for arbitrary finite alphabets.

The remaining ten geometries have98 binary fourth-field pairs:42 at D15
and56 at D25. All are exhausted using D15_D25_ROW_COVER.md. Python's
atomwise enumeration and native input recursion agree on13426560 raw
rows; reverse and forward implementations agree on2784960 retained
rows and all pointwise transports. Stabilizers have5040 elements when
E omits6 and720 when it contains6. Every second letter is labelled.
Both complete implementations test813607200 representative row pairs
and reject all before candidate subset BFS. Pure-letter masks use64bits;
the largest initial family has60 sets. D15/E24's companion25 and
D15/E25's companion24 are included.

The whole-D composition checks every original third-field pair and
every fourth alternative, discharging D15's three and D25's fourteen
third pairs. Binary negative scans do not discharge any unrestricted
survivor. The original20 fourth geometries/128 E labels for unrestricted
alphabets remain, and both maxima at (13,9,1) remain in [11,12].
