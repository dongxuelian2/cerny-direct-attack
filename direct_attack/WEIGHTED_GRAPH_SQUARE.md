# Original square resets from paired output differences

2026-10-03. **PROVED paper, all-n sufficient criterion and infinite
subclasses.** Finite controls COMPUTATIONALLY VERIFIED. NOT FORMALLY
VERIFIED. Automatic connectivity in the last theorem was later REFUTED
by WEIGHTED_GRAPH_AUTOMATICITY_BARRIER.md; its sufficient implication
remains valid. The complete order-two model and general Cerny remain OPEN.

## Model and endpoints

Use exactly the original model and mass from WEIGHTED_ORDER_TWO_EXTENSION.md:
M=2L>=6, Q=Z_M union {r}, b is the core cycle fixing r,
a(r)=0, a(0)=a(L)=r, and A=a|_(Z_M minus {0,L}) is an arbitrary
permutation. Core weight is1; root weight2. With delta=e0-eL,

    nu a = nu+delta, delta a=0, nu b=nu,
    nu a^k=nu+delta for all k>=1.

All products and costs below are ORIGINAL words.

**Endpoint lemma, PROVED paper.** Every mixed input has a root-fixed
word of cost<=M with root preimage mass exactly3, and a word of cost<=M
with root preimage mass exactly1. The latter gives weighted growth of
the whole core by complementing the root.

There cannot be exactly one mixed opposite input pair: the other full
output pairs would leave exactly one full output pair for it. Therefore
there are at least two mixed j in1,...,L-1. Take the least, j<=L-2.
For k_plus=(-A(j)) mod L and k_minus=(-A(j+L)) mod L, both <=L-1,
the words a b^j a b^k a cost j+k+3<=M. Their root masses are2+1
and2-1, respectively. Indeed

    nu a b^j a b^k a - nu = delta + delta b^k a
                               + delta b^j a b^k a.

The first two terms evaluate to0 on the root: the two kernel inputs
are opposite. The final term evaluates to+1 or-1, since k sends one
of the two different output residues into {0,L} and the other outside.
The plus word fixes r; the minus word does not map r to r. Hence the
literal root preimages are respectively root+ONE core and ONE core.
This proves an endpoint statement, not the formerly guessed short
root seedTHREE bound or an ordinary all-set extension theorem.

## A simple primitive-difference theorem

Define

    d = gcd(L, A(j)-A(j+L) for 1<=j<L).

**PROVED paper:** if d=1, EVERY proper nonempty set has an original
weighted extension of cost<=M. Consequently rt<=M^2=(n-1)^2.
In particular this holds for EVERY synchronizing input with PRIME L.
No separate condition on the permutation A is required for prime L:
mixing supplies a nonzero difference mod L, hence d=1.

Proof: nonwhole sets have the one-a extension already proved. If S is
whole, then for a b^j a b^s its mass difference is

    chi_S(A(j)+s)-chi_S(A(j+L)+s),

where core addition is mod M. The delta b^s term vanishes. Every
j in1,...,L-1 and every s in0,...,L-1 costs j+s+2<=2L=M.
On pair labels Z_L these words give every translate of an oriented
edge of step A(j)-A(j+L). The directed cyclic graph has components
exactly the residue classes mod d. If d=1, any nonconstant core
pattern has a positive edge. Constant core patterns leave only {r}
and the whole core as proper nonempty possibilities; the endpoint
lemma handles both. Integral mass increases from2 toM+2 in at most
M stages, with each actual word prepended to the existing suffix.
The same chronological word resets Q to r and costs<=M^2.

**Further PROVED paper sufficient case:** if d>1 and a mixed j satisfies
j<=L-d-1, the same conclusion holds. Nonperiodic patterns have a two-a
edge. For a period-d pattern choose k_plus when the root flag is1,
k_minus when it is0. The other endpoint after the last a is a core
state, because the pair is mixed. A final shift s<d can give this
endpoint the opposite membership from the root. In the displayed
three-a defect, delta b^k a b^s is0 on a period-d pattern by the
definition of d. Thus mass increases by1. Total cost is at most
(L-d-1)+(L-1)+(d-1)+3=M. No preservation of residue classes by A is
needed for this argument.

## More a powers, with every cost charged

For 1<=k<L and 1<=j<=L-k, define the differences
A^k(j)-A^k(j+L), and let

    h = gcd(L, ALL these triangular differences).

In particular h divides d. The ACTUAL words

    a b^j a^k b^s,       0<=s<L,

cost j+k+s+1<=M. On any whole S their mass differences are exactly
chi_S(A^k(j)+s)-chi_S(A^k(j+L)+s). The same translated-edge argument
therefore extends every core pattern that is not periodic mod h.
This uses arbitrarily many a, up toL, so it is not contradicted by
the previous restricted three-a barriers.

It remains to extend the period-h patterns, including their root flag.
Use vertices Z_h union {root}. For every triple j,k,s with

    1<=j<M, j!=L, k>=0, 0<=s<h, j+k+s+3<=M,

