# Lean kernel: abstract layered-certificate soundness

Date: 2026-10-01. **FORMALLY VERIFIED**, Lean4.19.0.
Concrete all-p family instantiation remains **PROVED (paper)** plus
**COMPUTATIONALLY VERIFIED** finite controls. General Cerny **OPEN**.

`LayeredPairBarrier.lean` formalizes the directed-pair certificate used in
COMPRESS_OTHER_EXACT_LOWER.md. Its state type and noncollapsing edge relation
are arbitrary. The hypotheses are exposed in `LayeredCertificate`:

* An index starts at0 and increases by at most1 per original edge.
* The first layer C has a potential increasing by at most1 on internal
  edges; each outside entrance is paid by the source index plus1.
* The second layer H has the same internal condition and entrances paid
  by either the previously proved C potential or the source index.
* Every entrance to a merging source K comes from H with potential
  at least bound-2, stated WITHOUT truncated subtraction.
* Every outside entrance to the other merging region U comes from K.
* The initial state is outside C, H, K and U.

`layered_invariants` proves all five bounds simultaneously along ANY
finite path: index<=time, C and H potentials<=time, K needs at least
bound-1 steps, and U needs at least bound steps. The induction handles
arbitrarily many exits and reentries. `first_collapse_cost` then proves
that a final merging letter from K or U has total cost>=bound.

The source compiles using only Std, with no extra axiom declarations,
proof holes, `native_decide`, foreign implementations or unsafe code.
The printed dependencies of BOTH theorems are exactly the standard Lean
axioms `propext`, `Classical.choice`, `Quot.sound`. The checker captures
the literal compiler invocation, version, exit code, standard output,
source SHA256 and executable SHA256. Successful kernel checking certifies
the conditional theorem, not its unstated hypotheses.

This file does NOT formalize the Figure3 transition rows, the excluded
main-pair invariant, complete symbolic entrance classification, or the
literal matching word for EVERY p. Those concrete steps are retained as
paper proofs with independent finite checks. In particular the general
Cerny upper bound remains OPEN and is not a consequence of this lower
certificate. Priority remains OPEN.

Registry115/198 preserves checkpoint114 verbatim and appends the Lean
compiler checker only. The198 mathematical data regeneration commands
are unchanged. This is not a fresh full115-check rerun.
