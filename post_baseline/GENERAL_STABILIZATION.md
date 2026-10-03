# A theorem for every fixed number of anchors

Status: **PROVED**, with an elementary proof independent of experiments.
The explicit value of the eventual constant for arbitrary r is still open
within this repository.

## Theorem (three-step extension and eventual linearity)

For every fixed integer r>=2 and every n>=r+1,

    B_r(n+1) <= B_r(n)+3.

Consequently, there exist integers N_r>=r+1 and C_r such that

    B_r(n)=3n+C_r  for every n>=N_r.

Equivalently the exact recurrence B_r(n+1)=B_r(n)+3 eventually holds.
Moreover -5<=C_r<=r^2-3r-3. For r=1, the separate exact theorem gives
B_1(n)=n-1; slope three is asserted only for r>=2.

## Proof of the extension inequality

Use the exact window description proved in `B3_PROOF.md`. Write m=n-r>=1.
Every vertex (j,x) in the capacity-m quotient is also a vertex in the
capacity-(m+1) quotient. Every edge embeds as well: the only
capacity-sensitive condition is t<=j<=m-1+t, which implies
t<=j<=m+t. Singleton classes have the same descriptions.

Put F=(1,...,1). In the larger graph start from (m+1,F), the full set of
n+1 states. There is a three-edge path

    (m+1,F) --b--> (m+1,10...1)
              --a[t=1]--> (m+1,01...1)
              --a[t=1]--> (m,F).

This statement includes r=2, where the intermediate words are 10 and 01.
All choices are feasible at capacity m+1. The final vertex is precisely
the embedded full-set vertex of the n-state quotient. Append an embedded
optimal path of length B_r(n). This proves the inequality. Notice that
the anchor indices in the two automata differ: the embedding is of their
window/count descriptions, not of concrete sets with identical labels.

## Proof of stabilization

Refining the two-anchor feature cannot create a shorter abstract path:
each refined edge projects to a two-anchor edge. The baseline's proved
two-anchor formula therefore gives

    B_r(n)>=B_2(n)=3n-5.

Define E_r(n)=B_r(n)-3n for integers n>=r+1. The extension inequality says
E_r(n+1)<=E_r(n), and the lower bound says E_r(n)>=-5. A nonincreasing
integer sequence bounded below can have only finitely many strict drops.
It is therefore eventually constant, say C_r. This proves the claimed
formula and recurrence for every fixed r, without an exchange of limits
or a finite-data assumption.

For completeness, an explicit synchronizing word of length r^2 exists
on C_(r+1): b(a^r b)^(r-1). This is an upper bound, so no theorem about
its optimality is needed here. To see synchronization directly, the first
b removes r. After each a^r (rotation by -1), the occupied interval
{0,...,s} becomes {r,0,...,s-1}; the next b removes r by merging it with0.
After r-1 repetitions a singleton remains. Thus B_r(r+1)<=r^2 and

    C_r <= E_r(r+1) <= r^2-3(r+1).

Together with -5 this proves the stated interval. The total number of
units by which E_r can drop is at most (r-1)(r-2). This bounds the number
of strict-drop events, but **does not** bound the index of the last drop.
In particular, observing two consecutive equal offsets is insufficient
to conclude stabilization.

## A useful upper bound valid at every capacity >=2

The same proof, iterated starting at n=r+2, gives the uniform estimate

    B_r(n) <= 3(n-r-2)+B_r(r+2),   n>=r+2.

This has a direct witness: repeat baa exactly n-r-2 times to reach the
embedded full set with hidden count2, then append an optimal capacity2
path. It is an upper bound for arbitrary r; equality from capacity2 for
every r is not proved here. The affine certificates prove equality for
2<=r<=17. This distinction is the principal remaining structural gap.

## What the general theorem does and does not establish

The slope3 and eventual recurrence are proved for every fixed r.
There is no explicit general N_r or explicit general C_r in this proof.
In particular it does not imply a formula along r=n-k when r grows with n.
The separate binary-depth conjecture in `AFFINE_CERTIFICATES.md` would
control that regime, but it requires a new general lower bound.
