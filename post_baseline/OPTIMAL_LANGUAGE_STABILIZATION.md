# Exact limiting optimal language and an explicit stabilization bound

Status: **PROVED** paper theorem. No general Lean claim.
The stronger `OPTIMAL_LANGUAGE_THRESHOLD.md` now proves the exact threshold;
this file retains the simpler coarse upper bound and the language definition.

Fix r>=2. Put L=floor(log2(r-1)), C=Lr-2^(L+1), K0=r+1,
A0=C+2K0. Define the finite relaxed language W_r by reverse split clocks

    0=s_1<...<s_K0=A0,
    s_(i+1)>=s_i+2,
    s_(2i)>=s_i+r when 2i<=K0.

There is a unique letter word associated with each clock vector: read a
split as b and each intervening clock step as a, then reverse that word.
Every word has length A0+K0=B_r(r+2). The odd release condition follows
from the even condition and spacing, so need not be separately imposed.

Let Opt_r(m) be the set of all optimal letter words for n=r+m, m>=2. Every
one starts with (baa)^(m-2), by the forced-prefix theorem. Strip that prefix
and call the resulting language R_r(m). Then

    R_r(2) subset R_r(3) subset ... subset W_r,
    R_r(m)=W_r for every m>=r+2.

Thus the entire optimal word language has an explicit eventual description,
not only an eventually linear distance. In terms of n, stabilization of
the reduced language is guaranteed by n>=2r+2. This bound is sufficient;
the exact sharper threshold is proved in the companion cited above.

## Necessity and nesting

All optimal b letters are effective. For an optimal path at capacity m,
the reverse genealogy clocks satisfy the timing constraints and all event
indices i>=p=2^L have the forced value C+2i. The first K0 reverse events
therefore end at s_K0=A0. Removing the forward prefix (baa)^(m-2) removes
exactly the extra reverse events after K0, so the reduced word is in W_r.

Prepending baa to any optimal capacity-m word realizes a capacity-(m+1)
path: the initial full state is taken to hidden count m with full window,
and the original path embeds. Its length is optimal by the exact formula.
After prefix stripping it yields the same reduced word. Hence the R_r(m)
form an increasing sequence.

## Sufficiency at capacity m>=r+2

Take any clock vector defining W_r. Reverse its word starting from singleton
at0. At each nonzero split clock input1 and split; at all other clocks
input0. Define ordered releases q_1=0, q_(2i)=s_i+r,
q_(2i+1)=s_i+r+1, and counts R(t),N(t) as in the uniform proof.
Spacing and the even release condition give q_k<=s_k for all k<=K0.
Consequently N(t)<=R(t) through A0. Before a rotation at t, hidden
occupancy is R(t)-N(t-1). At a split it is at least1; at all other times
it is nonnegative. There is no upper-buffer interlacing assumption here.

Before the last core split, there are at most r+1 total particles, so
hidden occupancy is at most r+1. For capacity m>=r+2 this satisfies
j<=m-1 for every input0, and j<=m for every input1. The split clocks are
spaced by2, so every input1 is preceded by0 and every split has bits10.
This proves the entire core reverse path realizable. At its endpoint
there are r+2 particles and its last split fills the first two window bits,
but the other bits need not be full.

Now append m-2 reverse aa-b cycles, choosing input0 then input1 and
splitting. After ell such cycles the newest min(2(ell+1),r) window bits
are all1, since the core's last split already filled two. Total particles
are r+2+ell. Therefore hidden occupancy before the next cycle is at most

    r-ell   if 2(ell+1)<=r,
    ell+2   if 2(ell+1)>=r.

For 0<=ell<=m-3, these bounds are at most m-1 because m>=r+2. Thus its
input0 is feasible. The following input1 is feasible: hidden count is at
least2 (there are at least r+2 particles), and after the first rotation
it is at most m. Its preceding input is0, so the split is legal.

After all m-2 cycles, 2(m-1)>=r ensures the anchor window is full. There
are r+m=n particles, so hidden count is exactly m. We have obtained the
full capacity-m feature. Reversing gives (baa)^(m-2) times the selected
word, of exactly the optimum length. Hence W_r subset R_r(m), proving
the equality and the stabilization theorem.

## Interpretation and remaining questions

Capacity2 suffices for the greatest timing schedule. A larger hidden buffer
eventually admits **every** relaxed optimal timing schedule; extra dense
splits wash all older holes out of the anchor window. This separates value
stabilization from language stabilization and supplies a normal form for
the latter. The minimum stabilization capacity M_r satisfies

    2<=M_r<=r+2,   M_2=M_3=M_4=2,   M_5>=3.

The exact M_r is now closed by `OPTIMAL_LANGUAGE_THRESHOLD.md`.
The size/combinatorial structure of W_r remains OPEN.
Neither the orbit semantics nor the standalone scheduling system is
claimed novel without further bibliographic comparison.
