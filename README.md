# Černý conjecture and synchronizing automata

This repository studies synchronizing automata, subset compression, and the
avoid-or-compress problem. Let `n` be the number of states, `s = n − m` the
size of the initial image, `r` the size of the protected subset, and
`q = n − r`. The extrema below concern strongly connected synchronizing
finite automata, reachable images, and `1 ≤ r < s`; the binary extrema
restrict the alphabet to two letters.

## Results

- **Codimension three, paper proof:** for `n ≥ 5` and `1 ≤ r < n − 3`,
  `F_bin(n,n−3,r) = F(n,n−3,r) = min(q,9)`. For `n ≥ 6`, the upper
  compression bound follows from the short-pair classification, trajectory
  ranks, and the action of the original letters. Binary constructions give
  the matching lower bound.
- **Codimension four, computer-assisted proof:** for admissible `n,r`,
  `F_bin(n,n−4,r) = F(n,n−4,r) = min(q,11)`.
- **Codimension five, computer-assisted proof:** for admissible `n,r`,
  `F_bin(n,n−5,r) = F(n,n−5,r) = min(q,14)`.

The upper bounds in codimensions four and five combine mathematical reductions
with exhaustive finite computations; binary constructions give the matching
lower bounds. The general Černý conjecture and the complete exact extrema
for `m ≥ 6, q ≥ 3m` remain open.

## Proofs and paper

- [Paper source](papers/problem4/main.tex): exact results, constructions,
  and computer-assisted proofs for codimensions four and five, with the
  codimension-three compression proof in an appendix.
- [Codimension-three proof](PROOF.md#problem4-codimension-three-upper-proof):
  nine short-pair types and `c(S) ≤ 9`; the
  [rank and image lemmas](PROOF.md#problem4-paper-three-domain-ranks) give
  a paper argument.
- [Independent codimension-three lemmas](PROOF.md#problem4-defect-three-independent-lemmas):
  five-cycle exit and compact-layer core arguments; their
  [controls](docs/RUNNING.md#codimension-three-independent-controls) provide
  cross-checks.
- [Research body](PROOF.md): computational reductions, coverage, auxiliary
  lemmas, and structural results.
- [Running guide](docs/RUNNING.md): paper compilation, verification programs,
  and commands for larger computations.

## Run

Python 3.10+ and a C++17 compiler are used for the research programs.
`run.py` is the entry point; paper compilation and enumeration are separate.

```sh
python3 run.py upper
python3 run.py script scripts/problem4/check_paper_rank_reductions.py
python3 run.py script scripts/problem4/check_type6_single_exit_lemma.py
python3 run.py open-point
```

The [running guide](docs/RUNNING.md) explains the expected cost and output of
these commands. Temporary build artifacts are stored under `build/`. The code
is distributed under the MIT license.
