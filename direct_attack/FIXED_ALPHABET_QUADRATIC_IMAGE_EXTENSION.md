# Quadratic actual-image extension with fixed ternary and binary alphabets

Date: 2026-10-01. **PROVED (paper)** for every parameter below.
Every universal linear actual-image extension bound is **REFUTED** even
for strongly connected, irreducibly synchronizing BINARY automata.
The ternary family is additionally simple. Independent finite audits are
**COMPUTATIONALLY VERIFIED**. Priority is **OPEN**; no **FORMALLY VERIFIED**
claim. The unrestricted Cerny conjecture and global policy square are **OPEN**.

The preceding fold/path obstruction has a growing alphabet. This proof
removes that limitation. Neither family is a Cerny counterexample: explicit
common reset words below satisfy the square. No unrestricted minimum-state
claim, exact reset-threshold formula, or general quadratic reset bound follows.

## The fixed ternary family and its actual image boundary

Use right actions. For p>=2 let

    Q = C union D,
    C = {C_0,...,C_(p-1)}, D = {D_0,...,D_p}, n=2p+1.

The THREE original letters are

    a: C_i -> C_(i+1 mod p), D_j -> D_(j+1 mod (p+1));
    c: swap C_0 and D_0, fix everything else;
    b: C_i -> C_i, D_j -> C_(j mod p).

Thus a,c are permutations and b is an idempotent of rank p. The two
a-cycles and their c bridge give strong connectivity. Every word containing
b has rank at most p, while every other word is a permutation. The ONLY
actual image larger than any actual p-set is Q. We use exactly the repository
definition

    e(S)=min{|u|: R is actual, |R|>|S|, and Ru is contained in S}.

Strict containment, intermediate rank drops and arbitrary words are allowed.

Put s=floor(p/2), k=p-s=ceil(p/2). Define a contiguous coordinate interval

    A={s,...,p-1} if p is even;
    A={0,...,s-1} if p is odd,

and T=b^-1(A), interpreting A as the corresponding states of C. Explicitly

    p=2s:   T={C_s,...,C_(p-1),D_s,...,D_(p-1)};
    p=2s+1: T={C_0,...,C_(s-1),D_0,...,D_(s-1),D_p}.

In either case |A|=s and |T|=p. An explicit word below reaches T EXACTLY;
therefore T is actual before the larger-image boundary is used, and

    e(T)=min{|u|: Qu is contained in T}.                 (1)

## A lower bound on the number of original a's in ANY entering word

Define a coordinate projection to Z_p by

    pi(C_i)=i, pi(D_j)=j mod p.

Letters b,c preserve pi. Letter a increases pi by one except on the
transition D_p -> D_0, which preserves zero. Call precisely that original
a transition a stall. For the trajectory of an ORIGINAL state C_i in a
word u, let d_i count its stalls and let t be the TOTAL number of a's in u.
Even after trajectories merge, each original trajectory is still defined.
Consequently

    pi(C_i u)=i+t-d_i mod p.                            (2)

Before C_i can first enter D, it must reach C_0 and use c. Its first
entry into D is D_0, so at least (-i mod p) a's precede that entry.
From D_0 at least p a's are needed to FIRST reach D_p: b,c cannot enter
D_p, and before the first visit to D_p every a advances pi by one. The
first visit requires a positive multiple of p a's, hence at least p.
The stall itself uses one more a and returns the state to D_0.
The same argument applies between ANY two stalls of this same trajectory.
Exiting D by b or c cannot shorten it. Thus

    t >= (-i mod p)+d_i(p+1).                           (3)

This counts repeated stalls on ONE original trajectory, not unrelated
stalls distributed over distinct states. It remains valid after collisions.

Let alpha be the first coordinate of A. If Qu is contained in T, (2)
belongs to A for EVERY i. Choose

    i=alpha-1-t mod p.

Before its stalls are subtracted, its final coordinate is alpha-1, at
the far end of the complementary contiguous interval. At least k=p-s
backward steps are needed to reach A, so d_i>=k. Equation (3) implies

    t >= B+(-i mod p),       B=k(p+1).                  (4)

In particular t>=B. The dependence of i on t strengthens this bound:

* If p=2s, write t=B+u. For 0<=u<=p-2, i=p-1-u, so (4) requires
  u>=u+1, impossible. The first possible u is p-1.
* If p=2s+1, for 0<=u<=s-2, i=s-1-u, and (4) requires
  u>=s+2+u, impossible. The first possible u is s-1. When s=1 the
  excluded interval is empty and this is still the same formula.

Both cases give the all-word lower bound

    #a(u)=t >= L_p=(p^2+3p-2)/2.                        (5)

No hypothesis about final rank equality, avoiding b, or an optimal
normal form was used. A reset landing at one state of T is also covered.

