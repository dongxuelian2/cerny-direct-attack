# Optimal local phases can force dependent growth indicators

Date: 2026-10-01. The exact finite obstruction is **COMPUTATIONALLY
VERIFIED**; the state-minimality lemma below is **PROVED (paper)**.
The existence claim specified below is **REFUTED**. General Cerny,
global policy square, and the weaker nongreedy shortest-word question
were **OPEN** at this checkpoint. Subsequent
SHORTEST_BINARY_INDEPENDENCE_REFUTATION.md refutes the latter existence
repair using a different simple binary input. General Cerny, policy
square and weaker proportional/expensive-phase bounds remain OPEN.
No **FORMALLY VERIFIED** claim or priority claim.

## The quantifier that fails

Let R be the nonempty actual image sets Qw. For S in R, let e(S) be
the shortest ORIGINAL word taking some T in R with |T|>|S| into S;
strict containment is allowed. All parents attaining e(S) are retained.
Set G(Q)=0 and G(S)=e(S)+min G(T) over these parents, and
P=min_q G({q}). An optimal policy chain starts at a singleton attaining
P and uses only parents satisfying this Bellman equality.

The refuted proposal is that SOME optimal policy chain has independent
normalized indicators of ALL its proper growth stages. Initial singleton
and final Q are excluded from that stage count. Normalization means
chi_S-(|S|/n)chi_Q, equivalently raw rank after adjoining Q, minus one.
This is stronger than the old D1 assertion about every history, and
different from choosing phases freely in a globally shortest reset word.

The witness reuses an already retained automaton; it is the exhaustive
optimal-choice quantifier and its nongreedy comparison that are newly
audited here. Nothing is inferred from the absence of a prior citation.

## A completely reachable binary five-state obstruction

On Q={0,1,2,3,4}, the ORIGINAL rows are

    a=(0,0,2,4,3), b=(2,0,3,4,1).

This is retained `n5_extremal/extremal_005.profile.json`. All 31
nonempty subsets are actual. Exact rt=P=14, and the singleton G vector
is (14,18,15,16,17). There is EXACTLY ONE optimal endpoint-set chain:

    1 -> 3 -> 7 -> 27 -> 31, phase costs (1,5,5,3).

Masks are sums of 2^q. Every shortest parent is included in the audit:
the relevant parent lists are 1:[3], 3:[7], 7:[23,27], 27:[31].
The rank-four tie 23 loses globally, so it creates no second optimum.
The three proper vectors obey the exact Boolean diamond identity

    chi_3 + chi_31 = chi_7 + chi_27.

Their raw rank with Q is three and normalized rank is two. Thus EVERY
optimal actual-image policy chain is dependent in this completely
reachable binary example, even though its P equals its reset threshold.

There are EXACTLY TWO shortest ORIGINAL reset words:

| Word | Inverse record-growth sets | Record phase costs | Normalized rank |
|---|---|---|---:|
| abbabbababbbba | 3,7,27,31 | 1,5,5,3 | 2 |
| abbabbaababbba | 3,19,27,31 | 1,6,4,3 | 3 |

Both reset to state zero and have length 14. Record growth is the first
time an inverse full preimage exceeds all earlier cardinalities; temporary
shrinking is allowed. In the second word, transporting actual parent 19
into target 3 costs six, while e(3)=5. The following stage costs four
instead of five. The extra letter is recovered later. The whole word,
not an isolated phase substitution, verifies compatibility. Its three
proper centered indicators are independent. BOTH words' full letter-by-
letter inverse histories have raw rank five.

Hence this does NOT refute existence of an independent record-growth
history among globally shortest reset words with unrestricted phases.
That weaker general claim survived THESE two inputs but is subsequently
REFUTED by SHORTEST_BINARY_INDEPENDENCE_REFUTATION.md. A universal positive
fraction of the number of stages for optimized policies is NOT refuted
by a three-stage/rank-two example; long-phase dimension tradeoffs remain OPEN.

## A second retained binary example and every shortest word

For `extremal_004`, rows a=(0,2,3,4,1), b=(1,0,3,2,0), there are
30 actual images and exact rt=P=15. Its singleton G vector is
(15,16,17,18,19). Its unique optimal chain is

    1 -> 18 -> 22 -> 27 -> 31, phase costs (1,5,6,3).

Again chi_18+chi_31=chi_22+chi_27 and normalized rank is two.
ALL THREE shortest ORIGINAL reset words are:

| Word | Inverse record-growth sets | Record phase costs | Normalized rank |
|---|---|---|---:|
| baabaaabaabaaab | 18,19,27,31 | 1,7,4,3 | 3 |
| baababaaabbaaab | 18,22,27,31 | 1,5,6,3 | 2 |
| baababaababaaab | 18,26,27,31 | 1,6,5,3 | 3 |

All reset to state zero. Each full inverse letter history has raw rank
five. The two nongreedy words respectively spend two/one extra letters
on the second stage and recover two/one on the next stage.

## Five states are minimal, over ANY finite alphabet

**PROVED.** Any strictly cardinality-growing actual-image chain on
n<=4 has at most two proper stages after its initial singleton. A
single nonempty proper indicator is independent of chi_Q. For two
distinct nonempty proper sets S,T, dependence of chi_S,chi_T,chi_Q
would force chi_T=alpha chi_S+beta chi_Q. Since both indicators take
both Boolean values, their distinctness forces T=Q\S. At n4 the
only possible two proper cardinalities are two and three, whose sum
is five rather than four. They cannot be complementary. At n<=3
there is at most one proper stage. This covers every allowed chain,
not just optimal chains, and makes the n5 counterexample state-minimal
over arbitrary alphabets, hence also within binary completely reachable
inputs. A minimum-cost policy exists since its rank-increasing graph
is finite and every proper actual target has an eventual larger parent
in a synchronizing automaton.

The same lemma makes the earlier D1 n5 dependence minimal, but does not
by itself establish that all optimal histories at that old witness are
dependent; that stronger fact uses the new exact Bellman audit.

## Verification scope

`optimal_phase_independence.py` reconstructs the actual family, uses
full-set inverse BFS for every e and ALL parents, and exact rational
Gaussian elimination. It enumerates ALL 32768/16384 original binary
words at the two exact reset thresholds, retaining every shortest reset.

`check_optimal_phase_independence.py` imports no generator or native
policy kernel. It reconstructs ALL-SOURCE forward transport distances,
including strict arrivals: 1177 forward vertices and 1861 transport
entries. Every e/G/W/parent entry is compared. A forward shortest-image
DAG independently enumerates ALL shortest reset words, rather than
repeating the generator's exhaustive word scan. Integer determinant
minors verify all 19 raw/centered/full ranks. All five original reset
words are checked literally, paying 73 letters. Seven corruptions,
including a spurious independent optimum, an omitted shortest word and
the nongreedy phase cost changed to five, are rejected.

This is continued check 104 and regeneration command 188, preserving
the 103-check checkpoint verbatim. Only this generator, deterministic
replay and independent checker are continued. No full 104-check rerun,
general square theorem, asymptotic optimized-rank theorem or proof kernel.
