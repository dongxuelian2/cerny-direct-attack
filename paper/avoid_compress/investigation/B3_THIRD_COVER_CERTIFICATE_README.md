# Auxiliary B3 third-admission certificate

This is investigation-only necessary-condition data, outside the accepted
109-file paper supplement. It treats the fourteen B3 joint geometries at
(13,9,1), conditional on target 12 and the previously established H-cover
and entrance flag. Read B3_THIRD_COVER.md and COMPRESSION_COVER_FLOOR.md.

Python >=3.10, standard library only. Keep assertions enabled.

    python -B enumerate_b3_third_cover.py
    python -B check_b3_third_cover.py

The generator uses exact rational rank and span coefficients. The checker
imports no generator, enumerates bit masks, independently checks rank and
all admissible covered Boolean fibers, and checks all 827 labelled D
choices. Its F_101 rank check equals rational rank by the proved minor
bound. All 127 B3 geometries and eighteen extra-fiber geometries are
retained except two third-profile exclusions under the known-cover cut.
The earlier three-case inventory is matched without changing its bytes.

There are eighteen files, including this README and CHECKSUMS.txt.
The wrapper in the parent investigation directory verifies every hash,
extracts into an isolated workspace directory, reruns both commands, and
requires byte-identical regenerated inventory and audit. No executables,
SAT results, timeouts or claimed sufficient transition tables occur here.
No new F value, numerical alphabet separation or complete answer follows.
