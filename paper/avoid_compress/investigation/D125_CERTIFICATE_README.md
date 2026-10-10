# Conditional binary D125 exclusion certificate

This auxiliary certificate excludes the B0/C14/D125 third type at
n=13, |S|=9, ac(S,{3})=12. It does not prove an exact value of F,
exclude unrestricted D125, or claim a complete answer to Problem4.

Read B1_D125_EXCLUSION.md, D125_FOURTH_ROWS.md and
D125_ROW_NORMALIZATION.md. Python>=3.10 (standard library), C++17,
and assertions enabled are required. Set CXX to your compiler path
if clang++/g++ is not on PATH. Do not use Python -O or C++ -DNDEBUG.

    python -B enumerate_b1_c14_nonsingleton_fourth.py
    python -B check_b1_c14_nonsingleton_fourth.py
    python -B enumerate_d125_fourth_rows.py
    python -B check_d125_fourth_rows.py
    python -B check_b1_d125_composition.py

The first two commands reproduce the complete five-D fourth inventory,
606060 literal masks and10444 augmented ranks. The next two reproduce
241920 raw rows using two independent enumerations, verify119520
pointwise conjugacies and40,320 initial masks with bits above31,
and check7,164,000 representative pairs per algorithm. The final
command checks all five D125 fourth alternatives, all29 E labels
and all three original third pairs. Every regenerated data/audit file
is byte-identical to the packaged record. Intermediate executable,
raw-row and transport files are written outside this directory.

The early-third inventory/audit and mandatory-core theorem/audit
are included fixed premises. This small package does not rerun their
upstream research chain. The root AUXILIARY_AUDIT_20261010_04.json
verifies every source binding in all63 accumulated audits, including
those premises, and preserves all121 accepted publication checksums.
Earlier fourth results remain immutable and are independently rerun
here. No search logs, executables or unrelated results are included.

The package CHECKSUMS.txt binds every included source, proof note,
data and audit. Larger-alphabet E6,E16,E26,E126 and other binary D
types remain open. Both extrema at(13,9,1) still lie in[11,12].
