# Alternating family: exact image structure and a linear extension theorem

**Status update (2026-10-01).** The unrestricted linear actual-image
extension target is now **REFUTED** by
[QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md](QUADRATIC_IMAGE_EXTENSION_OBSTRUCTION.md).
Earlier universal-linear OPEN labels below are historical and superseded;
this document's stated subclass results retain their original scope.

**PROVED on paper; priority OPEN.** This is a special-family result, not
an unrestricted quadratic bound. For n=2m+1>=5, use Q={0,...,2m},
a(2i+1)=2i, a fixes evens, and b(q)=q+1 mod n. Put
E={0,2,...,2m}, F=E\{2m}, and E_r=E b^r.

## Full reachable-image family

    R={Q} union {nonempty T: T subset E_r for some 0<=r<n}.

Every word containing a has its last a-image contained in E and a suffix
b^r. Words without a leave Q unchanged. This proves the upper inclusion.
Conversely Q a=E. On E, c=b^2 a is the (m+1)-cycle advancing each even
point to the next even point, while d=ba fixes all points except 2m,
which it sends to 0. These are precisely the standard Cerny generators
on E, with actual ambient word costs 3 and 2.

To reach any nonempty T subset E, conjugates of d by powers of c merge
each chosen even point into its successor and fix the other even points.
For each consecutive block of E\T, process the points in cyclic forward
order, merging each into its still-present successor, ending at T.
Only undesired source points are changed, so every T point remains.
Starting from Q a gives a full-Q reach word. Append b^r to reach any
subset of E_r. This also proves synchronization; b itself proves SC.

Consequently for every proper X subset Q,

    rho(X)=max_r |X intersect E_r|,

while rho(Q)=n. The full-Q exception is essential. This is an exact
capacity formula, not an assumption of complete reachability of Q.

## Linear image extension for every proper reachable S

**Theorem: e(S)<=2n for every nonempty proper S in R.** Choose a
representation S=S_0 b^r, where nonempty S_0 subset E and 0<=r<n.
If S_0=E, Q a b^r=S and 1+r<=n.

Otherwise there is an adjacent boundary h outside S_0, d inside S_0
on the cycle of even points. The following actual words have images
E\{h}, with exactly one double fiber at d and all other fibers single:

* If h=2m and d=0, the word a on V=E_1 has that property, with cost 1.
* If h=2i<2m and d=2i+2, the word u=a b^(2i+2) a on V=E_1 has
  that property, with cost 2i+4<=2m+2=n+1. Indeed E_1 a=F,
  F b^(2i+2) a=E\{2i}, and the initially doubled 0 maps to d.

Set T=V intersect S_0 u^-1. Its size is |S_0|+1, because h is absent
and the doubled image d is present. Every nonempty subset of V=E_1
is reachable by the image characterization, so T is a valid larger
image. T u=S_0, hence T u b^r=S. The cost is <=n+1+r<=2n.
This controls all reachable ranks, not only the measured middle rank.
The resulting class reset bound 2n(n-1) is not an improvement on known
circular-class bounds and says nothing universal about arbitrary DFAs.

## Exact middle-rank reduction

At rank m, all images are rotations of E\{2i}; there are mn distinct
sets. Above rank m the only images are Q and the n sets E_r.
Any E_r first dropping below rank m+1 under a reaches F: direct checking
gives E_r a=E for even r and F for odd r. A transport from a larger
image into an m-set S must have such a drop before its final suffix.
Thus

    e(S)=1+D(F,S),

where D(F,S) is the shortest word taking F into a subset of S. The upper
bound chooses initial image E_1 and prepends a. The lower bound uses
the necessary rank-m+1 drop (from Q a stage as well, if starting at Q).
This includes transport ending in a proper subset of S; equality of
the transported image with S is NOT required.

## Complete finite layer evidence and open lower-bound target

An inverse powerset BFS computes every rank-m cost through n=25.
An independently implemented forward presentation (B,r), B subset E,
computes D(F,S) and agrees on all entries through n=25. It then extends
the full layer calculation through n=37. Each presentation edge is an
actual a or b action; overlapping representations preserve exact word
distance after minimizing over all target representations.

The layer maxima at n=5,7,9 are 10,12,16. At every tested odd n from
11 through 37 the maximum equals 2n-4. For n>=13 the stored peak is

    S=(E\{2m-2}) b^(n-5),
    u=a b^(n-1) a b^(n-5), |u|=2n-4,

with larger image E_1. The same target's value is also checked at n=11.
The exact arbitrary-n LOWER bound e(S)>=2n-4 and the arbitrary-n maximum
formula remain **CONJECTURED**. The displayed word proves only an upper
bound. Finite agreement does not justify an asymptotic coefficient >=2
when an additive constant is allowed. The five-state exact cost 10
already forces C>=2 for the literal e(S)<=Cn envelope without slack.

The full reachable-family and 2n extension theorems above are separately
proved. Image extension itself is the known Kisielewicz--Szykula route:
[primary manuscript, Section 3.1](https://arxiv.org/pdf/1608.01268).
No new general Cerny proof, general upper bound or Lean statement follows.
