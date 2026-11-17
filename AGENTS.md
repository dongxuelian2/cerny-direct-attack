# Research workflow

## Mandatory English-language policy

- English is the sole language for repository-authored explanatory prose. Write and maintain `README.md`, `AGENTS.md`, `PROOF.md`, research notes, Markdown documentation, manuscript exposition, source-code comments/docstrings, and pull-request descriptions in English. Use English for new or revised public-facing messages and instructions.
- Audit **all tracked Markdown files**, including nested directories and archives, for Chinese-language explanatory text. Translate existing Chinese proofs and documentation into precise, idiomatic mathematical English in dedicated PRs. Preserve definitions, hypotheses, quantifiers, equations, proof dependencies, numbering, cross-references, bibliographic details, code behavior, and the exact strength of every claim. Never silently shorten or reinterpret a proof during translation.
- Keep mathematical notation, source identifiers, and faithful quotations or official titles in their original form when required; provide an English explanation around any unavoidable original-language quotation. Do not leave mixed-language paragraphs, headings, tables, or code comments.
- Before completing a documentation PR, inspect every changed file for residual Chinese prose and broken links/references. Review mathematical equivalence against the original and run existing relevant checks. A character scan is a useful audit aid, not a replacement for reading or proof review.
- This requirement applies to all future contributions and edits, not only the present translation cleanup. Do not create new Chinese prose or alternate Chinese documentation copies. Keep English clear, direct, and technically specific; avoid defensive boilerplate and unsupported claims.

This repository focuses on mathematical derivations for the Černý conjecture and related synchronizing automata. Understand the exact problem, assumptions, and existing arguments before proposing lemmas, constructions, counterexamples, or proofs. Research progress takes priority over engineering packaging.

## Mathematics and computation

- Prioritize mathematical arguments. Use programs to answer specific mathematical questions; do not substitute enumeration for a proof that can be completed.
- Use C++17 for large-scale finite-field verification, combinatorial enumeration, and searches, with appropriate multithreading. Partition the search space into disjoint pieces and state whether coverage is exhaustive. Retain assertions, boundary cases, and necessary positive and negative controls.
- Use Python for small independent checks, symbolic prototypes, and orchestration, not for established large-scale hot loops.
- Distinguish written proof, exhaustive finite-domain verification, restricted-family search, and conjecture. Program checks are not automatically Lean formal proofs; timeouts and failed random searches do not establish upper bounds.
- Work toward one well-defined research target at a time, reporting the actual derivation and executed results. Do not claim unproved parameter regions or the general Černý conjecture have been solved.

## Structural reduction and proof length

- Freeze new cores and named-domain coverage for the current phase. First test whether existing general lemmas absorb lengthy case-specific arguments; see `PROOF.md#problem4-proof-structure-compression` for dependency checks and assumptions that remain necessary.
- Computer-assisted proofs already establish exact extrema at codimensions four and five. Current pen-and-paper work should reduce independent proof mechanisms and case splits, not erase validated finite-field computations.
- Reuse the established (PFX), (JMAP), (SUP), (JPB), (JEB), (JCP), and rank bounds in `PROOF.md` when applicable. Before adding a core-specific lemma, identify the precise failure of those common hypotheses and prove only the missing case.
- Structural compression must preserve the quantifiers, parameter ranges, original word lengths, and synchronization/strong-connectivity assumptions of every lemma. Eliminating one later-stage shape does not automatically replace the entire named domain.
- Keep genuinely necessary complete proofs in the research body. Select for the paper only lemmas directly serving the main theorem; refer to auxiliary finite-domain coverage and other structural findings in the research body. Check dependencies before and after edits; renaming or renumbering is not a proof simplification.

## Repository conventions

- Retain necessary source code, mathematical notes, manuscript sources, concise research guidance, and a small number of essential mathematical inputs that cannot be regenerated. Do not commit runtime logs, JSON reports, enumeration inventories, certificate bundles, or binaries.
- Put runtime, compilation, and intermediate artifacts in ignored `build/`. Rebuild from clean sources. Run `run.py` in a research copy without overwriting tracked research material.
- Do not introduce cryptographic seals, provenance manifests, release packaging, submission snapshots, release-download restoration, CI/CD, automated reports, or formal-verification pipelines unless explicitly requested.
- Keep the existing Lean mathematical source in `formal/`; do not require Lean installation or maintain build/declaration inventories.
- Do not build application services, elaborate configuration frameworks, or dependency-management infrastructure around a research script.
- Let README and research instructions directly explain the problem, proof location, how to run essential programs, and which questions remain open.
- Preserve shared Git history; do not force-push. Removing tracked files does not erase old Git objects or shrink existing clones.

## Entry points and layout

- `PROOF.md` is the single mathematical research body. Organize by mathematical question, recording exact assumptions, derivations, applicability, and open gaps. Distinguish proved results, exhaustive finite checks, restricted searches, conjectures, and withdrawn claims.
- Update the relevant section of `PROOF.md` for new results. Use stable `PROOF.md#...` anchors; avoid additional topical, dated, continuation, or run-summary Markdown notes. Do not put mathematical notes into code directories.
- Put computational sources and implementation tests in `scripts/`, grouped by topics such as `problem4/`, `direct_attack/`, and `anchors/`. `automata/` and `native/` are shared reference implementations and kernels within that layout.
- `run.py` is the unified root execution entry point. `docs/RUNNING.md` covers execution only; `README.md` is a concise index of the question, current boundary, and reading entry points. Do not duplicate the research body.
- Store LaTeX manuscripts in `papers/` and existing Lean sources in `formal/`.
- Reuse existing scripts before introducing necessary new computations. Print results to the terminal by default, put intermediate files in `build/`, and avoid extra logs or audit infrastructure.