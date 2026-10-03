# Exact image-policy costs on the Cerny family

**PROVED on paper; novelty OPEN.** Let n>=2, Q={0,...,n-1}, a(q)=q+1
mod n, and let b fix q<n-1 and send n-1 to 0. Define
S_k={n-1} union {0,...,k-2} for 2<=k<=n. For the reachable-image
extension and all-tie policy recurrences in IMAGE_EXTENSION_POLICY.md,

    e({q})=q+1,
    e(S_k)=n                 (2<=k<n),
    G_min(S_k)=G_max(S_k)=n(n-k),
    G_min({q})=G_max({q})=(n-1)^2+q.

Every critical larger-image target is unique: S_2 from a singleton and
S_(k+1) from S_k. Both extrema fix the initial set. The global best
singleton costs (n-1)^2; the maximum over initial singletons costs n(n-1).
This is a family policy theorem, not an unrestricted reset bound.

## Proof

The actual word (ba^(n-1))^(n-k) maps Q to S_k, by
S_k ba^(n-1)=S_(k-1) for k>=3 and Q=S_n. The word
(ba^(n-1))^(n-2)ba^q resets to q. Only these reachable images are
needed; complete reachability need not be invoked.

Inverse a rotates an occupied set backwards by one. Inverse b replaces
the occupancy of n-1 with that of 0. On a nonempty proper circular
interval it fixes the interval, extends its left endpoint from 0 to
n-1, deletes its right endpoint n-1, or empties a singleton at n-1.
Empty inverse sets never grow. Until the first growth, a nonempty
inverse set stays a circular interval: deletion keeps its left endpoint,
and only inverse a changes that endpoint, decreasing it modulo n.

S_k starts with left endpoint n-1. Its first growth requires endpoint
0, hence at least n-1 inverse a steps and an inverse b. A preimage of
size >k must first grow, so the word has length >=n. At length n there
are exactly n-1 a steps and one b, and b must be the final inverse step.
The unique word is ba^(n-1), whose full preimage is S_(k+1). This image
is reachable. Its only contained image of size >k is itself, since it
has size k+1. Thus e(S_k)=n and the larger target is unique.

A singleton q starts with endpoint q. Its first growth needs q inverse
a steps; premature deletion makes the preimage empty. Its unique
shortest word is ba^q, with length q+1 and full preimage S_2, its only
larger contained image. This includes n=2, where S_2=Q.

The unique-target recurrence, with G_min(Q)=G_max(Q)=0, gives
G_min(S_k)=G_max(S_k)=n(n-k). Adding q+1 at the singleton gives
q+1+n(n-2)=(n-1)^2+q. This proves all formulas without assuming the
classical lower bound on the reset threshold.

## Consequences and audit correction

The average-singleton proposal sum_q G_min({q})<=n(n-1)^2 fails already
at n=2, with exact excess n(n-1)/2 on every C_n. Requiring every
initial singleton to meet the square also fails at n=2. The global
policy conjecture minimizes over q and remains unaffected.

The previously quoted C6 cost 30 is a maximum OVER initial singletons.
It does not come from extension-tie choice after fixing q=0: at each
fixed q both extrema equal 25+q. IMAGE_EXTENSION_POLICY.md corrects
that interpretation. The numerical arrays themselves were correct.

circular_image_policy.py recomputes ordinary-set inverse distances through
n=12, compares native arrays on all critical sets, and verifies exact e,
both tie extrema and full-Q reach/reset words. This finite audit supports
the parameter proof above, which remains outside Lean. Classical C_n
extremality and image-extension methods are known; priority of this exact
policy formulation remains OPEN.
