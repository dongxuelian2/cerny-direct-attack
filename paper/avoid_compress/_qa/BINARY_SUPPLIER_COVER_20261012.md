# Two-letter supplier coverage

Let L be the retained literal pool, and suppose the actual alphabet E is
contained in L and meets every required domain R_j. If |E|<=2, the two
membership patterns of its letters must together cover every group index.
Repeated labels or equal transformation rows do not change this condition.
Every literal letter contributes one pattern. If no pair of these patterns,
including a pattern paired with itself, covers all indices, no binary
actual alphabet meets the necessary supplier requirements.

The generator tests every distinct pair of patterns. The independent
checker builds group memberships with ordinary sets, reconstructs the
complete pattern inventory and checks all pairs with replacement. An
empty required group is left to the existing missing-group rule. A
covering pair returns no cut and is not automatically a witness: safety,
strong connectivity, synchronization and reachable-image checks remain.

This elementary binary-only rule needs no extremal or alphabet-separation
claim. A complete native-geometry use must still cover every transported
prefix and pass the independent flag checker and isolated replay gates.
