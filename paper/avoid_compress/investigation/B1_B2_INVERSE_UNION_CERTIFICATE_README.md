# Conditional B1/B2 inverse-union certificate

This archive concerns only `(n,s,r,ac)=(13,9,1,12)`. It excludes the
24 explicitly selected third geometries for arbitrary finite alphabets,
including binary alphabets, and retains one overapproximation as a control.
It determines neither F(13,9,1) nor an alphabet separation. The accepted
paper remains a partial answer to Open Problem4.

Use Python3.10 or later, standard library only, with assertions enabled:

```
python -B enumerate_b1_b2_inverse_union.py
python -B check_b1_b2_inverse_union_controls.py
python -B check_b1_b2_inverse_union.py
```

The generator enumerates all immediate graphs as unions of native exact
letter kernels, with at most four pair edges, and computes exact allowed
one-letter arrows by output coloring. It uses no timeout or alphabet bound.
The independent checker imports no generator: it rebuilds all covered
native kernels, all graph classes by edge-subset tests, literal output
independent sets, atom/type quotas, supplier decisions, closed sets and
labelled D transports. It independently composes all four older binary
profile-cut lists. The controls include retained and excluded records,
seven finite union-closure tests, and nine deliberately corrupted proofs.

Regeneration must reproduce the inventory and both new audit reports
byte-identically. Source hashes bind all inputs. CHECKSUMS.txt verifies
every archive member other than itself. The historical checkpoint included
in the archive is a frozen provenance record; this package does not claim
to reproduce all older audits listed in that checkpoint.

The mathematical premises and precise scope are in
B1_B2_INVERSE_UNION_EXCLUSION.md and b1_b2_inverse_union_scope.json.
Baseline composition leaves112 unrestricted B1/B2 geometries and
99 binary geometries (95 typed families,437 profile pairs). Neither joint
count changes: binary18, unrestricted20. Retained graph domains do not
assert existence of a safe, strongly connected, synchronizing automaton
or reachability of a particular S. Every negative covers all relevant S,
so applies in particular to actual reachable images.

The accepted manuscript, BibTeX and publication supplement are separate
and unchanged. This archive contains a fixed-parameter auxiliary proof.
