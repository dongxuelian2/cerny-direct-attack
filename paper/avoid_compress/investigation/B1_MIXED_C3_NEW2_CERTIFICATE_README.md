# B1/C3 mixed third-entrance certificate: sole new point 2

This auxiliary package contains B1_MIXED_C3_NEW_POINT_2_EXCLUSION.md and
an independent audit of its complete kernel and finite core reductions.
At (13,9,1), binary equality with B={4}, C={0,1,5} cannot have common
third entrance D={0,2},{2,5},{0,1,2} or {0,2,5}. Initial-set reachability
is unnecessary for the negative. No unrestricted exclusion is claimed.

With Python 3.10+ and its standard library, run:

```sh
python check_b1_mixed_c3_new2.py
```

The checker must report pass, 50,574 F R-kernel partitions, 4,140 L
R-kernel partitions, 40,320 fixed-kernel L-output injections, 240 finite
core-port configurations and twelve final core cases. It verifies the
backward-closed pair graphs for every unspecified thirteen-state ordinary
output possibility. Complete literal normalized row controls have 720
assignments at n=7 and 6,480 at n=8; forward pair BFS and ordinary graph
reachability independently discharge all of them. These small completed
row scans are controls, not extrapolated F uppers. The symbolic proof
handles the six ordinary points at n=13 without a full row enumeration.

The H cover and |P1|<=4 bound, and the earlier outside-kernel obstruction,
are premises with their proof notes included. Their earlier larger
certificates are separate prerequisites, not reproduced here. The intact
235-orbit small-first admission is included so the four removed third
profiles remain explicit. After previously proved exclusions, 169 binary
typed third orbits and 930 letter-profile pairs remain. These are necessary
admission counts, not numbers of automata. The original joint count stays
26 binary / 43 unrestricted, and both extrema stay [11,12].

The retained B1/C3 mixed D labels are {6},{0,6},{2,6},{0,1,6},{0,2,6},
{0,1,2,6}. Here 6 follows the original inventory's marking of a D point;
it must not be conflated with the E-kernel partner q=6 in the excluded
profiles. The paper and its accepted 109-file supplement are unchanged.
CHECKSUMS.txt authenticates the original bytes, and this standalone checker
regenerates b1_mixed_c3_new2_audit.json byte for byte. No solver negative,
new F value, complete answer or numerical alphabet separation is asserted.
