# Rooted period-rank payment in the original order-two model

2026-10-03. **PROVED paper, ALL-n subclass bounds.** This closes further
infinite square cases and gives an unconditional17/16 quadratic bound
for the remaining model. It does NOT reduce arbitrary automata to this
model. General Cerny and the complete order-two SQUARE remain OPEN.
No new FORMALLY VERIFIED statement or priority claim is made.

## Model, rank parameter and theorem

M=2L>=6, Q=Z_M union {r}; b is the ORIGINAL core cycle fixing r.
The ORIGINAL a has a(r)=0, a(0)=a(L)=r; its restriction A to
R=Z_M minus {0,L} is an arbitrary permutation. Assume it mixes an
opposite pair; equivalently

    d=gcd(L,A(j)-A(j+L) for1<=j<L) < L.

Give core states weight1 and r weight2. For a nonconstant Boolean
d-pattern of weight c, let p be its least period and D the rational
rank of the p cyclic shifts of its p-pattern. Define

    e(pattern)=max(0,p-D-1),
    e_d(c)=max of e over ALL weight-c Boolean d-patterns,
    E_d=sum_(c=1)^(d-1) e_d(c).

**PROVED paper:** ONE compatible ORIGINAL reset word satisfies

    rt <= M^2 + E_d - (L-d).

In particular square holds whenever E_d<=L-d. Universally

    E_d <= (d-1)max(0,d-3),    d<=L/2,
    rt <= (17/16) M^2.

These are bounds for THIS rank-one/root-two-cycle/core-cycle model,
with every a and b charged. The17/16 statement is unconditional for
all mixed inputs in the model; it does not assert the Cerny square.
The crude square condition for d>=3 is L>=d^2-3d+3.

## Every chosen extension retains the root and grows by ONE

With nu=(1,...,1,2) and delta=e0-eL, exact counting gives

    nu a=nu+delta, nu b=nu, delta a=0,
    nu a^k=nu+delta for all k>=1.

For S containing r, weighted and ordinary growth agree whenever its
inverse target also contains r. The following actual words ensure both
root retention and ONE additional core state.

If core U=S intersect Z_M is not whole under the opposite-pair shift,
choose j in U with j+L outside U. The word a b^j has weighted gain1,
and sends r to the selected state j. If |U| is even, there are at least
TWO split pairs, hence the least positive j<=M-2 and cost<=M-1.

For whole U not periodic mod d, translated edges from a b^j a b^s
(1<=j<L,0<=s<L) give positive gain. In fact cost<=M-1, not just M.
To see the saving, the undirected output graph on pair labels1,...,L-1
has degree2: input pair j is the edge joining the two output pair
labels A(j),A(j+L). A nonconstant coloring on a cycle cannot cross
exactly one edge. Thus at least two j have a nonzero translated
membership difference. Each nonzero difference has a positive translate
by cyclic summation, so some positive j<=L-2 exists. Its word costs
j+s+2<=M-1. Its root image A(j)+s lies in U.

The initial root alone has the earlier endpoint word
a b^j a b^k a of cost<=M, root-fixed, with inverse exactly root+ONE
core state. At least two pairs are mixed, so j<=L-2; take
k=(-A(j)) mod L. The next one-a word from that singleton core gives
root+{0,L}. These are genuine original words, not zero-cost seeds.

## Periodic extension lemma with its exact cost

Let U be a nonconstant period-d pattern, of least period p|d. Since
d<L, all p residue classes occur in R. Its p translated characteristic
columns, restricted to R, span a space X of the same dimension D as
the p-state Boolean circulant. D>=2 and X includes the constant column.

Set K=L-D. Consider EVERY original word

    a b^j a^k b^s,     1<=j<L, 1<=k<=K, 0<=s<p.

Its mass difference on S is
chi_U(A^k(j)+s)-chi_U(A^k(j+L)+s). If positive, the difference is1,
the root maps to its positive endpoint, and the word costs at most

    (L-1)+(L-D)+(p-1)+1 = M+p-D-1.

Suppose none is positive. For each fixed j,k, summing over all p shifts
gives0. All those differences therefore are0. Let W_i be the rational
row span of (e_j-e_(j+L)) A^t for1<=j<L,0<=t<=i, on R.
W_0 has dimension L-1, and W_K annihilates X, whose annihilator has
dimension2L-2-D. If all K successive inclusions were strict, then

    dim W_K >= (L-1)+K = 2L-D-1 > 2L-2-D,

a contradiction. Some W_i=W_(i+1) occurs. Since
W_(i+1)=W_i+W_i A, it is A-invariant; A is a permutation, so it is
also A^-1-invariant. It follows that every inverse opposite pair
A^-1(j),A^-1(j+L) has equal membership in ALL p shifts of U. Least
period p then forces equal residues mod p for these two states.

