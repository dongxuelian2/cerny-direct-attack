# Public repository structure

```text
README.md, CONTRIBUTING.md, LICENSE, CITATION.cff, REPRODUCIBILITY.md
.github/                 lightweight core/formal CI, five issue templates, PR template
docs/                    current status, results navigation, roadmap, notation, literature,
                         licensing, validation, structure; original baseline manuals
formal/                  accepted-module manifest and scope guide
proofs/paper/            paper-proof navigation; new proof location
computations/            computational navigation; new source location
results/                 classified result JSON/Markdown, finite index, open problems,
                         source catalog
scripts/                 reproduce.py, hydration, Unix and PowerShell check wrappers
archive/                 original-to-public hash/path inventory, historical commit list,
                         release asset manifest, archived entrypoints/prompts/templates
submission/openmath/     frozen submission identity, receipts, exact theorem inventory
submission/              historical tools/receipts retained at compatible paths
lean/                    baseline formal core and two excluded frozen drafts
post_baseline/           anchor proof sources, sprint Lean units, checkers/certificates
direct_attack/           research notes, Lean units, Python/C++ tools and retained data
src/                     baseline search/export/independent certificate checker
reference_results/       all 83 baseline certificates and baseline run records
tests/                   baseline tests and publication tooling tests
examples/                original DFA examples
```

Root historical files retained: `OPENMATH_SUBMISSION.md`, `POST_BASELINE_RESEARCH_LEDGER.md`, `STATUS.json`, `MANIFEST.sha256`, `lean-toolchain`, `run.py`, `start_unix.sh`, `start_windows.bat`, `requirements.txt`. Existing source/data paths keep compatibility. The tree is fully enumerated by Git and by [source_manifest.json](../archive/source_manifest.json) for inherited files. Scientific inputs larger than 1 MiB are release assets (57 paths in [assets.json](../archive/assets.json)); hydration restores them to ignored original locations. Generated `.reproduction/` and native/cached binaries are not part of Git.
