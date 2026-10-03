# An elementary reset-length-dependent bound for every seed tie

**PROVED on paper for SC synchronizing n>=2 over every finite alphabet.**
This is a bound on the shortest-image policy given an EXISTING reset word,
not a new general reset bound. It uses the ordinary SC state-distance
argument and the previously proved seed normal form. Novelty is not claimed.

If a reset word of length ell is known, then every proper actual image S
of size k has

    e(S)<=delta(Q,S)<=ell+n-k.                       (1)

After the reset, walk from its endpoint to S in the ordinary state graph.
A shortest first-entry path has distinct intermediate states outside S,
so its length is at most n-k. This proves (1) with full concatenation cost;
the walk is not a free change of the reset endpoint.

Let r be the maximum proper-image rank, and H the ACTUAL one-letter seed
targets. From any p in H the initial phase costs 1. Every subsequent phase
starts at an actual image of rank at least 2; ranks strictly increase, so
each k=2,...,r is visited at most once. Applying (1) to each phase gives,
including EVERY future shortest-phase tie,

    W({p}) <= B_r(ell)=1+sum_(k=2)^r (ell+n-k).

If the first merged source is Q, that chain has cost 1 and bypasses the sum.
If r=1 the sum is empty. Since r<=n-1 and all summands are positive,

    rt<=P<=min_(p in H) W({p})
         <=1+(n-2)ell+(n-2)(n-1)/2.                 (2)

For n>=3, subtraction of the square gives exactly

    [right side of (2)]-(n-1)^2
        =(n-2)(ell-(n+1)/2).

Consequently, if ell<=(n+1)/2, EVERY initial one-letter seed and every
future tie has total cost <=(n-1)^2. At n2 all chains have one letter,
so the same conclusion holds directly. Nonseed initial targets are not
covered by this all-tie square statement. Conversely a failure of the
best-policy square necessarily has rt>(n+1)/2 (n>=3).

This explains why the new rt=3 search family cannot violate the policy
square for n>=5, regardless of alphabet size or other letter ranks. Its
unbounded ratio P/rt is still substantive; it cannot be upgraded to a
square counterexample. The short-reset square corollary is not progress on
Cerny's reset bound by itself: its hypothesis already supplies a much
shorter reset. Future direct policy-counterexample searches should exclude
that settled regime rather than repeatedly mutate it.

check_first_drop independently reconstructs rt, every e/G/W value and
all actual seed targets, then checks (1), the rank-sensitive B_r bound,
and the conditional square statement. These finite checks supplement the
paper argument; no Lean theorem and no n-only bound is asserted.
