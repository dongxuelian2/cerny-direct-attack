# A charged reset construction for the published compress-with-another family

Date: 2026-10-01. **PROVED (paper)** for the explicit family below.
Finite tests are separately **COMPUTATIONALLY VERIFIED**. Priority is
**OPEN**, and no **FORMALLY VERIFIED** claim is made. The unrestricted
Cerny conjecture remains **OPEN**.

Continuation: COMPRESS_OTHER_EXACT_LOWER.md now proves the missing
LOWER bound for EVERY p>=3: mu0=4p=4n/3. Its ALL-word proof covers all
partners and the p3 endpoint exception found by independent auditing.
Older records retain their historical finite-only lower-bound flags;
the separate new proof supersedes that OPEN boundary.

COMPRESS_OTHER_SHORT_RESET.md further improves the charged all-Q upper
bound to3p^2+4p-1 for EVERY p>=3. It proves an ACTUAL pure reflection
return and descending shrinking-set reset. The matching ordinary lower
bound remains CONJECTURED; the earlier reset below remains a valid
historical certificate.

## Source and a complete transition definition

[Szykula 2026, Figure 3 and Conjecture 8](https://arxiv.org/pdf/2608.24245v1)
describes a 3k+6-state family whose synchronization and specified-state
compression threshold were left conjectural. We inspected the rendered
figure. Its displayed case table omits b(0) and some last-state matching
cases; the diagram supplies them. Our theorem uses the COMPLETE definition
given here. It never interprets an undefined case as a free transition.

Put p=k+2>=3 and n=3p. States are the integers 0,...,3p-1. Define:

* a(0)=0. For 1<=i<=2p-1, a(i)=i+1 if i is odd and i-1 if i is even.
  Also a(2p)=2p+1 and a(2p+1)=3. On 2p+2,...,3p-1, a swaps successive
  pairs starting at the EVEN index 2p+2; a leftover last point is fixed.
* For 0<=i<=2p-1, b(i)=i+1 if i is even and i-1 if i is odd.
  Also b(2p)=2. On 2p+1,...,3p-1, b swaps successive pairs starting at
  the ODD index 2p+1; a leftover last point is fixed.

This includes b(0)=1. At the final state, a fixes it when it is even
and otherwise swaps it with its predecessor; b fixes it when it is odd
and otherwise swaps it with its predecessor. Both letters have rank n-1.
All products below use right actions and count every original a/b letter.

## Two actual cyclic cores and their entering words

Let c=ba and u=ab. Direct substitution gives a c-cycle R, in this order:

    R=(0,2,4,...,2p-2,2p,1),       r=|R|=p+2.

The remaining main-line odd states 3,5,...,2p-1 move down by two under c
and enter at 1. The outer states 2p+1,...,3p-1 form a single directed
chain under c: visit their odd indices upwards, reflect at the last
state, visit their even indices downwards, then go to 3 and 1.
There are p-1 outer states, so the largest c-distance into R is p.
Since c permutes R, we have the EXACT image equality

    Q c^p = R.                                             (1)

Likewise u has cycle

    U=(0,1,3,5,...,2p-1,2),       |U|=p+2.

The other main-line evens move down by two into 2. The directed u-chain
from 2p visits the outer EVEN indices upwards, reflects at the last
state, visits their ODD indices downwards, and enters at 2. It consists
of 2p plus the p-1 outer states, so its distance into U is p. Thus

    Q u^p = U,       U a = R.                              (2)

These are literal words of lengths 2p and 2p+1, not free cycle powers.
The base state graph is strongly connected: the alternating matching
edges connect the whole main line, a reaches 2p and the outer path,
and the exceptional a/b edges return to states 3/2. No group inverse
or external circular-automaton theorem is required.

## An actual rooted return word

Label R by c-position, with positions 0,...,p+1. Thus position 0 is
state 0, positions 1,...,p-1 are states 2,4,...,2p-2, position p is
state 2p, and position p+1 is state 1. Let d=u^p a, length 2p+1.
In these coordinates its restriction to R is

    d(i)=p-i       for 0<=i<=p-1,
    d(p)=d(p+1)=p+1.                                      (3)

To check (3), state 2i for 1<=i<=p-1 reaches 2 after i-1 applications
of u, then traverses the U-cycle for the remaining p-i+1 applications;
the final a gives position p-i. The cases 0,2p,1 follow immediately
from the listed U-cycle and its outer entering chain.

Both d and c map R into R. Their actual composite v=d c d, of length
4p+4, has the particularly simple row

    v(0)=v(1)=p+1,
    v(i)=i-1       for 2<=i<=p-1,
    v(p)=v(p+1)=p.                                        (4)

This has exactly one directed cycle, the fixed point p. Every position
reaches it within p iterations, with position p-1 attaining p. Therefore

    R v^p={p},
    W=c^p v^p=(ba)^p [ (ab)^p a (ba) (ab)^p a ]^p          (5)

resets ALL Q to original state 2p. Its ORIGINAL length is

    |W|=2p+p(4p+4)=4p^2+6p
       =4k^2+22k+28=4n^2/9+2n.                           (6)

For p>=3, its square slack is

    (3p-1)^2-|W|=5p^2-12p+1
                    =5(p-3)^2+18(p-3)+10 > 0.             (7)

Thus this explicitly defined published family synchronizes for EVERY
k>=1 and has a charged reset witness strictly below Cerny's square.
This is a special-family proof, not a general n-state reset bound.
It settles the synchronization part of the diagram-completed family;
it does not by itself settle the numerical lower-threshold assertion.

## The specified-state word and the remaining lower bound

The shorter actual word

    z=c^p u^p=(ba)^p(ab)^p,       |z|=4p=4n/3,              (8)

merges states 0 and 2: c^p sends them to 2p and 1, and u^p sends both
to 2. Hence the compress-with-another threshold of state 0 is AT MOST
4n/3 for all parameters. At the initial checkpoint the matching LOWER bound was OPEN. It is
now PROVED (paper) in COMPRESS_OTHER_EXACT_LOWER.md, independently of
the older finite pair BFS.

The source displays `(ab)^p a (ab)^p` beside a length 4n/3 claim.
That displayed word literally has 4p+1 letters. It does merge state 0
with state 1, but cannot itself be a shortest word of length 4p.
Equation (8) supplies the correctly charged upper-bound witness with
a different initial partner. This is an arithmetic/word clarification,
not a refutation of the numerical threshold conjecture.

## General mechanism and limits

The reusable statement is elementary: for r>=4, if actual words c,d
preserve an actual image R and act as the cycle and row (3), then d c d is a rooted
transformation of height r-2. An entering word of length E gives

    rt <= E+(r-2)(2|d|+|c|).                               (9)

All entering, reflection and rotation costs are paid. No arbitrary
image is presumed to have such a return structure. In particular, the
earlier arbitrary-image return-synchronization obstruction is unaffected.
Producing an analogous inexpensive rooted word for GENERAL automata is
still missing; membership in their transformation semigroup does not
bound its original word cost or its root height.

This extends to every phase of a reflected adjacent unit. On positions
0,...,r-1 put c(i)=i+1 mod r, h_t(i)=t-i mod r, and let e map 0 to r-1
while fixing the other positions. Suppose d=h_t e is an ACTUAL return
word. If t>=1, direct composition gives

    d c d = (h_t e h_t) c^(-1) e,
    (h_t e h_t): t -> t+1 mod r, all other points fixed.

This equality is used only to compute the row of the ACTUAL word d c d;
it never gives an inverse or the abstract h_t at zero word cost.
The row fixes t. All other points move down by one, with 1 jumping to
r-1. Its root height is r-1 for t=1 and r-2 for 2<=t<=r-1.
For t=0 that word has a nontrivial cycle, so it must NOT be called
rooted. Instead use the actual word d'=c d, whose reflected phase is
r-1. The word d' c d' is then rooted of height r-2, with charged length
2|d|+3|c|. Thus the entering-word reset budgets are, respectively,

    E+(r-1)(2|d|+|c|)         for t=1,
    E+(r-2)(2|d|+|c|)         for 2<=t<=r-1,
    E+(r-2)(2|d|+3|c|)        for t=0.                    (10)

The public family uses t=r-2, giving (6). These conditional budgets
apply to arbitrary actual images with this specified return structure;
a congruence hypothesis is not needed. They do not assert that a general
synchronizing automaton admits such short words. Separate finite tests
include EVERY offset at r=4,...,200, including the bad-phase repair.

Generation and separate verification are in compress_other_family.py
and check_compress_other_family.py. Their scopes and retained literal
words are recorded in data/compress_other_family*.json. They do not
claim an exact whole-Q reset threshold.

Finite scopes: 69 explicit family cases, k=1,...,64 and
{100,128,256,512,1024}; 67 complete pair audits total 859431 vertices.
All 69 entering/reflection/rooted word rows, SC claims, and charged
lengths are separately recomputed. The whole expanded reset words for
k=1,...,12 charge 4652 original letters and are applied to all states.
Six deliberately corrupted certificates are rejected. For k=512/1024
the macro rows and rooted heights are checked; no full pair-distance
enumeration is claimed there. Finite q0 equality holds in the 67 pair
scopes; its arbitrary-parameter LOWER bound is now supplied by the separate
COMPRESS_OTHER_EXACT_LOWER.md continuation proof.
