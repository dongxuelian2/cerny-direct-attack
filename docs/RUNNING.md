# Running research programs

## Read or compile the paper without rerunning research

The manuscript in `papers/problem4/main.tex` consolidates the exact
codimension-four and codimension-five results. Its mathematical supplement
is [PROOF.md](../PROOF.md#problem4-paper-synthesis), including completed
finite-domain coverage and the paper exclusion of the sole relaxation survivor.
Compiling the `article`-style manuscript (matching the previously
submitted arXiv paper) uses LaTeXmk and BibTeX. From the repository root:

```sh
mkdir -p build/paper
cp papers/problem4/main.tex papers/problem4/references.bib build/paper/
(cd build/paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex)
```

The result is `build/paper/main.pdf`. LaTeXmk invokes BibTeX and the
required reruns automatically; figure generation uses TikZ and needs no
external image files. The proof computations remain separate from typesetting. The remaining commands in this document are optional research
computations for replication or further investigation. Several are expensive;
they are not prerequisites to editing or reviewing the paper.

## Research runtime

Run commands from the repository root. Python 3.10+ and a C++17 compiler are needed
for the documented tasks. `CXX=clang++` selects another compiler. The launcher uses
`-O3 -pthread` without `-DNDEBUG`, so the mathematical assertions remain active.

## Main tasks

| Command | Calculation | Inputs |
|---|---|---|
| `python3 run.py reset --cerny 12` | Exact shortest reset word by native subset BFS | Constructs Černý transitions from `n` |
| `python3 run.py eleven --threads 8` | Complete proof calculation for `(13,9,1)` | Rebuilds the lower witness, graph classifications, P6 reduction and both all-entrance flag domains |
| `python3 run.py open-point` | Exact lower witness at `(13,9,1)` | Rebuilds the two-block construction |
| `python3 run.py c7 --threads 8` | Complete C7 action/distance exclusion | Generates both action domains in the current run |
| `python3 run.py c7 --threads 8 --independent` | Same, plus small Python cross-check | Uses the freshly generated domain |
| `python3 run.py tau4 --threads 8` | Complete nine-core classification and exclusion of a cover-four P6 | Rebuilds graphs, compares independent letter/arrow enumerations, exhausts distances and connectivity |
| `python3 run.py families` | Reconstructs and checks the lower-construction scopes | Generates its own intermediate data |
| `python3 run.py upper` | Rebuilds all codimension-three upper-proof components | Python prototypes plus independent C++17 enumerators |

`families` and `upper` perform broader calculations and can take considerably
longer than the small examples. They are explicit research tasks, not automatic
checks on every edit. No stored inventories or remote assets are required for
these tasks.

`tau4` proves the necessary condition `tau(P6)=3` under codimension-four
compression length at least twelve. It does not settle `(13,9,1)`.
`tau4 --pair-cap 7` (also 8 or 9) rebuilds the same complete graph and action
classification and checks the corresponding later layer. See the precise
[compression hypotheses](../PROOF.md#problem4-four-cover-late-layers).
For the distance calculation alone, run `problem4_core_distances.cpp` through
`run.py script` with `--pair-cap 7 --pair-order reverse`; `forward` is the default.
The optional `scripts/problem4/upper_bound/problem4_core_distances_check.py` needs
`z3-solver` and checks the same finite distance/strong-connectivity relaxation
using a different algorithm; the main `tau4` command has no solver dependency.

`run.py` copies research sources to `build/work/<task>/` and runs them there.
Intermediate JSON needed by existing producer/checker pairs is created in that
copy, never committed. Binaries are under `build/bin/`. Delete `build/` to start
with a clean local computation.

## Small controls for the uniform paper proofs

These use only the Python standard library and explicit small domains.
They check the constructions and finite boundary cases; the proofs for
arbitrary parameters are in the linked PROOF.md sections.

~~~sh
python3 run.py script scripts/problem4/check_quadratic_exit_sparsification.py
python3 run.py script scripts/problem4/check_chain_rigidity.py
python3 run.py script scripts/problem4/check_full_cycle_extrema.py
python3 run.py script scripts/problem4/check_uniform_static_barrier.py
python3 run.py script scripts/problem4/check_protected_cover_saturation.py
python3 run.py script scripts/problem4/check_component_ranks.py
~~~

The quadratic control checks exact exit distances (including infinity), the
selected original alphabet, and the actual shortest witness words from the
observable basis. It includes protected and nonmaximum families, a 125-member
family of quadratic rank 61, and a synchronization-loss negative control.
The chain control checks all explicit compression words in its stated small
domain and compares avoid-or-compress distances after protected subdivision.
The full-cycle control checks the original ternary construction, the new
all-parameter binary construction, actual reaching/reset words, and explicit
residue-class pair routing in the noncoprime cases. It checks all S,A in the
complete three/four-state binary cycle domain and the antipodal-kernel bound.
The static-barrier control compares literal short-word safety with the graph
family at nine parameter choices, computes exact rational ranks, applies actual
reaching words, and checks the single-protected-column obstruction.
The protected-cover control checks all ordered binary DFAs on two/three states
and the restricted four-state cycle-plus-map family. It includes synchronizing
automata that are not strongly connected and effective codimensions 0, 1, 2.
It also checks the matching-saturated residual-graph refinement.
The component-rank control uses exact rational elimination on every labelled
graph through order five. For all 1252 nonisomorphic graphs through order seven,
install/build the official [nauty geng](https://pallini.di.uniroma1.it/) under
ignored `build/tools/`, then pass its absolute executable path:

~~~sh
python3 run.py script scripts/problem4/check_component_ranks.py --geng "$PWD/build/tools/nauty2_9_3/geng"
~~~

This checks the [component formulas and matching bounds](../PROOF.md#problem4-component-ranks-and-matching);
it is a complete small-graph control, not an exhaustive automaton search.
No inventory or output file is needed. These commands each complete in seconds;
run them sequentially because `run.py script` refreshes the shared manual copy.
See the [quadratic theorem](../PROOF.md#problem4-quadratic-exit-sparsification),
[chain rigidity](../PROOF.md#problem4-signed-chain-rigidity),
[full-cycle formula](../PROOF.md#problem4-full-cycle-exact),
[rank obstruction](../PROOF.md#problem4-real-safe-family-rank-barrier), and
[protected-cover saturation](../PROOF.md#problem4-protected-cover-saturation).

<a id="codimension-three-independent-controls"></a>
## Codimension-three independent controls (PR #18)

The codimension-three paper proof uses trajectory rank and actual image
families. These four independent controls preserve shorter alternative
five-cycle and tight-layer arguments and the two type-7 four-cycle tests.
All use the Python standard library and leave the main proof unchanged.

```sh
python3 run.py script scripts/problem4/check_defect_three_tight_cores.py
python3 run.py script scripts/problem4/check_type6_single_exit_lemma.py
python3 run.py script scripts/problem4/check_type7_four_cycle_exit.py
python3 run.py script scripts/problem4/check_type7_two_cycle_exit.py
```

The five-cycle script checks all permutations and all rank-`n-1`
transformations with sole kernel pair 01 for n=6,7,8, without early-pair
filters. The type-7 controls separately test the four-cycle permutation
action and the inverse-pair-compatible two-cycle/V action. The tight-core
control checks the finite graph classification, not the arbitrary-n
exclusion. Mathematical arguments and precise scopes are in the
[independent defect-three lemmas](../PROOF.md#problem4-defect-three-independent-lemmas).

## Small controls for paper dependency replacements

```sh
python3 run.py script scripts/problem4/check_paper_rank_reductions.py
python3 run.py script scripts/problem4/check_paper_family_reductions.cpp
python3 run.py script scripts/problem4/check_single_edge_obstruction.cpp
python3 run.py script scripts/problem4/check_two_exception_closure.cpp
python3 run.py script scripts/problem4/check_three_exception_closure.cpp
python3 run.py script scripts/problem4/check_three_exception_closure.cpp --coverage
python3 run.py script scripts/problem4/check_triangle_exchange.cpp
python3 run.py script scripts/problem4/check_triangle_one_deletion.cpp
python3 run.py script scripts/problem4/check_doubleton_remainder.cpp
python3 run.py script scripts/problem4/check_doubleton_flower.cpp
python3 run.py script scripts/problem4/check_doubleton_anchors.cpp
python3 run.py script scripts/problem4/commonhole_exit.cpp
python3 run.py script scripts/problem4/commonhole_exit.cpp --coverage
```

This standard-library control reconstructs the displayed images from their
holes, checks ranks and row relations by rational elimination, and applies
the literal closed-T exit words. It includes the reachable, strongly connected
synchronizing five-state example with pure compression length ten. The
[uniform proofs](../PROOF.md#problem4-paper-dependency-reductions) provide
the all-parameter conclusions. The C++17 control exhausts all 870,199 maps
on six and seven states for the local balanced-bipartite and tight-clique
conditions; it does not claim that these local maps realize short-pair layers.
The single-edge control checks the equivalent graph conditions on every
simple labelled graph through six vertices. Thirty explicit synchronizing
strongly connected automata realize the prescribed P1 graphs; ordinary subset
BFS checks 1,199 independent subsets. A separate three-letter example checks
six subsets without strong connectivity. The exhaustive binary domain through
four states has no qualifying P_h and is explicitly reported as an empty
applicability domain, rather than as successful instances of the bound.
See the [general theorem and exchange structure](../PROOF.md#problem4-single-edge-obstruction).
The two-exception control checks the single-edge image classification on all
simple graphs through order six and exhausts 5,998,081 local transformations
on twelve small representative graphs, including deleted isolated points.
Its private-pair control enumerates all center-edge graphs for three private
pairs and zero/one isolate. Among 1,183,488 four-row-safe local maps, every map
leaving the proposed support causes at least two row exits; the third exception
is deliberately allowed to be unsafe. These are local lemma controls rather
than global short-pair graph realizations. See the
[two-exception](../PROOF.md#problem4-two-exception-closure) and
[disjoint-hole](../PROOF.md#problem4-disjoint-exchange-holes) proofs.
The three-exception control checks the single-edge classification on all
33,867 labelled graphs through six vertices, then checks complete forced-image
local domains on two hard-case cores with zero/one isolate. It retains the
orientations that would give two/three-step mergers, so those proof steps
have nonempty negative controls. Four-container transition tables independently
check the four-step budget. These maps are not prescribed-P_h realizations.
For arbitrary exception counts, it checks the Johnson triangle structure on
all small unique-maximum graphs, eight clique-family templates, and 1,068
admissible local maps forcing the kernel in a three-row far clique.
The common-hole negative control has one row exit and a two-edge maximum-set
image; it prevents reusing the five-row container classification with only
four safe rows. The [four-row obstacle](../PROOF.md#problem4-common-hole-four-row-obstacle)
leads to the later two-layer resolution below.
The common-hole exit control exhausts the local domains with one row exit
on zero/one isolate (528 and 1,446 maps). It checks the entry normal forms,
the protected-pair implication and the private-pair successor classification.
A separate construction enumerates the local domains for k=2,...,5, with
zero/one isolate, and checks the general versions of these implications.
Ordinary pair BFS on actual Cerny automata checks the shortest-path closure
lemma, including a nonclosed two-pair counterexample to dropping its hypothesis.
See the [general common-hole double-exit theorem](../PROOF.md#problem4-common-hole-double-exit).
The additional five-row control checks that an image of A in the extra row B
has at least k preimages from D, and that keeping A in D allows at most one
D exit. The two-layer proof uses the actual first image layer to exclude A
mapping to B. Thus it covers the full named P9 domain, including a fifth
P8-safe row, rather than assuming the two layers have the same safe family.
The separate `--coverage` mode rebuilds only the common-hole core's 14 named
domains and identifies the one covered domain (canonical core 2069024,
local index 6); the other 13 remain outside this theorem.
The three-exception program's `--coverage` mode rebuilds all 4,658 existing cover-four cores,
then uses the production domain generator and static filters for the selected
unique-maximum branches: 521 cores, 7,960 raw domains, and 7,519 previously
dynamic domains. It runs no dynamic solver. Of the latter, 7,499 belong to
the five-to-ten-point branch and 20 to the separate eleven-point branch.
See the [three-exception theorem](../PROOF.md#problem4-three-exception-closure)
and the [general Johnson-cluster theorem](../PROOF.md#problem4-exception-cluster-kernel).
For the [proof-structure compression](../PROOF.md#problem4-proof-structure-compression),
the three-exception control also checks the ECC/bootstrap/ECK case split on every
applicable labelled graph through six vertices, the four hard representatives,
and eight explicit graph templates. Each of the six routes has nonempty controls;
the ECK route always has exactly one far Johnson edge and at least three exterior
container states. The triangular-exchange control reconstructs all independent
rows on 228 literal graphs: disjoint-hole cores with three/four centers and every
center-edge graph, and common-hole cores with three through six centers, each
with zero through two isolates. It checks 228 complete four-row paths, 12 complete
edge-plus-isolate families, all 468 exterior rows, and all 36 two-row prefixes of
the three-row families. Twelve A-only families explicitly fail the exterior
boundary hypothesis. Three doubleton families with one through three isolates
check the full-support obstruction and the three-row component used by JCP.
The one-deletion control supplies the actual-prefix JCP
checks and its depth-zero negative control. These checks add no core coverage
and do not require rerunning the historical domain enumerations.

The [common-intersection capacity](../PROOF.md#problem4-common-intersection-capacity)
control in check_doubleton_remainder.cpp exhausts all 74 labelled graphs through
four vertices and all 16,608 graph/map inputs. It checks 85,572 safe row families
with nonempty intersection, including 8,556 with full support, and retains
unsafe-row and omitted-defect negative controls. Before the first/last-layer
budget, all 1,440 admissible map/R2 combinations containing B preserve I;
72 violate the old budget. The old 1,368 budget-filtered controls and the
one-isolate empty-I boundary remain present.
The [prefix exit-capacity](../PROOF.md#problem4-prefix-exit-capacity) control in
commonhole_exit.cpp uses ordinary subset BFS on actual Cerny automata of orders
two through five. It checks 229,320 (S,d,E,word) inputs, enumerating every same-size
family E containing the actual R_d and words through length three. Of these,
183,456 use words of length two/three, 70,920 have positive prefix depth, and
5,814 attain the bound. Separate negative controls check the slow-row threshold
and charging aa as two original letters. The existing common-hole, doubleton,
and triangular-exchange local controls remain necessary application checks;
these runs add no core or named-domain coverage.

The [connectivity propagation](../PROOF.md#problem4-johnson-component-prefix)
checks extend check_triangle_one_deletion.cpp on all 66,281 binary automata of
orders two through four. All 124,494 connected positive-depth uncompressed
prefixes have connected next prefixes; 84,126 of these grow strictly. The same
automata supply 3,916,812 (automaton,S,C,word) inputs for the
[single-target rule](../PROOF.md#problem4-prefix-single-target), with C ranging
over every same-size row family containing R_(2|word|), for words of length one
or two. The 554,648 one-letter and 1,306,024 two-letter singleton intersections
all fix their actual anchors. Nonsynchronizing inputs are included because
these two prefix statements do not require synchronization. The existing
depth-zero propagation negative and a C3 example with only R1 in C check the
two depth requirements.
check_doubleton_remainder.cpp also checks the capacity-equality complement on
all 3,412 maps of orders two through five and 97,504 nonempty proper supports:
15,674 saturated cases, including 11,698 with nonzero defect. Wrong global
defect and strict-capacity negatives check the global defect and equality hypotheses.
check_doubleton_anchors.cpp retains its 972 prefix candidates and identifies
87 candidates that cannot supply B in R2 from R1 when X_a is absent in R2
and B absent in R1, even using the entire compatible letter pool. The existing
three cross-letter gf controls still verify the two-original-letter kernel conflict.
The [two-target fold](../PROOF.md#problem4-row-fibre-separation) control extends
the same complete binary-automaton domain: 18,432 actual R2 folds, with 5,520
P2-independent protected unions (1,248 on prefixes of more than two rows).
All 2,376 comparisons with a letter fixing A also fix B. Actual four-state
counterexamples retain the depth-two and two-original-letter requirements.
The doubleton control separately compares the two row images under gf:
15,192 comparisons identify the protected rows, and the other 97,392 preserve
the two-row block itself, including all 95,664 comparisons without any witness
kernel conflict. The triangular ordinary-letter controls now also check the
forced row identification before the second kernel guard, both with and
without the rank restriction; the two independent guard negatives remain.

The [triangular mixed-return proof](../PROOF.md#problem4-triangle-exchange-one-deletion)
now uses the actual two-row R1 and an entrance letter. Its control enumerates
all 139,968 six-core inputs for one through three isolates and every permutation
of those isolates, retaining 2,196 ordinary-map/direction choices and constructing
all 46 entrance maps. Of 32,292 compatible joint prefix comparisons, 15,444 move
A0; all compress the protected maximum independent set M by fg, gf, or fgg,
in 14,040 / 468 / 936 cases. The ordinary maps have no defect or pair-layer
budget filter. The previous one-letter two-kernel-guard controls remain valid
but are no longer prerequisites for the upper proof. An actual prefix of sizes
2/3/4 protects all G nonedges for two letters and is first rejected by fgg;
another defect-two moving map preserves the full nonedge pair orbit with the
entrance but has no compatible two-row R1. These check the three-letter cost
and actual-first-layer hypotheses separately.

The generalized row-fibre argument requires only an independent subset of the
row union larger than either row. The complete binary-automaton fold control
also checks this rank condition: it finds the same 5,520 applicable cases as
the full-union condition through four states, with no extra proper-subset
folds in that small actual-automaton domain.

The [common-hole single-A proof](../PROOF.md#problem4-common-hole-one-deletion-A)
now requires an actual third-layer supplier C_j t=B_x. In commonhole_exit.cpp,
the existing zero/one-isolate, all-hole, four/five-row, and two-initial-row map
domains retain the original-letter defect-two condition, but no first/last-layer
or P2 saturation filter is used in the new supplier check. Ordinary subset BFS
on 1,401,372 small alphabets compresses M in two letters in 1,115,822 cases,
three in 282,226 cases, and four in 3,324 cases. The paper proof works for
arbitrary isolates with explicit bounds of five and three original letters;
the observed finite four-letter maximum is not claimed as that general bound.
The old layer-budget and private-pair controls remain as separate historical
checks; neither is a dependency of this branch's new closing argument.

The [doubleton flower support proof](../PROOF.md#problem4-doubleton-eighth-entry)
replaces its five-pair shortest-path closing argument with a proper two-point
support. check_doubleton_flower.cpp constructs all 46 entrances for one through
three isolates and every isolate permutation. It rejects 92 wrong complement
images by ff and checks 438,750 ordinary comparisons without rank or kernel
filters. Of these, 70,200 preserve {b,r}; all other 368,550 merge an original
G nonedge under the three-original-letter word fgf. The old P1/P2 and five-pair
controls remain independent historical checks.

The common-hole two-letter barrier remains a scope control. Two explicit
seven-state maps produce an actual 2/3/4-row prefix while keeping a 17-pair
family containing every G nonedge forward closed under all words. The private
pairs pj and pr never merge, so this nonsynchronizing model is not a prescribed-P7
automaton. Its four immediate kernel pairs also violate the old layer budget.
The new closing argument uses the finite geodesics of actual G edges.

The [private-leaf anchor corollary](../PROOF.md#problem4-private-leaf-anchor-closure)
applies the existing pair-geodesic rule to all three private edges. In CHT3,
the actual initial row Ci forces every private leaf other than wi to map into
the leaves/isolates; pi is already immediate and needs no leaf condition.
All private distances are at most three, contradicting the distance-h private
edge in a maximum-set exit. This removes the Af-to-Bi supplier, four-edge P2
saturation, the prohibition on kernels incident to ur, and the two-pair distance
classification from the main proof. The original k=3, h>=7 scope is retained.

commonhole_exit.cpp checks all 490 local maps over zero/one isolates with the
derived M-image forms, one-letter G-nonedge protection, F-row safety and actual
prefix identities. All 162 G-valued successors of the other private edges stay
private. No rank, layer-budget or pair-distance filter is used. The control
retains 40 old triangle-swap cases and 260 maps with kernels incident to ur;
the old four-edge/two-pair controls remain separate historical domains.

The [pair-geodesic rule](../PROOF.md#problem4-pair-geodesic-closure) itself now
only requires closure for successors inside P_(h-1). Distance-h boundary
escapes cannot be a shortest-path descent. This absorbs the separate two-pair
argument for CHT2; the former G-closed condition remains a sufficient special
case. The same 2,168 actual Cerny horizon/family cases for orders two through
five admit 68 strict-interior-closed families, including all 55 former positive
cases and 13 additional cases. Every observed distance meets the family-size
bound. C3 retains both a genuine missing-fast-pair negative and a boundary-only
escape positive. The D-family center-entry case retains its necessary global
budget but directly invokes the existing joint-word first/last-layer count.

The shared [protected-reset support rule](../PROOF.md#problem4-reset-support-propagation)
records the literal two-letter gf and three-letter fgf costs used by both
doubleton branches. The [U-entry proof](../PROOF.md#problem4-doubleton-double-entry)
first completes the original four safe rows to the four/five-row family using
the unique maximum set. In the five-row family, four petals force defect at
least three. In the four-row family, the actual reset excludes B from R2 and closes {b,r}; gg
rejects the last possible exit into an isolate hole. The whole-core upper
proof therefore no longer uses the joint first/last-layer budget. Its numerical
bound remains an auxiliary statement with the original hypotheses.

check_doubleton_anchors.cpp also revisits the same 35,294,830 literal maps
without pre-excluding U entries. One-letter G-nonedge protection, source-row
safety and defect at most two leave 7,470 maps, including 324 U entries (none
in the five-row family). The 972 strict
prefix candidates yield 1,512 U-entry witnesses; 1,368 fail ff. Of the remaining
41,836 cross-letter comparisons, 12,328 preserve {b,r}; fgf, gf and gg merge an
original G nonedge in 12,956, 16,432 and 120 cases. No layer-budget filter is
used. Three explicit row-safe maps also generate an actual 2/3/4-row prefix
but merge the protected zb under gg, checking the final hole-exit case.

The strengthened [doubleton anchor proof](../PROOF.md#problem4-doubleton-actual-anchors)
also runs the same complete 35,294,830-map domain with only Jf contained in M,
allowing simultaneous entries into a and b. Its 9,708 local maps include 1,120
double entries, of which 480 have defect two. The same 972 nested prefix
candidates supply 1,200 double-entry witness selections, including 180 of
defect two. Every applicable double entry supplies both actual anchors and
the two-target fold. Of 316,488 gf comparisons, 39,688 identify the protected
rows; the other 276,800 preserve their two-row block. No single-entry, defect,
or first/last-layer budget filter is applied in this relaxed control. An
explicit seven-state defect-two double entry and a second letter pass the
one-step prefix conditions, but gf merges the G nonedge zb. This retains the
two-original-letter protection requirement and checks that the relaxed domain
has genuine new cases. The historical single-entry and matched-kernel controls
remain separate; the matched-kernel fixed-point argument is no longer a
dependency of the whole-core upper proof. These are finite local application
controls, not realizations of prescribed short-pair layers or added coverage.

The historical `upper` task remains available for independent computational
checks; its action/distance enumerations are no longer prerequisites for the
codimension-three upper proof.

## Individual research sources

The arbitrary-core-cycle rigidity proof has a C++17 word-level control and
a complete restricted construction scanner. The initial set and chain letter
are fixed as in [the theorem](../PROOF.md#problem4-arbitrary-core-cycle-rigidity).

```sh
python3 run.py script scripts/problem4/two_block_cycle_orders.cpp --control
python3 run.py script scripts/problem4/two_block_cycle_orders.cpp --control-all-u
python3 run.py script scripts/problem4/two_block_cycle_orders.cpp 7 4 15 16 --all-p-permutations --verify-words
python3 run.py script scripts/problem4/two_block_cycle_orders.cpp 8 5 18 16 --verify-words
```

Arguments are P size, chain size t, compression threshold, and thread count.
By default a swaps the last two P states and has any single cycle on U.
`--all-p-permutations` covers every P permutation. `--verify-words` directly
applies the paper's compressing word to every table. `--all-u-permutations`
instead covers all U permutations, including multiple cycles, and cannot be
combined with `--verify-words`: the uniform theorem does not cover that domain.
High compression candidates still need separate reachability and avoidance
audits. Counts and results are printed to the terminal; no inventory is saved.

The larger complete multiple-cycle domains used in the construction investigation:

```sh
python3 run.py script scripts/problem4/two_block_cycle_orders.cpp 7 4 15 16 --all-u-permutations --all-p-permutations
python3 run.py script scripts/problem4/two_block_cycle_orders.cpp 8 5 18 16 --all-u-permutations
python3 run.py script scripts/problem4/two_block_cycle_orders.cpp 9 6 21 20 --all-u-permutations
```

These contain 1,828,915,200, 39,916,800, and 6,227,020,800 named tables,
respectively. The last command took about four minutes on this machine.
Only the first also varies the P permutation; all keep the same b and initial S.

General rank-descent controls and the enlarged restricted odd-core family:

The rank control also checks maximum-set/reset-row separation and the
common-image core escape bound, with singleton and nonsynchronizing controls.
It checks all maps on four through six states for the four-cycle preimage
closure used in the sparse-pair entrance theorem, including a six-edge
negative control. The theorem for arbitrary state counts is proved on paper.

The global codimension-four compression bound thirteen uses a separate complete
P9 core domain. This reconstructs all 45 cores, checks two full action generators,
and tests the shared subset/pair distances; the eight-state positive control is
included. The codimension-five bound twenty follows by the cover-transfer lemma.

```sh
python3 run.py script scripts/problem4/compression_fourteen_cores.cpp 4 --actions --control
python3 run.py script scripts/problem4/check_short_pair_core_bounds.py
```

Without `--actions`, the first program only classifies graph cores; `--control`
additionally compares the complete generators. `--emit` prints the graph edges.
The name refers to the excluded compression length fourteen. A nonzero joint
distance vector is a necessary relaxation, not a constructed automaton.

For compression length thirteen, `--layer 8` adds the eight-edge graphs and
checks all 74 cover-four cores. The remaining cover-three branch has support at
most nine by the paper support bound. Its nine-point equality cases reduce to
three four-row domains; `star_nine_domain.cpp` rebuilds every single-letter map
with zero through six crossing isolates and compares an independent generator
which chooses target rows first. Neither calculation excludes the remaining
cover-three cores on at most eight vertices.

```sh
python3 run.py script scripts/problem4/compression_fourteen_cores.cpp 4 --layer 8 --actions --control
python3 run.py script scripts/problem4/star_nine_domain.cpp 4 --control
python3 run.py script scripts/problem4/check_low_cover_support.cpp
```

The last command independently checks the support inequality, its equality
graphs, and the four-row preservation lemma on all maps in the stated small
domains. `check_short_pair_core_bounds.py` also checks the persistent-isolate
bound on literal automata and subset families. These controls support paper
proofs; they are not automaton exclusions at arbitrary parameters.

The final thirteen-step exclusion reconstructs 73 low-cover cores and 1988
common safe domains. It gives the current codimension-four bound twelve and,
by cover transfer, the codimension-five bound nineteen. The first command
compares two complete domain generators. The action command also compares two
complete single-letter generators and checks shared subset/pair distances.

```sh
python3 run.py script scripts/problem4/low_cover_core_domains.cpp --domains --control
python3 run.py script scripts/problem4/low_cover_actions.cpp --positive
python3 run.py script scripts/problem4/low_cover_actions.cpp 0 1988 4 --control --actions
```

The three numeric action arguments are the starting domain, number of domains,
and threads. Shorter intervals print `PARTIAL`; a full exclusion needs their
disjoint union to cover all 1988 domains. Without `--actions`, only the letter
domains are constructed. `--positive` reconstructs a real eight-state Černý
example and retains its actual letter signatures and compatible distances.
Common isolates are represented only for single-step constraints, with a
possibly omitted auxiliary output; they are never iterated as anonymous states.
When there are no common isolates, the program does not apply a proper-core
escape test to the whole state set. See the [full proof](../PROOF.md#problem4-four-global-twelve).

For twelve-step candidates, layer seven has 91 cover-four cores and 117
cover-three cores. The first command completely excludes the former for
`n>=9`. The second reconstructs 10142 later maximum-set domains in the latter
branch, comparing two complete family generators. Its closure predicate is
shared by those generators. The action command checks a safe single-step
relaxation of the actual two-step requirements; a surviving vector is not an
automaton. The full domain has now been excluded using quotient connectivity
and same-letter squares where needed; see the [exact codimension-four theorem](../PROOF.md#problem4-four-exact-eleven).

```sh
python3 run.py script scripts/problem4/compression_fourteen_cores.cpp 4 --layer 7 --actions --control
python3 run.py script scripts/problem4/low_cover_core_domains.cpp --layer 7 --domains --control
python3 run.py script scripts/problem4/low_cover_actions.cpp 0 10142 4 --layer 7 --control --actions
```

The low-cover programs default to layer eight. `--stop-on-survivor` can be
added to the action command to stop at the first compatible vector and print
`PARTIAL`; it never constitutes a complete negative result. The layer-seven
domains assume `n>=11` and a nonempty common-isolate set, as justified in
[the reduction](../PROOF.md#problem4-twelve-finite-domains).

`--quotient` also records arrows from common isolates into named states and
requires the resulting quotient graph to be strongly connected. `--squares`
adds the same-letter two-step condition by matching auxiliary output identities
to inputs; it does not directly compose independently renamed representatives.
`--square-control` additionally compares literal identity alignments on all maps
with at most three crossing isolates, reporting their count. These two-step
options require layer seven. `--two-step` enumerates all candidate named
intermediate families, retaining the necessary constraints for different
letters; it can multiply the work and still omits some auxiliary-hole
compatibility conditions.

```sh
python3 run.py script scripts/problem4/low_cover_actions.cpp --positive-quotient
python3 run.py script scripts/problem4/low_cover_actions.cpp 0 10142 4 --layer 7 --control --actions --quotient --squares
```

The positive control uses the real ten-state Černý automaton with two common
isolates and keeps both actual letters and six compatible distance vectors.
The accompanying square countercontrol is rejected. See
[the identity and quotient proofs](../PROOF.md#problem4-twelve-actual-two-step).

For the codimension-five eighteen-step candidate classification,
`rank_core_graph6.cpp` consumes a graph6 stream. Use a separately built
[nauty/Traces geng](https://users.cecs.anu.edu.au/~bdm/nauty/) (the checked version
was 2.9.3); keep downloaded sources and binaries under ignored `build/`.
Set `NAUTY_GENG` to its executable path. No graph inventory is required.

```sh
set -o pipefail
for n in 7 8 9; do "$NAUTY_GENG" -q -d1 -D5 "$n" || exit; done |
  python3 run.py script scripts/problem4/rank_core_graph6.cpp 5 7 11
for n in 6 7; do "$NAUTY_GENG" -q -d1 -D4 "$n" || exit; done |
  python3 run.py script scripts/problem4/rank_core_graph6.cpp 4 6 0 --control-m4
```

The first command classifies 257 cores, without assuming an upper edge count.
The second compares the smaller full stream with the existing nine-core
classification. Append `--actions 0 257 4` after `5 7 11` to check every core's
joint distances. Append `--letter-control` after those interval arguments for
the independent complete input-by-input letter/arrow comparison; append
`--power-control` instead for literal output-identity controls on every map
with at most two crossing isolates. Both control modes skip distances, and the
terminal summary distinguishes the checked components. These three runs, the
complete graph stream, and the paper reduction establish the
[codimension-five bound seventeen](../PROOF.md#problem4-five-global-seventeen).
Smaller `START COUNT THREADS` intervals are explicitly partial. The power
filter tracks missing named states only while the whole common-isolate set is
retained; it does not compose independently renamed individual-subset images.

For the seventeen-step candidate domain, generate orders 6 through 10 and use
`5 6 11` instead. It contains 1994 static cores; its complete dynamic exclusion proves the
[codimension-five bound sixteen](../PROOF.md#problem4-five-global-sixteen). The ten-vertex cases additionally check the paper's unique
matching and shattering bounds. Run the small exhaustive matching control with:

```sh
python3 run.py script scripts/problem4/rank_core_graph6.cpp --matching-control
python3 run.py script scripts/problem4/matching_guard_control.cpp
python3 run.py script scripts/problem4/transversal_guard_control.cpp
python3 run.py script scripts/problem4/proper_guard_tower_control.cpp
python3 run.py script scripts/problem4/saturated_exit_control.cpp
python3 run.py script scripts/problem4/maximum_set_exchange_probe.cpp --control
python3 run.py script scripts/problem4/short_pair_entry_control.cpp
python3 run.py script scripts/problem4/exit_rank_control.cpp
```

For `5 6 11 --actions START COUNT THREADS`, the program uses the weaker power
constraints appropriate to target seventeen and a proved crossing bound of
`N-6`. It reports whole-pool closure exclusions separately from distance counts.
It also applies the paper's descending safe-row-space bound to each row-distance
tail. The two additional controls above enumerate small transformations and
small binary automata respectively; neither establishes a global extremum.
For a ten-vertex interval, `--guard MASK PARITY` instead restricts every letter
to one common matching-transversal guard (or the whole cube). The five matching
pairs are returned in the deterministic order of the unique-matching routine.
`MASK` selects one or two of those coordinates, and `PARITY` is 0 or 1. All
thirty choices are required for a complete common-guard exclusion; one choice
is a partial domain. The filter is applied to actual maps before signatures
and arrows are merged.

The difficult fifteen-edge pair-distance controls can optionally use
[CaDiCaL](https://github.com/arminbiere/cadical) through IPASIR. Download a tagged
source release into `build/tools/` and build it there with `./configure -shared`
and `make -j8` (checked release: `rel-3.0.1`). Then set the shared-library path:

```sh
export CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so"
python3 run.py script scripts/problem4/check_pair_sat.cpp
CERNY_PAIR_SAT_MIN_EDGES=0 python3 run.py script scripts/problem4/low_cover_actions.cpp --positive-quotient
```

The main interval-propagation search still runs, and its count must equal the
SAT projection count. Without this variable, the original scalar control runs.
The optional `CERNY_PAIR_SAT_MIN_EDGES` defaults to 15; zero forces SAT for every
row profile, useful for controls. This is a Linux shared-library option using
`dlopen`; no downloaded solver source or binary belongs in Git. SAT blocks only
distance vectors, validates every model against the original predicates, and
requires a final unsatisfiable result to finish a profile.
For `5 6 11 --actions START COUNT THREADS --sat-distances`, SAT instead performs
all pair-distance searches, without the main interval or scalar search. Output
marks this mode explicitly. The same source also accepts `5 6 10` for the
**conditional** sixteen-step domain with vertex cover five at layer ten; it
does not include the layer-ten cover-four branch. Its safe power depth remains
five, although its pair-distance cap drops to ten. Neither a partial interval
nor this one cover branch establishes a global fifteen-step bound.
`--stop-on-survivor` stops at a necessary relaxation survivor, not a witnessed
automaton. Compile once before launching parallel runs of the same source to
avoid concurrent writes to its executable; an observed compilation failure is
not a mathematical result.

The single-exit construction family permits arbitrary within-block collisions,
but fixes the common cycle and almost all common-state actions. The optional
`--all-pair-permutations` expands the other letter from one core cycle to all
signed matching-pair permutations. It is a restricted
lower-bound search, not an automaton upper bound:

```sh
python3 run.py script scripts/problem4/check_proper_transversal_constructions.py
python3 run.py script scripts/problem4/proper_transversal_constructions.cpp 4 7 15 4
python3 run.py script scripts/problem4/proper_transversal_constructions.cpp 4 7 15 4 --all-pair-permutations
```

Arguments are matching-pair count, common-cycle length, target, and threads.
Printed compression maxima include all declared initial transversals; only
threshold survivors undergo the additional marked-subset reachability check.

For stochastic lower-bound exploration, `mutate_compression.cpp` computes the
exact maximum pure compression of each visited automaton by bounded vertex
cover, before attempting the more expensive reachability/avoidance audit.
Generate a seed from the existing construction in the research copy:

```sh
python3 - <<'PY'
import sys
from pathlib import Path
from run import workspace
work, _ = workspace('manual')
sys.path.insert(0, str(work / 'scripts/problem4'))
from two_block_family import construct
z = construct(7, 4, 1)
seeds = [z['rows']]
# For a three-letter run, replace the preceding line by:
# seeds = [z['rows'] + [extra] for extra in
#          [list(range(z['n'])), *z['rows']]]
Path('build/mutation_seed.txt').write_text(str(len(seeds)) + '\n' +
    '\n'.join(' '.join(str(q) for row in rows for q in row)
              for rows in seeds) + '\n')
PY
python3 run.py script scripts/problem4/mutate_compression.cpp --control
python3 run.py script scripts/problem4/mutate_compression.cpp \
  16 5 1 2 5000000 8 738 "$PWD/build/mutation_seed.txt" 15
```

Arguments are `n m r alphabet_size proposals_per_thread threads first_seed
seed_file target`. Worker `i` uses `first_seed+i`; use `p=n-2*m+1,t=m-1`
in the construction for the other runs listed in
[the lower-bound exploration](../PROOF.md#problem4-proper-transversal-lower-search).
The count includes repeated and rejected proposals. No failed stochastic run
proves an upper bound. With zero avoidance audits, `maximum_audited_ac=0`
means unexamined. An avoidance candidate still requires an independent full
witness check; the scorer considers at most forty reachable subsets.

The [linear codimension conjecture](../PROOF.md#problem4-linear-codimension-conjecture)
has a small independent checker for the three low-codimension exceptions and
the paper construction with unbounded adjacent compression jumps:

```sh
python3 run.py script scripts/problem4/check_linear_codimension_conjecture.py
```

To reconstruct the nine binary seeds used in its broader mutation search:

```sh
python3 run.py script scripts/problem4/check_linear_codimension_conjecture.py \
  --write-seeds 19 2 "$PWD/build/conjecture_seed_n19_k2.txt"
python3 run.py script scripts/problem4/mutate_compression.cpp --control
python3 run.py script scripts/problem4/mutate_compression.cpp \
  19 6 1 2 100000 8 20261020 "$PWD/build/conjecture_seed_n19_k2.txt" 18
```

The seed generator supports `n=19,20` and two or three letters. Three-letter
seeds append the identity or a copy of either original letter, giving 27 seeds.
Use the other run parameters in the proof's search table for those runs.
All transition outputs may mutate. The maximum compression of each valid
proposal is exact; the sequence of automata examined is stochastic and may
repeat. No negative result from these runs proves the conjecture.

The cover-four branch at layer ten has a separate complete **static** generator:

```sh
python3 run.py script scripts/problem4/low_cover_five_cores.cpp --control
python3 run.py script scripts/problem4/low_cover_five_cores.cpp 5 11 4
python3 run.py script scripts/problem4/low_cover_five_domains.cpp --control
python3 run.py script scripts/problem4/low_cover_five_domains.cpp 0 4143
```

The latter command also checks saturated reachable unions, exit-preimage
cliques and transversal partitions. These are necessary conditions, not a
complete dynamic exclusion. For the remaining double-common-neighbor branch:

```sh
python3 run.py script scripts/problem4/five_low_cover_positive.cpp
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/five_double_neighbor_actions.cpp 0 747 8 --control --distances
```

The shared library path is local and optional; without it the existing pair
interval solver and its scalar cross-check are used. The full interval
`0 747` covers this conditional branch only. Both letter generation orders
share kernel partitions and target sets. No square-safety filter is applied:
the early and late pair layers differ by one. See the exact scope in
[the double-neighbor exclusion](../PROOF.md#problem4-five-double-neighbor-exclusion).
Append `--entry-filter` to prune incoming-state sets with the proved
[joint entrance budget](../PROOF.md#problem4-joint-short-word-entry). Omitting
it reproduces the complete exclusion without this additional condition.

The one-point-petal theorem has a literal small-automaton control and an
all-parameter binary equality construction:

```sh
python3 run.py script scripts/problem4/check_sunflower_exit.cpp
python3 run.py script scripts/problem4/check_full_common_displacement.cpp
python3 run.py script scripts/problem4/five_low_support_actions.cpp 10 8 --remaining-sunflowers
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/five_low_support_actions.cpp 6 8 --control --distances
```

The first command also checks the exact first-cardinality-face construction
under simultaneous bounds on original-letter kernel fibers and rank defects.
It verifies the actual retraction, reaching and reset words, as well as every
short safe image and an attaining avoidance word. Its finite parameter domain
is printed explicitly; the all-parameter claim uses the
[paper proof](../PROOF.md#problem4-bounded-kernel-first-face).

The support driver's arguments are maximum named support and worker count.
Without `--distances` it only counts static domains and checks the paper's
fourteen-edge bound for sunflower domains. It rebuilds the 1000088 domains
remaining before the new paper filter, reports all 121 sunflower exclusions,
and reports 999967 domains outside that paper filter. All 1000088 domains have now been dynamically excluded in the disjoint early-core intervals 5–6, 7, and 8–10. `--remaining-sunflowers` selects only
the 42 sunflower domains with more than six named points. The final command
completely checks all 79 six-point domains with both letter-generation orders;
it does not run the larger domains. See the
[general theorem and precise scope](../PROOF.md#problem4-sunflower-kernel-exit).

For complete intervals of early nonisolated core size, while retaining all
later named supports through ten:

```sh
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/five_low_support_actions.cpp 10 8 --core-bound 6 --distances --control --parallel-domains
```

`--core-min N --core-bound M` selects the inclusive early-core interval;
the first positional argument independently bounds the later named support.
`--parallel-domains` partitions domains between workers, using one letter
generation worker per domain, and prints progress instead of each domain's
internal counters. It retains both full generation orders with `--control`.
The completed runs cover 4231, 180339, and 815518 domains respectively, all with zero joint vectors; together with the other cover branch they prove the [global fifteen bound](../PROOF.md#problem4-five-global-fifteen).
The early-layer filter includes the kernel-pair budget, the joint entrance
condition, and their combined first/last-layer budget with the kernel-pair
excess over rank defect. Executables already running when a refinement is
added retain their earlier filters; they are not counted as runs of the
stronger version. Scope and completed coverage are in
[the proof](../PROOF.md#problem4-short-pair-kernel-budget).

`check_full_common_displacement.cpp` checks the separate sharp family for
multiple unprotected points, under the full common-displacement hypothesis.
It applies every conjugate as an original word, verifies the constructive
reset, and expands all short safe images. Its parameter domain is printed;
it does not enumerate all automata or remove the hypothesis from the theorem.

It enumerates nonempty neighborhood multisets on a fixed four-vertex cover,
then canonicalizes accepted graphs. The paper excludes twelve-vertex support
before this run; the later paper argument also excludes all 81 eleven-vertex
classes and bounds total named support by ten. Its 4224 static classes and the
bounds on later maximum families do
not establish a dynamic exclusion or a fifteen-step global upper bound.
The last command completely expands the remaining ten-named-state closed
later families, including the K5 control domain. Its first two positional
arguments select a non-overlapping interval of early graph IDs. It prints
counts only; the resulting 1048490 static domains are not automata.
The control compares ordinary subset selection, both canonicalization schemes,
and literal maximum families with two and three common isolated states.

The bounded-word reverse-frame control independently compares literal forward
images with shared-identity predecessor data. It checks the alphabet-selection
lemma, pair and row distances, quotient connectivity, and both positive and
negative safety outcomes. This is a small implementation control for a paper
reduction, not an enumeration of the unresolved codimension-five domain.

```sh
python3 run.py script scripts/problem4/check_backward_word_frame.cpp
```

```sh
python3 run.py script scripts/problem4/check_rank_descent.py
python3 run.py script scripts/problem4/check_odd_core_target.py
python3 run.py script scripts/problem4/odd_core_target.cpp 15 4 12 --all-partitions --threads 4
python3 run.py script scripts/problem4/odd_core_target.cpp 16 5 15 --all-partitions --threads 12
```

`odd_core_target.cpp` permits every local rank-one-defect map, rather than only
redirected involutions. It still covers only the explicitly defined odd-core
family in [the proof](../PROOF.md#problem4-arbitrary-odd-core-threshold).
`--all-partitions` covers every external permutation cycle type; without it,
only one long external cycle and a fixed point are used. `--emit` prints every
qualifying transition/subset/marker set. `--max-tasks N` restricts the prefix
domain and prints `PARTIAL`; only an unrestricted `COMPLETE` run exhausts the
chosen family. No negative result from this program is a general upper bound.
The independent Python check compares all small positive and negative instances
using literal subset BFS and a different transformation generator.

```sh
python3 run.py script scripts/problem4/upper_bound/problem4_k4_controls.py
python3 run.py script scripts/problem4/upper_bound/problem4_p3_shapes.py
python3 run.py script scripts/problem4/upper_bound/problem4_p2_rank.cpp
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --threads 3
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --two-three --threads 4
python3 run.py script scripts/problem4/upper_bound/problem4_p3_entry.cpp --overlap-two-two --threads 4
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags.cpp --threads 4
python3 run.py script scripts/problem4/upper_bound/odd_cycle_joint_distances.cpp --cycle 9 --threads 4
python3 run.py script scripts/problem4/upper_bound/check_odd_cycle_joint.py --cycle 9 --threads 4
python3 run.py script scripts/direct_attack/check_native_policy.py
python3 run.py script scripts/direct_attack/avoid_compress_all_gaps.py
python3 run.py script scripts/direct_attack/check_avoid_compress_all_gaps.py
```

`odd_cycle_joint_distances.cpp` rebuilds the normalized one-letter domain and
exhausts compatible subset/pair distances for the C9 branch. `--cycle 7`
reproduces the earlier C7 exclusion; `--injections` selects the independent
omitted-output/permutation traversal. The Python check compares both complete
retained map sets, reconstructs their signatures, and reverses both distance
search orders. It invokes C++17 for the large transformation enumeration and
requires no solver. These commands test the branch specified in
[the C9 reduction](../PROOF.md#problem4-c9-eighth-layer), not every m=5 graph.
Add `--full-kernel --all-layers` to either program to include every cycle-edge
matching kernel and check every possible short-pair layer. This proves the
[C7/C9 bounds](../PROOF.md#problem4-c7-c9-uniform-cycle-bound) without a separate
letter-rank hypothesis. With `--cycle 5` those flags test the nonzero relaxation
controls; the Python audit also checks the actual five-state Cerny counterexample.
`--columns` uses the proved equality-case column construction and a complete
partial-permutation traversal. With this option, `--cycle 11` and `--cycle 13`
are also supported. `--canonical-isolates` preserves all signatures while
quotienting independent auxiliary input/output labels; its row count is a
representative count. The precise domain proof is in the
[column reduction](../PROOF.md#problem4-odd-cycle-column-generation).
`--reverse-search` reverses both distance assignment orders. The optional
`--pair-closure` and `--pair-levels` apply the proved merging-reachability and
nonempty-distance-layer conditions. `--all-layers` reuses the same complete
subset candidate list with separate compatible pools at every pair cap.
For C11/C13, the Python command with `--full-kernel --signatures-only` checks
one literal representative per generated signature; it does not independently
enumerate all transformations or rerun the distance search.

`problem4_p3_shapes.py` 核对 P3 二点覆盖的十三种核心和三点覆盖的十二种核心。
`problem4_p2_rank.cpp` 核对至多四条边、覆盖数为三的图的最大独立集行秩界，
并以 C5 检查五条边的反例边界；它不枚举自动机。数学推导见
[q=13 的第二层覆盖](../PROOF.md#problem4-q13-second-layer)。
`problem4_p3_entry.cpp` 排除三点保护入口剩余的三个五点核心，默认同时运行两种
字母枚举和两种距离算法。它不要求保存证书或安装求解器；完整数学归约见
[三点入口定理](../PROOF.md#problem4-three-entrance-p3-reduction)。
加 `--two-three` 检查“二点第一入口、三点第二入口”的三点覆盖分支：先重建四个
完整核心，再对唯一粗域幸存组合保留共同保护点的身份并排除。该模式同样默认
独立核对完整映射域及距离，最多按四个互不重叠的映射域并行；本机完整运行约七秒。
二点覆盖分支由[三点第二入口定理](../PROOF.md#problem4-second-entrance-three-reduction)
中的纸面证明排除。

加 `--overlap-two-two` 检查两个二点入口相交的三点覆盖分支，完整遍历 86 个有序
核心选择。各选择可独立并行，默认同时运行逐输入赋值的独立生成器和完整距离
笛卡尔积/BFS 核对，本机四线程计算约四秒，首次编译另计。此模式 `--core 1` 至 `--core 11`
使用三点覆盖核心的原编号；旧模式的 `--core` 仍使用从零开始的局部编号。
完整三点覆盖归约见[重叠二点入口](../PROOF.md#problem4-small-entrance-overlap)。

## Complete thirteen-state calculation

The authoritative fixed-parameter calculation is:

```sh
python3 run.py eleven --threads 8
```

It uses at most 32 worker threads per C++ search, assigned to disjoint flag
or graph domains. It runs the native subset lower check, an independent literal
word tree, peeling controls, both P3 graph classifications, the full `tau4`
reduction, and these two complete entrance searches:

```sh
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags.cpp --all-entrances --quotient --threads 8
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags.cpp --all-entrances --tau3 --quotient --threads 8
```

`--all-entrances` includes every initial B,C clique of size one to three,
whether disjoint or overlapping, and every third clique or fresh isolated
singleton. The two-cover domain includes all thirteen cores; the three-cover
domain includes all twelve, including K4 (ID 100). Later fibers have no size
cutoff. `--quotient` acts on the whole ordered flag under core automorphisms.
The mathematical reduction and actual full counts are in
[the exact-value verification](../PROOF.md#problem4-eleven-audit).

Every letter domain is regenerated with two distinct enumerators. Exact integer
and modular ranks, reverse pair distances and two connectivity checks agree.
Whole-alphabet short words are exhaustively checked; no alphabet-size bound is
used. Folded and raw small-alphabet searches are checked against explicit word
trees on 512 pools, including noncommuting examples and distance restrictions.
An additional three-letter control requires the mixed-word check beyond pairs.

The default mode and `--sizes 1 1`, `1 2`, `2 1`, `2 2` retain the previous
restricted investigations. `--tau3-disjoint` is the old spelling of `--tau3`.
Those modes do not replace the all-entrance commands above. `--core ID` and
`--depth k` restrict the search, so their completion alone is not global
completion. Two-cover IDs are 0–12 and three-cover IDs are 100–111; ID 100
requires `--all-entrances`. `--flag` takes eleven masks B through the eleventh
fiber, with unused trailing entries zero, plus `--core`.

Default depth is eleven; all complete searches reject by depth ten or earlier.
A `COMPLETE` line confirms that the requested domain was actually exhausted.
Retained relaxation vectors cause exit three and an error from the launcher;
they are not DFA witnesses. Counts are printed to the terminal, generated
intermediates stay under `build/`, and no saved inventory is read.

## Fourteen-state q=13 equality calculation

```sh
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags_q13.cpp --all-entrances --quotient --threads 8
python3 run.py script scripts/problem4/upper_bound/full_fiber_flags_q13.cpp --all-entrances --tau3 --quotient --threads 8
python3 run.py script scripts/problem4/check_protected_slack.py
```

The first two commands use fourteen states, ten-element safe subsets, and
target length thirteen. They retain all entrance sizes and the same independent
letter generators and short-word controls. Both full domains reject by flag
levels ten and eleven, respectively. The represented eleven-level prefix would
be insufficient if survivors remained; exit three means unresolved.
See [the mathematical reduction and complete counts](../PROOF.md#problem4-q13-second-layer).

The last command checks the general protected-set contraction on small
constructed examples, including exact avoidance lengths, ranks, short pairs,
dual-space growth, synchronization with one spare protected state, and
stepwise reachability-preserving contraction and expansion. Its finite controls support
[the general proof](../PROOF.md#problem4-protected-slack-collapse);
they do not search all twelve-step candidates. The flag programs above handle
equality at thirteen, not the remaining target twelve.

The same Python control script also compares the protected-count quotient for
expanded-model reachability with every literal reachable subset in 300 small
domains. The [quotient criterion](../PROOF.md#problem4-expanded-reachability-quotient)
has at most 1578 states for a single-protected q=13, m=4 candidate expanded to
five protected states; passing terminal safety alone does not imply reachability.

For the separate six-cycle/eight-channel lower-bound family:

```sh
python3 run.py script scripts/problem4/probe_even_ring_channel.cpp 1 --screen-powers
python3 run.py script scripts/problem4/probe_even_ring_channel.cpp 2 --screened-permutations
python3 run.py script scripts/problem4/probe_even_ring_channel.cpp 2 --all-permutations
```

The first argument is the thread count. The first command reconstructs the
short-word proof over 1800 second letters and 15 initial sets: 104 cases survive
the first word family, and uniform two-b collision words reject all 104.
The second independently checks all 40320 channel permutations on those
104 cases. The third directly enumerates all 72576000 transition pairs.
Without a mode flag, only 29 channel permutations are used.
Permutation indices assign disjoint work to threads. `TARGET_FOUND` stops on
a reachable target; `COMPLETE` confirms exhaustion of the selected domain.
None of these results is a bound for all DFAs. See the
[family definition, proof, and complete counts](../PROOF.md#problem4-even-ring-channel-family).
The screening mode also accepts ring size, channel size, and target length:

```sh
python3 run.py script scripts/problem4/probe_even_ring_channel.cpp 1 --screen-powers 7 9 14
```

It checks words shorter than the target. The current implementation requires
ring size at least four, channel size at least ring size minus two, total size
at most twenty, and target at least the ring size. See the
[general family and codimension-five result](../PROOF.md#problem4-ring-channel-higher-defect).

For target twelve with two distinct first entrances:

```sh
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --arrival --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --arrival --fourth --threads 8
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --arrival --depth 7 --threads 8
```

This completes the initial three-layer domain and single-letter cell-capacity
relaxation, with integer/modular rank checks and exhaustive small-map controls.
`--pairs` additionally checks a common P1/P2/P3 distance assignment and exact
single-letter pair profiles. `--delay-cut` uses the proved exclusion of two
singleton first entrances; `--ranks` adds four one-step safe-source rank tests.
Both options require `--pairs`. Anonymous output permutations are retained
through exact one-letter projections; these projections are not iterated as words.
`--arrival` requires `--ranks` and additionally checks that each of the first
three safe-source families covers every state, as forced by four-step arrival.
`--fourth` (with `--arrival --delay-cut`) extends every surviving initial flag
by an actual fourth-layer fiber, including its supply, one-step rank/coverage,
and joint P6 cover constraints. It retains all fourth-layer one-count preimages,
not just cliques of P3.
`--depth 3..11` continues the same necessary-condition recursion. Depths four
and above require `--arrival --delay-cut`; `--fourth` is equivalent to depth four.
The seventh layer allows five-point fibers and does not impose P6's cover-three
condition. A new state is required there only when the extra dimension growth
has not yet occurred. Starting at layer eight, the program
includes mixed fibers consisting of one protected point and external coordinates
absent from the current family. `LAYER_COMPLETE` reports each completed layer.
The complete default split-layer domain is empty at layer nine, excluding all
two-first-entrance candidates without requiring mixed-word tests.
`--split-layer 2` and `--split-layer 3` instead select a unique first entrance
with the extra dimension growth at the indicated layer. Values `4..11` select
later growth, `0` selects no extra growth through layer eleven, and `--all-late-splits` (or value `12`) jointly
explores all later-growth and no-growth possibilities using shared prefixes.
Here `12` is a mode selector, not an extra safe layer. Before a split the Boolean
family may have either of two ranks; actual letter preimages must also lie in
the chosen dual space. `TERMINAL_SPLIT layer=0` at a truncated depth means only
that the split has not happened yet. These domains remain separate from the
completed split-layer-one exclusion until their own full runs finish.
Survival at any requested depth is not an automaton existence result.
Use `--flags --threads 1` to print the retained initial masks directly.
`--core ID` restricts to one of IDs 0–12 or 100–111; omit it for the complete domain.
The [proof and counts](../PROOF.md#problem4-slack-one-initial-flags) explain
the remaining obligations.

`python3 run.py script scripts/problem4/upper_bound/graded_flags_control.cpp`
compares the separate early-split and generic graded initial enumerators on
core 106, checking both retained flags and common distance-vector counts.
It checks enumeration consistency, not completion of the remaining domain.

For complete labeled terminal checks, add `--terminal-powers` at depth eleven
in a single-entrance domain, or `--terminal-mixed` to additionally check every
pair of letters and iteratively remove letters without compatible suppliers
for all required fibers and short-pair descents. Each possible initial subset
is handled separately. All output labels are expanded before words are tested.
These remain necessary conditions; a surviving pool is not an automaton.
`--terminal-alphabets` also invokes the existing arbitrary-alphabet search to
test all mixed words up to length eleven while requiring strong connectivity
and every supplier. A surviving alphabet still needs synchronization and
initial-set reachability checks before it could establish a lower bound.
`--terminal-avoidance` additionally requires that the selected alphabet can
avoid the protected state from the full state set. It computes the entire
backward subset closure, with no word-length cutoff, and branches on letters
that leave a non-avoiding closure. This option includes the other terminal
checks. Its [proof and independent controls](../PROOF.md#problem4-full-state-avoidance-cut)
explain why it is necessary even when the contracted model is not synchronizing.
With `--threads 1`, `--terminal-example` prints the first alphabet accepted by
the enabled complete terminal search, together with its initial set and basis.
It does not stop enumeration or certify synchronization or reachability.
`--terminal-reachable` adds reachability in the four-protected-state expansion
to the alphabet search. It computes the complete protected-count quotient and
branches on letters leaving a closed set that does not contain the target.
The [original-class equivalence](../PROOF.md#problem4-terminal-original-class-equivalence)
states why this stronger acceptance condition exactly matches the q=13 target
over the complete necessary flag domain. Its controls use independent ordinary
subset searches in seventeen-state expanded automata and compare reachability
with the previous eighteen-state expansion. The smaller quotient only removes
permutation self-loops at full external occupancy and four missing protected states.
`--literal-prefix` expands all output labels when at most two remain unnamed,
then tests the necessary cyclic-rank bound and powers from families whose row
counts prove that every member is an actual short image. It skips this stronger
test when more labels remain; no anonymous profile is composed as a word.
`--initial-flag B,C,D` with `--core ID` restricts a late-split run to one
canonical initial flag. Early-split runs use four masks instead. This permits
disjoint prefix jobs; a completed restricted job is not a complete core result.
The [core-106 partition](../PROOF.md#problem4-literal-prefix-constraints) lists
all four surviving late-split prefixes and the required coverage boundary.
All four prefix jobs have now completed with zero terminal flags, as have the
other 24 cores and both early split layers. The combined proof gives
`F_bin(r+13,r+9,r)=F(r+13,r+9,r)=11` for every `r>=1`; see the
[complete coverage and scope](../PROOF.md#problem4-q13-exact-eleven).
The final prefix can be reproduced with:

```sh
python3 run.py script scripts/problem4/upper_bound/slack_one_initial_flags.cpp --pairs --delay-cut --ranks --arrival --all-late-splits --depth 11 --terminal-reachable --literal-prefix --canonical-prefix --initial-flag 64,128,256 --core 106 --threads 1
```

Its completed layer eleven has 37561536 weighted choices, 783532 actual orbit
representatives, and zero surviving flags or distance vectors. This command
alone covers one prefix; the theorem uses all the domains listed in the proof.
The baseline does not enable periodic-state, stable-kernel, or isolated-column
pruning. Adding `--cyclic-isolates` gives the completed strengthened comparison.

`--canonical-prefix` also quotients every later ordered prefix by core
automorphisms fixing its initial flag. Outside and protected labels remain
fixed. Layer counts are weighted by orbit size, so they are comparable to the
unreduced run; `representatives` reports the number actually checked.
See [the prefix-orbit proof](../PROOF.md#problem4-prefix-automorphisms).
`--canonical-isolates` additionally sorts the ordered membership columns of
noncore external states. Its weights account for the existing first-appearance
normalization and combine with the core-orbit weights. It can also be used
without `--canonical-prefix`; see the [column-orbit proof](../PROOF.md#problem4-isolated-prefix-orbits).
`--periodic-isolates` rejects letters omitting any output outside the P3 core,
including at prefixes with anonymous labels. This property is invariant under
the allowed output-label permutations; no anonymous map is iterated.
The [general periodic-state lemma](../PROOF.md#problem4-periodic-isolated-states)
gives the long-safe-word hypothesis and its parameter scope.
`--cyclic-isolates` strengthens this to actual periodicity of every noncore
state and cyclic rank at least n−3. The conjunction is invariant even for
anonymous completions, by the [output-relabeling lemma](../PROOF.md#problem4-cyclic-core-relabeling).
It implies `--periodic-isolates`; the older flag retains its weaker meaning
for reproducing earlier counts.
`--stable-kernel` additionally requires every pair eventually merged by a
letter to belong to the P3 core. It implies `--cyclic-isolates` and replaces
its transient-state cap by min(3, the core vertex-cover number), which is two
for cores 10 and 12. The [stable-kernel proof](../PROOF.md#problem4-stable-kernel-core)
justifies applying this condition to anonymous completions; it does not justify
arbitrary iterated-word checks on those completions.
`--stable-partitions` implies `--stable-kernel` and also enforces the equivalent
clique-partition condition during output assignment. Its [proof](../PROOF.md#problem4-stable-kernel-partitions)
explains why partial block permutations and the final anonymous completion are exact.


`--controls-only` runs the implementation controls and skips flag enumeration.
See [the terminal compatibility proof](../PROOF.md#problem4-terminal-labeled-compatibility).


## Odd-cycle preservation controls

The [sharp threshold and compression consequences](../PROOF.md#problem4-odd-cycle-sharp-compression)
are proved symbolically. Rebuild their finite controls with:

```sh
python3 run.py script scripts/problem4/check_odd_cycle_span.py
python3 run.py script scripts/problem4/audit_cycle_seven_six_images.cpp --all-maps 4
```

The Python control uses small complete domains and exact rational ranks. The
C++ mode exhausts all maps on C5 plus one isolate and C7 plus one isolate,
including kernels outside the cycle. It partitions by the first output value
and prints results without requiring or writing report inventories.

## Uniform graph and rank controls

The all-length proofs and their scope are in
[PROOF.md](../PROOF.md#problem4-odd-cycle-all-lengths-bound). These programs
check finite domains and identities; they do not establish the unbounded
parameter claims by extrapolation.

```sh
python3 run.py script scripts/problem4/odd_cycle_geometry.cpp 7 4 --literal
python3 run.py script scripts/problem4/odd_cycle_geometry.cpp 9 4
python3 run.py script scripts/problem4/odd_cycle_path_distances.cpp 6 --compare-old
python3 run.py script scripts/problem4/odd_cycle_path_distances.cpp 2 0 0 --compare-legacy
python3 run.py script scripts/problem4/odd_cycle_path_distances.cpp 14 0 0
python3 run.py script scripts/problem4/check_odd_subdivision_deletion.cpp 10 4
python3 run.py script scripts/problem4/check_odd_subdivision_deletion.cpp --general 4
python3 run.py script scripts/problem4/check_short_pair_core_bounds.py
```

`odd_cycle_geometry.cpp N threads` accepts N=5,7,9,11,13; `--literal` adds
full state-map controls for N=5,7. The path solver uses k=(N−1)/2, then a
common-domain parameter t and a pair-distance cap h; zero means all relevant
values. It supports k=2,…,14. `--compare-old` accepts k=2,…,6 and compares
complete singular signature sets. `--compare-legacy` compares the distance
solvers on the requested small domain. C5 has positive survivors, as required
by its actual counterexample.

The subdivision checker exhausts all six-edge subdivision vectors for
m=4,…,10. Its separate `--general` mode uses all base graphs on two to five
vertices without isolates, with total subdivision budget at most two. The
Python checker uses ordinary pair/subset BFS to verify the Černý distance
formula and the eight-state h=2 counterexample, including actual reaching
and reset words.

Rebuild the complete near-maximal-rank core and action domains with:

```sh
python3 run.py script scripts/problem4/near_max_rank_cores.cpp 4 9 4 --literal
python3 run.py script scripts/problem4/near_max_rank_cores.cpp 5 13 4
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --all-caps
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --all-caps --m4
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --literal 1
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --literal 1 --m4
python3 run.py script scripts/problem4/near_max_rank_actions.cpp -1 4 --compare-defects
```

Action arguments start with core ID (`-1` for all), then threads. The default
is m=5 (27 cores); `--m4` selects 8 cores. `--all-caps` covers h=1,…,13 or
h=1,…,9, respectively; `--cap H` selects one layer. Every distance run compares
integer-domain propagation with a separate reverse-order edge assignment.
`--literal 1` compares complete one-isolate maps with the full normalized
auxiliary-state domain, including the unions of core-state arrows.
`--compare-defects` independently widens m=5 from defect at most two to four;
`--full-defect` can also widen the domain for a distance run.

`connected_vectors` only counts pools with no closed nonempty core subset;
it is not a count of strongly connected automata. In m=4 only h=2 has such
pools; the explicit actual counterexample is checked separately. In m=5 all
joint pools are empty. Mathematical coverage and limits are in
[the m=4 proof](../PROOF.md#problem4-four-cover-third-layer) and
[the m=5 proof](../PROOF.md#problem4-five-cover-late-layers).

## Earlier conditional sources

`scripts/problem4/experimental/tau2_third_pair_profiles.cpp --threads 4` 保留早期九个
二点覆盖核心中“第三入口为核心边”的受限原型，默认独立核对两种映射生成器。
它不覆盖单点第三入口；其 202 个选择有 28 个放松方案幸存，因此程序返回三，
统一入口会报告该退出码。这是探索结果，不能作为九核心完整排除的结论。

Individual sources share `build/work/manual/`, so a generator can be followed by
its checker. Some older exploratory programs depend on outputs from other
programs: read their imports, CLI and the corresponding section of [PROOF.md](../PROOF.md), and run the
producer first. Historical run inventories and package-based replay tools have
been removed; the launcher does not recreate old logs or replay a sealed snapshot.

`check_native_policy.py` constructs its 857 small inputs afresh and compares the
native scorer with independent ordinary-set BFS; it does not pass by scanning
an empty directory of old reports.

Many `synthesize_*.py` prototypes need `z3-solver`. A few numerical probes need
NumPy. These optional tools are outside the standard-library entry points above.
Timeouts and unsatisfiable restricted prototypes need a separate completeness
argument before they can support a theorem.

## Native subset search

The standalone `scripts/native/subset_search.cpp` accepts text records on standard input:

```text
reset n alphabet_size
<one row of n zero-based transition targets per letter>

avoid n alphabet_size S_mask A_mask
<transition rows>
```

It outputs the shortest length (`-1` if no word exists), visited-subset count,
then zero-based letter indices. Multiple records can be passed together with
`--threads 8`; independent automata are distributed across worker threads and
answers remain in input order. Single-automaton BFS is sequential. This avoids
claiming a parallel speedup where the search has not been partitioned.

The dense search accepts at most 24 states and caps estimated concurrent BFS
memory at 512 MiB. Subset search still has an exponential worst case; switching
languages does not change that mathematical cost. C7 parallelizes disjoint
blocks of the literal distance-assignment domain without dropping assignments.

The Python engine in `scripts/automata/` remains useful as a small independent reference.
`python3 -m unittest discover -s scripts/tests -v` checks implementation behavior locally;
there is no CI or Lean verification requirement.


The next, fifteen-step candidate uses **P9/P11**, not P10/P11. Its cover-five
branch is `rank_core_graph6.cpp 5 6 9 --actions START COUNT THREADS --sat-distances`
on the same complete geng stream of orders 6 through 10. There are 2294 cores.
Use `--letter-control` for the separate full generation comparison. This branch
alone cannot establish the upper bound fourteen.

For example, the first 32-core interval is reproduced with the following
complete graph input (nauty/Traces `geng` 2.9.3, no connectedness restriction):

```sh
set -o pipefail
export CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so"
for n in 6 7 8 9 10; do "$NAUTY_GENG" -q -d1 -D5 "$n" || exit; done |
  python3 run.py script scripts/problem4/rank_core_graph6.cpp 5 6 9 --actions 0 32 8 --sat-distances
```

The complete historical coverage uses `START=32*j, COUNT=32` for `j=0,...,70`,
then `START=2272, COUNT=22`. Each interval reads the complete graph stream;
`START` and `COUNT` select the canonical retained-core order, not graph6 input
lines. This is an optional expensive reproduction, not a paper-build step.

For the cover-four branch, the generalized closed-family generator retains
rank at least four, at most two absent states, and named support up to eleven.
It uses 128 bits for the 66 pair/coexistence positions; the previous 64-bit
representation is insufficient at eleven named states. Run:

```sh
python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp --control
python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 5 11 8
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 11 11 8 --distances --letter-control
```

The first two positional arguments select an inclusive early-core size interval;
the third is worker count. The static full run yields 4658 cores, two excluded
by the necessary entrance bound, and 3248981 closed domains. Dynamic runs also
apply the proved square-identity matching test, because P11 rows must remain
P9-independent after every two-letter word. Squares alone do not check mixed
words. Survivors print their exact row masks and are necessary relaxations,
not realized automata. Only a completed interval is counted as checked.


The saturated-union filter now accepts any nonempty omitted set, but callers
must prove that safe depth is at least union size minus row size. In the
fifteen-step domain this is justified for exactly two omitted states. The
[small-surplus maximum-family theorem](../PROOF.md#problem4-small-surplus-maximum-family-exit)
also bounds the two common-neighbor counts by 1 and 2 after sorting. The full
static union exclusion is 39281 domains, leaving 3209700; overlapping filters
must not be added as disjoint counts. Controls:

```sh
python3 run.py script scripts/problem4/saturated_exit_control.cpp
python3 run.py script scripts/problem4/check_low_cover_support.cpp
python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp --matching-control
```

For only the saturated half-density branch (two omitted points and six varying
points), append `--matching-branch` after `--distances --letter-control`.
Every potential common exit is a separate guard. Both generation orders check
the same whole-cube safe-domain condition; different guards are never merged.
Early kernel/row-target pruning only anticipates this explicit map condition.
The output reports selected dynamic domains separately from the full static
count. A partial guard run is not a complete eleven-point exclusion.

`CERNY_UNION_GROWTH=1` enables the additional reachable-union test for complete
row-distance profiles in `rank_core_graph6.cpp`. It requires at least one slow
starting row whose short images grow by one state per step until full support.
The fifteen-step low-cover driver enables this condition directly. Existing
running binaries retain their original filters; completed older intervals do
not require reruns merely because this necessary pruning was added.


The cover-five branch of the fifteen-step candidate is now completely excluded:
72 disjoint intervals cover all 2294 cores, all child exit codes are zero, and
all joint counts are zero. The remaining branch has cover four at P9.

For the low-cover dynamic driver, `--parallel-domains` stages the complete
selected domain and distributes individual domains, rather than whole cores,
across workers. `STAGED_CORE` lines are classification progress, not dynamic
completion. Only the subsequent completed count and terminal summary establish
the selected dynamic coverage. `--quotient-sc` checks both directions of the
necessary common-state quotient. `--joint-sat` solves row and pair distances
jointly and returns an existence indicator, not a model count:

```sh
python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp --capacity-control
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/check_joint_sat.cpp
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 5 10 14 --distances --letter-control --parallel-domains --quotient-sc --joint-sat
```

For eleven-point EARLY cores, the [plateau proof](../PROOF.md#problem4-five-fifteen-eleven-plateau)
justifies `--plateau`: every letter must preserve the same auxiliary maximum
source into the two early maximum targets. `--single-omission` selects only
one absent point. Two absent points and six varying points were independently
excluded in the completed matching-branch run. The inclusive early-core range
11..11 contains 90 cores and 3595 static domains; after the current necessary
filters it has 2712 domains, including 1530 single-omission domains.
`--core-index N --domain-index M` can select an explicitly restricted diagnostic;
indices refer to canonical early-core order and that core's complete later
family order, not the parallel completion order.

`SURVIVOR ... joint=1` reports existence in a necessary relaxation, not an
automaton or a count of all models. In particular, core 447/domain 0 in the
5..10 range (K4,4, rows 7,11,112,176) is excluded by the
[multipartite overlap proof](../PROOF.md#problem4-multipartite-overlap-exclusion).
The current `--joint-sat` path also requires at least one compatible letter
with a nonedge entering the complete proper early pair layer; see the
[pair entrance condition](../PROOF.md#problem4-proper-pair-layer-entrance).
This strengthens the old relaxation. The historical full run used the older
predicate and had 3,206,987 UNSAT domains and exactly one surviving domain,
this K4,4 case; the paper exclusion closes that exception. Its negative results
remain valid under the stronger necessary condition. Other SAT survivors,
if encountered in a different selected domain, still require analysis.

For a narrow comparison, `--historical-no-pair-entrance` explicitly disables
only this additional SAT condition in the current implementation. It requires
both `--distances` and `--joint-sat`; the stronger predicate remains the default.
The following two selected-domain runs generate the same 1,768 signatures.
The default reports `SOLVED joint=0`; the historical-predicate run reports
`SOLVED joint=1` (a relaxation, not an automaton). The terminal summary records
`pair_entrance` and `historical_no_pair_entrance` to distinguish the predicates.
This comparison does not repeat the full 3,206,988-domain dynamic calculation.

```sh
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/check_joint_sat.cpp --pair-entrance
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 5 10 1 --distances --letter-control --quotient-sc --joint-sat --core-index 447 --domain-index 0
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 5 10 1 --distances --letter-control --quotient-sc --joint-sat --historical-no-pair-entrance --core-index 447 --domain-index 0
```

```sh
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 11 11 8 --distances --letter-control --parallel-domains --quotient-sc --plateau --joint-sat --single-omission
python3 run.py script scripts/problem4/five_low_cover_positive.cpp --plateau
```

The native runs optionally use a CXX compiler wrapper adding `-march=native
-mtune=native` to the ordinary C++17/O3 build; assertions remain enabled.
Single-thread letter generation runs inline inside an outer domain worker.
The inverse table modulo 1009 verifies every nonzero inverse once; it replaces
the previous per-pivot trial loop without changing the field or rank semantics.
Interrupted development runs remain partial and are not added to coverage as
if they had reached their terminal summaries.


The eleven-point EARLY-core branch is now completely excluded by disjoint
components, as detailed in the [coverage proof](../PROOF.md#problem4-five-fifteen-eleven-excluded).
The older task completed 89 core components and was then interrupted; it is
not labelled a single normally completed 90-core run. The final core's two-
omission cases were already covered by the complete matching run; its 26
single-omission domains have now completed both auxiliary-maximum branches,
52 UNSAT decisions, with exit code zero. The exact last-core command is:

```sh
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 11 11 8 --distances --letter-control --parallel-domains --quotient-sc --plateau --joint-sat --single-omission --core-index 82
```

Core and domain indices always refer to the complete static order for the
selected early-size range. Completed independent components may be combined
only after checking their exact input union; unfinished components are excluded.
The five-to-ten-point run has 3206988 selected necessary domains. An earlier
run was interrupted at 285952 with no joint survivor; it remains incomplete
and is not used to fill the final coverage. The optimized run started over and
completed all 3206988 domains. The user's terminal output reports
`completed=3206988/3206988 cumulative_joint=1`, the unrestricted `COMPLETE`
summary, and `Completed in 22923.697s` (dynamic phase 22922.9 seconds).
It used paired full letter generation, 24 workers, quotient strong connectivity,
and joint SAT, with no sampling, row-count, core, domain, or omission restriction.
Its unique surviving domain is core 447/domain 0, excluded by the paper theorem.
Together with the completed cover-five and eleven-point components this proves
the [codimension-five exact value](../PROOF.md#problem4-five-exact-fourteen).
The earlier codimension-five publication check rebuilt the static domain and
reran small independent controls and the single exception, without repeating
the six-hour full run. The subsequent manuscript consolidation inspected
existing completion records and compiled the paper; it did not repeat those
research calculations.

The later [two/three-exception paper reductions](../PROOF.md#problem4-three-exception-closure)
replace the dynamic dependency for 7,499 of those 3,206,988 domains and for
20 domains in the separate eleven-point branch. The `--coverage` control above
reconstructs this overlap with the old domain definition; it does not repeat
the historical dynamic run or alter its completion count.

The completed full run used the older relaxation without the new pair-entrance
condition. Current source enables that necessary condition in `--joint-sat`;
the old negative decisions plus the paper exception exclusion suffice. The
opt-in `--historical-no-pair-entrance` reconstructs the older SAT predicate,
not the byte-for-byte historical executable. For an optional full rerun from
source with the current stronger condition (not needed for paper compilation):

```sh
LD_PRELOAD=/usr/lib/libmimalloc.so \
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
CXX="$PWD/build/native-cxx" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 5 10 24 --distances --letter-control --parallel-domains --quotient-sc --joint-sat
```

`LD_PRELOAD` and the compiler wrapper are optional local performance settings;
omit them if unavailable. Parallel completion order is not canonical domain
order, so skipping a count of canonical domains does not resume an interrupted
run. Samples and unfinished prefixes do not contribute complete coverage.

For a bounded performance investigation, select evenly spaced domains after
sorting by canonical core and domain indices:

```sh
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 5 10 14 --distances --letter-control --parallel-domains --quotient-sc --joint-sat --sample-domains 256 --profile-time
```

`--sample-domains N` selects at most N domains and prints `SAMPLE_COMPLETE`,
never a full-domain completion claim. `selected_dynamic` is the eligible count
before sampling; `TIMING domains` is the actual number checked. The selection
does not depend on worker scheduling. `wall_seconds` measures only the dynamic
phase, excluding graph classification and staging. The setup, generation,
independent-control and solve times sum elapsed time across workers and can
exceed wall time. Progress now also shows elapsed time and prints on a domain
completion after ten seconds without a scheduled progress update.

`--letter-control` pairs the two complete enumerations within each kernel and
incoming-set job. For that fixed job, each map is exactly an injection of the
ordered kernel blocks into the n outputs not reserved for auxiliary inputs.
Its mixed-radix permutation rank is a bijective identifier, accumulated during
assignment. The primary order produces strictly increasing ranks; the complete
target-first order is sorted and compared with it, including duplicate checks.
This compares exact full maps, not fingerprints. The shared deterministic square/signature/arrow
processing runs once. It was already the same code in the two separate passes;
equality of its full input sets implies equality of all its outputs.
`--separate-letter-control` retains two separate complete passes, including
repeated postprocessing, for a slower comparison. In paired mode the dynamic
`generate_seconds` includes both enumerations, and `control_seconds` is zero.

The optimized generator caches targets by incoming set and membership counts
by kernel, sorts each kernel once, and reuses action and recursion buffers.
The independent target-first generator retains its complete domain: adding a
source row splits each old membership column into bit-zero and bit-one parts.
Matching the bit-one counts determines the bit-zero counts for every old
nonzero column. For the old zero column, only the new bit-one part needs
equality; its remaining zero-column inequality follows from at most n kernel
blocks and exactly n available outputs. Point masks and population counts
implement these comparisons without scanning all 2^rows patterns per target.
These are exact enumeration changes, not additional mathematical exclusions.

The [partial-map budget proof](../PROOF.md#problem4-partial-map-joint-budget)
moves the existing first/last-layer test into both assignment searches.
Merged edges are fixed by the kernel; forced edges only accumulate. Cached
output-neighborhood masks update the latter without rescanning all input pairs.
The [partial-square cover test](../PROOF.md#problem4-partial-square-cover)
also removes impossible first-image targets as soon as their partial second
images violate independence or lose every possible incoming repair point.
The full cross-row identity matching still runs at complete maps. Auxiliary
maximum sources are subject only to their stated one-step condition.
`maps` now counts leaves reached after partial pruning; the budget-rejection
counter counts rejected partial extensions, not rejected complete maps. Earlier
raw map counts therefore need not match, while signatures and arrow unions must.

Use `--late-budget-control` instead of `--letter-control` for the slower oracle:
the primary generator prunes partial assignments, while the complete independent
target-first generator computes forced edges literally and applies the budget
only at complete maps. It also keeps square filtering at complete maps. It
compares every resulting signature and arrow union.
For rare large families, `--min-rows N` restricts the selected dynamic domain;
it never changes the full static-domain count. For example:

```sh
CERNY_PAIR_SAT_LIBRARY="$PWD/build/tools/cadical-3.0.1/build/libcadical.so" \
  python3 run.py script scripts/problem4/fifteen_low_cover_domains.cpp 5 10 14 --distances --late-budget-control --parallel-domains --quotient-sc --joint-sat --min-rows 13 --profile-time
python3 run.py script scripts/problem4/low_cover_actions.cpp --column-control
```

The thirteen-row restriction has 37 eligible domains, not 3206988. The column
refinement control independently compares against dense histograms on 1726001
cases, including every zero-column surplus in its stated finite range. SAT
conjunction sharing reuses only identical Boolean expressions; it leaves the
encoding relation unchanged. The existing 100686-case independent joint SAT
control also runs with this sharing enabled.

GCC profile-guided optimization was also compared using 256 training domains
and a different 1021-domain selection (only the first domain overlaps). Its
additional benefit was not reliable enough to make it a required build step.
The recommended build remains C++17/O3 with assertions; a local compiler
wrapper may add `-march=native -mtune=native`.
