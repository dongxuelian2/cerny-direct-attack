# C1 actual-word staircase certificate

Conditional scope: n=13, |S|=9, A={3}, avoid-or-compress length12,
arbitrary finite alphabet. This package checks the last retained B3 third
geometry relative to the frozen entrance-fiber, exact-kernel and
inverse-clique premises. It does not determine F(13,9,1), establish alphabet
separation, or answer all parameters of Open Problem4.

Requirements: standard-library Python3.10 or newer. No Z3, NumPy, network,
external automaton library or bounded alphabet search is used.

From this directory run:

```
python enumerate_c1_word_staircase.py
python check_c1_word_controls.py
python check_c1_word_staircase.py
```

The first command enumerates every feasible first pair for all retained
immediate graphs, every literal letter in each canonical domain, and every
actual-image staircase branch. It stores complete transports and rejection
trees, sorted row/flag counts and digests, and concrete bad words supporting
every forced-letter deletion. The second checks two valid inference controls
and seven invalid-proof controls. The third independently rebuilds literal
letters by assigning kernel blocks to labelled states, uses rational span
checks, composes every deletion word on sets, and verifies all branches and
proper closed sets.

Expected outputs are c1_word_staircase_inventory.json,
c1_word_controls_audit.json and c1_word_staircase_audit.json. The isolated
reproduction procedure regenerates all three byte-identically. The ZIP is
immutable and includes per-file CHECKSUMS.txt.

C1_WORD_STAIRCASE_EXCLUSION.md explains the mathematical containment argument.
Historical checkpoint manifests are included to bind baseline data; these
three commands reproduce the new conditional exclusion, rather than rerunning
all earlier historical certificates. Earlier domain premises and their
bound sources/audits are included as frozen inputs. No exploratory files,
SAT timeouts or unsaved negative searches support the certified cut.
