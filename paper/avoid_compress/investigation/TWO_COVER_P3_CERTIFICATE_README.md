# Uniform two-cover P3 classification certificate

For every n>=4 and arbitrary finite alphabet, if the automaton is
synchronizing and K has two states covering P5, P3 after deletion of
isolates is triangle, four-vertex path, or two disjoint edges.
Strong connectivity and initial-image reachability are unnecessary.
This is a necessary classification, not an F value or full answer.

Read FINITE_INDEPENDENT_IMAGE_TRAP.md and
TWO_COVER_P3_CLASSIFICATION.md. Independent exact image-set counting
forces at least three two-state covers of P3, and an elementary
matching argument gives the complete graph classification. The proof
is uniform; finite controls are support, not its source of completeness.

Python >=3.10, standard library only; keep assertions enabled.

    python -B check_finite_independent_image_trap.py
    python -B check_two_cover_p3_classification.py

These reproduce two audits byte-identically. The first exhausts all
65,536 n4 labelled binary alphabets and32 fixed-cover graph choices at
h=1,2. Its76,560 qualifying graph/depth cases are checked by forward
pair and full/subset BFS. The second exhausts43,680 fixed-two-cover
graphs through n9 and independently classifies their degrees. It also
checks all65,536 n4 binary alphabets:24 satisfy synchronization and the
fixed P5 cover, all strongly connected, with16 path and8 triangle P3
graphs. These are structural controls, not new extremal F examples.

The residual K12 cover in the current singleton-C roots permits this
classification. D15/E26 contains supplied matching15,26, so its P3
graph is those edges with at most one crossing edge. E26 and E6 remain
admitted; both F(13,9,1) intervals remain[11,12]. The accepted paper
and publication supplement are separate and unchanged. CHECKSUMS.txt
binds every byte of this auxiliary package.
