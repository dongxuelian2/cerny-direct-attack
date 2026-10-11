# Černý direct attack

Direct research on the Černý conjecture, with explicit proof boundaries and reproducible certificates. **The general conjecture remains OPEN.** This repository makes no priority claim for auxiliary results whose literature audit remains open.

The strongest current branches are:

- **Open Problem 4 (2026-10-11):** the seven-page partial-answer paper determines the low-codimension and cofinal regions, refutes the proposed formula, and preserves the latest conditional search reductions. The latest auxiliary snapshot has 171 audits, 84 remaining unrestricted geometries and no remaining B3 geometry; the first unresolved point (13,9,1) remains in [11,12]. [Paper](paper/avoid_compress/main.pdf), [research handoff](paper/avoid_compress/HANDOFF.md).
- **Quadratic image-extension obstruction:** paper constructions refute every universal linear bound for the repository's actual-image extension quantity, including fixed binary alphabets. These are method obstructions; their automata still have square-bounded resets. [Proof](direct_attack/FIXED_ALPHABET_QUADRATIC_IMAGE_EXTENSION.md).
- **Avoid-or-compress sharpness:** paper families attain the known bound along infinite state-count progressions for every fixed cardinality pair. The known upper bound is attributed in the source. [Proof](direct_attack/AVOID_COMPRESS_ALL_GAPS.md).
- **Rank-two / low-rank permutation classes:** paper reset normal forms and linear bounds for explicitly restricted alphabets; higher-rank boundaries remain separate. [Proof](direct_attack/RANK_TWO_ONLY_NONPERMUTATIONS.md).
- **Congruence/profile compression:** paper bounds for compressible minimum classes, refined by terminal-kernel arguments. No general short common suffix follows. [Profile bound](direct_attack/PROFILE_CLASS_COMPRESSION.md), [refinement](direct_attack/TERMINAL_KERNEL_FRANKL.md).
- **Figure-3 / compress-with-another:** the completed family has paper specified-state threshold `4p`, and an original reset upper bound `3p²+4p−1`, for `p≥3`. The matching reset lower bound is conjectured. [Threshold](direct_attack/COMPRESS_OTHER_EXACT_LOWER.md), [reset](direct_attack/COMPRESS_OTHER_SHORT_RESET.md).
- **Later subclass squares:** paper results cover stated rooted/core-cycle models, including primitive opposite output pairs with arbitrary tail geometry. They do not reduce arbitrary automata to those models. [Latest proof](direct_attack/OPPOSITE_KERNEL_PRIMITIVE_SQUARE.md).

**Formal verification:** the frozen OpenMath core has ten Lean 4.19.0 modules and 100 declarations (including helpers). It checks potential/graph soundness, C3/C4 finite subset paths, the literal Kari inverse-shrink obstruction and length-25 base cut, layered-pair certificate soundness, and the abstract reflection cut. A separate post-release module proves the literal n25 extension minimum 10. General family instantiations remain paper proofs. Two noncompiling baseline drafts are excluded. [Exact inventory and scope](formal/README.md).

## Start here

Python 3.10+ needs no third-party packages. With Lean 4.19.0 on PATH:

```sh
python scripts/reproduce.py --suite core
python scripts/reproduce.py --suite formal
```

Use `python3` on systems where that names Python 3. Windows wrappers are `scripts/check_core.ps1` and `scripts/check_formal.ps1`. [Reproduction guide](REPRODUCIBILITY.md) explains compiler selection, certificate replay, data hydration, and expensive audits.

Read the [result index](results/theorem_index.md), [computational index](results/computational_index.md), [current status](docs/STATUS.md), and [collaboration guide](CONTRIBUTING.md). Detailed chronological records remain in [direct-attack results](direct_attack/RESULTS.md) and the [research ledger](POST_BASELINE_RESEARCH_LEDGER.md); historical statements retain their checkpoint scope and may be superseded by later entries.

## Layout and provenance

`formal/`, `proofs/paper/`, and `computations/` are navigation layers. Existing `lean/`, `post_baseline/`, `direct_attack/`, `src/`, and `reference_results/` paths remain executable source locations because scripts and certificates depend on those paths. [Exact tree](docs/REPOSITORY_STRUCTURE.md).

The [OpenMath freeze](submission/openmath/README.md) records commit `ac948e7001bff5428c22d236f96974856452d34d`, mathematical input `f30afd64643d785dff7ec5d44c730cb36a80dce6`, and original ZIP SHA-256 `1a09dadd3de876028430fa4dc7aa8353f600075d8daff9c5eae79e0a8ed7c050`. Historical Git objects and the exact original ZIP remain in the original local checkout; this public repository starts a documented publication snapshot, without rewriting that history. [Provenance and exclusions](archive/README.md).

Bulky scientific inputs are checksum-verified [release assets](archive/assets.json). The public OpenMath payload has path-redacted metadata and a distinct checksum; it is explicitly not the immutable original ZIP. Sources and retained evidence are MIT licensed; cited third-party works keep their own rights. AI assistance and historical baseline provenance remain disclosed in the original submission report.
