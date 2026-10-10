# Third entrance certificate

This auxiliary package contains the symbolic binary b3_mixed_c11
exclusion at (13,9,1), the forced c7 preimage profile, and the general
four-dimensional third entrance space. It does not determine F(13,9,1),
whose interval remains [11,12], and does not exclude unrestricted
alphabets. It is outside the unchanged article's 109-file supplement.

Read THIRD_ENTRANCE_SPACE.md, BINARY_THIRD_ENTRANCE_CROSSING.md and
FOUR_POINT_SECOND_ENTRANCE_EXCLUSION.md. A common third fiber is proved
only in the stated special profiles; the geometric inventory retains
all six orbits permitting an additional same-level fiber. The explicit
rectangle is a linear/geometric control, not an automaton witness.

Python 3.10+ with its standard library is sufficient. From this directory:

```sh
python enumerate_third_entrance.py
python check_third_entrance.py
```

The first command rebuilds all 36 stabilizer orbits and their exact
Boolean preimage columns. The checker independently enumerates labelled
covered subsets, literal nine-set intersections and augmented integer
ranks, and checks the 17 supplied existing equality witnesses by ordinary
subset/pair BFS. It also checks all 16 maps of the four-point C into its
two-point B intersection. It must report status pass, 36 geometric
orbits, six additional-fiber orbits, 17 controls, and 31/43 remaining
binary/unrestricted joint cases.

third_entrance_control_witnesses.json contains only the directly used
existing controls. extract_third_entrance_controls.py records their
provenance in the full repository; it is not required for standalone
reproduction, and its larger input frontier is deliberately omitted.
Historical native scans mentioned in antecedent proof notes are in
separate earlier certificates and are not used in this symbolic proof.

CHECKSUMS.txt authenticates the distributed bytes. No solver, native
compiler, numerical rank tolerance or search timeout is used here.
