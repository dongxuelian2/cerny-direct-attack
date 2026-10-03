# A six-state rank-three boundary for signed components

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

Date: 2026-09-30. The finite counterexample below is
**COMPUTATIONALLY VERIFIED** by an independent full-word enumerator.
It **REFUTES** the direct three-color analogue of the binary
signed-component stagnation lemma. It does not refute the sharp
linear-algebra first-drop bound in PERMUTATION_RAINBOW_FIRST_DROP.md,
the universal `e(S)<=2n` target, or Cerny's square.

On `Q={0,1,2,3,4,5}`, use permutations and a rank-three letter

    a = [5,3,1,2,0,4]
    c = [2,0,3,5,4,1]
    b = [0,2,4,0,2,4].

The actual first image is `B=Qb={0,2,4}`. Color a state by its image
under `b`, giving three colors `0,2,4`. The two depth-one triples are

    Ba={0,1,5},   Bc={2,3,4}.

All three displayed triples are rainbow. As hyperedges they form one
connected component on **every** state, so the component counts for
the graphs generated through depths zero and one are `4,1`. Exact
enumeration of all four length-two permutation words gives only

    {0,1,2}, {3,4,5},

both rainbow. The graph therefore remains connected and collision-free
through depth two. But `B a a c={1,4,5}`, whose colors are `{2,2,4}`.
This first collision occurs at depth three, with component counts

    [4,1,1,1].

The state graph is strongly connected. Ordinary full-subset BFS gives
`rt=9` and a shortest word `b a a c b c c c b`. This exceeds `n+1`
but remains far below `(n-1)^2=25`. The reset threshold is included
only as a finite contextual fact; the refutation needs just the
rainbow hyperedge sequence above. A second independent seven-state
witness and its literal check are also retained.

`rank_three_color_cover.py` exhausts one first-permutation
representative per cycle type, every second permutation, and every
labeled rank-three row. The complete designated covers have:

| n | tested triples | finite first collisions | stagnant before later collision |
|---:|---:|---:|---:|
| 4 | 17280 | 16212 | 0 |
| 5 | 1260000 | 1239264 | 0 |

Conjugation covers every ordered two-permutation/one-rank-three input
up to state relabeling for these `n`; the counts are overlapping cover
designations, not isomorphism classes. The six-state witness is thus
state-minimal **within that precise alphabet shape**. No minimum for
larger alphabets is asserted. The n4/n5 negative counts are exact
finite computation, whereas the counterexample is also directly
checkable from the displayed words. The separate random probes at
n7/n10 are samples and prove no absence statement.

The failure mode is structural: rainbow triples sharing just one
vertex can be transported with different permutations of their three
colors. Connectivity alone does not force a uniform color action on
the whole component. The incidence-vector span in
PERMUTATION_RAINBOW_FIRST_DROP.md tracks information retained after
components have stopped merging.
