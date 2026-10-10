# Three-cover atom/kernel certificate

Investigation-only necessary exclusions at (n,s,r)=(13,9,1), target12.
The accepted article and its 109-file supplement are unchanged.

Run in this directory with Python3 and its standard library:

    python -B check_general_atom_kernel_controls.py
    python -B enumerate_three_cover_atom_kernels.py
    python -B check_three_cover_atom_kernels.py

The complete historical data cover362 third geometries,2,529 exact
fields and67,700 compatible letter-kernel instances. The independent
checker uses edge graphs/disjoint cliques, rather than the generator's
three-guard group partitions. Both methods retain permutations, all
covered triple/multiple-pair kernels, all Boolean companion fields and
empty membership atoms. No realization of retained automata is claimed.

Raw controls compare159,736 single partition/field instances against
129,241 labelled-map/output instances, and53,882 binary partition
coverage instances against1,120,753 labelled-binary-map/output instances.
These controls support the uniform quotient proof, not extrapolation
to all automata on13 states.

The immutable comparison state is byte-bound to checkpoint16. Relative
to it,11 binary third types/22 profiles and40 B1/B2 plus47 B3 arbitrary-
alphabet third geometries are newly excluded. Some current empty binary
geometries also fail the supplier test: the total new binary geometric
exclusions are38. Complete joint composition records two additional
binary and five additional unrestricted joint exclusions, including
consequences of earlier recorded third cuts.

Remaining: binary107 types/459 profiles/122 geometries/18 joints;
unrestricted141+67=208 third geometries/34 joints. Both numerical
F(13,9,1) remain[11,12]. The Problem4 goal is still unachieved.

Historical premises are explicit frozen source/data/audit bindings;
this certificate does not rerun every preceding research certificate.
CHECKSUMS.txt verifies every package member. The isolated package check
requires the generated inventory and both new audits to reproduce byte
identically. No SAT timeout, sampled negative, alphabet-size reduction,
or unproved higher-layer edge cap is used.
