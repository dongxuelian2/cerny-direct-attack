# A compatible shortest-phase chain despite binary quadratic local extension

Date: 2026-10-01. **PROVED (paper)** for the direct binary family:

    P<=p^2+p-ceil(p/2)-1 for EVERY p>=3;
    P=5 for p=2.

P is the GLOBAL best actual-image policy in IMAGE_EXTENSION_POLICY.md;
ALL phases constructed below are genuinely shortest, with their actual
parents and full original-letter costs verified. Exact arbitrary-p
equality P=p^2+p-ceil(p/2)-1 is only **CONJECTURED**. It is separately
**COMPUTATIONALLY VERIFIED** in five complete scopes p2..6. Priority
**OPEN**; no **FORMALLY VERIFIED** statement. General Cerny and the
unrestricted policy square remain **OPEN**.

This is a positive compatibility result for the binary quadratic local
obstruction, not a universal proof. It improves that family's charged
reset upper bound by one for p>=3. Its e(T)=n^2/8+O(n) theorem remains
valid: a best compatible chain need not use that particular expensive target.

## Notation and actual membership, before selecting any parent

Use the original a,b,C,D,E,pi,p,s,k from
DIRECT_BINARY_QUADRATIC_IMAGE_EXTENSION.md, with n=2p+1, s=floor(p/2),
k=ceil(p/2). On E the CHARGED words d=a^(p+1)b and f=a^p b remove
one C-tail point and one D-prefix point respectively, fixing the other part.
Define, for the ranges used below,

    B_j={C_0,...,C_(j-1),D_0,...,D_(j-1),D_p}, |B_j|=2j+1;
    H_j(t)={C_t,...,C_(t+j-1),D_t,...,D_(t+j-1)}, |H_j(t)|=2j.

The following original whole words reach them EXACTLY:

    Q b d^(s-j) f^(k-j-1) a^((j+1)(p+1)-1)=B_j,  1<=j<=k-1;
    Q b d^(s-j) f^(k-j) a^(j(p+1)+t)=H_j(t),       2<=j<=s, t=k-j.

After the two shrinking powers their image has C-tail size j and
D-prefix size j+1 or j; the two a-cycle residues give the displayed
targets. Every exponent is nonnegative in its stated range. These are
actual-membership certificates only. They are NOT charged as free
histories in the later reset construction: the later chain explicitly
transports Q into each parent and pays its own words.

## A general safe-preimage lower certificate

Let a be a permutation and b any transformation. For an arbitrary set X
write X_t=X a^(-t), meaning full preimages by t copies of the ORIGINAL a.
If

    b^-1 X_t is contained in X_t for 0<=t<L,

then EVERY inverse word with fewer than L copies of a has preimage of X
contained in X_t, where t is its total a-count. This follows inductively:
a^-1 takes a contained set into X_(t+1); monotonicity of full preimages
and the assumed containment keep every b^-1 step inside X_t.
Thus no such word can contain a larger actual image, since |X_t|=|X|.
An extending word also needs a b, as a alone preserves cardinality.
Consequently any actual-image extension costs at least L+1.
This lemma uses SET preimages, not an inverse b word. Shrinking steps,
strict arrivals, and arbitrary orders of a,b are all included.

## Exact shortest phases for the odd and even targets

For B_j with 2j+1<p, set L=p-k+j+1. Direct inspection gives

    b^-1(B_j a^(-t)) contained in B_j a^(-t), 0<=t<L.

For t<=j the paired interval wraps at zero and its needed D_p fiber
is present. For j<t<L, the sole unpaired D endpoint has coordinate
p-t+j>=k, so it is NOT a b-output. Its deletion introduces no point.
Every selected b-output has its whole fiber already present. This also
covers t=0, where B_j is already a union of full b-fibers.
The general certificate yields e(B_j)>=L+1.

At t=L, the unpaired D endpoint first reaches k-1, a selected output.
The full preimage contains the ACTUAL parent

    H_(j+1)(k-j-1),

whose cardinality 2j+2 is larger than |B_j|. The word b a^L maps this
parent into the D-only subset {D_p,D_0,...,D_(j-1)} of B_j. Hence

    e(B_j)=p-k+j+2, with parent H_(j+1)(k-j-1).         (1)

If that full preimage has an extra point, we retain the actual smaller
parent H; nonactual supersets are not substituted into the policy.

