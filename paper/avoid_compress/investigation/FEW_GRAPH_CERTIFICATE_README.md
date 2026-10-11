# Full first-pair structural certificates

This is an auxiliary conditional certificate at (13,9,1), target ac=12.
It supplies no F value, alphabet separation or complete formula. It does
not replace the publication supplement, manuscript or earlier certificates.

The included *_scope.json specifies the frozen baseline, selected cases,
whole-graph transports, every labelled first pair and output_tag. The
mathematical premises are in FEW_GRAPH_FIRST_PAIR_CERTIFICATES.md and its
bound referenced notes. The complete case inventories and independent
case audits are accompanied by metadata adversarial controls and a
composition audit. Existing prefix-column premises have a paper proof
and a separate bound audit.

Python 3 standard library suffices. Replace SCOPE and CASE by the included
scope filename and an ID in its selected array:

    python -B check_few_graph_case.py CASE --scope SCOPE
    python -B check_few_graph_controls.py --scope SCOPE
    python -B check_few_graph_composition.py --scope SCOPE

Each checker refuses to overwrite its existing corresponding audit.
For a manual rerun, rename only that specific audit output first. For
fresh generation use enumerate_few_graph_case.py CASE --scope SCOPE,
after renaming its specific *_inventory.json. The independent case checker
does not use generator rank elimination or output-atom enumeration.

The workspace packager accepts --scope SCOPE --check-package. It extracts
the immutable archive into a fresh verified QA directory, validates every
checksum, removes only the exact named regenerated reports/inventories,
runs the prefix-column audit, every generator, every independent checker,
the metadata controls and composition, then requires byte-identical
regeneration. No authority or publication is changed during this check.

The controls reconstruct the native domains first and invoke the actual
generic checker on both valid and corrupted first-pair metadata. A sentinel
at its first literal-pool call distinguishes structural acceptance from a
later output-overwrite assertion. These metadata controls complement the
full literal-map and rational flag checks in each case audit; they are not
an alternative to them. A separate recorder may adopt only after complete
historical audit bindings, regeneration and publication checksums pass.
