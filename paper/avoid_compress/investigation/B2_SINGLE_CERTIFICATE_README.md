# Complete B2 single-class first-pair certificates

These are conditional structural exclusions at (13,9,1), target ac=12.
They do not determine an F value, an alphabet separation, or a complete
formula. The paper remains a partial answer.

The package contains the frozen checkpoint04 baseline, literal parent
domains, full labelled first-pair transports, five complete inventories,
five independent case audits, a composition audit, the existing prefix
column audit, their referenced local sources and proof premises.
Each selected geometry has exactly one retained immediate graph class.
The certificate proof is B2_SINGLE_CLASS_FIRST_PAIR_EXCLUSION.md.
Full publication artifacts and earlier checkpoint certificates remain
separate; this package is an auxiliary certificate, not the publication
supplement or a replacement for it.

Use Python 3, with no third-party packages. From the extracted directory:

    python -B check_basis_column_reaching.py
    python -B check_b2_single_case.py b2_mixed_c12_third4
    python -B check_b2_single_case.py b2_in_c1_third6
    python -B check_b2_single_case.py b2_mixed_c1_third11
    python -B check_b2_single_case.py b2_mixed_c1_third9
    python -B check_b2_single_case.py b2_mixed_c1_third10
    python -B check_b2_single_composition.py

The case checker refuses to overwrite its saved audit; rename ONLY the
corresponding *_single_audit.json output before invoking it for a manual
rerun. The composition checker similarly refuses to overwrite its audit.
The basis audit may be regenerated in place. The generators refuse to
overwrite their *_single_inventory.json outputs.

The workspace packager's --check-package mode extracts to a fresh verified
QA directory, verifies every checksum, removes only the twelve exact
named regenerated outputs, runs all twelve commands sequentially, and
requires byte-identical regeneration of seven audits and five inventories.
It never changes the authority or publication. The separate recorder may
adopt the result only after all old/new audit bindings, prior profile
cuts, isolated regeneration and publication checksums have passed.