## Independent lower bounds on c and b, and a matching actual word

Track the p original C identities which have NOT yet visited D.
Two such identities remain distinct: every original letter is injective
on C. Only c can export one of them into D, and one c exports at most
ONE previously unexported identity. Identities already exported and later
merged with an unexported one do not change this count. At the end, at
most s unexported identities can lie in the s states T intersect C.
Therefore EVERY entering word also satisfies

    #c(u)>=p-s=k.                                      (6)

At least one b is required since a,c are permutations and T is proper.
The three independent counts (5),(6) give

    |u|>=L_p+k+1=ceil(p(p+4)/2).                        (7)

Set M=L_p-k+1 and take the single actual word

    U_p=b (ca)^(k-1) c a^M.                            (8)

After b(ca)^(k-1)c, the image is

    {C_k,...,C_(p-1)} union {D_0,...,D_(k-1)}.

For even p=2s, M=2s(s+1), hence M=0 mod p and M=s mod (p+1).
For odd p=2s+1, M=2(s+1)^2-1, hence M=s mod p and M=p mod (p+1).
The final power of a therefore sends this image EXACTLY onto T in both
cases. It has L_p actual a's, k actual c's and one actual b. This proves
T's actual reachability and attains (7), establishing the exact theorem

    e(T)=ceil(p(p+4)/2),        n=2p+1.                 (9)

At p=5, n=11 and e(T)=23>2n=22. This is the first strict 2n violation
IN THIS specified ternary family, not an unrestricted minimum-state result.
Equation (9) is n^2/8+O(n), so it violates EVERY fixed linear coefficient
and additive slack with a fixed three-letter alphabet.

## A charged square reset and the simple/irreducible boundary

On C, the actual word

    d=c a^(p+1) b

acts as C_0 -> C_0 and C_i -> C_(i+1 mod p) for i>=1. It is rooted
at C_0 with height p-1. Hence

    R_p=b d^(p-1)

resets Q to C_0 with its FULL original length

    |R_p|=1+(p+3)(p-1)=p^2+2p-2 <= (n-1)^2.           (10)

This is an upper bound, not a claimed exact reset threshold. Deleting b
leaves permutations; deleting c preserves C with a,b acting there as
permutations; deleting a preserves distinct C identities (only C_0 can
visit D_0, whose b-image is C_0). Thus every proper subalphabet is
nonsynchronizing: the ternary family is irreducibly synchronizing.

Since p,p+1 are coprime, conjugates of the single c by actual powers of a
are every cross transposition C_i <-> D_j. Their abstract group generates
S_n, so the DFA is simple. For image membership, this also implies that
every k-set, 1<=k<=p, is actual: transport an actual k-set to one with
exactly one b-kernel pair and distinct remaining b-values, apply b to
drop one rank, and transport again. Thus the complete actual family is

    {Q} union {S:1<=|S|<=p}.

Abstract group membership is used ONLY for existence of these images and
absence of nontrivial congruences. No such conjugate or inverse is charged
as a free letter in (8),(10). All length bounds use original a,b,c.

## A binary encoding preserving the actual-image predicate

Here is a general coding lemma, proved explicitly because image reachability
and larger-parent capacity must survive the alphabet reduction. Let an
original alphabet be x_0,...,x_(h-1), h>=2, and assume union_i Qx_i=Q.
This assumption holds for every strongly connected DFA with n>=2.
On Q'=Q x {0,...,h-1} use TWO original letters

    0:(q,i) -> (q,i+1 mod h);
    1:(q,i) -> (q x_i,0).

