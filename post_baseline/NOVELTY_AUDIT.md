# Prior work and novelty audit (2026-09-28)

This is a bounded literature audit, not a proof of priority. Mathematical
status and publication novelty are separate. The exact anchor formula and
layout theorems have paper proofs in this repository. Their novelty status
is **LOOKS NEW; NOT FULLY CONFIRMED**. No first-discovery claim is made.

## Sources checked and distinctions

| Primary source | Established subject | Relation to the present result |
| --- | --- | --- |
| M. V. Volkov, *Synchronization of finite automata*, Russian Math. Surveys 77(5), 819–891 (2022), [full article](https://www.mathnet.ru/eng/rm10005), DOI 10.4213/rm10005e | General survey; Proposition 3.1 states and proves the classical Cerny-family threshold `(n-1)^2` | That quadratic threshold is prior work, used in the injective boundary and modular-layout corollary. Our `B_r` is a different, information-quotient distance. |
| M. Szykuła, *Synchronizing Automata: Open Problems*, [arXiv:2608.24245](https://arxiv.org/abs/2608.24245), 2026 | Current overview; subset synchronization, subset compression, power-set methods and algebraic bounds | Fixed-subset synchronization and easiest k-subset synchronization preserve actual subset trajectories. They do not permit independent changes of representative between letters. No identified statement in this source gives the present anchor formula. |
| A. Kisielewicz, J. Kowalski, M. Szykuła, *Computing the shortest reset words of synchronizing automata*, J. Combin. Optim. 29, 88–124 (2015), [publisher full text](https://link.springer.com/article/10.1007/s10878-013-9682-0), DOI 10.1007/s10878-013-9682-0 | Exact bidirectional search in the power automaton | BFS, reverse search, subset pruning and exact-reset computations are established techniques. We do not claim an algorithmic invention from using them. The new construction is search-free. |
| A. Kisielewicz, J. Kowalski, M. Szykuła, *Experiments with Synchronizing Automata*, [author-hosted paper](https://kot.rogacz.com/Publications/Kisielewicz2016ExperimentsWith.pdf) | Exhaustive experiments; Cardoso's subset bound, discussed as Conjecture 7, is tight for subsets of the Cerny family | This is close-looking but different: the parameter is concrete subset size, not retained membership information in an existential quotient. |
| M. V. Berlinkov, M. Szykuła, *Algebraic synchronization criterion and computing reset words*, Information Sciences 369, 718–730 (2016), [author preprint](https://arxiv.org/abs/1412.8363), DOI 10.1016/j.ins.2016.07.049 | Algebraic synchronization methods and reset bounds for finite-prefix-code/Huffman decoders | A binary-tree/prefix-code connection to synchronization already exists. Here `E(r)` describes marked-state information in an abstraction of Cerny automata, rather than a decoder's reset threshold. |
| J. Araújo, P. J. Cameron, B. Steinberg, *Between primitive and 2-transitive: Synchronization and its friends*, EMS Surv. Math. Sci. 4, 101–184 (2017), [publisher PDF](https://ems.press/content/serial-article-files/36997?nt=1), DOI 10.4171/EMSS/4-2-1 | Permutation groups together with singular transformations | Permutation-based synchronization is a substantial established area. Our orbit interpretation is an elementary costed semantic reformulation: hidden permutations cost zero, original letters cost one. It is not presented as new group theory. |
| M. Golin, A. Schuster, *Optimal point-to-point broadcast algorithms via lopsided trees*, Discrete Applied Math. 93(2–3), 233–263 (1999), [publisher abstract](https://www.sciencedirect.com/science/article/pii/S0166218X99001079), DOI 10.1016/S0166-218X(99)00107-9 | Broadcast schedules modeled by trees with unequal edge lengths; postal-model analysis | The delayed binary genealogy resembles known lopsided-tree scheduling. Full text was not available through the accessed endpoint. Priority for the isolated relaxed scheduling recurrence is therefore **OPEN**, even though its proof here is independent. |
| J. Bruck, L. De Coster, N. Dewulf, C.-T. Ho, R. Lauwereins, *On the design and implementation of broadcast and global combine operations using the postal model*, IEEE TPDS 7(3), 256–265 (1996), [institutional record](https://authors.library.caltech.edu/records/43aw7-78d60), DOI 10.1109/71.491579 | Latency-dependent broadcast and combine schedules | Additional established scheduling context. The available record/abstract was inspected; the linked PDF fetch failed. It does not settle whether our exact event recurrence is new. |

The equal-weight optimal binary-tree external path length is a classical
prefix-code fact; the manuscript gives its elementary balancing proof.
Huffman's 1952 paper has DOI 10.1109/JRPROC.1952.273898. Its original PDF
fetch failed here, so the general coding background is cross-checked through
the primary Berlinkov–Szykuła paper rather than claimed from unread content.

## Search scope and outcome

Searches combined Cerny/Černý, synchronizing automata, subset/power automata,
reset threshold, subset compression, potential/ranking, quotient abstraction,
marked states, landmark information, anchor, binary trees, prefix codes,
external path length, free permutations, broadcast, and lopsided trees.
Exact cross-topic searches included `"Černý" "external path length"`,
`"Cerny" "quotient" "anchor"`, `"Cerny" "landmark" automata`,
`"synchronizing automata" "marked" "abstraction"` and
`"synchronization" "lopsided trees"`.

No directly matching theorem was located for

    B_r(n)=3n+E(r)-2r-3,  r>=2, n>=r+2,

with this cardinality-plus-membership existential abstraction, nor for the
capacity-two realization and same-count layout order separation (now three
orders, including an exact linear endpoint family). This is
negative search evidence, not proof of nonexistence. Search engines omit
papers and may index notation poorly. The broad surveys were read for the
relevant definitions and nearby problems, not exhaustively verified reference
by reference. Strong priority claims require further citation tracing,
especially the lopsided-tree scheduling literature and abstraction/model
checking literature.

## Claim-by-claim classification

* **KNOWN:** the Cerny-family quadratic reset threshold, power-automaton
  search, subset-distance monotonicity, binary prefix-code optimization,
  and links between prefix codes and synchronization.
* **REFORMULATION / STANDARD ARGUMENT:** feature classes as hidden-permutation
  orbits, zero-cost orbit moves, potential telescoping, monotone-simulation
  distance transfer, nonincreasing integer stabilization.
* **LOOKS NEW; NOT FULLY CONFIRMED:** the all-parameter contiguous-anchor
  formula, explicit capacity-two clock schedule with realizability proof,
  exact information increments, the linear endpoint family, and the
  adjacent/periodic order separation
  for the same number of anchors.
* **OPEN PRIORITY:** the standalone relaxed binary-release recurrence and
  its dyadic solution; comparison with postal/lopsided-tree models is needed.
* **NO STRONG NOVELTY CERTIFICATION:** this sprint alone cannot support a
  claim of first discovery or a complete bibliographic exclusion.

Subsequent results include forced optimal genealogies, absence of ineffective
b in every optimum, an exact reduced optimal-language description, and the
sharp dyadic capacity threshold M_r. These are likewise **LOOKS NEW; NOT
FULLY CONFIRMED**, with paper proofs. Additional searches for
`"synchronizing automata" "optimal language"`,
`"reset words" "quotient abstraction"`, and `"Černý" "marked states"`
did not identify a direct matching statement. Irrelevant hits were not used
as evidence for technical claims. The isolated scheduling extremal theorem
still needs comparison with the primary lopsided-tree literature.

The work proves an exact information-limited lower-bound model for one
family. It does not prove the Cerny conjecture or improve a known upper bound
for arbitrary synchronizing automata.
