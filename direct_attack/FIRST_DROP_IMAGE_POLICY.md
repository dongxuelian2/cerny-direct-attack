# First-drop normal form and exact singleton policy propagation

**PROVED on paper for every SC synchronizing DFA with n>=2, every finite alphabet.**
These are structural equalities for actual reachable images and the all-tie
image policy. No new n-only reset upper bound or Cerny proof follows.
Priority of the precise policy equalities remains OPEN. One-step inverse
seeds themselves are established, not a new algorithmic idea.

Use right actions, R={Qv}, and delta(T,S)=min{|w|: T w subset S}.
Assume n=|Q|>=2 throughout. At n=1, rt=P=0 and Cerny's bound is trivial;
the seed set is empty, so none of the nonempty-seed formulas is asserted.
For proper S in R, k=|S|, let e(S)=min_(T in R, |T|>k) delta(T,S).
G(S),W(S) use the minimum/maximum future tail over every T attaining e(S),
with G(Q)=W(Q)=0. Rank jumps and strict terminal subsets are permitted.

## Every shortest phase crosses the target rank in its FIRST letter

If |T|>k and w=xv attains e(S), then |T x|<=k. Otherwise T x is another
ACTUAL image of size >k, and its suffix v transports it into S in e(S)-1
letters, contradicting the definition of e(S). Thus x is nonpermutational
on T. All cardinality losses after that first drop are still allowed.

Define the boundary family

    B_k={U=T x: T in R, |T|>k, x a letter, |U|<=k}.

Put d(U,S)=min{|v|: U v subset S}. Then

    e(S)=1+min_(U in B_k) d(U,S).                       (1)

Indeed, every shortest phase has this boundary form, and every listed
boundary edge is an actual larger-image witness. If d(U,S)=e(S)-1, then
EVERY parent T of that boundary edge is an allowed policy endpoint:
delta(T,S)<=1+d=e(S), and global minimality excludes strict inequality.
Conversely every allowed endpoint supplies such an edge. Consequently
G/W tails are exactly min/max over the parents of winning boundary images.
This is a universal characterization, not merely a selected normal word.

## Singleton seeds and exact nearest-seed formulas

Let H={p: T x={p} for some T in R, |T|>=2, letter x}. H is nonempty:
the last letter of a shortest reset merges its preceding actual image.
Let D(p,q) be ordinary state-graph distance and

    d(q)=min_(p in H) D(p,q),
    N(q)={p in H: D(p,q)=d(q)}.

Boundary (1) for k=1 gives e({q})=1+d(q). In particular H is EXACTLY
the set of singleton targets with e=1; an ordinary fiber with two states
is not sufficient without a reachable image inside that fiber.

All shortest extension endpoints into q are precisely the actual images
merged in one letter to some p in N(q). Therefore

    G({q})=d(q)+min_(p in N(q)) G({p}),
    W({q})=d(q)+max_(p in N(q)) W({p}).                 (2)

At a seed p, e=1 and G/W are 1 plus min/max tail over its one-letter
merged images; substitution proves both equalities with every tie included.
This implies the global normal form

    P=min_(q in Q) G({q})=min_(p in H) G({p})
     =1+min{G(T): T in R, |T|>=2, T x singleton}.       (3)

Thus an optimal image policy ALWAYS starts with a one-letter phase.
Longer initial singleton phases are unnecessary for the global minimum.
This does not make later image phases optimal reset prefixes or prove a
square budget. It explains why C_n's larger worst singleton values come
from initial state distance, while allowing independent future-tie losses.

In particular a POLICY square failure is equivalent to G(T)>=(n-1)^2
for EVERY actual image T merged by one letter. An actual Cerny counterexample
must satisfy this condition because rt<=P. The converse for rt is not
asserted. This isolates the missing budget on actual kernel-contained images;
it does not make their ordinary reach words or G tails free.

The nearest-seed constraint in (2) is essential. An unrestricted minimum
min_p[G(p)+D(p,q)] is a valid reset-to-q upper witness but can be smaller
than G(q). The retained n4 state-edge obstruction has G(0)=2,G(1)=4 and
D(0,1)=1, while 1 is itself a closer seed. Thus ordinary weighted shortest
state paths do not equal the restricted policy recurrence.

## Largest seed is a stronger, refuted optimality restriction

Let kappa=max{|T|: T in R, T x singleton}. Define

    F_kappa=1+min{G(T): T merged by a letter, |T|=kappa}.

Always P<=F_kappa, but equality is REFUTED at state-minimal n4 over ANY
alphabet, already ternary:

    a=[0,0,0,3], b=[3,0,1,2], c=[3,0,1,3].

Here kappa=3, P=rt=2, F_kappa=4. Qac={3}; its first actual image is
{0,3}, a one-letter merge source. The only maximum source is {0,1,2},
merged by a. It has G=3, so insisting on it pays 4. Full actual reachability,
all distances and words are checked. At n<=3, either a constant letter
gives kappa=n and both costs 1, or every merged image has size 2, so (3)
gives equality. This proves arbitrary-alphabet state minimality.

The binary first failure is n5:

    a=[0,0,0,0,1], b=[4,1,1,2,3], kappa=3,
    P=rt=2, F_kappa=3.

Complete distinct-letter binary covers through n4 exclude earlier binary
failures; unary/duplicate letters cannot be SC synchronizing at n>=2.
Largest-seed square existence F_kappa<=(n-1)^2 remains OPEN. It is stronger
than the original global policy square conjecture, not a proved reduction
preserving optimality.
MAXIMUM_SEED_PENALTY_THEOREM.md strengthens this to an unbounded additive
and multiplicative penalty: rt=P=2 but F_kappa=n-2 for every n=6h.
SEED_INCLUSION_OBSTRUCTIONS.md refutes the weaker inclusion-maximal
restriction at arbitrary-alphabet state minimum n5, and antitonicity of G
at state minimum n4. Neither negative statement refutes a square guarantee.

Nor can all future ties be ignored: the retained binary n6 extremal

    a=[0,1,2,4,3,3], b=[1,3,5,0,2,4]

has kappa=2, the ONLY seed target 3, P=rt=25 but W({3})=26. Thus even
largest one-letter seeds can exceed the square under worst ties. This
strengthening is binary-minimal n6 by the complete covers through n5.
The best-policy square conjecture remains intact. A concrete worst-tie
word and phase chain are independently checked, not just a scalar value.

## Attribution and limits

The image-extension proposal and singleton inverse-search seed convention
are known from [Kisielewicz--Szykula, Sections 3.1 and 4](https://arxiv.org/pdf/1608.01268).
Their ordinary inverse seed definition and the present actual-image
capacities are not silently identified. The exact all-tie formulas above
are proved here; priority remains OPEN. No new Lean theorem. Complete and
sampled search scopes are recorded separately in the accompanying audit.
