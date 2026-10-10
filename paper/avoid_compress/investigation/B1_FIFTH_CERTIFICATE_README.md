# Conditional fifth-entrance certificate for Problem 4

This auxiliary package treats only the necessary equality branch
n=13, |S|=9, ac(S,{3})=12, B0/C14/D5, with E6 or E26.
It gives no new extremal F value and is separate from the accepted
109-file article supplement. The article remains a partial answer.

The mathematical premises are the previously proved local equality
flag, entrance descriptions, and K12 cover of P5. Their proof notes,
the earlier fourth inventory and its audit are included. These are
upstream premises; this package does not rerun the whole upstream
classification or certify absence of every thirteen-state automaton.
All new generators and independent checkers are operationally
self-contained using only the Python standard library.

With Python>=3.10 and assertions enabled, run in this directory:

    python -B enumerate_b1_fifth.py
    python -B check_b1_fifth.py
    python -B enumerate_b1_e6_f2_letters.py
    python -B check_b1_e6_f2.py
    python -B check_b1_e6_fifth_pair_exclusions.py

Two inventories and three audits reproduce byte-identically. No
checker imports a generator. CHECKSUMS.txt authenticates the other
22 files in this 23-file archive.

The fifth inventory checks all54 labelled choices,14 geometric
orbits,221,130 literal masks and6,410 exact augmented ranks. It
retains both covered cross companions in E26 and its uncovered
Boolean companion. Four E26 crossed fibers are impossible over
every finite alphabet by individual-letter disjointness. E26 retains
F7,F17,F27 (18 labelled choices,161 binary field pairs).

E6/F2 is excluded over every finite alphabet, using the correct P2
isolation depth. The short proof shows that a singleton P2 cover in
a strongly connected automaton permits at most one immediate
collision edge; that edge is backward closed in this branch.
An independent expanded incoming proof is also checked. Complete
individual-letter controls have80,168,528,524,160 full letters at
n=7,8,9,13. A three-state strongly connected synchronizing control
admits a singleton P2 cover, guarding against a false cover floor.

The binary E6/F12 and E6/F127 proofs each discharge12 field pairs.
Every normalized row pair is checked at n=8,9,10:512,6,912,147,456
pairs per F. Complete individual n13 port checks include all5,040
ordinary X systems per F and35,280 ordinary L systems. The symbolic
proof covers arbitrary coupled outputs; no n13 transition-pair scan
is claimed. E6 retains F7,F17,F24,F27 (19 labelled choices,268
binary field pairs). Both residual E branches still cover all14
original third pairs. The full answer and F(13,9,1) remain unresolved.
