# After the formal Kari obstruction: all-d product tradeoff

Date:2026-10-02. Start HEAD7bd8e4b. General Cerny OPEN.
Research continued after the previous intermediate commit, without
repeating the original reset-threshold search or old failed shortcuts.

The unique forward-to-backward one-decrease bridge is47->60. A fresh
backward finite invariant classifies EVERY last decrease as45->44 or
47->60. This enabled an independent-coordinate Cartesian family,
n=6^d/alphabet2d, requiring at leastd decreases in EVERY reset.
It was then attacked for cost compatibility: minimum largest absolute
loss3^(d-1) differs from best ordinary-shortest loss4^(d-1), with exact
minimum cost27d-2 versus ordinary rt25d. All matching schedules keep
the factors compatible and reverse ONE literal original word.

The product proofs are PROVED paper for ALL d, not a finite extrapolation.
The original singular coranks grow exponentially, so this does not settle
whether all-corank<=1 automata permit a constant decrease budget. No
fixed alphabet, novelty, near-critical threshold or Cerny proof claim.

KariShrinkProducts.lean also upgrades the earlier only-computational
literal base cost25 LOWER bound to FORMALLY VERIFIED. It proves ALL-word
last-bridge classification,25 lower,27 lower when the last bridge enters
size3, and the matching25/27 phase witnesses. The arbitrary-d Cartesian
lifting remains paper. The first attempt at elaboration exposed a reserved
identifier, unwanted dependent hypotheses during revert and a missing
decidability unfolding; these were repaired before a clean captured
compilation. Failed elaborations/sorryAx output are never proofs.

Independent checker controls: ALL64 literal masks,128 cut and362 Bellman
edges,744 base particle letters,20 symbolic parameters191640 controls,
ALL Cartesian states at d1..4 with608424 controls in both directions,
TEN rejected corruptions. Large-d masks/words are not exhaustively covered.
The complete d2 RECTANGLE graph additionally has4096 nodes/81900 Bellman
controls over ordinary, loss caps2/3/4 and cap3 count/cost certificates:
50, impossible,52,50 and(3,52), respectively. The cap2/cap3 corruptions
are rejected. This independently attacks the exact cost/loss tradeoff.
Generation replays without normalization. The registry135/216 preserves
the previous134 capture records verbatim; no full135 rerun; native builds8.
Compiler/source hashes and exact Git/manifest coverage are sealed.

New primary literature2609.21603 was consulted. Its per-subset sign
certificate does not give a general reset bound, and its own Section8
already rejects B as a flat-walk potential and a universal flat-only walk.
Those documented failures are not re-run as allegedly fresh conjectures.

The unrestricted proof bottleneck remains a compatible paid chain that
allows actual inverse decreases and still fits the square. The stronger
fixed-root/coprime square subclass remains PROVED paper, not formal.
All changes stay within direct_attack; frozen168ffff remains unchanged.
