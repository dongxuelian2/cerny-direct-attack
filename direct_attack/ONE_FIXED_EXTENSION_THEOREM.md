# Exact maximum image extension 2n-2 with only 4n-2 images

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

**PROVED on paper for all n>=6.** This improves the additive term in the
two-fixed-point 2n-4 family. The asymptotic necessary coefficient is still
2; neither a universal 2n upper bound nor Cerny is refuted. Priority OPEN.

Let L=n-1>=5, C={0,...,L-1}, and f=L. The letter a cycles C and fixes f.
The rank-three letter b satisfies

    fb=0, (L-1)b=L-2, cb=f for c in C\{L-1}.

Use right actions and write P={f,0,L-2}, B={f,0}, H={0,L-2},
S={L-3,L-1}. Strong connectivity follows from f b=0, the cycle on C,
and any default cycle state b=f.

## Complete image closure

The reachable images are exactly Q, all singletons, and the three families

    {f,j}, {j,j-2 mod L}, {f,j,j-2 mod L},  j in C.       (R)

There are 4n-2 images: the cycle-pair orbit has L distinct members since
L>=5 (the possible two-point rotational symmetry occurs only at L=4).
Qb=P, and a reaches every triple. Pb=B, whose rotations give all f-pairs.
{f,L-1}b=H, whose rotations give all cycle-pairs. Hb={f}, and strong
connectivity reaches all singletons. The displayed family is closed:
triples containing L-1 map under b to P, others to B; f-pairs map to H
when the cycle state is L-1 and to B otherwise; cycle-pairs map to
{f,L-2} when they contain L-1 and to {f} otherwise. This proves (R).

## Exact bottleneck, allowing singleton arrivals

Every first drop from a larger image to size <=2 gives B: a larger image
is Q or a triple, Q first becomes P, and the first triple rank drop is b
on a triple not containing L-1. Some actual triple drops in one letter.
Consequently e(S)=1+D(B,S), where D allows any terminal subset of S.

To reach a cycle-pair from B one must pass through {f,L-1}b=H. This first
entry costs at least L letters: L-1 rotations from 0, then b. Any later
entry again gives H. After the last entry, only a's can lead to S as a
pair: b either merges the pair or exits the cycle-pair family. The unique
rotation H a^j=S has j=L-1 modulo L, because L>=5 excludes the swapped
orientation symmetry. Thus every pair arrival costs at least 2L-1;
a^(L-1)b a^(L-1) attains it.

The first singleton is produced only by a cycle-pair not containing L-1,
and is f. It costs at least L+1 from B. The shortest state path from f
into S has length L-2: b to 0 and L-3 rotations to L-3. A b from a
default cycle state restarts at f; a b at L-1 first requires a path of L
letters from f and cannot shorten that path. Hence any singleton arrival also
costs at least (L+1)+(L-2)=2L-1. Both arrival types are covered, so

    e(S)=2L=2n-2.

The actual larger image P and word b a^(L-1)b a^(L-1) attain this value.

Every proper image has e<=2L. Triples use Qb a^j, cost <=L. f-pairs use
Pb a^j, cost <=L. Cycle-pairs use Pb a^(L-1)b a^j, cost <=2L. Singletons
use H b={f}, followed if needed by b a^j, cost <=L+1. These are actual
larger-image witnesses and account for every image in (R). Therefore
max e=2n-2, not just a lower estimate on one pair.

## rt=P_best=n+2

Q needs at least two letters to first reach B, then the first merge costs
at least L+1 as proved above. The word bb a^(L-1)bb resets Q to f in
L+3=n+2 letters, proving exact rt. Singleton f has e=1 via H and b.
H has e=L+1: a pair arrival from B requires L letters before the first
H entry, while a singleton in H requires at least L+1 to merge to f
and at least one further letter. Prepend the triple drop. The shortest
H extension can use P, and P has e=1 via Qb. Thus the exact policy chain
f -> H -> P -> Q costs 1+(L+1)+1=L+3. Since rt<=P_best, equality follows.

## Boundaries and verification

n5 is excluded: L=4 gives a cycle-pair of period 2 and max e=6, not 8.
n4 separately has max e=6. All n4..63 saved arrays have independent
ordinary-set all-source forward distances, and their complete image
closures and full-Q words are checked. The general jump-location scan
has 147 parameter cases at nine n values; every saved summary is also
independently checked. This scan proves no arbitrary-jump formula.

This family was extracted after a n63 permutation-mutation search first
found e=123; normalization and a jump-location scan then found e=124.
The algorithm and parameter proofs are separate from that sampled evidence.
The underlying image-extension formulation is known from
[Kisielewicz--Szykula, Section 3.1](https://arxiv.org/pdf/1608.01268).
Novelty remains OPEN. There is no new Lean theorem or general reset bound.