insert the directed edge from

    label(a(A(j+L)+k)b^s)  to  label(a(A(j)+k)b^s),

where core label is residue mod h and root has its own label. Its
literal witness is a b^j a b^k a b^s. For a period-h target, the
first two terms in the three-a defect vanish: h divides every
one-step paired difference. The edge is therefore the EXACT remaining
mass difference, even if either endpoint is the root.

**Graph criterion, PROVED paper:** if this finite directed graph is
strongly connected, all period-h targets have a positive entering
edge of cost<=M. Together with the triangular words and nonwhole
formula this proves WEXT and ONE original square reset for the input.
If h=1, the endpoint lemma automatically supplies both directions
between the two vertices, so the criterion holds. A mixed j<=L-h-1
is another automatic sufficient case, by the previous argument with h.
Construction/checking is polynomial in M. This is an input-dependent
general theorem, not a claim that the graph always is connected.

## Independent validation and attacks on the missing step

The endpoint checker covers COMPLETE720 M8 permutations plus72 controls
through n257:743 mixed and49 nonsync,422639 forward particles,80 displayed
words at cost M, five rejected corruptions. It also checks the NEW
weighted metric on six earlier periodic families p3..8:82368 canonical
three-a words,1658 zero/one/two-a controls and48 successes.
The exact weighted three-a minima remain M+p-1, just as in the earlier
root-positive metric. The algebra above and the prior periodic construction
prove the same infinite barrier for the weighted three-a pool; changing
the mass does not make a fixed n+C three-a pool universal.

The graph/reset checker covers772 explicit inputs: COMPLETE672 mixed M8,
84 sampled controls, fourteen prior periodic rows, and two new adversarial
residual rows. It independently recomputes every triangular gcd, verifies
1615 residual-edge ORIGINAL words,11204 chronological mass-growth stages,
and9189235 full-reset forward particles through n257. There are738 h1
and34 residual inputs. Five corrupted certificates are rejected.
Complete scope is M8 only; no all-input coverage at larger n is implied.

Two tempting replacements for the missing connectivity theorem are FALSE.
Both of the following M12 rows have triangular h=2, and their actual
residual graphs are connected:

    [12,8,9,5,1,4,12,2,3,7,11,10,0]
    [12,2,11,10,9,3,12,8,5,4,1,7,0].

The first has inverse paired-difference gcd1, so triangular h does NOT
force A^-1 to preserve opposite-pair residues mod h. The second has
least mixed j4>L-h-1=3, so it does NOT force the cheap early-mix condition.
These refute shortcuts to automatic connectivity, not the graph theorem,
WEXT, or Cerny. Their literal assertions are independently checked.

**Former CONJECTURED / OPEN, now REFUTED:** the residual graph is strongly connected for
EVERY mixed permutation A. This would close the original order-two
model, still without reducing arbitrary automata to this model. A
failed graph criterion would refute this pool conjecture; it would
not automatically refute unrestricted WEXT or the Cerny conjecture.
The later n25 counter has ordinary/weighted minimum9, so it refutes
automaticity of this pool while satisfying both actual extension goals.

## Complete M12 graph and original reset audit

`order_two_weighted_graph_pressure.cpp` now enumerates ALL3628800 M12
permutations. The sparse certificate retains only the24832 nonprimitive
residual inputs;3600128 mixed inputs have triangular gcd1, and3840 are
nonsync. This is a new metric/criterion scope, not a repeat claim about
the earlier unsealed M12 root-positive three-a search.

The independent C++ checker reconstructs EVERY input by factoradic
decoding, computes differences by independent starting-pair walks,
checks every nonsync stable quotient, and verifies every retained edge
with ORIGINAL forward particles. It constructs and literally checks
ONE chronological reset for EACH of the3624960 synchronizing inputs.
There are121280 edge witnesses,43499520 mass-growth stages and3123781271
full-reset forward particles. The largest displayed reset costs128<144;
this is an algorithmic upper certificate, not an exact reset threshold.
Complete finite coverage and actual resets are COMPUTATIONALLY VERIFIED,
not FORMALLY VERIFIED. Automatic all-n connectivity is now REFUTED;
the successful finite M12 statements are unchanged.

Eight additional late-two searches through M128 make800000 native
proposals. Those counts remain EXPLORATORY. Only1125 retained residual
inputs are independently checked:986 at M16/M20 also have literal reset
checks;139 at M24/M32 have graph/edge certificates only. The M48/64/96/128
files contain no residual rows, so their independent checks are empty
retained scopes and do not certify the omitted proposals.

The separate larger weighted-BFS pressure retains exact minima13 at
M18 and M20, certified by full Bellman checks of1048576 and4194304 edges.
Its4917/1763 evaluated native counts remain EXPLORATORY. No counterexample
is retained; that is not a universal absence theorem.

The native scoped audit authenticates the complete M12 capture, executes
eleven additional commands, rejects eight corruptions (including missing
coverage, wrong literal edges, and malformed/truncated trailing data),
and protects all35 prior release/Lean hashes. Neither the historical
registry nor the release inventory is regenerated.
