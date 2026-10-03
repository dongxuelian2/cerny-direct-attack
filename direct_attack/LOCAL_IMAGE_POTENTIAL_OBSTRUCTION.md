# Local rank potential and union transfer

These claims concern G from IMAGE_EXTENSION_POLICY.md. Neither refutes
the Cerny bound or the proposed min_q G({q})<=(n-1)^2 guarantee.

## I3: every reachable S has G(S)<=n(n-|S|) — REFUTED

The binary five-state example is

    a=[0,2,3,4,1], b=[1,0,0,4,3], S={2,3,4}.

It is SC and synchronizing, and S is Q-reachable. Exact image-extension
cost e(S)=8; the best shortest-extension policy costs G(S)=11>10.
An optimal chain chooses T={0,1,2,3} with transport u=ba^3ba^3 into S,
then Q with transport v=ba^2 into T. The combined word is vu, not uv,
under right action. Every shortest-extension tie is included in the
lower-bound calculation. The shortest full-Q word into S also costs 11.
Its reset threshold is 11 and its minimum singleton policy is 13<=16.

Complete binary first-map covers at n=2,3,4 check 9,182,4845 overlapping
inputs with no violation. Thus n=5 is binary-minimal in this SC scope;
identical letters are unary and cannot be SC synchronizing at n>=2.
The complete four-state three-letter cover also passes (2763520 inputs).
No arbitrary-alphabet five-state minimality is asserted. Searches at
n=5 and n=6 STOP upon the first local violation and are not complete.

The six-state example is

    a=[0,1,3,4,5,2], b=[1,2,0,0,5,4], S={3,4,5}.

Here e(S)=9 and G(S)=9+7+3=19>18. Optimal full-Q transport into S
costs 16; reset threshold is 18 and minimum singleton policy is 23<=25.
This also separates shortest-phase policy cost from optimal transport.
Saved arrays are independently checked by inverse-set BFS; critical
chains and shortest reach words are in data/new_image_checks.json.

## Attempted infinite lifts — NOT ESTABLISHED

For n=5,...,12, the fixed-swap/growing-cycle family with S=Q\{0,1}
has policy costs 11,11,11,12,13,14,15,16. The fixed-four-cycle/growing-arm
family with |S|=3 has costs 11,19,26,34,43,52,60,69. Only n=5,6 in
the latter violate n(n-3). Neither finite pattern proves an infinite
obstruction. All 16 instances have independently checked e, G, avoiding
and reset distances plus actual full-Q reset words. The growing-cycle
instances have 2^n-2 reachable nonempty images in this tested range;
no arbitrary-parameter reachability theorem is claimed.

## I4: capacity union transfer — REFUTED

The attempted statement: for reachable S,T,U=S union T with proper U,
if u properly extends U and rho(Uu^-1)>|U|, it image-extends S or T.
It fails even when a larger reachable witness maps ONTO U.

    n=3, a=[0,0,0], b=[1,2,1], S={1}, T={2}, U={1,2}, u=b.

The complete image family is Q, {1,2}, and the three singletons.
Su^-1={0,2}, Tu^-1={1}, Uu^-1=Q have capacities 1,1,3.
Qb=U, so the union expands properly, while neither singleton gains
image capacity. The expanding ordinary preimage {0,2} is unreachable.
This precise non-nested, nonempty, proper-union statement is state-minimal
at n=3 over any alphabet: two such sets cannot have a proper union at
n<=2. The search's word-length limit is not used for that minimality proof.
Independent ordinary-set checking confirms all fields.

## A valid conditional lemma

If V is reachable, Vu=S union T, |V|>|S union T|, and BOTH
X=V intersect Su^-1 and Y=V intersect Tu^-1 are reachable images,
then u image-extends S or T. Indeed, V=X union Y and the surjection
Vu=S union T gives |X intersect Y|>=|S intersect T|. Hence
|X|+|Y|=|V|+|X intersect Y|>|S|+|T|, and one set is larger
than its target. This proves a conditional counting lemma, not the
missing intersection-closure property or a general reset bound.

## Literature boundary

Ferens--Szykula's quadratic reaching bound assumes complete reachability,
or reachability of all sets larger than the target. Their proper-extension
union lemma concerns ordinary preimages. Requiring a contained larger
image to be reachable adds the failed step above; the completeness
hypothesis has not been removed.
[Primary manuscript, Lemma 3.2 and Theorem 5.7](https://arxiv.org/html/2208.05956v5).
Exact reaching, transport into a subset and shortest-phase policy costs
are different quantities. Priority of these finite examples remains OPEN.
