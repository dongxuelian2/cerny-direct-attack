# Research and editing rules

This repository studies synchronizing automata. The Open Problem 4 project has been **separated into a reader-facing theorem track**. Mathematical truth and reproducibility take precedence over formatting.

## Evidence categories

Every mathematical statement must be labelled as one of: paper proof; paper reduction plus completed finite exclusion; bounded/restricted search; counterexample; conjecture; or withdrawn/obsolete historical claim.

- A SAT model satisfying necessary constraints is **not** an automaton; an UNSAT result proves an exclusion only after the actual-to-relaxation completeness reduction is justified.
- Original input letters count individually; never charge a long macro word as one letter.
- Keep F versus F_bin, ac(S,A) versus pure compression c(S), reachable S versus arbitrary S, and any restrictions on the alphabet or transition family explicit.
- Random searches, partial intervals, timeouts and absent counterexamples never imply universal upper bounds.
- The m>=4 conjecture is **not proved**; m=3 has known large-q value 9, not 8.
- The complete 3,206,988-domain m=5 run is reported from a terminal summary, without a full committed per-domain certificate. Do not silently upgrade its audit status.

## Main Open Problem 4 reading and writing locations

1. `research/problem4/PROOF_ROUTE.md`: **concise, linear** final theorem chain and all assumptions/quantifiers.
2. `research/problem4/CERTIFICATES.md`: claim-to-code and necessary-domain map; record *completed* scopes and surviving relaxations accurately.
3. `research/problem4/AUDIT.md`: verified checks, open validation gaps and evidence provenance.
4. `research/problem4/CONJECTURE.md`: explicitly unproved conjectures and targeted negative tests.
5. `papers/problem4/main.tex`: publication-facing mathematical argument, with figures, theorem statements, sufficient detail of completeness, and references.
6. `archive/legacy/PROOF.md`: **preserved historical** mathematical notebook (not the new linear proof). Old internal section claims may be superseded. The short root `PROOF.md` is only a compatibility index for legacy deep links.

Do not append raw experiments, intermediate negative branches, abandoned threshold cases, or huge enumerations to the **main route or paper**. Put them in the historical archive or research source, with a summary and exact link from the manifest when the case supports an essential exclusion. Avoid proliferating new standalone Markdown notebooks or multiple competing 'main proofs'.

## Code and reproducibility

- `scripts/problem4/`, `scripts/direct_attack/`, `scripts/anchors/` retain their established relative paths: moving them en masse may break includes, imports and `run.py`.
- Keep necessary original source and minimal reproducibility commands. Use C++17 for large finite-domain enumerations and Python for symbolic/small independent controls.
- Place generated builds, large temporary logs, inventories and binaries under ignored `build/`. Do not mistake their absence from Git for an independent successful verification. If a future independent audit requires a portable certificate, document its exact reproducibility and consider an external artifact only with user authorization.
- `docs/RUNNING.md` is a compact index; `archive/legacy/RUNNING.md` retains the exhaustive historical run catalog.
- Do not casually edit Git history, delete original evidence or force-push collaborator work. Make organizational changes on a dedicated PR.
- Don't add CI, releases, archives or substantial new infrastructure without a clear task or explicit permission.

## Publication and audit discipline

- Keep the computational dependence chain readable: precise mathematical reduction; finite domains; actual-to-relaxation inclusion; independently auditable solver predicate; all completed ranges; and paper treatment of every relaxation survivor.
- New results update **both** the short route and the paper where appropriate; do not resurrect obsolete lines by copying older notebook paragraphs.
- Distinguish draft/not compiled from PDF checked in a renderer, and computer-assisted theorem from external peer review.
- Research/AI-assisted contributions should be disclosed accurately; authorship decisions require author review.
