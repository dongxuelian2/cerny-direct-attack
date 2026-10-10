# Auxiliary binary overlap-fourth certificate

This conditional certificate is outside the unchanged109-file paper
supplement. It excludes E24 and E16 in the B0/C14/D5 equality branch
at (13,9,1), binary only. Read B1_PARTIAL_COVER_E24_EXCLUSION.md and
B1_PARTIAL_COVER_E16_EXCLUSION.md, with the supplied prerequisite
common-fourth proof. The established K-cover and protected isolation
are hypotheses of these local exclusions; this is not a full F certificate.

Python>=3.10, standard library only; keep assertions enabled.

    python -B enumerate_b1_partial_cover_e24.py
    python -B check_b1_partial_cover_e24.py
    python -B enumerate_b1_partial_cover_e16.py
    python -B check_b1_partial_cover_e16.py

Neither checker imports a generator. They reuse the supplied earlier
independent partition routine, then check every new pattern, explicit
word and closed graph. Each exclusion has complete normalized smaller
row controls at n=7,8,9, and423,360 complete individual n13 hard-profile
letters with all ordinary permutations and protected variants. Arbitrary
coupled letters in the hard profiles are discharged by the symbolic
four-cycle argument, not by an unperformed n13 transition-pair scan.
The E24 one-count exception is checked literally. No outside-C
injectivity, higher-layer edge cap, timeout or alphabet extrapolation is used.

There are twenty files, including README and CHECKSUMS.txt. The parent
wrapper verifies all hashes, safely extracts into an isolated workspace
folder, runs all four commands and requires both inventories and both
audits to reproduce byte-identically. Binary fourth admission becomes
two geometries /82 field pairs, still covering fourteen original third
pairs. Joint/third counts and both F intervals[11,12] do not change.
No complete answer, F value or numerical alphabet separation is claimed.
