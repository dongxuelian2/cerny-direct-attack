# Reachable image extension and its exact capacity obstruction

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

The unrestricted Cerny conjecture and a universal linear image-extension
bound remain **OPEN in this work**. No quadratic upper bound is established.
Finite statements below are **COMPUTATIONALLY VERIFIED**. The capacity
reformulation and conditional implication have direct paper proofs; neither
is claimed as a new bound. No new Lean result.

## Definition and exact reformulation

Let R={Qv:v in Sigma*} be the actual reachable image family. For X subset Q,
define rho(X)=max{|T|:T in R, T subset X}, taking zero for an empty family.
For a proper nonempty reachable S, define

    e(S)=min{|u|: rho(Su^-1)>|S|}.

Equivalently, e(S) is the shortest transport word sending a larger reachable
image into S. Preimages may lose cardinality during that word. No condition
S subset Su^-1, nor equality Tu=S, is imposed.

The family R is forward closed. Capacity is certified on the subset lattice:

    rho(empty)=0,
    rho(X)=max(|X| if X in R else 0, max_{q in X} rho(X\{q})).

This identity follows by separating T=X from proper reachable T subset X;
any proper T omits some q. It uniquely determines capacity by induction.
For fixed k, the preimage graph has goals rho(X)>k. Its distance from S
with |S|=k equals e(S). Positive distance values satisfy the Bellman equality,
with zero at goals and -1 at the empty set. This yields a complete finite
certificate. It is not a universal upper potential.

If e(S)<=Cn for every proper reachable S in every strongly connected
synchronizing n-state DFA, choose any reachable singleton. Repeatedly pick
a larger reachable T and u with Tu subset S, and prepend u to the current
suffix resetting S. Cardinality increases strictly at each choice; at most
n-1 choices reach Q. This gives reset length <=Cn(n-1). Full reach words
for T are needed to certify membership in R but are not appended to the
reset suffix. This is why a universal linear image-extension theorem would
give a quadratic bound. It does not prove such a theorem.

The underlying conjecture and this conditional route are known:
[Kisielewicz--Szykula (2016), Section 3.1](https://arxiv.org/pdf/1608.01268).
Their lower-bound family requires asymptotic coefficient at least 3/2.
Priority of the particular finite witnesses retained here is **OPEN**.

## Five-state obstruction to ceil(3n/2)

Use states 0,...,4 and right actions with

    a=[0,0,2,2,4], b=[1,2,3,4,0].

The reachable pair S={3,4} has exact image-extension cost 10. The ten-letter
word abbbbabbbb sends the reachable triple T={0,1,3}=Qab into S. The
independently checked full-Q reach word for S is stored literally in the
certificate; b is a full cycle, and full-Q reachability of a singleton
establishes synchronization. Exhaustive independent inverse BFS from S
finds no shorter preimage containing any reachable set of size at least 3.
Thus e(S)=10>ceil(15/2)=8, and an exact bound e(S)<=Cn for all n would
require **C>=2**, already from this finite example. This does not imply an
asymptotic coefficient lower bound 2 with additive corrections.

The proposal e(S)<=ceil(3n/2) is **REFUTED** at binary-minimal n=5.
Complete binary tests give maxima 3 at n=3, 6 at n=4, 10 at n=5 and 11 at
n=6. The n=3 value and n=2 bound are separately checked; no arbitrary-
alphabet minimality claim is made. All five/six-state first-map counts are
covering counts with overlap, not unique isomorphism class counts.

Exact inputs, full preimage Bellman values, capacities, endpoint words and
independent checks are in data/image_extension_n5/, data/image_extension_n6/
and data/image_extension_checks.json. No conclusion about the general
e(S)<=2n proposal follows from the absence of finite counterexamples.

## Structural lesson and remaining route

### Exact top-rank boundary (PROVED, elementary reconstruction)

For every reachable (n-1)-image S, e(S)<=n, over any finite alphabet.
Before a word first reaches rank n-1, permutation letters leave Q unchanged,
so an initial rank-n-1 letter suffices. A shortest subsequent path inside
that rank layer has at most n-1 edges, since there are only n possible
(n-1)-subsets. Thus some full-Q word of length <=n reaches S; taking T=Q
proves the bound. Synchronization and strong connectivity are not needed
for this local statement. This is not a new asymptotic bound.

The constant is sharp for every n>=2. In C_n, let a be q->q+1 modulo n,
and b fix all states except n-1->0. Take S=Q\{n-2}. The word ba^(n-1)
reaches S and has length n. Any word with A<n-1 occurrences of a has its
holes contained in {n-1,0,...,A-1}; induction handles a by rotation, and b
by retaining holes other than 0,n-1 and introducing n-1 (a hole at 0 after
b requires both old holes 0,n-1, hence A>=1). The hole n-2 is absent.
An avoiding word must contain b and at least n-1 copies of a, so its
length is >=n. Since Q is the only reachable image larger than S, e(S)=n.
Independent short-image BFS checks n=2,...,12 in top_rank_boundary.py.

Thus the first inverse image phase at top rank has a linear boundary;
the unresolved image-extension difficulty lies in lower reachable ranks.

Ordinary inverse cardinality can grow before capacity grows. In the
five-state example, the gap in the reachable ranks (no four-state image)
and the geometry of reachable triples make that difference observable.
This is a concrete obstacle to applying an arbitrary-preimage extension
lemma without controlling reachable images.

Capacity need not be submodular: take a constant letter and a three-cycle
on three states. The reachable images are Q and all singletons. For
X={0,1}, Y={1,2}, rho(X)+rho(Y)=2, while rho(X union Y)+rho(X intersect Y)=4.
Thus rho is not a matroid rank function in general. That observation does
not rule out a different dimension or charging argument.

The four tested parameter families and random/adversarial runs are finite
data, not formulas or proof of a general linear bound. The promising open
target is a short preimage path with capacity growth, or an amortized
sequence of such paths whose full costs are quadratic. A failed local
constant does not close that target.
