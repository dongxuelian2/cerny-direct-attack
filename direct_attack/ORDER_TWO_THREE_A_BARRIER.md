# A three-a root-preserving extension barrier

Date: 2026-10-03. Post-release research based on HEAD ac948e7.
The release audit and its frozen receipts remain historical snapshots.

**PROVED (paper)**: an infinite synchronizing order-two family has minimum
root-preserving positive extension cost **n+1** among all words with at most
THREE occurrences of the original singular letter a. Thus the universal
three-a witness pool of ordinary cost <=n is **REFUTED**.
This does not refute root-preserving n-extension (RP), its seed condition,
the order-two square bound, or general Cerny: all remain **OPEN**.
No novelty claim. The infinite-parameter proof below is not formalized.

## Family, including all admissible completions

Let m>=2, L=6m, M=12m, delta=3m and h=2m. The states are
Q={r} union Z_M, n=M+1, and b cycles the core and fixes r.
Set a(r)=0 and a(0)=a(L)=r. The other core inputs map bijectively
onto C\{0,L}. Consider opposite input pairs {j,j+L}, 1<=j<L.

Let G0={j: 1<=j<L, j=0 mod3}. Fix their two inputs individually.
Choose a delta-invariant G1 of size h among the nonzero residues mod3,
containing {delta-2,delta-1,L-2,L-1}. This exists: start with these
two delta-orbits and add h/2-2 other orbits. Let G2 be the remaining
indices not in G0 or G1. It has size h and is delta-invariant.

Specify the four exceptional rows:

    a(L-2)=1,       a(M-2)=1+delta,
    a(L-1)=1+L,     a(M-1)=1+delta+L.

Map the other G1 pairs bijectively to the output pairs with base
1 mod3, excluding bases 1 and 1+delta. Map G2 pairs bijectively to
all output pairs with base 2 mod3. Either orientation within an
ordinary pair is allowed. These are literal original letters.
There are exactly TWO split opposite pairs. The previously proved
order-two classification therefore gives synchronization. The cost
proof does not assume a cost-free preparation word or return letter.

Let S={r} union {q in C:q=0 or1 mod3}. It is proper, root-present,
and a union of opposite pairs; |S|=8m+1. Its core period is THREE.

## Exhaustive word reduction

A leading b-prefix can be deleted without changing inverse cardinality
or root membership: b is a permutation fixing r. Reduce the powers
between successive a letters modulo M. Reduce the final b-power modulo3,
since S b^-3=S. These reductions do not increase cost or a-count.
It is therefore sufficient, for at most THREE a letters, to consider

    b^s, a b^s, a b^j a b^s, a b^j a b^k a b^s,
    0<=j,k<M, 0<=s<3.

Write chi for membership in S and core sums modulo M. For every core x,
the two values a(x),a(x+L) have the same membership after any b^s:
both are r at x=0,L; otherwise their output colors agree mod3.
The singular full multiplicity defect is e_r-e_L.

For ONE a, inverse growth is 1-chi(s), and root retention is chi(s),
so positive growth and retention cannot coexist. For TWO a, the
full multiplicity defect after a b^j a is

    e_r+e_0-e_L-e_{a(L+j)}.

After the final shift, growth is 1-chi(a(L+j)b^s), while root
retention is chi(a(j)b^s). They agree by the paired color property,
so again no root-preserving positive extension exists.

For THREE a define F_s(x)=chi(a(x)b^s), with F_s(r)=chi(s).
The defect after a b^j a b^k a gives growth

    1-F_s(a(L+j)b^k),

while retention is F_s(a(j)b^k). These formulas include kernel
inputs: b fixes r, and a(r)=0. The paired color property cancels
the e_{a(k)}-e_{a(L+k)} contribution; chi(s)=chi(L+s).

On the core F_s factors through x mod L. All ordinary paired j
have a(j)=a(L+j) mod L, and the kernel pair has identical outputs r.
They cannot give positive rooted growth. Only the four exceptional
input indices can do so.

For s=0,1, F_s is delta-invariant: its zero set is respectively
G2 or G1. For s=2, its zero set modulo L is G0, while F_2(0)=1.
Consequently its only oriented delta-boundary is

    F_2(x)=1, F_2(x+delta)=0  iff  x=0 mod L.

For j=L-2,L-1 the root-side output has base1, so k=L-1 mod L.
The cheapest choice has j=L-2,k=L-1,s=2, cost

    3+(L-2)+(L-1)+2 = 2L+2 = n+1.

For j=M-2,M-1 the root-side output has base1+delta, so
k=delta-1 mod L. Their cheapest cost is M+delta+2>n+1.
There are eight successful standard-form triples in the full stated
ranges (two k representatives per exceptional j), all growing by ONE.
The displayed cheapest word proves attainment. At most TWO a never
suffice, so the minimum singular count is THREE, but that count does
not minimize ordinary word cost.

## Independent finite evidence and precise base boundary

`order_two_three_a_barrier.py` generates 22 literal controls through n769,
including arbitrary pair orientations and different color assignments.
`check_order_two_three_a_barrier.py` imports no generator and checks
actual particle images, family coverage, all standard forms in19 controls,
and literal reset witnesses in16 controls. It rejects eight corruptions.
19 exhaustive controls cover157680 THREE-a words and21050878
single-letter particle checks. Larger controls verify the structural
table and displayed witness rather than claiming a full word search.

The n25 base rows are

    a=[24,2,5,3,4,10,6,8,11,9,1,13,24,14,17,15,16,22,18,20,23,21,7,19,0]
    b=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0,24].

For this SAME S, ordinary minimum cost is10, attained by a b a^8
(NINE a). A566-vertex sparse cut with604 checked edges covers every
word of length<=9 and contains no positive root-preserving goal.
The independent checker proves the lower bound by closure induction,
not by rerunning BFS or enumerating all2^25 subsets. The witness's
literal preimage has size18 and contains r. These finite statements
are **COMPUTATIONALLY VERIFIED**.

`post_release/OrderTwoThreeABarrier.lean` **FORMALLY VERIFIES** the
literal n25 ordinary minimum10. It includes the25 actual states and
both original transition rows, checks every cut-edge membership against
the literal inverse action, proves the all-word closure induction through
length9, and checks the length10 witness. The certificate uses Std/kernel
`decide`; printed axioms are only `propext` and `Quot.sound`.
The inverse word is explicitly the reverse of the original word; universal
quantification is invariant under reversal. The cardinality is computed
over ALL25 states. This does not formalize the infinite family or its
restricted n+1 bound. The new unit is outside the frozen release inventory.

Run with a direct working Python interpreter:

    python -m direct_attack.order_two_three_a_barrier
    python -m direct_attack.check_order_two_three_a_barrier
    python -m direct_attack.audit_order_two_three_a_barrier

The scoped audit records actual regeneration, independent checker and
Lean command captures, source/data hashes, and unchanged release/old-Lean
hashes in `data/order_two_three_a_barrier_audit.json`. It does not claim
another full historical-registry or submission rerun.

No prior release inventory, frozen formal source, or historical capture
is rewritten. The RP and SEED conjectures must now allow more than
THREE original a letters. This result removes a falsely promising
finite witness restriction and supplies no new general reset bound.