Now use the degree2 graph of inverse output pairs on input pair labels.
Every edge has endpoints in the same residue class mod p. A mixed
component is a nonloop cycle, with at least two MIXED INPUT vertices
in the same residue class. One of them has j<=L-p-1. Take
k=(-A(j)) mod L. The original a b^j a b^k a fixes r; the other
opposite endpoint after the final a is a core state. A shift s<p
can make that core endpoint absent from U. The middle defect
delta b^k a b^s is0 because p|d. Thus this word has weighted/ordinary
gain1, retains the root, and costs

    j+k+s+3 <= (L-p-1)+(L-1)+(p-1)+3 = M.

Combining the alternatives proves a root-retaining ONE-core extension
of cost<=M+max(0,p-D-1). The dimension proof is on the actual
permutation of R; no averaged quotient or derived-letter unit cost
is used. This lemma remains valid when the earlier residual graph fails.

## ONE chronological chain pays the periodic surcharges

Start at {r} and prepend each chosen word. Each inverse set retains r
and has one more core state; hence the core levels are EXACTLY
0,1,...,M. There are M charged stages, producing ONE reset to r.

Among the L-1 positive even core levels2,4,...,M-2, a period-d core
set is possible only at levels (M/d)c for1<=c<d. There are only d-1
such exceptional levels. Every other even level saves at least ONE
letter, by the nonwhole or degree2 translated-edge argument. Therefore
at least L-d savings occur on THIS SAME chain.

At exceptional level (M/d)c, the periodic surcharge is at most e_d(c).
The level occurs once; root retention is why a second root-absent
copy of the surcharge is NOT counted. Total surcharge is at most E_d.
Summing all actual stage lengths gives M^2+E_d-(L-d), as claimed.

Since D>=2, e_d(c)<=max(0,d-3), giving the crude E bound. A proper
divisor d of L satisfies d<=L/2=M/4; consequently E_d<=d^2<=M^2/16.
This proves the unconditional17/16 bound without any finite rank table.

## Further square classes

If d is prime, each nonconstant d-pattern has shift rank d: its Boolean
polynomial cannot be a multiple of1+x+...+x^(d-1). Irreducibility follows
by applying Eisenstein to that polynomial at x+1. Thus E_d=0.
For d4, least-period4 patterns have both primitive fourth-root modes
and the constant mode, so D>=3 and again E4=0.

Exact small-period factor analysis gives

    E6=1, E8=4, E9=2, E10=3.

For p6 the only positive surcharge has three selected residues and
cost parameter1. For p8, weight2/6 has parameter at most1 and weight4
at most2. For p9 only weight3/6 can have parameter1. For p10 only
weight5 can have parameter3. Lower periods do not increase these maxima.
Integer cyclotomic divisions and independent RATIONAL circulant
elimination certify EVERY Boolean pattern through d12, including these
cases. All d<=11 have E_d<=d, and L-d>=d because d is a proper divisor.
Hence every such input satisfies square at ALL n.

In particular square is PROVED for ALL mixed inputs whenever L is prime,
a product of two primes (possibly equal), or L<=23. The last statement
is only about this original model, not all automata below n49.
Further infinite square cases follow from the E condition or crude bound.

## Validation, failed shortcuts and remaining gap

Independent controls:8166 COMPLETE Boolean rank patterns through d12;
746 rooted chains including COMPLETE672 mixed M8;10488 original unit
stages;4496 checked saved stages;69447261 full-reset forward particles,
through n257. Five corrupted rank/chain certificates are rejected.
The chains happen to encounter no positive surcharge parameter; this
is NOT evidence that the surcharge never occurs.

A separate six-model COMPLETE periodic-pattern audit checks10036 targets
and20072 original extension words,40955518 forward particles. Of the
cost-saturation words,1688 exceed M and still satisfy the exact M+e bound.
These deliberately long valid witnesses test the payment parameter;
they do NOT establish necessity, shortest length, or a composable chain
of those separate target controls. Four corruptions are rejected.
The all-n compatible-chain proof is the argument above, not separate
row-wise minima or these saturation controls.

The literal period12 pattern on residues{0,1,5,6,9} has weight5 and
rational shift rank8. Therefore the guessed bound
D>=p-gcd(p,weight)+1 is REFUTED; coprime weight does not imply full rank.
The complete exact table has E12=28. At L24,d12, the global guarantee
is M^2+16, and at L36,d12 it is M^2+4. These are failures of this
budget proof, NOT Cerny counterexamples. At L>=48,d12 the same verified
finite rank table supplies a square bound.

General WEXT/RP remain OPEN. To complete the model square, one must
reduce the reachable periodic surcharges, secure more savings, or find
a different compatible policy in the large-composite-d/small-L/d gap.
Even that would leave the general automaton reduction unresolved.
