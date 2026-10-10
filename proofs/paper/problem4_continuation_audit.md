# Problem 4 continuation: verified results and remaining scope

10 October 2026. Continued at the user's request, then prepared for GitHub
synchronization. Source baseline: `d57a2077e19932ff69bea9307b69110678e213de`.
AI/tool assistance: Codex supplied mathematical derivation, source inspection,
independent enumeration, and implementation; no external researcher review
or formal-kernel verification of the new arguments is claimed. Coordination:
[issue 2](https://github.com/dongxuelian2/cerny-direct-attack/issues/2).

Both F_bin(13,9,1) and F(13,9,1) still lie in [11,12]. The complete open
problem is unresolved. The original manuscript, release archives and
historical pruning retractions are retained unchanged.

## Results now supported

- [Peeling, short-pair caps, rank transfer, and K4 exclusion](problem4_short_pair_peeling.md):
  written uniform proofs, with supporting finite controls indexed separately.
  In particular |P_h|<=h+3 for 1<=h<=7 under codimension-four compression
  at least twelve, and P3=K4 is impossible for n>=8.
- [P6 seven-cycle exclusion](problem4_c7_sixth_layer.md): a uniform reduction
  plus complete finite action/distance checks, independently reproduced.
  This is stronger in layer number than the inherited P5 cycle exclusion.
- The supplied twelve P3 shapes have been independently reclassified under
  the precise graph hypotheses below. Their historical elimination labels
  have not been accepted as proof.

## What the twelve-shape list actually certifies

The following classification is complete for simple graphs with no isolated
vertices after restricting to their support, Delta<=4, at most six edges,
cover number exactly three, empty intersection of all minimum covers, and
maximum-independent-set row rank at least four. The checker enumerates
all relevant labeled graphs, performs rational elimination, and compares
isomorphism classes with the supplied list.

| Supplied ID | Edges on the nonisolated support | Current exclusion status |
|---|---|---|
| 0 | 01 02 03 12 13 23 | Excluded by the written K4 proof |
| 1 | 01 23 24 34 | Historical exclusion unverified |
| 2 | 03 12 14 24 34 | Historical exclusion unverified |
| 3 | 03 04 12 14 23 | Historical exclusion unverified |
| 4 | 04 12 13 23 24 34 | Historical exclusion unverified |
| 5 | 03 04 12 14 23 34 | Unresolved |
| 6 | 05 14 23 | Historical exclusion unverified |
| 7 | 05 14 23 45 | Historical exclusion unverified |
| 8 | 05 14 23 35 45 | Unresolved |
| 9 | 05 14 23 25 34 | Unresolved |
| 10 | 05 14 23 34 35 45 | Unresolved |
| 11 | 05 14 23 25 34 45 | Unresolved |

Why support at most six is complete: use the tight-exchange argument in
[SHORT_PAIR_SPAN](../../paper/avoid_compress/investigation/SHORT_PAIR_SPAN.md).
For a maximum independent set I and a three-vertex complement C, let U
be the union of tight exchanged subsets of C and B=N_I(U). Empty minimum
cover intersection means every vertex appears in some maximum set, hence
U=C. The union inequality gives |B|<=|C|=3. Every vertex of I\B is
isolated. Thus the nonisolated graph has at most six vertices.

These conditions follow for an actual short-pair graph **if additionally
one has tau(P3)=tau(P6)=3**. Take an independent (n-3)-set R of P6. All
its images through depth three are uncompressed and independent in P3,
so they are maximum independent sets of P3. Their span has dimension at
least four. Strong connectivity reaches every state from R within three
letters, so their union is Q and no vertex belongs to every minimum
cover. The edge and degree caps follow from the new peeling argument.

This does not establish the additional equality of cover numbers globally.
Cases with tau(P3)<3 or tau(P6)=4 must not silently be omitted. In particular,
"seven exclusions leave five types" is not presently a verified complete
reduction. The original unidentified P7 branch could not be recovered;
only the newly specified K4 branch has a full eleven-edge argument here.

## Exploratory work and negative evidence

A separate exploratory atlas scan of the tau(P6)=4 boundary, imposing
maximum degree four, at most nine edges, maximum-independent-set rank at
least six, and coverage of every core vertex by those sets, produced nine
candidate support graphs on six or seven vertices. One is C7, now excluded
by the independent proof above. The other eight have **not** been excluded;
this atlas scan is not used as a certified complete automaton classification.
The nine support edge sets observed were:

```text
6: 01 04 05 12 15 23 25 34
6: 01 04 05 12 23 25 34 35 45
7: 01 04 12 23 34 56
7: 02 04 05 14 23 36 56
7: 01 06 12 23 34 45 56  [C7, excluded separately]
7: 01 05 06 12 15 23 34 45
7: 04 12 15 23 24 36 45 56
7: 01 04 12 23 25 36 45 56
7: 01 04 12 15 23 34 35 45 56
```

Local letter tests on these graphs retained candidates. Some scratch tests
used powers of a map after identifying different isolated input/output
labels. Such power cuts are not invariant under that projection and are
not accepted here. The final C7 enumeration was rerun without those cuts;
its uniform proof uses only single-letter profiles and actual distance
inequalities. This correction is material to the scope audit.

Other partial SAT/early-pair probes timed out or retained configurations;
they supply no exclusion. A small rank-two-defect binary probe at six
states is not an all-n theorem. Scratch binaries, caches and unsuccessful
search implementations are omitted from the contribution; their lack of
a proved conclusion is preserved here. No unavailable earlier ChatGPT ZIP
or claimed 137-to-108 geometry reduction is asserted to have been recovered,
verified or synchronized.

## Reproduction and verification boundaries

Supporting standard-library controls:

```sh
python computations/src/problem4_peeling_controls.py
python computations/src/problem4_k4_controls.py
python computations/src/problem4_p3_shapes.py
```

Observed outcomes: 41031 peeling graph/parameter instances; 40320 K4
outside permutations and 48 local g alternatives; exactly twelve conditional
P3 isomorphism classes with labeled multiplicities
1,10,60,12,60,60,15,180,360,360,120,360 in supplied-ID order.

For the two complete C7 map enumerations and independent distance checks,
use [the C7 reproduction commands](problem4_c7_sixth_layer.md). Outcomes:
604800 kernel-domain maps; 16777216 independently filtered literal rows;
1484 retained rows identical between generators; 896 signatures; 3960 exit
vectors; 14 surviving exit vectors; 3919104 joint vectors with zero
survivors; independent Python search 4946 partial nodes with zero solutions.
Both distance checks accept the artificial positive control.

Fresh repository verification: `python scripts/reproduce.py --suite all`
passed the core tests, all 83 baseline certificates, provenance/link/privacy
checks, and the exact Lean 4.19.0 replay of 11 existing modules / 114
declarations (the frozen core remains 100). In this entry point, `all`
runs core and formal; the separate historical 146-command audit and broader
focused/post/native suites were not rerun, since those sources are unchanged.
The relevant new independent checks above were all run. A final core replay
follows publication-seal refresh. None of these repository checks certifies
the new paper proofs. Fresh experiment outputs remain in `.reproduction/`,
as required by CONTRIBUTING.md.
