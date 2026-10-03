# Exact binary boundary of original one-step positive balancing

Date:2026-10-02. **PROVED (paper), EVERY n>=2.** No novelty or
FORMALLY VERIFIED claim. General Cerny remains **OPEN**. This is
an exact scope audit of ORIGINAL_LETTER_DEFECT_REVERSAL.md, not an
ordinary reset-threshold search or a refutation of its square theorem.

Let the ORIGINAL binary alphabet be{f,b}, rank(f)=n-1, with b a
permutation. Write e for f's unique omitted image and d for its unique
doubled image; they are distinct. There is NO assumption on f's kernel
inputs, level, fixed points, SC or synchronization. Put D(w)=[Q]P_w-[Q].

Then positive one-step balancing

    alpha D(f)+beta_f D(f f)+beta_b D(f b)=0,
    alpha>0, beta_f>=0, beta_b>=0,

is feasible IFF

    b(e)=d and b(d)=e.

Weights may be real/rational/integer; the equivalence holds in each
case, and the sufficient certificate has alpha=beta_b=1,beta_f=0.
Thus positive weights enlarge the preceding criterion for richer or
higher-corank alphabets, but NOT for this binary rank-one/permutation
class. The permutation must literally exchange the two OUTPUT defects;
having them on the same longer cycle does not satisfy this criterion.

## Necessity by two single-state coordinates

Here c_f=[Q]+e_d-e_e, so

    D(f)(e)=-1, D(f)(d)=1.

Because f never outputs e, f f never outputs e either:

    D(f f)(e)=-1.

Let p!=q be the TWO original preimages of d under f. The column at d
of f f has mass c_f(p)+c_f(q). Only e has c_f(e)=0, while every other
state has mass at leastONE. Two distinct states cannot both be e.
Therefore

    c_(f f)(d)>=1, D(f f)(d)>=0.

Finally b is a permutation, giving

    D(f b)=e_(b(d))-e_(b(e)).

If b(d)!=e, this last vector is nonpositive at e. ALL three balanced
terms are then nonpositive at e, with the alpha D(f) term strictly
negative. No nonnegative beta weights can make the sumZERO.

If b(e)!=d, D(f b) is nonnegative at d. ALL three terms are then
nonnegative at d, with alpha D(f) strictly positive. Again their sum
cannot vanish. These are explicit single-state dual obstructions;
no linear-program numerical infeasibility claim is used.

Feasibility hence requires BOTH b(d)=e and b(e)=d. Conversely these
equalities give D(f b)=-D(f), so alpha=beta_b=1,beta_f=0 works.
This proves the equivalence for EVERY n.

The positive coefficient on the leading singular f is essential.
Permutation-only stationary distributions cannot replace it in the
negative-change repair argument. The criterion's failure still gives
NO lower bound beyond the Cerny square, and does not refute a different
compatible extension or reset policy.

## Complete finite matrix cover, independent of the generator

Relabel e=0,d=1. Every allowed f is an arbitrary map with column
counts(0,2,1,...,1), so there are n!/2 distinct f rows. There are n!
possible original permutation rows b. The independent checker validates
all rows, uniqueness and these exact combinatorial counts, then ALL
matrix pairs and their state-coordinate duals.

The complete labeled canonical scope n2..5 has7508 inputs:
2,18,288,7200 respectively. Exactly388 satisfy the criterion:
1,3,24,360 respectively. Those are precisely the earlier positive
canonical binary cover, now characterized as the ENTIRE eligible binary
class. The additional7120 have certified infeasibility, not an alleged
synchronization or threshold failure:5989 use coordinate e,1131 use d.

74420 literal composition controls check f f and f b, and eight corruptions
are rejected. The checker imports NO generator, LP routine or graph
solver. Exact finite coverage is **COMPUTATIONALLY VERIFIED**; the
arbitrary-n equivalence follows from the paper coordinate proof.
No full/general proof, new automaton counterexample, external reviewer
or FORMALLY VERIFIED all-n characterization is claimed.
