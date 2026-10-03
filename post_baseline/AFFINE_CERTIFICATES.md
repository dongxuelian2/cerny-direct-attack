# Binary-depth formulas: finite symbolic certificates for infinite n

## Exact theorem established by the saved certificates

**PROVED by finite integer certificates and the extension lemma below**:
for every integer 2<=r<=17 and every integer n>=r+2, put
L=floor(log_2(r-1)). Then

    B_r(n) = 3n + L*r - 2^(L+1) - 3.

This covers infinitely many n. It is not an inference from a finite n
sweep. The lower bounds are explicit functions of an unbounded integer
counter, reduced to finitely many representative local inequalities by
an affine identity. The upper bounds are finite witness paths plus a
uniform padding argument. Python has checked the finite certificates;
there is no claim of Lean/kernel verification.

| r | constant C in B_r(n)=3n+C | minimal n in this theorem |
|---|---:|---:|
| 2 | -5 | 4 (baseline also covers3) |
| 3 | -4 | 5 |
| 4 | -3 | 6 |
| 5..8 | 2r-11 | r+2 |
| 9..16 | 3r-19 | r+2 |
| 17 | 33 (=4r-35) | 19 |

The theorem only asserts the indicated r values. Extending the last row
to all 17..32, or the logarithmic expression to all r, remains a conjecture.

## Finite certificate format and extension lemma

Fix r>=2. A certificate consists of an integer J>=2, a nonnegative integer
table T(j,x) for 0<=j<=J, 0<=x<2^r, and a labelled capacity2 path W from
(2,2^r-1) to a singleton, of length V. Ignore the entry (0,0), since the
empty set is not a vertex. Define on all j>=0

    P(j,x)=T(j,x)                         if j<=J;
    P(j,x)=T(J,x)+3(j-J)                  if j>J.

It is enough to check these finite conditions:

1. P(0,2^i)=0 for i=0,...,r-1, and P(1,0)=0;
2. for every nonempty state with 0<=j<=J+1,
   P(j,x)<=1+P(j,b(x)), where b(x) replaces the first two bits by
   (x_0 OR x_1,0), and
   P(j,x)<=1+P(j+x_0-t,shift_t(x)) for both t=0,1 with t<=j;
3. P(j,2^r-1)=3(j-2)+V for 2<=j<=J+1;
4. W is a valid path at capacity2 and has length V.

These conditions imply

    B_r(n)=3(n-r-2)+V for ALL n>=r+2.

### Proof of the lemma

Condition2 is intentionally checked on a graph larger than any finite
capacity graph: t=0 is always allowed, and t=1 is allowed whenever j>=1.
Thus it covers every actual edge at the checked j values.

For any j>=J+1, both endpoints of an a or b edge have hidden count at
least J: a changes j by at most1, while b preserves j. On this entire
region, P(j,x)=3j+[T(J,x)-3J], including j=J itself. The difference
P(source)-P(target) therefore depends only on x,t and the change in j,
not on the absolute value of j. All these edge types have been checked
at j=J+1. The singleton constraints and nonnegativity hold everywhere,
so P is a feasible potential at every finite capacity m>=2.

Condition3 gives P(m,F)=3(m-2)+V for 2<=m<=J+1; for larger m it follows
from the same affine identity at j=J. Telescoping the potential proves
the lower bound 3(m-2)+V for the full-set vertex (m,F).

For the upper bound, repeat the feasible baa cycle m-2 times to reach
(2,F), then use W. Every edge feasible at capacity2 remains feasible at
capacity m>=2, as proved by the graph embedding in
`GENERAL_STABILIZATION.md`. Length is 3(m-2)+V. This proves equality.

### Checking the actual certificates

`affine_certificates/r2.json` through `r17.json` give every T entry and W
explicitly; `index.json` records their hashes, J and V. The encoding of x
is sum(x_i*2^i), i.e. the low bit is the member bit of0.
`check_affine_certificates.py` checks precisely conditions1--4, importing
neither BFS nor the analytic edge generator. Its arithmetic is fully
visible and uses only integer comparisons, bit operations and path length.
The theorem can thus be reviewed by checking finite displayed data and
the lemma, without trusting the search which discovered those data.

`certify_fixed_r.py` regenerates the tables using a separate dense reverse
BFS and selects a valid affine cutoff. For this run the full-state value
in every certificate is exactly the expression displayed in the theorem.
The formula is explicitly evaluated in the generator; the checker checks
the stored bound and local validity independently.

## Rigorous failure of the earlier conjecture

The proposed formula 3n+2r-11 on 4<=r<=n-4 is false. Its first failure by n
is (n,r)=(13,9): the r9 certificate and the extension lemma prove

    B_9(13)=3*13+8=47, whereas 3*13+2*9-11=46.

There is no earlier admissible failure: n<8 has no admissible r, and for
8<=n<=12 every admissible r lies between4 and8, covered by the exact theorem.
The matching r9 base witness has length41 at n=11; padding two baa cycles
gives a length47 path at n=13. The r9 potential gives the matching lower
bound, so this is a rigorous counterexample, not a numerical mismatch alone.

## A more natural general conjecture

**CONJECTURED:** for ALL r>=2 and n>=r+2 the logarithmic formula holds.
Writing h=ceil(log_2 r), it is equivalently

    B_r(n)=3n + E(r) - 2r - 3,
    E(r)=(h+1)r-2^h.

E(r) is the minimum sum of leaf depths of a full binary tree with r leaves.
For a quick proof of that independent combinatorial fact, minimize the
external path length. A deepest sibling leaf pair can be contracted; if
there is also a leaf of depth at least two less, expand that shallow leaf
instead. This preserves leaf count and decreases total depth, so optimal
leaf depths differ by at most1. The full-tree Kraft equality then forces
2^h-r leaves at depth h-1 and 2r-2^h at depth h, giving E(r).
Balanced full trees with exactly these counts exist by starting from the
complete depth-(h-1) tree and expanding r-2^(h-1) leaves.

This binary-tree interpretation is a candidate explanation for the
powers-of-two transitions, **not a proof of the automaton formula**.
The missing lemma would connect arbitrary quotient paths to an external
path-length cost at least E(r), with a matching scheduling construction.
No such cost-preserving correspondence has been established here.

If the conjecture is true, the boundary n>=4 would satisfy

    B_(n-2)(n)=n-2 + E(n-2)+3 = n+1+E(n-2),

and, for each fixed k>=2, substituting r=n-k gives a formula of order
n log n along r=n-k. The certificates presently prove the n-2 boundary
only for 4<=n<=19. The cases r=n-1 and r=n are outside the conjectured
range: their features recover the concrete subset. No logarithmic
formula is asserted at those injective boundaries.
