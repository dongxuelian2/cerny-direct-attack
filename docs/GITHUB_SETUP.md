# GitHub collaboration setup

Public repository: [dongxuelian2/cerny-direct-attack](https://github.com/dongxuelian2/cerny-direct-attack). Default branch `main`; Issues enabled; wiki disabled; merged PR branches automatically deleted. Topics: `cerny-conjecture`, `synchronizing-automata`, `lean4`, `formal-verification`, `reproducible-research`.

Labels: proof, formalization, computation, literature, counterexample, exploratory, documentation and bug. Five issue templates and a proof-status/reproduction PR template are committed under `.github/`.

Main protection requires the `core` and `formal` checks with an up-to-date branch, resolves review conversations, disallows force pushes/deletion and dismisses stale reviews. Mandatory reviewer count is zero; administrator enforcement is disabled so the owner can maintain the repository alone. Peer review remains recommended for substantive mathematical changes. No collaborator was added; the owner should invite the actual collaborator through repository Settings → Collaborators when their username is known.

The first public commit was `1b6b1aa7735584a9fe280a7de634321f1fe0efe6`. [Its initial GitHub Actions run](https://github.com/dongxuelian2/cerny-direct-attack/actions/runs/37110164179) passed both core and formal jobs. Subsequent run/release status is recorded in the final handoff and validation receipt; CI is not a paper-proof audit.

The release holds checksum-pinned scientific-data and path-redacted OpenMath payload ZIPs, with separate checksum files. Exact original OpenMath ZIP/bundle remain in the original local checkout and are not uploaded with private machine paths. There is no unresolved oversized-Git-file issue. The repository adopts MIT; cited third-party works retain their own rights. No affiliations/coauthors are invented. If the owner wants a full name/ORCID citation, they can update CITATION.cff later; the current metadata uses the authenticated handle.
