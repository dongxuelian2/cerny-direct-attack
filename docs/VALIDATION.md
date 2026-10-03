# Publication validation

Fresh executions on 2026-10-03 (Asia/Shanghai), Python 3.12.14, Windows x86_64. These runs use the derived public checkout; they do not replace or rewrite historical OpenMath receipts. Complete portable commands, outputs and exit codes are linked below.

| Check | Fresh result | Receipt |
|---|---|---|
| Authoritative Lean compilation and theorem/axiom checks | PASS: 11 modules, 114 declarations; ten frozen modules/100 declarations and one separate later module/14 declarations. Exact Lean 4.19.0. No sorryAx or unapproved axioms. | [formal](validation/formal.json), [exact public inventory](../formal/public_inventory.json) |
| Baseline tests and publication tooling tests | PASS: 17 methods, including the original 14, all 729 binary three-state automata, 128 seeded controls and rejection checks | [core](validation/core.json) |
| Independent baseline certificates | PASS: 83/83 (55 exact, 11 bounds, 17 nonsynchronizing) | [core](validation/core.json) |
| Strongest-branch independent replay | PASS: nine checks; path-fold and binary quadratic obstruction, two avoid/compress families, two rank-two classes, class compression, n25 extension cut and latest primitive opposite-kernel controls, including corruption rejection | [focused](validation/focused.json) |
| Post-baseline registered checks | PASS: ten existing checks; affine certificates cover 10,343,428 local representatives r2…17; manuscript check is static source consistency, not PDF compilation | [post](validation/post.json) |
| C++ build | PASS: all 15 committed C++ sources, g++ 4.9.2 with C++11; no pressure search launched | [native](validation/native.json) |
| Scientific asset hydration | PASS: all 57 allowlisted members restored and full ZIP/member SHA-256 values verified | [asset manifest](../archive/assets.json) |
| Python/JSON syntax, source integrity, internal links, privacy | PASS at the prepublication checkpoint: 402 Python sources at the publication checkpoint; all public JSON and relative Markdown links checked; included public JSON parses; no secrets/private emails/private machine paths detected in tracked text | [core](validation/core.json) |
| Preserved manual metadata | Word creator/lastModifiedBy empty; no private path/email in document XML; no PDF author field found | Original manuals retained without changing timestamps |
| Git whitespace | PASS: staged initial tree `git diff --cached --check`, and `git diff --check` | Repeated by core CI |

The separate 146-command historical direct registry completed: **PASS, 146/146 checks**, on isolated public copies. The first 30 successful executions were retained from the initial attempt; after repairing path/EOL hash adaptation, the remaining 116 ran in dependency-migrated scratch. Every command returned zero. [Complete execution receipt](validation/audit.json) preserves the actual outputs and records the restart; this is a public-metadata replay, not a byte-identical rerun of the immutable ZIP. The historical immutable OpenMath 146/146 receipt remains in `submission/openmath/validation_direct.json`. Expensive searches are excluded from CI.

The citation fields were reviewed against the [official CFF 1.2.0 schema](https://raw.githubusercontent.com/citation-file-format/citation-file-format/main/schema.json); the authenticated owner's handle is used without affiliations/coauthors. [License scope](LICENSING.md). Public GitHub CI passed both jobs on the initial commit and the collaboration commit. [Configuration and CI links](GITHUB_SETUP.md). The final documentation commit is checked before release publication.