For H_j(t), t=k-j and 2j<p, its paired coordinates are positive before
t inverse a's. Every b^-1 step fixes the corresponding paired set.
At t inverse a's the pair interval begins at zero and its b-preimage
adds D_p, giving the ACTUAL B_j. The same certificate and matching
word b a^t therefore give

    e(H_j(k-j))=k-j+1, with parent B_j.                 (2)

Here too the forward arrival can be a strict D-only subset. Actual
membership, shortestness and cardinality growth are separate facts.

## The terminal p-image phase

When p=2s+1, the terminal image is B_s, the canonical target in the
direct binary proof. Its sole larger actual source is Q, and that proof
gives the exact terminal word b a^M, M=2(s+1)^2-1.

When p=2s, the terminal image is H_s(0), also of size p. Its sole
larger actual source is Q. Its projected coordinate target is {0,...,s-1}.
The first-stall proof gives at least kp+1 a's. For t=kp+u, 1<=u<s,
the complementary initial coordinate i=p-1-u is in the C-selected part;
its repeated-stall inequality requires t>=t+s+1, impossible. Thus at
least kp+s=s(p+1) a's are needed. The word b a^(s(p+1)) reaches H_s(0)
exactly, proving

    e(H_s(0))=1+s(p+1).                                (3)

Both terminal costs are genuinely shortest into-image transport; neither
designates an arbitrary reset prefix as a shortest phase.

## One compatible whole chain and its sum

For p>=3 start at singleton D_0. Its cost-one phase b has ACTUAL parent
B_1. Then alternate

    B_j -> H_(j+1)(k-j-1) -> B_(j+1),

using (1),(2), stopping the alternation as soon as cardinality p is reached.
The terminal target is H_s(0) for even p and B_s for odd p. Use (3) or
the canonical odd terminal word to reach parent Q. All arrows are inverse
policy arrows: prepend their actual forward words in REVERSE phase order.
Every word maps its entire parent inside its child. Therefore their
composition sends the single common full-Q image into D_0, even when
intermediate images are strict inside the nominal policy targets.

For odd p, each complete alternating pair costs p+2; there are s-1 such
pairs, a seed cost one, and terminal cost 2(s+1)^2. For even p, there
are s-2 complete pairs of cost p+2, one final odd phase of cost p+1,
the seed, and terminal cost 1+s(p+1). Both sums are exactly

    p^2+p-k-1 < (2p)^2=(n-1)^2.                        (4)

The even sum is used only for s>=2. At p2 use actual pair {C_0,D_0}
as the cost-one b parent of D_0, then the shortest whole-Q phase baaa
of cost four. Direct evaluation of all words through length three
excludes earlier entry to that pair. The common policy word baaa b
costs five, agreeing with its exact reset threshold.

Equation (4) proves P at most this compatible cost for every p>=3.
It does NOT prove that no different chain costs less. The arbitrary-p
equality suggested by the finite values remains CONJECTURED.

## Independent verification and boundary

`check_direct_binary_policy_chain.py` imports no generator, previous
checker, native solver or policy algorithm. It uses only the 69 retained
parameter values, reconstructs all original rows, and proves membership
by original-row composition with FULL charged exponents. Across these
controls through n2049 it verifies 4027 whole actual-image membership
words and 743444 safe-preimage containment/fixing controls. Every proposed
parent word is checked, and the ENTIRE common image chain is composed
without resetting to its nominal target at intermediate phases.
Twenty-three controls p2..24 additionally evaluate every original letter
of the complete concatenated reset literally.

Five complete actual-image scopes p2..6 (1147 images) have independently
computed per-target ordinary full-preimage BFS, collecting ALL shortest
larger-parent ties and solving G by descending cardinality. They visit
22746 inverse vertices and give P=5,9,17,26,38, respectively, matching
the upper construction. At p5,rt25<P26; at p6,rt36<P38. Thus even this
binary obstruction's shortest-image policy is not asserted equal to rt.
Four deliberately corrupted chain fields are rejected.

The new result is continued check 100, with the 184 regeneration commands
unchanged. The 99-check checkpoint is preserved verbatim; only this new
literal checker is continued. No full 100-check rerun, formal proof
kernel, general policy-square theorem or complete Cerny proof is claimed.
