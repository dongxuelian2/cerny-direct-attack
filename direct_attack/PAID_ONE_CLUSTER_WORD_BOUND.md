# One-cluster words with original costs and a failed universal bridge

Date: 2026-10-02. **PROVED (paper, derived conditional bound).** General
Cerny **OPEN**. No novelty or formal verification is claimed. The proof
uses the reconstructed annular mechanism of
[Zhu2026, Sections3..8](https://arxiv.org/pdf/2607.19675v1), documented in
ONE_CLUSTER_UPPER_PROOF_AUDIT.md. One-cluster WORDS and their paid costs
already occur in [Kisielewicz--Kowalski--Szykula2016, Theorem2](https://arxiv.org/pdf/1607.04025).
The formula below is a direct cost refinement of the reconstructed
mechanism, not a claim to have originated the weighted-word approach.

Let A be ANY synchronizing n-state DFA over its ORIGINAL alphabet Sigma.
Let v be a nonempty actual Sigma-word of length s. Suppose its functional
graph has a unique cycle C of size m and level ell, and put t=n-m. All
original letters remain available with cost1. Add a macro T=v with cost s;
it is not a new cost-one letter. At m1, the elementary bound is s*ell.
For m>=2 put

    h=ceil(t/ell) if ell>0, and h=0 if ell=0,
    E=1+s*(m-1)+max_(0<=r<=n-2){s*min(t,ell*r)-(s-1)*r}
     =s*(n-1)+1-(s-1)*h,
    B=t+1+m*s*ell+(m-2)*E
     =s*((m-1)*(n-1)+m*ell)-(s-1)*(n-1+(m-2)*h).

Then every nonempty proper S in C extends relatively by w v^ell with
ORIGINAL |w|<=E, and ONE actual reset has ORIGINAL length<=B. The
distinguished-word cost is paid every time it occurs, including both
initialization and entry. The case ell0 necessarily has t0,m=n and gives
B=(n-1)+s*(n-1)*(n-2). At s1 this recovers the square/subclass bound.

## Paid annular proof

Keep the fixed-seed spaces L_r/M_r and the annular sum from the preceding
audit, but let EVERY original letter be a control. This includes letters
used inside v and may include a transformation equal to T. Redundancy is
harmless. Crucially, the control alphabet Sigma itself synchronizes.
The algebra depends on T's transformation, not on the macro's cost.

At order r1..n-2 put kappa=min(t,ell*r). An annular term with a prepended
seed has r+1 unit-cost controls and at most m+kappa-r-1 macro occurrences,
excluding the common terminal v^ell. Its ORIGINAL prefix cost is at most

    r+1+s*(m+kappa-r-1)
      =1+s*(m-1)+s*kappa-(s-1)*r <= E.

At r0 the m cycle shifts have prefix costs<=1+s*(m-1)<=E. Thus assuming
no extending original prefix through cost E makes every annular pairing
nonpositive. Fixed-seed descent and the old-space induction force them
all to vanish. The same generating families remain complete; a label
with r controls has macro-exponent total<=Dplus-1. Padding by a cycle
period puts it in the annulus without changing its R-row. Its padded
prefix is one of the costed terms above. Stabilization at r=n-2 and
leftmost-control deletion give the same contradiction with an ORIGINAL
reset. No polynomial projection is used as a free or positive word.

For ell0 there is no nilpotent space. The nontrivial eigenlines are simple
and exclude1. Here kappa=0, and Dplus=m-r-1 for r1..n-2. Repeated
eigenvalues remove controls; for distinct eigenvalues the numerator has
degree m-r-2, one below Dplus, so the annular coefficient vanishes. The
generating bounds reduce to d_r-1; the same induction and stabilization
work. This supplies the stated circular macro-cost refinement directly.

For ell>0, ell<=t and m>=2 imply ceil(t/ell)<=t<=n-2. Writing t=ell*j+k,
0<=k<ell, the maximum defining E occurs at r=j if k0, and at r=j+1 if
k>0: the slope before saturation is s*(ell-1)+1>0; at the final partial
step its increment is s*(k-1)+1>0; after saturation the slope is1-s<=0.
Thus the displayed closed form is exact for this worst-layer budget.

Initialization uses the ORIGINAL Sigma span chain, not a weighted macro
chain. Centered columns T^ell(chi_q-Q/m), q in C, have dimension m-1 and
sum0. Since Sigma alone synchronizes, their left orbit escapes ker[C]
within t+1 ORIGINAL letters. Some q then has positive relative pairing,
giving an initial factor costing<=t+1+s*ell and covering at least two
cycle states. At most m-2 extensions cost E+s*ell each. Prepending
v^ell costs another s*ell and sends Q into C. Hence the same reset costs
t+1+m*s*ell+(m-2)*E, exactly B. Every factor is compatible and literal.

This theorem does NOT apply with unit initialization cost to an arbitrary
weighted alphabet whose only synchronizing generator has cost s. Its
assumption is that the original Sigma alphabet has unit costs and already
synchronizes; the macro is an actual word in that alphabet.

## Useful necessary conditions and the bridge obstruction

At m2 the bound simplifies to (n-1)+2s*ell. Since ell<=n-2, ANY sync
DFA with such a word of length s<=floor((n-1)/2) satisfies the square.
In particular a two-letter ORIGINAL word with a unique two-cycle excludes
a Cerny counterexample at EVERY n>=5. Rooted words of length<=n-1 also
exclude a counterexample by their fully paid power. These conditions
concern WORDS, with costs retained, and can exclude inputs whose individual
original letters all have multiple cycles. They are not universal claims.

The proposed bridge was: every SC sync DFA has a NONCONSTANT one-cluster
word for which its B formula (or s*ell at m1) is within the square.
It is **REFUTED**, even outside the trivial fast-reset cases:

    n5: a=[0,0,1,3,4], b=[3,1,3,4,2], rt=13 < square16.
    n4: a=[0,2,1,1],   b=[2,1,3,0],   rt=8  < square9.

Both graphs are SC and both original letters have multiple functional
cycles. ALL511 literal words through length8 at n5, and ALL31 through
length4 at n4, fail the proposed NONCONSTANT budget certificate. These
finite enumerations suffice for ALL lengths: every eligible rooted row
has ell>=2, hence s*ell>=2s; for m>=2, B has the form C0+s*D with C0>=0
and D=(m-2)*(n-1-h)+m*ell>=2. The circular case has D=(n-1)*(n-2)>=2
in these n4/n5 inputs. Thus any eligible longer word exceeds the square.
The best short n5 formula is18, attained by v=a a b a b a a with m2,
ell1,s7; at n4 the best is11, attained by v=a b with m2,ell2,s2.
Actual reset words remain below the square; no Cerny counterexample results.

The obstruction refutes ONLY this worst-case FORMULA bridge. Better
initialization, original compression of C, or other compatible factors
can be cheaper. Indeed the finite checker constructs an actual reset on
each retained input; its exact cost need not equal B. Allowing a constant
reset word as the selected macro makes the bridge tautological and is
explicitly excluded from the refuted proposition. One-cluster word
methods as a whole are not refuted.

The new generator/checker retain original-word macros, all proper cycle
extension certificates, initialization and common literal resets. Their
verification is finite **COMPUTATIONALLY VERIFIED**, not an all-parameter
computational or formal proof. The counterexample enumerations are
independently checked and threshold minimality is verified by full subset
distances. General Cerny and a universal cheap compatible structure remain
**OPEN**; the goal continues after saving this conditional result.

Completed finite scope:293 original-word macro cases,5758 complete proper
cycle-subset extensions,5713 macro state/letter controls,283495 literal
state/letter controls and542 complete obstruction words.166 formula
cases fit the square;15 cases have multicycle EVERY original letter.
Eight deliberate corruptions are rejected. Registry128/209 preserves
127 earlier check records verbatim and appends ONE checker; it is not
a full128 rerun. Native builds remain8. The 293 controls include circular
and rooted boundaries, non-SC inputs and a seven-letter composite macro.
