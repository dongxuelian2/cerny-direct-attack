# Three anchors: a uniform exact theorem

Status: **PROVED** (paper proof; no Lean claim). Definitions are exactly those
in `POST_BASELINE_RESEARCH_LEDGER.md`. No literature-priority claim is made.

## Theorem

For every integer n >= 5, B_3(n) = 3n-4. Also B_1(n)=n-1 for every n>=2.

## An exact description of the quotient

For r>=2, r<n, put m=n-r and write a vertex as (j,x), where
x=(x_0,...,x_{r-1}) is the anchor word in order (0,n-1,...,n-r+1),
and j is the number of occupied hidden positions. Its cardinality is
k=j+sum(x_i). The realizable vertices are precisely 0<=j<=m, k>=1.

The complete labelled edge relation is

* a: (j,x) -> (j+x_0-t, (x_1,...,x_{r-1},t)), where t is 0 or 1
  and t<=j<=m-1+t;
* b: (j,x) -> (j, (x_0 OR x_1,0,x_2,...,x_{r-1})).

Indeed t specifies membership of n-r, a particular hidden position.
One can choose its membership exactly when the other m-1 hidden positions
can hold j-t ones. Under rotation, x_0 enters the hidden region, while t
leaves it. The b action has no hidden endpoint. These arguments establish
both necessity and sufficiency, including capacity endpoints. Thus this
description does not relax the baseline's existential quotient.

## Lower bound

For r=3 write x=uvw, and define P(k,x) by this table. A dash means weight(x)>k,
so that the vertex cannot occur.

| x | k=1 (when realizable) | k=2 | k=3 | k>=4 |
|---|---:|---:|---:|---:|
| 000 | 0 | 4 | 8 | 3k-1 |
| 001 | 0 | 3 | 7 | 3k-2 |
| 010 | 0 | 5 | 8 | 3k-1 |
| 011 | — | 2 | 6 | 3k-3 |
| 100 | 0 | 4 | 8 | 3k-1 |
| 101 | — | 6 | 7 | 3k-2 |
| 110 | — | 1 | 5 | 3k-3 |
| 111 | — | — | 6 | 3k-4 |

We verify P(source)-P(target)<=1 for each edge. This also holds in the
larger graph which only requires j>=0, omitting the upper capacity bound.

For a, cardinality is unchanged. For k>=4 the difference is c(uvw)-c(vwt),
where c is the final-column offset. The following lists the two differences:

| uvw | t=0 | t=1 |
|---|---:|---:|
| 000 | 0 | 1 |
| 001 | -1 | 1 |
| 010 | 0 | 1 |
| 011 | 0 | 1 |
| 100 | 0 | 1 |
| 101 | -1 | 1 |
| 110 | -2 | -1 |
| 111 | -1 | 0 |

For k=3 the differences are, in the same row order,
(0,1), (-1,1), (0,1), (1,0), (0,1), (-1,1), (-3,-2), (1,0).
The t=1 case in the last row is impossible since j=0.
For k=2 the realizable differences are
000:(0,1), 001:(-2,1), 010:(1,-1), 011:(1,—),
100:(0,1), 101:(1,—), 110:(-3,—).
Every singleton maps to a singleton, so k=1 gives difference zero.

For b, v=0 gives a loop. If (u,v)=(0,1), the target word is 10w;
the differences for k>=4 are 0 (w=0) and -1 (w=1),
for k=3 they are 0 and -1, and for k=2 they are 1 and -4.
If (u,v)=(1,1), cardinality drops by one. For k>=5 the offset
calculation gives difference 1 for either w. The k=4 transitions are
P(4,110)-P(3,100)=9-8=1 and P(4,111)-P(3,101)=8-7=1.
At k=3 the differences are 5-4=1 and 6-6=0.
At k=2 only 110 is possible, and its difference to a singleton is 1.
These exhaust the edges.

P is nonnegative and is zero on all singleton classes. Telescoping the
edge inequalities proves that every abstract path from Q to a singleton
has length at least P(n,111)=3n-4.

## Matching upper bound

When all three observed bits are 1 and j>=1, the cycle

    (k,111) --b--> (k-1,101) --a[t=1]--> (k-1,011)
              --a[t=1]--> (k-1,111)

decreases hidden occupancy by one and has length three. In each cycle the
hidden occupancies are j,j,j,j-1, so all edges are feasible even at j=m.
Starting from Q, perform n-4 such cycles to reach (4,111) with j=1.
Then use the following eight-edge tail:

    (4,111) --b--> (3,101) --a[1]--> (3,011) --a[0]--> (3,110)
       --b--> (2,100) --a[1]--> (2,001) --a[1]--> (2,011)
       --a[0]--> (2,110) --b--> (1,100).

The hidden occupancies along the tail are 1,1,1,1,1,1,0,0,0.
The only extra capacity requirement is that a zero can be selected when
j=1, which is valid because m=n-3>=2. Every arrow is therefore witnessed
by a concrete subset. Total length is 3(n-4)+8=3n-4. In compressed word
notation it is (baa)^(n-4) b a^2 b a^3 b, interpreted in the existential
quotient; the concrete witnesses may change between arrows.

The two bounds prove the theorem, including n=5.

## One anchor

Every b decreases cardinality by at most one and a preserves it, giving
the lower bound n-1. At a class (k,1), k>=2, choose a representative
containing both 0 and n-1. It exists for every k<=n. Then b witnesses
(k,1)->(k-1,1). Repeating this abstract edge n-1 times gives the upper
bound. This proves B_1(n)=n-1; it is not a concrete word b^(n-1).

## Verification boundary

`verify_structural.py` checks the displayed potential with finite symbolic
representatives: k=1,2,3,4 and k=5 representing all k>=5. Affine expressions
make the last group's edge differences independent of k. It also compares
the analytic edge relation with concrete powerset enumeration at 44
parameter pairs, and checks the entire P3 distance table for n=5..100.
The latter two claims are **COMPUTATIONALLY VERIFIED**; the theorem above
rests on the explicit local calculations and the uniform witness path.
