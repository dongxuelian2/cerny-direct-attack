# Positive original-letter reversal criterion after the product obstruction

Date:2026-10-02. Start HEAD844c223. General Cerny OPEN.
Research continued after committing the all-d backtracking tradeoff.

The final positive result is the BROADER weighted criterion(B1): for
each original singular f, alpha_f>0 and beta_(f,g)>=0 balance
alpha_f D(f)+sum_g beta_(f,g)D(fg)=0 using ORIGINAL letters g.
The paid sign-repair argument still gives n-extension, and maximum
column in-degree M supplies a cost1/sizeM seed: rt<=1+n(n-M)<=square.
No rank cap is required. Exact row reversal below is a corollary.
Five high-indegree/all-original-multicluster controls n4..64 pass(B1)
even though exact row reversal is impossible at ANY cost. Their given
integer weights are independently checked, without an LP solver.

An ORIGINAL row identity c_f+c_(f g)=2Q, with one original correcting
letter for EACH singular original f, closes a square subclass at every
n/alphabet. The usual centered-column orbit chain gives a SHORT nonzero
cardinality change within n-1; if its sign is negative, inserting the
paid correcting letter between f and its existing suffix flips it.
Every proper subset extends<=n; c_f<=2 provides a size2/cost1 seed;
one compatible chain costs<=square. This removes fixed-root/kernel,
rank-one, transitive-group, separate SC and permutation-corrector
assumptions UNDER the explicit row condition. PROVED paper, not formal;
no novelty/priority claim. The escape ingredient is Steinberg2010 Lemma6.

Self-attack retains the existing n5 cost2 corrector b^2: its unavoidable
seed needs extension6, exactly n-1+2. No old failure search is repeated.
A new ALL-n metric on ordinary Cerny proves minimum row-reversing suffix
cost2n-3 by an omitted/doubled-index gap count, with actual
(b a)^(n-2)b attainment. The original-family reset threshold is not new.
The class criterion thus cannot be claimed universal; in-degree>=3
also makes such row reversal impossible at ANY cost.

Independent checker:430 inputs/388 complete canonical binary n2..5,
309SYNC/37 multidefect/133 all-original-multicluster,18780 subset words
(9403 negative flips),319898 pair Bellman edges,481632 literal controls;
32 old-counter Bellman edges. Nineteen complete retained Cerny rank-one
row graphs through n257 have89140 edges/38639553 weighted controls.
TEN corruptions are rejected, including a Cerny reversal potential.
No generator/solver imports. All-n proofs are paper; no new Lean claim.

Registry136/217 preserves135 previous captures verbatim, appends ONE
new independent checker, and does not claim a full136 rerun. Eight
native build hashes and the unchanged earlier Lean compiler/source
hashes are checked; deterministic regeneration and Git/manifest exact
coverage are sealed. Frozen168ffff is unchanged outside direct_attack.

The general proof remains unfinished. A state-minimal hypothetical
counterexample must evade this explicit positive one-step balance criterion,
as well as the prior original-one-cluster and proved congruence tests.
No unconditional improved n-only upper bound, full proof, independent
human audit or complete Cerny counterexample has been obtained.
