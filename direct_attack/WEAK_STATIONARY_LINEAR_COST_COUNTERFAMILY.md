# A fast-reset family needing longer weak stationary support

Date: 2026-10-02. **PROVED (paper, EVERY n>=4).** General Cerny **OPEN**;
no novelty or formal-verification claim. This directly attacks the proposed
universal maximum-support-cost n bridge after SINGULAR_STATIONARY_WORD_COST.md
established cost n for the Cerny family. The same universal claim is
**REFUTED** here. This is not a lower bound on expected cost or reset cost.

On Q={0,...,n-1}, let a fix0 and cycle1,...,n-1, and let

    b(0)=1, b(n-1)=1, b(q)=0 for1<=q<=n-2.

The state graph is SC. The ORIGINAL letter b has a unique two-cycle0/1
and level1, so this is already within the proved one-cluster subclass.
Write N=n-2 and M=n-1. The ordinary reset threshold is EXACTLY n,
attained by b a^(n-2) b. Nevertheless the EXACT minimum maximum ORIGINAL
support cost for a nonnegative full-Q stationary average with positive
singular mass is

    K*=ceil(3n/2)-1.

The attaining mixture uses only singular words, and its macro-word support
itself is SC and synchronizing. Thus even a fast-reset SC one-cluster DFA
can require maximum stationary-support cost larger than n.

## Exhaustive all-word row classification and original minimum costs

Leading a's preserve [Q], so the first b gives N e0+2 e1. After a b has
occurred, a nonreset word has only two particle positions:0 and a core
point j. A subsequent b either swaps their two masses and returns their
positions to0/1, or merges them at1. The latter occurs exactly when the
intervening a-run has length n-2 modulo M. This exhausts ALL literal
words, including redundant words and leading/trailing powers.

The possible singular full-Q rows and their minimum ORIGINAL costs are:

    A_j=N e0+2 e_j,       b a^(j-1),                cost j;
    B_j=2 e0+N e_j,       b b a^(j-1),              cost j+1;
    R_j=n e_j,           b a^(n-2) b a^(j-1),      cost n+j-1;
    R_0=n e0,            b a^(n-2) b b,             cost n+1.

Here1<=j<=M. At n4 the A/B rows coincide, so their minimum cost is j;
the displayed B witness still has its charged cost j+1. No false claim
of distinct row types is made at this degeneracy. At n>4, the two mass
orientations distinguish A/B. The shortest final core phase j needs
at least j-1 trailing a's; orientation B needs at least two b's. Before
the first merge every completed b block returns the pair to0/1, so a
merge needs a FULL contiguous a-run of n-2 between two b's. Its earliest
cost is n and its endpoint is1. Getting to core j afterwards costs at
least j-1; reaching0 costs at least one more b. This proves the costs,
the ordinary threshold n, and the completeness of the row classification.

## A strict all-short-word separator

Let L=K*-1 and k=L-n+1. Reset rows attainable by cost L can only have
core endpoints j<=k, together with0 if there is enough budget. Define
H={k+1,...,M}; equivalently H={ceil(n/2),...,n-1}. Give the functional
phi the values

    phi(0)=N, phi(j)=-2 for j in H, phi(j)=0 otherwise.

Its full-Q value is N-2|H|, equal to-2 at even n and-1 at odd n. Every
singular row of ORIGINAL cost<=L has NONNEGATIVE phi value. For A_j
it is N^2 minus4 if j in H, otherwise N^2; for B_j it is0 on H and2N
off H. Available R_j off H have value0, and R_0 has value nN. Therefore

    ([Q]M_w-[Q])phi >= 2|H|-N >0

for EVERY singular word |w|<=L. Pure a words are permutations and have
deviation0. A nonnegative average with positive singular mass therefore
cannot be full-Q row stationary within L. This includes ALL redundant
short words, not just the minimum-cost representatives. It disproves the
proposed universal maximum-support bound n for every n>=4.

## Exact positive attainment, including its support lifecycle

Put k*=ceil(n/2), H*={k*+1,...,M}. All B_j in H* cost at most n, and
all R_j with1<=j<=k* cost at most n+k*-1=K*.

For even n, give each high B_j weight1/N and each low R_j weight1/n.
The high rows give mass1 to every high coordinate and mass1 to0; the
low rows give mass1 to each low coordinate. Total weight is1/2+1/2=1.

For odd n, give each high B_j weight1/N, add B_1 with weight1/(2N),
give R_1 weight1/(2n), and each R_j,2<=j<=k*, weight1/n. The additional
B_1 fills the missing1/N at0 and gives1/2 at1; R_1 supplies its other
half. The remaining coordinates are exactly1. The two weight groups
again each sum to1/2. These are exact positive rational weights.

The longest low reset R_(k*) has positive weight and cost exactly K*.
Every supported word is singular; R_1 is constant, so the support
synchronizes. From every state the low constants reach all low core
states. From1, each high B_j reaches j, including n-1. From n-1 any
high B_j reaches0. Thus the support state graph is SC as well. All
actions and costs are literal ORIGINAL words, with no free macro letters.

This boundary does NOT refute general linear bounds with a larger
constant, the two-factor averaging framework, or a general square reset
bound. Expected support cost still has infimum0 when a small positive
amount of the attaining mixture is combined with the empty word. Weak
stationarity does not by itself make its maximum support budget<=n.

The independent finite checker verifies the proposed row classification,
separator, rational weights, support SC and literal original reset
certificates. Finite checks are COMPUTATIONALLY VERIFIED; the every-n
argument above is PROVED paper and receives no FORMALLY VERIFIED label.
General Cerny and universal paid compatibility remain OPEN.

Completed independent finite scope:63 parameters n4..64,127,257;
7308 closed row vertices /14616 original-letter closure edges,6031
short singular row classes,2427 exact supported words and23497012
literal particle/letter controls. Complete closure covers ALL words
on each fixed retained family input, not all DFA inputs or all n.
Eight corruptions are rejected. Registry129/210 preserves128 old check
records verbatim and appends ONE checker; no full129 rerun. Native builds8.
