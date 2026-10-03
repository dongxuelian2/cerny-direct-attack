# A shorter original reset and an actual reflection return

Date: 2026-10-01. **PROVED (paper), EVERY p>=3** for the completed
Figure3 rows, n=3p. General Cerny and publication priority **OPEN**.
Exact ordinary threshold below is **CONJECTURED**, not proved or formal.

The older reset bound4p^2+6p improves to

    rt(A_p)<=3p^2+4p-1=n^2/3+4n/3-1.                      (1)

This is a fully charged original word. The all-p specified-state threshold
mu0=4p from COMPRESS_OTHER_EXACT_LOWER.md is unchanged.

## An actual pure reflection on the cyclic image

Use c=ba, u=ab and the cyclic image

    R=(0,2,4,...,2p,1), r=p+2, Q c^p=R.

Positions of R are0..p+1. On R, c is the forward cycle. For every j>=p,
the ACTUAL return d_j=a c^j has row

    d_j(i)=j-i mod r,               0<=i<=p-1;
    d_j(p)=d_j(p+1)=j+1 mod r.                            (2)

State2i reaches odd2i-1 after a, then reaches1 after i-1 applications
of c. The outer state a(2p)=2p+1 reaches1 after p applications of c.
The endpoints0 and1 give the other cases directly. This proves (2)
without treating a cycle inverse as an original word.

There is also an ACTUAL pure reflection, overlooked by the previous
rooted-return construction:

    h_j=a^3 c^j,       j>=p-2;
    h_j(i)=j-i mod r,  EVERY 0<=i<=p+1.                  (3)

Indeed a^3 sends2p to4 instead of the outer path, while its action on
the other R points equals a. The longest remaining odd-state c-height
is p-2. At position p the output is j+2 mod r, which equals j-p mod r;
the other positions give (2)'s ordinary reflection rule. Thus
h_(p-2), of ORIGINAL length2p-1, is an involutive permutation of R.
It is an actual return word even though a itself is singular on Q.
This does not give a free reflection or inverse on an arbitrary image.

## Preparing the shrinking interval

After the original prefix

    F_p=c^p u^(p-1) a^4 c^(p-2),       |F_p|=6p-2,

the exact R-position image is

    S_(p-2)={0,...,p-2} union {p,p+1}.                   (4)

Here is the full original-row calculation. The image of R under u^(p-1)
is {0,1,3,...,2p-1,2p+1}: the main even points descend to the u-cycle,
while2p ends at the last outer point of its u-chain. The two exceptional
points2p-1 and2p+1 both go to4 under a^4. All remaining points are fixed
by a^4. The image is therefore {0,1,3,...,2p-3,4}. Finally c^(p-2)
carries this set exactly to (4): its positions are0..p-2 together with
p and p+1. The calculation includes p3, where the odd-state list has
only3 and the interval endpoint p-4 is absent.

## Each paid return removes one interval point

For t>=0 put S_t={0,...,t} union {p,p+1}, and set S_(-1)={p,p+1}.
Equation (2) gives, for EVERY 0<=t<=p-2,

    S_t d_(p+t)=S_(t-1).                                  (5)

For t>=2, the reflected interval p,...,p+t reduces modulo p+2 to
{p,p+1} union {0,...,t-2}; the merged pair goes to t-1. At t1 its
two interval points go to p+1/p and the pair goes to0. At t0 the point0
goes to p and the pair goes to p+1. These check both terminal cases.

Thus use original returns in the descending order j=2p-2,...,p.
They leave exactly {p,p+1}, meaning original states{2p,1}. The literal
word u^p then sends both to2, as already proved in the earlier note.
An all-Q reset is consequently

    W_p=c^p u^(p-1) a^4 c^(p-2)
          [ product_(j=2p-2 down to p) (a c^j) ] u^p.     (6)

Its letter count is

    (6p-2) + sum_(j=p)^(2p-2)(2j+1) + 2p
      = (6p-2)+(3p-1)(p-1)+2p=3p^2+4p-1.

For p>=3 its square slack is

    (3p-1)^2-(3p^2+4p-1)=6p^2-10p+2>0.

This improves the earlier genuine quadratic special-family result;
it does not give an unrestricted reset bound. Equations (2)--(5) also
give a conditional shrinking-return lemma on ANY actual image R with
the same stated rows, preparation and final merging word. Their ORIGINAL
costs must all be paid, and the action hypotheses must all be proved.

## Exactness remains a separate lower-bound problem

Ordinary complete subset computations in small parameters suggest

    rt(A_p)=3p^2+4p-1 for EVERY p>=3.                      (7)

This is **CONJECTURED**. The specified-state4p pair-entry proof does NOT
prove (7); first merging0 is much cheaper than resetting ALL Q. Nor does
matching the observed shortest word pattern give a global lower potential.
There is no claim that every shortest word has form (6), or that all
current images are the sets (4)--(5). A proof would need to control every
alternative original word, not just the displayed shrinking program.

The independent checker reconstructs the original rows and pays the
preparation on every state. It verifies the original base return a c^p,
then every further return by original ba steps, separately verifies the
pure reflection a^3 c^(p-2), and checks every shrinking-set equality.
Small expanded words and independent full forward/reverse subset
computations corroborate (7) only in their finite scopes. The proof of
(1)--(6) is paper only; the earlier abstract Lean theorem is a lower
certificate and does not formalize this reset construction.

Completed finite scope:67 parameters p3..64 and100/128/256/512/1024,
n through3072,35850770 original macro state/letter controls and867768
expanded reset state/letter controls. The5 COMPLETE small subset graphs
have16011 vertices and32022 edges; their exact ordinary thresholds are
38/63/94/131/174 atp3/4/5/6/7. Ten corruption rejections are recorded.
Registry117/200 archives116 verbatim and appends this deterministic
generator/replay and independent checker; not a full117-check rerun.
