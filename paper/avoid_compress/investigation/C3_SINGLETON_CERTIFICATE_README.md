# Binary c3 singleton-third-entrance certificate

This auxiliary package contains C3_SINGLETON_THIRD_EXCLUSION.md and
an independent finite audit of its symbolic proof. Together with the
three earlier c3 third-profile proofs included here, it excludes the
entire binary c3 joint orbit at (13,9,1). Unrestricted c3 is not excluded.
The paper's 109-file supplement remains unchanged, and both extrema
at (13,9,1) remain [11,12].

The further conclusion |B|<=2 also uses the earlier audited exclusions
of the other B3 second-entrance shapes. They are explicitly named in
the proof and indexed by the repository's auxiliary audit; their larger
native certificates are separate and are not reproduced in this minimal
package. Likewise the established H cover is a premise here. This package
does not claim a complete answer, new F value or alphabet separation.

Python 3.10+ and its standard library suffice:

```sh
python check_c3_singleton_third.py
```

The checker must report status pass, fourteen binary letter pairs,
27,041 abstract X kernels, 306 typed core maps and 864 nonconstant
core configurations, with 29/43 remaining joint records. It independently
enumerates all kernel partitions, shared outside-pair restrictions,
actual disjoint input types and B indegrees. It checks backward pair
preimages, non-H input ports for the explicit short pair witnesses,
and literal short core reachability. Port checks cover conservative
block choices; they are not full completed transition-table scans.

Read the paper proofs for the universal case arguments. This checker
audits the new singleton case; the other included c3 proofs have their
own earlier independent certificates. The singleton antecedent note is
used for its five-pair endpoint budget, not its historical native scan.
No solver, timeout result, rank tolerance or full-frontier data is needed.
CHECKSUMS.txt authenticates the original bytes, and the new independent
audit regenerates byte for byte from this standalone package.
