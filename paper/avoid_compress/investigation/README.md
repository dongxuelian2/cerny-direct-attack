# Exact-formula investigation supplement

This is local research provenance. The final submission supplement is
../release/reproducibility.zip, with exact contents in ../reproducibility/README.md.
**The proposed all-parameter formula is refuted for BOTH alphabet classes:
F_bin(11,8,1)=F(11,8,1)=9.** The uniform arbitrary-alphabet proof is
CODIMENSION_THREE_UPPER_PROOF.md. The older binary-only obstruction is
historical provenance, not the current extent of the conclusion.
Historical probes and broader construction notes below are not part of
the final supplementary release. No reset-threshold result is claimed.
CURRENT_FRONTIER.md is the current authoritative research status. All 290
supplied frontier points are exact for BOTH alphabet classes, including
every parameter through n=12 and four additional n=13 points. The current
release contains a seven-page manuscript and 109 supplementary files.
The smallest unknown (13,9,1) remains in [11,12]. Investigation-only
searches, auxiliary lemmas and corrected/retracted pruning records below
are not in that supplementary release.

Quick independent verification (Python >=3.10, standard library only):

```text
python verify_certificates.py
```

Expected result: 165 checked triples, all 2<=n<=10, with binary, strongly connected, synchronizing automata and actual reachable images. Every exact local length is recomputed by ordinary subset BFS. Each certificate includes literal reaching, attaining and reset words.

The uniform proofs `COFINAL_PROOF.md` and `DEFECT_TWO_PROOF.md` determine all n>=2s-r-1 and all n-s<=2. Their generators, independent checkers and data are included. Reproduce the family audits with `python check_cofinal.py`, `python check_boundary.py` and `python check_defect_two.py`. The reports check 316, 33, 300 and 378 parameter choices; these finite checks support, rather than establish, the uniform proofs.

To reproduce the exhaustive small binary cover from this directory, compile the portable C++17 source with a working compiler, for example:

```text
clang++ -O3 -std=c++17 exhaust_binary.cpp -o exhaust_binary.exe
```

PowerShell:

```powershell
2..7 | ForEach-Object { ./exhaust_binary.exe $_ "binary_n$_.json" }
python audit_small.py
```

`audit_small.py` checks all saved witnesses and repeats a complete, labelled, explicitly-A-enumerated independent search for n<=4. The first-letter orbit cover for n=7 contains 282,475,249 row pairs, not that many isomorphism classes.

The remaining sources and reports document bounded construction tests:

* `structured_probe.cpp`, `structured_n8.json` ... `structured_n12.json`: one fixed three-active-state action and permutation paths through other states. Compile as above and invoke `structured_probe.exe n structured_nN.json`.
* `active_probe.cpp`, `active_n*_h*.json`: arbitrary first action on h active states with other states fixed, and permutation paths between the active states. Invoke `active_probe.exe n h active_nN_hH.json`. The scans target s=n-3,r=1. They stop upon attaining the known upper bound; scans below the bound run the complete stated structured scope. A failed structured scan is not an exhaustive automaton counterexample.
* `audit_extensions.py`, `extension_audit.json`: independent ordinary-set checks of the structured witnesses and four failed direct extensions of Proposition 5. Invoke `python audit_extensions.py` after generating the saved structured and active files.
* `chain_probe.py`, `chain_probe.json`: finite checks of a direct chain variant; failures of its synchronization or delay hypotheses are retained as diagnostics.
* `reuse_probe.py`, `reuse_n*.json`: all actual reachable images in the original manuscript families through n=12. These two generation scripts and `assemble_certificates.py` import the manuscript's unchanged `../reproducibility/generator.py` or their local checker modules as indicated in the source; the standalone certificate check has no such dependency.
* `unresolved_intervals.json`: lower bounds found by these probes and the known upper bounds, with no assertion that an interval's lower endpoint is the true maximum.

`reproducibility.zip` in this directory is a **standalone verification package**: this README, the audit, `verify_certificates.py`, the 165 certificates, `exhaust_binary.cpp`, `audit_small.py`, six exhaustive-cover reports, `small_case_audit.json`, `extension_audit.json`, `unresolved_intervals.json`, both uniform proof notes, both family generator modules, three family checkers and four family reports, the original software LICENSE and `SHA256SUMS.txt`. It excludes search implementation files, SMT checkpoints and raw structured outputs; the audit reports their bounded scope. Those sources remain beside this README in the repository. The ZIP's hash is recorded in `ARCHIVE_SHA256SUMS.txt`.

The local ZIP above is a historical snapshot predating the binary obstruction. Use only ../release/reproducibility.zip for the current paper. The current source archive and submission bundle contain the seven-page manuscript, arbitrary-alphabet codimension-three upper, cofinal and low-codimension constructions, uniform two-block proof and finite frontier. Historical local checksums describe the old snapshot, not the current sources.
