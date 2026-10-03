# A weighted target for the unresolved order-two model

2026-10-03. General Cerny OPEN. The target below is CONJECTURED / OPEN;
the algebra and its conditional square implication are PROVED paper.
No result in this note is FORMALLY VERIFIED.

Later progress: WEIGHTED_GRAPH_SQUARE.md proves WEXT and square for all
primitive paired output-difference inputs, hence every PRIME half-core L,
and gives a broader all-n sufficient graph criterion. Separate complete
M8/M12 graph audits now supplement the TSV scopes below. Automatic
all-input connectivity of that original graph is now REFUTED in
WEIGHTED_GRAPH_AUTOMATICITY_BARRIER.md; general WEXT remains OPEN.

## Original model and exact mass

Let M=2L>=6, Q=Z_M union {r}, b(q)=q+1 on the core and b(r)=r.
The ORIGINAL letter a satisfies a(r)=0, a(0)=a(L)=r, and is any
bijection of the other M-2 core states onto themselves. Pair-splitting
is equivalent to synchronization, as proved in the prior order-two work.
All costs here count original a and b; no derived letter has unit cost.

Give each core state weight 1 and r weight 2. Write
nu=(1,...,1,2), mu(S)=|S|+1_{r in S}, and delta=e_0-e_L.
Direct output counting proves

    nu P_a - nu = delta,       nu P_b = nu,
    delta P_a = 0,             delta P_b^L = -delta.

Consequently nu P_a^k=nu+delta for EVERY k>=1, and

    (nu P_a + nu P_(a b^L))/2 = nu.

This is a stationarity identity for two ACTUAL WORDS of lengths 1 and
L+1. It is not a positive original-letter stationarity assertion and
does not supply a free linear extension theorem.

## Target and compatible implication

**(WEXT), CONJECTURED / OPEN.** For every synchronizing input in this
model and every nonempty proper S subset Q, an original word w of cost
at most M satisfies mu(S w^-1)>mu(S).

If U=S intersect Z_M is not a union of opposite pairs, choose
j in U with j+L outside U. The ACTUAL word a b^j, 0<=j<M, gives
mass gain 1 and costs j+1<=M, whatever the root flag. Thus only the
2^(L+1)-2 proper nonempty whole-pair/root patterns require WEXT.

**PROVED paper, conditional:** WEXT implies ONE reset word of cost
at most M^2=(n-1)^2. Begin with {r}, of mass 2. Every inverse extension
increases integral mass by at least 1; total mass is M+2, so at most M
extensions are needed. Prepend each actual extension word to the prior
suffix. The final inverse image is Q, hence the concatenation resets
every original state to r and costs at most M*M. The root need not
remain in intermediate sets; its weight accounts for this possibility.

**PROVED paper local case:** a whole-pair S whose a-preimage T is not
whole has an extension within M. Since delta(S)=0, mu(T)=mu(S) is
even; the core of T has even size, so at least TWO opposite pairs split
in T. There are at least two positive orientations j, and one has
j<=M-2. Then a b^j a has cost j+2<=M and mass gain
delta P_b^j P_a chi_S=delta P_b^j chi_T=1.
This does not bound the first split after a longer word.

## Independent finite evidence

The TSV checker uses original forward particle maps for every retained
word and constructs/checks ONE compatible chronological reset per sync
input. For complete scopes it verifies valid, unique permutations and
the factorial input count. Nonsync rows have a literal stable quotient
on opposite pairs plus root, with both induced letters permutations.

| M | input scope | total inputs | sync inputs | whole-pattern witnesses |
|---|---|---:|---:|---:|
| 6 | COMPLETE | 24 | 16 | 224 |
| 10 | COMPLETE | 40320 | 39936 | 2476032 |
| 12 | sampled | 10000 | 9995 | 1259370 |
| 14 | sampled | 5000 | 5000 | 1270000 |
| 16 | sampled | 2000 | 2000 | 1020000 |

These word upper bounds and resets are COMPUTATIONALLY VERIFIED for
exactly the retained scopes. No M8 exhaustive run is implied by this
table. Sample coverage is not all-input absence of counterexamples.

Separate structured/hill searches favor permutations that split few
opposite pairs. Only their retained peak instances receive independent
full Bellman checks over every subset: exact weighted minima 11 at M12,
13 at M14, and 12 at M16. The 42656/18898/4790 evaluated proposal counts
are EXPLORATORY; no independent all-proposal coverage theorem is asserted.
No retained case refutes WEXT. Previously proved three-a pool barriers
do not control words with unrestricted a-count.

`audit_order_two_weighted_extension.py` captures eleven actual commands,
checks all five TSV scopes and three peak Bellman arrays, rejects seven
corrupted TSVs, and protects all 35 prior release/Lean files by hash.
Its separate receipt is `data/order_two_weighted_extension_audit.json`;
neither the historical registry nor the ten-unit release is regenerated.

## A precise limit of generalization

The same weighted M-extension assertion for ALL rank-one root/core
models is REFUTED. In the synchronizing reflection example M5,n6,

    a=[5,5,4,3,2,0], b=[1,2,3,4,0,5], S=Z_5,

mu(S)=5 and the minimum weighted positive extension is 6>M, attained
by a b a b^2 a. Its a/b-preimage removes only one core state, yielding
mass 6. The complement {r} has minimum weighted shrink 6; an independent
literal cut of eleven vertices proves every word of length<=5 fails,
checks the witness and synchronization, and rejects four corruptions.
See `data/weighted_extension_reflection_barrier.json` and its checker.
This is COMPUTATIONALLY VERIFIED, not FORMALLY VERIFIED, and it is not
an order-two WEXT counterexample or a Cerny counterexample.

## Remaining obstacle

When successive preimages remain whole, the first pair split can be
delayed. A signed defect may be available only after a long prefix;
switching its sign by b^L adds L original letters. Neither a dimension
argument with uncharged derived letters nor the averaged paired quotient
proves the required M cost. General WEXT, the unresolved c0,t2 square,
and the unrestricted Cerny conjecture remain OPEN.
