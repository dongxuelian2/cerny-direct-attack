# Reproduction

The single entry point is `python scripts/reproduce.py --suite SUITE`. Run from the repository root. All receipts go to ignored `.reproduction/`; accepted evidence is never overwritten.

| Suite | What it checks | Cost |
|---|---|---|
| `core` | 14 baseline unittest methods (729 binary n3 automata, 128 seeded controls, corrupt certificates), 3 publication tests, all 83 baseline certificates, Python/JSON syntax, documentation links, publication integrity/privacy | Lightweight; normal CI |
| `formal` | Ten frozen Lean modules plus the separate post-release module; exact declaration inventory, forbidden-code scan and printed axioms for every theorem | Kernel computations may take several minutes; normal CI with generous timeout |
| `certificates` | All baseline certificates, independently of the search engine | Lightweight |
| `focused` | Nine independent checks of the strongest retained branches, including rejection controls | Opt in; hydrate data first |
| `post` | Ten existing post-baseline checks, including 10,343,428 affine local representatives | Expensive; opt in, hydrate data first |
| `audit` | Existing 146-command direct-attack registry, on an isolated copy with public path/hash metadata migration | Potentially hours; opt in, hydrate data first; no new search generation |
| `native` | Build each committed C++ source with C++11, without running pressure searches | Compiler dependent; opt in |
| `all` | Core and formal | Same accepted CI scope |

Python: **3.10+**, standard library only; `requirements.txt` intentionally has no packages. Public validation records the actual interpreter version. Lean: exactly **leanprover/lean4:v4.19.0**, upstream compiler commit `6caaee842e94`, bundled `Std`, no Mathlib or Lake dependency download. Install the toolchain separately and put it on PATH; the runner refuses a different version. Select an installed executable with `--lean PATH` or `ORION_LEAN`. On Windows, `& ./scripts/check_formal.ps1 -Python python -Lean lean` works with installed commands. `.olean` files are generated into `.reproduction/formal/`.

C++: `g++` or compatible compiler supporting `-std=c++11`; use `--cxx PATH` / `CXX`. The historical Windows preparation used g++ 4.9.2. Current wrappers use PATH/environment selection. Compiler binaries are excluded.

```sh
python scripts/reproduce.py --suite core
python scripts/reproduce.py --suite formal --lean lean
python scripts/hydrate_data.py
python scripts/reproduce.py --suite focused
python scripts/reproduce.py --suite post
python scripts/reproduce.py --suite audit
python scripts/reproduce.py --suite native --cxx g++
```

Hydration downloads the pinned `scientific-data.zip` from release `v0.1.0`, checks the full ZIP SHA-256 and every extracted member, and writes only the allowlisted ignored data paths. For offline use, add `--asset /path/to/scientific-data.zip`. It refuses an unexpected file or checksum. These include large certificates as well as pressure inputs; storage size does not imply proof strength.

The historical `submission/check.py` and `submission/package.py` are preserved tools for the original sealed Git history, not publication entry points. They require original objects/seals and the old exact tracked-Lean set. The public runner selects modules explicitly, checks the published source manifest, and keeps the post-release formal unit separate. The optional registry audit translates known historical file hashes to the corresponding public bytes only in its scratch copy; original hashes stay in the provenance manifest. Its result is recorded as a public-metadata replay, never as a rerun of the byte-identical OpenMath freeze. Do not use `direct_attack.reproduce --full` for ordinary validation: it regenerates searches.

Python/C++ acceptance is **COMPUTATIONALLY VERIFIED**, even when historical output says `VERIFIED`; it is never promoted to Lean verification. Formal imports, hypotheses and axiom dependencies are part of the exact statements. [Formal inventory](formal/README.md), [frozen receipts](submission/openmath/VALIDATION.md), [fresh publication receipt](docs/VALIDATION.md).
