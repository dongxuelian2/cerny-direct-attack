# Sharp dyadic threshold for the full optimal word language

Status: **PROVED**, complete paper argument below. Not generally Lean-verified.
This sharpens the coarse r+2 bound in `OPTIMAL_LANGUAGE_STABILIZATION.md`.

## Theorem

Use the reduced optimal languages R_r(m) and relaxed optimal language W_r
defined in the stabilization companion. Let M_r be the least m>=2 with
R_r(m)=W_r (nesting implies equality at every larger capacity). Then

    M_2=2;
    M_r=1+2^(L-1),   r>=3, L=floor(log2(r-1)).

Thus M=2 for r=2..4, M=3 for r=5..8, M=5 for r=9..16, M=9 for r=17..32,
and so on. The main distance already stabilizes at m=2; it is the complete
optimal **letter language**, after stripping baa padding, that has this
additional dyadic threshold.

## Setup and exact release counts

For r>=3 put p=2^L (even), M=p/2+1. Any clock vector for W_r has K0=r+1
events, s_1=0, s_(2^d)=dr for d<=L, and

    s_i=Lr+2(i-p)  for i>=p.

Given any m>=M, extend it by m-2 extra events spaced2, so K=r+m-1 and
the same dense formula holds to K. These extra events retain all timing
inequalities. Indeed for a newly added even child 2i>K0, its clock is
C+4i, while its parent has s_i<=C+F(i)=C+2i because 2i>r. Their difference
is at least2i>r; odd releases then follow from spacing.

Run the reverse process, input1 exactly at split clocks, input0 otherwise.
Let q_1=0, q_(2i)=s_i+r, q_(2i+1)=s_i+r+1; let R(t),N(t) count ready
particles and splits. They are strictly ordered, and q_k<=s_k proves
N(t)<=R(t). Before a rotation at t,

    j_(t-1)=R(t)-N(t-1).

The root's dummy count cancels. Input1 has j>=1; input0 has j>=0. Splits
have bits10 because their preceding input is0. It remains to prove the
capacity upper bounds j<=m for input1 and j<=m-1 for input0.

## Uniform buffer upper bound, all timing vectors

Write a=s_p=Lr. Let i=N(t-r), interpreted as0 when t-r<0. We always have

    R(t)<=1+2i.

### Before the rigid tail: t<a

Since s_(p/2)=(L-1)r, t-r<s_(p/2) and i<=p/2-1. Also N(t-1)>=i.
Hence j<=i+1<=p/2=M-1. The case i=0 is covered as well (the root cancels).
Both input upper bounds hold.

### At its start: t=a

The ordered releases and q_p=s_p=a, q_(p+1)=a+1 give R(a)=p,
N(a-1)=p-1, so the scheduled input has j=1.

### Intermediate releases: t=a+delta, 1<=delta<r

Past-parent index i is at most p-1, because t-r<a. Spacing from the fixed
event p/2 gives

    s_i >= (L-1)r+2(i-p/2),

so i<=min(p-1,p/2+floor(delta/2)). Meanwhile the dense current tail gives

    N(t-1)=p+floor((delta-1)/2).

If delta=2z>=2 (a scheduled split), then

    j<=2*min(p-1,p/2+z)-p-z+2
      <= p/2+1=M.

For z<=p/2-1 the first expression is z+2; for z>=p/2 it is p-z.
If delta=2z+1 (no split), then

    j<=2*min(p-1,p/2+z)-p-z+1 <=p/2=M-1.

For z<=p/2-1 it is z+1; for z>=p/2 it is p-z-1. These are exactly the
two different input conditions, not merely a bound on final occupancy.

### Dense releases: delta>=r

All children of parents i<p are now ready, and the dense parents i>=p
release exactly one particle per successive clock. Therefore the exact
count is

    R(t)=2p+delta-r.

For delta=2z or 2z+1, in either case

    j=p-r+z+1.

At a split, z<=K-p, giving j<=K-r+1=m. At a nonsplit, z<=K-p-1,
giving j<=m-1. This finishes realizability for every W_r vector.

The last K-p+1 splits fill at least 2(K-p+1)=2(r+m-p)>=r terminal
stream slots, because m>=p/2+1 and r>=p+1. The anchor window is full.
There are K+1=n particles, so hidden occupancy is m. Reversing proves
R_r(m)=W_r for every m>=M. For r=2 the unique optimal word already gives
M_2=2. This proves the sharp upper bound.

## Matching obstruction at capacity M-1

For r>=5, p>=4 and m=M-1=p/2>=2. Choose the earliest relaxed clock
vector, continued through K=r+m-1:

    t_1=0,
    t_k=max(t_(k-1)+2,t_floor(k/2)+r+(k mod2)).

This has the optimal deadline and the same forced spine and dense tail.
Its reduced core is a word in W_r. **Every reverse input is forced.**
At a split input must be1; immediately before a split it must be0. At
any other intermediate clock before the next split, that next event is
waiting for its next release (otherwise spacing2 would leave only the
immediately preceding clock). Thus R(t)=N(t-1), hidden count is0, and its
input must also be0. Induction proves that no unpaired input or different
representative can change this birth-only input pattern.

The explicit earliest recurrence gives

    t_(p-1)=(L-1)r+p-2.

Consider the nonsplit clock t*=Lr+p-1, immediately before the dense event
of index p+p/2. That index exists: K=r+p/2-1>=p+p/2 since r>=p+1.
At this clock all first p-1 parent pairs are ready, including

    q_(2p-1)=t_(p-1)+r+1=t*,

whereas q_(2p)=Lr+r>t*. Hence

    R(t*)=2p-1,
    N(t*-1)=p+(p-2)/2=3p/2-1,
    j_(t*-1)=p/2=m.

Its forced input0 requires j<=m-1, a contradiction. If a previous edge
already fails, the word is of course impossible as well. Thus this W_r
word is absent from R_r(M-1). By nesting, M_r>=M. Together with the upper
bound this proves the exact threshold. For r=3,4 the upper bound is2,
which is minimal in the m>=2 regime.

## Status and reproduction

The proof uses only the all-parameter formula, the proved optimal-event
rigidity/no-wasted-b theorem, ordered releases, and explicit buffer counts.
No finite enumeration is a proof premise. `check_language_stabilization.py`
enumerates all1352 relaxed vectors for r2..16 and all relevant capacities;
their exact smallest thresholds match the theorem. The earliest vector is
a universal adversarial witness for the lower threshold. The paper bridge
and full language theorem are not yet Lean-formalized.
