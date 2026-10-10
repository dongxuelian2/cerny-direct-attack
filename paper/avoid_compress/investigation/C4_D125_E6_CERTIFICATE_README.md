# Unrestricted C4/D125/E6 conditional certificate

This auxiliary package excludes the E6 fourth geometry at (13,9,1),
conditional on equality 12 and the B0/C4/D125 entry flag. It does not
determine either F(13,9,1), exclude E16/E126 for unrestricted alphabets,
or prove alphabet separation. The accepted paper and supplement are
unchanged. The separate c4_d125_complete.zip is a historical binary
certificate; its statement that unrestricted E6 remained unresolved
describes the frontier before this new proof.

Read C4_D125_E6_UNRESTRICTED_EXCLUSION.md. Its exhaustive four-class
argument and last-entrance construction are the all-alphabet proof.
The complete individual rows and seeded alphabet controls support it;
sampled negative searches are not used as mathematical exclusions.
The earlier entry/local-equality flag, mandatory-core isolation,
complete C4 fourth classification, and closed merging block are explicit
fixed premises. Their direct reports and proof notes are included; this
package does not rerun all accumulated historical audits.

Python >=3.10, standard library only; assertions must remain enabled.

    python -B enumerate_c4_d125_e6_unrestricted.py
    python -B check_c4_d125_e6_unrestricted.py

These commands regenerate two data files and one audit byte-identically.
They reconstruct all 16 individual fields and all 1,944 allowed rows at
n=7,8,9 using distinct generators, and check 18,000 seeded alphabets.
For every strongly connected sampled alphabet with a mixed kernel, the
checker materializes a word of length at most four merging a pair that
touches J. Otherwise the closed-block obstruction is checked. An n=8
strongly connected synchronizing boundary control has earliest J-pair
merging length exactly four. It is not an attaining F witness.

CHECKSUMS.txt binds every included file. Current remaining unrestricted
C4/D125 alternatives are E16 and E126, two geometries and 21 labels.
Both numerical extrema at (13,9,1) remain in [11,12].
