# Conditional complete binary D15/D25 certificate

This auxiliary package is outside the accepted paper/release. At
(13,9,1), assumed ac=12 and B0,C14,K12, it excludes the complete
binary third types D15 and D25. It is not an exact F value, unrestricted
exclusion, alphabet separation, or complete answer to Open Problem4.

Python>=3.10 (standard library) and C++17 suffice. Set CXX to the
compiler if it is not on PATH. Keep all assertions enabled.

    python -B enumerate_b1_c14_nonsingleton_fourth.py
    python -B check_b1_c14_nonsingleton_fourth.py
    python -B enumerate_d15_d25_fourth_rows.py
    python -B check_d15_d25_fourth_rows.py
    python -B check_b1_d15_d25_composition.py

These regenerate three data files and three audits byte-identically.
Temporary native executables and large sorted row files go in a sibling
_qa directory, not this package. Proof notes establish completeness;
checksums bind every included byte. Earlier entry/local-equality,
mandatory-core and small-third audits are explicit fixed premises;
this package does not rerun their full independent proofs.

The parent fourth classifier covers606060 masks and10444 ranks. The
new ten row domains include every Boolean companion and98 fourth pairs,
with13426560 raw and2784960 retained rows. First-letter stabilizers
have720 or5040 elements; every second row remains labelled. All20160
independent group actions and2784960 pointwise transports are checked.
Both complete pair algorithms test813607200 representative pairs,
with no candidate. Exactly2217576 retained initial masks exceed bit31;
64-bit masks and a bit59 control cover the60-set family.

D15/E2 retains nine formal field pairs but is excluded by the old
arbitrary-alphabet compression-cover floor, not by a row scan. D25's
four old all-alphabet empty-tuple cases are explicitly composed. The
new negative therefore removes all17 original D15/D25 third pairs.
Unrestricted fourth alternatives remain. The separate whole-B0/C14
joint composition uses earlier D2,D5,D12,D24,D125 certificates and is
not part of this minimal new-domain package. Both F(13,9,1) remain[11,12].
