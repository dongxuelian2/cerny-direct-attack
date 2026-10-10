# Singleton B and a two-point C completing H

This auxiliary certificate excludes binary equality at (13,9,1) in
the joint B={0},C={1,2}. All two third-profile orbits are included:
D={4} (fourteen earlier pairs), D={1,4} (three pairs). Initial
reachability of S is unnecessary for this negative. Larger alphabets
are not excluded by this certificate.

With Python 3.10+ and the standard library, run:

```sh
python check_b1_c2_h_cover.py
```

The checker independently regenerates all outside-C injective kernel
partitions from unrestricted set partitions. It retains170/42 row
patterns and497/54 kernel pairs in the two D profiles. Seventeen
singleton-D configurations have a universally inverse-closed graph;
the remaining cases are covered by the symbolic short-word proof.
No C3 kernel budget is used: protected0 turns the H-cover into the
actual two-point C-cover of P5.

The complete normalized row controls at n=6,7,8 contain752,11,952,
301,824 assignments. Every stated merging word is evaluated on its
literal rows. Inverse-closed pair graphs and incoming obstructions
are checked separately. These are controls under the stated local
pair premises, not equality claims at the smaller subset sizes.

All362,880 ordinary R-output permutations and362,880 J-output
injections are checked individually at n=13. The L port controls
include replacement of4 by either unused protected input. Coupled
ordinary permutations remain free in the symbolic proof. This is
not a full13-state transition-table scan.

Composition with previous complete exclusions leaves24 binary joint
cases,43 unrestricted. The intact inventory retains161 binary typed
third orbits /884 earlier pairs. Both extrema at(13,9,1) remain[11,12];
no numerical alphabet separation follows. The article and109-file
release are unchanged, and the full goal is incomplete.

CHECKSUMS.txt authenticates all bytes. The standalone checker and
generator regenerate their JSON outputs byte for byte. Earlier
equality/cover proofs are included; their prerequisite certificates
remain separate.
