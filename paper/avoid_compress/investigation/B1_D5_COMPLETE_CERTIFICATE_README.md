# Binary singleton-D5 exclusion certificate

Research certificate for n=13, |S|=9, ac(S,{3})=12, normalized
B={0}, C={1,4}, D={5}. It excludes this entire third geometry in
binary strongly connected synchronizing automata. Both extremal values
at(13,9,1) remain in[11,12]; larger alphabets are not excluded.

Python>=3.10 (standard library) and a C++17 compiler with assertions
enabled suffice. Set CXX to a compiler path if it is not on PATH.
Run these commands in the extracted directory:

    python -B enumerate_b1_e26_f7_seventh.py
    python -B check_b1_e26_f7_seventh.py
    python -B enumerate_b1_e26_f7_seventh_rows.py
    python -B check_b1_e26_f7_seventh_rows.py
    python -B check_b1_d5_composition.py

Read B1_E26_F7_SEVENTH.md, B1_E26_F7_SEVENTH_ROWS.md and
B1_D5_EXCLUSION.md for the precise hypotheses and composition.
All23 seventh geometries/59 labelled H choices and every Boolean
companion are checked independently, including241,605 masks and39,365
augmented ranks. Exact shared output atoms and empty input atoms are
retained. The two complete individual generators agree on51,168 raw
and24,960 retained rows and every initial-image mask. Each coupled
implementation checks all5,689,728 retained pairs, with zero survivors.
Four additional typed pair domains are literally empty; that does not
make all individual supplying letters impossible. Nine unrestricted
survivors have separately checked literal supplying-letter witnesses.

The42-file archive contains all direct sources/data/proofs/reports used
by the three new audits, this README and41 checksums. The five commands
reproduce three data files and three audits byte identically, including
both complete scans and exact all-level composition. Compiler binaries
and canonical row dumps go into a sibling _qa directory.

Earlier fourth/fifth/sixth classifiers and exclusions are explicit
included premises. The new composition rerun checks their status and
literal coverage; it does not rerun their entire upstream proof chain.
The repository's authoritative auxiliary checkpoint separately checks
the full source bindings of all old and new audits. This research
archive does not replace the article's accepted109-file supplement.
No exact F value, numerical alphabet separation or complete solution is
asserted. The article and release remain unchanged.
