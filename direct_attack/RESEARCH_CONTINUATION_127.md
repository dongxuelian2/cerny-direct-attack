# Weak stationarity, paid costs, and a precise conditional positive bound

Date: 2026-10-02. Starting commit519c608b374da7d5f9ff75f18f9acb5cdde0cf10.
Goal ACTIVE; general Cerny OPEN; frozen168ffff unchanged. All edits
direct_attack. Registry126/207 preserves125 checks verbatim and adds
ONE independent checker; no full126 rerun. Registered native builds8.

Latest PROVED paper statements in SINGULAR_STATIONARY_WORD_COST.md:
on binary Cerny automata, with h(q)=n-2-q except h(n-1)=n-1,
EVERY literal word |w|<=n-1 has ([Q]M_w-[Q])h = -number of b-runs.
Duhamel telescoping uses e0-e_(n-1) followed by each literal suffix.
Suffix length<=n-2 means a first b merges the pair; otherwise outputs
are k,k-1 with k number of a's, giving h difference-1. Exactly the
last b of each b-run contributes. ALL redundant words included.
Thus nonnegative full-Q stationary averages on words shorter than n
cannot have positive singular weight. This is weaker than simultaneous
J/n and allows singular words in the search; old adjacent-transposition
permutation-only cost obstruction did not cover it.

The EXACT minimum MAXIMUM support cost with positive singular mass
is n, attained by uniform words b a^k,k0..n-1. This even gives J/n,
SC support (b,ba suffice), and a literal reset
(b a^(n-1))^(n-2) b of square cost. Expected cost has infimum0 if
mixing a small positive mass with the empty word; never confuse these
cost notions. No novelty, arbitrary-DFA linear lower bound, general
reset upper bound, or formal proof is claimed.

The positive conditional theorem is the known averaging-chain mechanism
with dimension d of an INVARIANT column space W. Assumptions: W contains
Q/e_q, ALL original letters preserve it, and strictly positive ALL-letter
probabilities give [Q]P x=[Q]x for every x in W. A centered Boolean
indicator starts in W intersect ker[Q], dimension d-1. Its orbit must
escape via a reset into the subset; growth gives an escape through d-1
letters. Averaging P^j,j0..d-1 gives functional mean0 and positive mass
on every alternative word, hence a positive cardinality extension in
that paid cost. Repeating at most n-1 times gives ONE common reset to q
of length <=(n-1)(d-1). This does NOT prove that the space of a single
optimal history is invariant or that the needed probabilities exist.
Source: Steinberg0910.0410 Lemmas2/6; no novelty claim.

The non-pseudo-Eulerian SC sync five-state example is
f=[4,0,4,0,0],g=[1,2,2,1,4],h=[1,3,3,1,0]. Normalalpha=[1,1,-1,-1,0]
is killed by all letters; Wkeralpha dim4 contains e4/Q. Equal-weight
P has full-Q deviationalpha/3, so projected stationarity holds but full
stationarity fails. Columns2/3 would force g/h weights each1/2, giving
column4only1/2. f g f resets, all13 words shorter than3 have rank>=2,
so rt3 EXACT. This is a small distinction example, not an asymptotic
class breakthrough. Checker enumerates ALL12 Boolean vertices in W,
10 proper inverse-extension witnesses, maximum paid extension cost<=3.

Independent exact checks:131053 ALL short words n2..16,65519 distinguished
pair suffix paths,130918 strict singular separations,34 attaining
parameters n2..32,64,127,257;9830808 original support-state letter
controls and19369452 reset-state letter controls;12 corruptions rejected.
The generator initially passed the obstruction-only controls. After
adding the conditional example, both generator/checker were rerun and
the FINAL literal captures are used in the new registry record. Earlier
initial captures retain their explicit smaller stage. Deterministic
replay and manifest/Git coverage are separately sealed.

Continue the ACTIVE general proof research after saving/committing this
intermediate result. Another unfiltered scan of the same domains has
little value. A meaningful route would find genuinely universal charged
structure, handle noninvariant histories, or complete the still-incomplete
independent audit of the reported one-cluster annular descent without
silently extrapolating it to multiple clusters. Previous continuation126
restores the marked-cost source error and its strict existential boundary;
125/124 restore the all-binary-n7 EXPLORATORY history pressure and fully
verified all-binary-n6 stronger-history statement. General Cerny remains
OPEN, and no full proof or full-proof audit artifact exists.