Before the first 1, the full image is Q'. That first 1 has image Q x {0}
because of the stated union condition. Every later actual image is pure,
R x {i}, where R is an original actual image. Conversely, starting with
that first 1, codes 0^j 1 realize every original x_j on a pure selector-0
image, and trailing 0's realize every selector. Thus EXACTLY

    R_binary={Q'} union {R x {i}:R original actual, 0<=i<h}.             (11)

For a proper original actual target S, every larger binary actual source
is either full Q' or a pure R x {i} with |R|>|S|. A word from a pure
source decodes its successive 1's into an actual original word Ru contained
in S. From the full source its first 1 produces Q x {0}; the remaining
decoded word must take this larger original actual source into S. Therefore

    e_binary(S x {0})>=e_original(S).                  (12)

There is also an exact weighted characterization. Pure R x {i} is an
actual source for EVERY selector i, so the first decoded letter can be
selected with one 1 and no preceding 0. After every 1 the selector is 0;
the next x_j costs exactly j+1 original binary letters. Superfluous selector
cycles and trailing 0's cannot improve entry into selector 0. Starting
from Q' cannot beat the already eligible source Q x {0}. Consequently

    e_binary(S x {0})=
      min [1+sum_(ell=2)^m(index(x_ell)+1)],             (13)

where the minimum is over ALL original actual R with |R|>|S| and ALL
nonempty original words x_1...x_m transporting R into S. This is an exact
local phase-cost identity, not a statement about the full reset history.
It also gives e_binary<=1+h(e_original-1). All parent cardinalities in
(11)--(13) are actual; mixed nonactual selector sets are never added as sources.

## Exact fixed binary quadratic obstruction

Apply this coding with

    h=3,       x_0=c, x_1=b, x_2=a,       N=3(2p+1)=6p+3,
    T'=T x {0}.

Equation (11) shows that the ONLY actual sources larger than |T'|=p
are Q' and Q x {0},Q x {1},Q x {2}. In (13) the original source is Q.
Every original prefix before the first b consists of permutations and
can be deleted: it preserves Q. The corresponding binary prefix can be
deleted by beginning instead at the already actual source Q x {1};
the first 1 then executes b at cost one. All subsequent a,c,b cost
3,1,2 respectively. Bounds (5),(6) therefore give

    e_binary(T') >= 3L_p+k+1.

Encode (8) starting from Q x {1}. Its first b costs one and its remaining
letters use c -> 1 and a -> 001, attaining exactly that bound. Hence

    e_binary(T')=3(p^2+3p-2)/2+ceil(p/2)+1
                =(3p^2+10p-4+(p mod 2))/2
                =N^2/24+O(N).                         (14)

T' is actual: from Q', first apply 10 and then this entering word.
The FULL reachability word has length e_binary(T')+2. The two-letter
word 10 alone reaches the actual larger source Q x {1}; these costs are
not silently erased from any whole reset construction.

For p=6, N=39 and exact e_binary(T')=82>78=2N. This is the first strict
2N violation IN THIS encoded family. No global binary minimum is claimed.
Every fixed C,d fails eventually in (14), even restricted to binary DFAs.

The binary DFA is SC: select original letters by 0's and 1, follow any
original state path, then rotate to the desired selector. A charged
whole reset is the first 1 followed by the encoded R_p, using codes
c -> 1, b -> 01, a -> 001. Its length is

    3+(3p+6)(p-1)=3p^2+3p-3 <= (N-1)^2.               (15)

Letter 0 is a permutation. After the first unary 1, its image is Q x {0},
and all further 1's act there by the permutation c. Neither unary alphabet
synchronizes; the binary family is irreducibly synchronizing. No simple
binary claim is made: its selector partition is a congruence.

## Relation to the open proof route and literature

[Kisielewicz--Szykula 2016, Section 3.1, Conjecture 1](https://arxiv.org/pdf/1608.01268)
uses precisely an actual image target and a preimage containing a larger
actual image. The primary definition was reread in this continuation.
The growing-alphabet family already refutes its unrestricted formulation;
(9),(14) remove the remaining fixed-alphabet and binary qualifications.
Two-cycle constructions and alphabet reductions are established ideas.
Priority of these precise families, exact costs and the explicit coding
identity remains OPEN; absence of a search hit is not a novelty proof.

The potential compatibility route must now tolerate QUADRATIC individual
phases even on binary SC irreducibly synchronizing inputs. This does not
prove a global policy square failure, and the actual reset words (10),(15)
leave the Cerny conjecture unthreatened. We do not promote this method
obstruction to a general reset theorem or stop the research objective here.

## Verification and reproducibility boundary

`two_cycle_image_obstruction.py` saves 69 controls, p2..65 and
p100,128,256,512,1024, through ternary n2049 and binary N6147.
`check_two_cycle_image_obstruction.py` imports neither that generator
nor any preceding policy solver. It reconstructs original rows, the
coordinate identity, C-injectivity/export boundary, and first-stall
distances by independent zero/one-cost BFS. It checks the small residue
inequality giving (5), evaluates the charged original word powers, and
checks both common resets and actual target words. Fifteen controls p2..16
add complete LETTER-BY-LETTER transformation evaluation. Larger powers
are evaluated from original-row compositions, with their full exponents
charged; they are not free new letters.

Ordinary-set full forward scopes p2..9 use 349520 ternary vertices;
independent full-preimage target BFS uses 89655 visited vertices. Binary
scopes p2..8 use 262135 full forward vertices and independently the same
count from ALL actual larger sources; pure/mixed image classification is
compared exactly. Five binary full-preimage target scopes p2..6 use 4896
vertices. All arriving subsets, including strict containment, participate
in these BFS minima. Seven deliberately corrupted fields/rows are rejected.

The arbitrary-parameter results follow from the proof, not extrapolation
of these finite scopes. The preceding 97-check record is preserved;
this independent check continues it as number 98. One deterministic
generator/replay raises the regeneration registry to 183 commands.
No full 98-check rerun, proof kernel, or unrestricted Cerny proof is claimed.
