# Exact uniform permutation averaging can require quadratic word cost

Date: 2026-10-01. **PROVED (paper)**, a method obstruction with no
publication-priority or **FORMALLY VERIFIED** claim. The unrestricted
Cerny conjecture remains **OPEN**.

The single-permutation theorem has a positive averaging polynomial of
short original degree. A possible extension would use transitivity of
an arbitrary permutation group to average to J/n within original word
length n-1. This extension is **REFUTED** for all n>=6. The distinction
between group membership and original word cost is essential here.

## Exact optimal EXPECTED cost

On Q={0,...,n-1}, n>=2, take the n-1 adjacent transpositions tau_i
swapping i and i+1. They generate S_n. For a permutation word w set

    F(w)=sum_q |qw-q|.

Every letter moves exactly two original tokens by one line position.
The triangle inequality therefore gives F(w)<=2|w|. Suppose a
nonnegative probability distribution p_w on actual permutation words
has exact uniform matrix average

    sum_w p_w M_w = J/n.

Every state's final position is uniform. Consequently

    E F(w) = (1/n)sum_(q,r) |r-q| = (n^2-1)/3,
    E |w| >= (n^2-1)/6.                                (1)

This lower bound is attained. Use the uniform distribution on the
n cyclic shifts g_k(q)=q+k modulo n. The shift g_k has k(n-k)
inversions and is a product of exactly k(n-k) adjacent transpositions.
For a nonidentity row g, choose adjacent OUTPUT labels i,i+1 whose
preimages satisfy g^(-1)(i)>g^(-1)(i+1). Right multiplying by tau_i
swaps those values and decreases the inversion count by exactly one.
Repeat until identity and reverse the recorded letter indices. Since
each letter is an involution, this is an actual positive right-action
word for g of its inversion length. Their average matrix is J/n, and

    (1/n)sum_(k=0)^(n-1) k(n-k) = (n^2-1)/6.             (2)

Thus the exact minimum EXPECTED original word length of any uniform
permutation average is (n^2-1)/6. If a distribution had support entirely
on words of length at most L, its expected length would be at most L.
Hence its maximum support cost is at least ceil((n^2-1)/6). This is
strictly larger than n-1 for every n>=6, since

    (n^2-1)/6-(n-1) = (n-1)(n-5)/6.

The cyclic-shift construction supplies a quadratic maximum support cost
floor(n^2/4). No exact optimum for MAXIMUM support cost is asserted.
Nor is n6 asserted to be the minimum possible refutation of that
maximum-cost proposal; the all-n lower bound suffices.

## Synchronizing embedding and scope

Adjoin the unit letter sending n-1 to zero and fixing other states.
The base automaton is strongly connected because its permutation group
is S_n. It synchronizes: conjugating the unit by actual permutation
words gives every desired single-state collapse p->q, so one can
reduce any nonsingleton image until only one state remains.
Inverse words are reversals of adjacent-transposition words and their
costs are not removed. This is an existence argument, not a reset bound.

The obstruction (1) still applies to its PERMUTATION-only averaging
support. It makes no claim about averages that also use singular words,
one-row averages, target-dependent distributions, or other stationary
mass arguments. It does not refute a linear extension bound or the
square for this synchronizing family. In particular, a short transversal
for one state is not a simultaneous uniform average for ALL states.

This closes the proposed direct generalization of the earlier positive
cycle average. A general proof would have to exploit singular actions,
subset-dependent transport, or another compatible global mechanism.
Independent audit/check records are kept separately and must retain
the exact original-letter interpretation.
