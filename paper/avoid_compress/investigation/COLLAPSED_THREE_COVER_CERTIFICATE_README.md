# Collapsed three-cover certificate

Investigation-only, with arbitrary finite alphabets. Run:

    python -B check_collapsed_three_cover.py
    python -B check_collapsed_three_cover_application.py

The written uniform proof assumes n>=4, synchronization, |P1|<=4,
a three-state cover K of P5, and a letter sending K to one point
isolated in P4. It derives a contradiction from the known compression
refinement of Kisielewicz--Kowalski--Szykula (CIAA2016, Theorem1).
There is no new compression theorem, priority claim or F value.

Controls include74,046 literal ordered three-pair sequences on n4..9,
all covered collapsed maps on n4..6, and all65,536 ordered labelled
binary alphabets on n4. The latter verify1,872 two-cover P4 instances,
31,696 three-pair refinement controls and4,464 collapsed-cover
instances. A strongly connected synchronizing boundary retains the
collapsed letter when the target is not isolated. The n3 singleton
complement boundary is explicitly retained.

The arbitrary-alphabet equality application at(13,9,1) uses the frozen
checkpoint17 state. It checks231 labelled D transports and72 full
labelled whole-joint choices. It excludes the entire B3-in first branch,
the b1_out_c6 joint, and two further current third geometries. This
removes two current binary types/11profiles andnine unrestricted types.

Remainingbinary105types/448profiles/120geometries/18joints;
unrestricted136+63=199thirdgeometries/30joints,withfivefirsttypes.
Both F(13,9,1) remain[11,12]. Full Problem4 is still unresolved.

Historical premise sources/data/audits are explicit. This package does
not rerun every preceding research certificate. All package members
are checked by CHECKSUMS.txt, and the isolated runner requires both
new audit outputs to reproduce byte-identically. The accepted paper
and its109-file supplementary release remain unchanged.
