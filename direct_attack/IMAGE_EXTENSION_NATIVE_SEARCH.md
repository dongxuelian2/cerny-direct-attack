# Direct adversarial tests of a precise linear-capacity target

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

**CONJECTURED / OPEN:** in every strongly connected synchronizing DFA,
every nonempty proper reachable image S satisfies e(S)<=2n, where

    e(S)=min{|u|: a reachable T has |T|>|S| and Tu subset S}.

The larger image may be Q; a preimage may first lose cardinality. This
candidate is stronger than the known conjecture that some universal linear
constant exists. It is not necessary for the Cerny square bound. The saved
five-state cost 10 already forces C>=2 for the literal e(S)<=Cn envelope,
without additive slack. Finite tests do not establish any uniform constant.

Complete binary image-extension coverage through n=6 has maxima 2,3,6,10,11.
The new dedicated native objective maximizes e over ALL proper reachable
images, rather than maximizing reset threshold or global policy cost. It
uses exact full-powerset / capacity scoring and freezes the initial rows.

| n | binary frozen seeds | mutation proposals | SC synchronizing proposals | max e observed |
|---|---|---|---|---|
| 10 | 779 | 30000 | 23397 | 16 |
| 11 | 856 | 30000 | 23123 | 18 |

The n11 seeds explicitly include the alternating-folding family and the
nonhereditary permutation/unit-defect family. The maximum n11 witness is
the alternating family; the search did not improve its cost 18. These are
proposal counts, not distinct automata, complete covers, or nonexistence
proofs. Eight improving e/policy certificates are retained, and independent
ordinary-set inverse BFS checks every stored reachable-image e and policy
value. The exact 2n-4 arbitrary-parameter LOWER bound for the alternating
middle layer is still unproved; its explicit upper word and finite layer
computations do not establish an asymptotic coefficient with additive slack.

The unrestricted target and the global all-tie policy square target remain
separate open routes. No general reset bound or new formal theorem follows.
