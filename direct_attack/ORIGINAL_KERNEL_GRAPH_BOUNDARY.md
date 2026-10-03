# Forward kernel congruence and terminal merge graphs have different boundaries

Date: 2026-10-01. **PROVED (paper)** for the general forward-closure
lemma and all-n counterfamily. The separate n6 terminal witness is
**COMPUTATIONALLY VERIFIED**. Priority and general Cerny **OPEN**.
No **FORMALLY VERIFIED** claim or unrestricted reset bound.

## A general short forward-congruence certificate

Let E_0 contain all unordered ORIGINAL letter-kernel pairs. Let E_j
contain their noncollapsed forward images under ORIGINAL words of
length at most j; retain the earlier edges. Let Pi_j be its component
partition. These are NOT the pairs merged by short words.

For ANY DFA, if Pi_j=Pi_(j+1), every letter maps each Pi_j-class INTO
one Pi_j-class. Indeed an E_j path maps to a path of E_(j+1) edges
with some edges possibly collapsed. Thus Pi_j is a congruence, and
all further forward edges stay in its classes. Stagnation is permanent.
The final partition theta is EXACTLY the smallest original congruence
containing all letter kernels: each such congruence contains every
forward edge, and the stabilized partition is itself a congruence.

If Pi_0 has c_0 classes and theta has t, define D=c_0-t. Its first
stabilized partition occurs at depth at most D, since every preceding
layer strictly reduces the number of components. Select a spanning
forest of E_0 and extend it at each strictly growing layer. If layer j
joins m_j components, choose m_j new edges with image-word length<=j.
Since every preceding layer joins at least one component and
sum m_j=D, the total IMAGE-WORD cost is at most D(D+1)/2. Initial kernel
edges have image-word cost zero. This is a forest certificate, NOT a
reset word and NOT a collection of short merging words.

The depth and cost are sharp. In C_n, take a full n-cycle and the unit
0->1. Through depth j<=n-2 the forward kernel graph has successive
cycle edges {0,1},...,{j,j+1}; the unit adds no other joining edge.
Exactly one joining edge appears per layer. Its depth is n-2 and the
minimum forest image-word cost is (n-2)(n-1)/2. Every original letter
is counted in an edge label; virtual inverses are not used.

## Connectivity is NOT necessary for synchronization, even SC corank-one

For every n>=3 use ORIGINAL letters

    a(q)=q+1 for q<n-1,       a(n-1)=n-1;
    b(q)=q+1 for q<n-2,       b(n-2)=b(n-1)=0.

Both have rank n-1 and the SAME sole kernel pair {n-2,n-1}. Every
nonempty original word collapses this pair, so its forward graph
contains only that initial edge at ALL depths. Its n-1 components are
singletons0,...,n-3 and {n-2,n-1}.

Nevertheless a^(n-1) resets. Corank saturation gives rt>=n-1, hence
rt=n-1 EXACTLY. Strong connectivity follows from b's cycle0,...,n-2
and the a-edge n-2->n-1 followed by b back to0. In fact the ONLY shortest
labeled words are a^(n-1) and a^(n-2)b: any b before the last step
leaves an image without n-1, so the following letter cannot decrease
rank with the common kernel pair. All preceding letters must be a.

Here theta is a genuine congruence, but its quotient a is singular:
the predecessor singleton and the last class both map to the last
class. Containment of original kernels in a congruence does NOT imply
permutational quotient actions. Unequal class sizes allow distinct
classes to map disjointly INTO one class. This explains why replacing
the virtual NORMAL graph of PERMUTATION_COMPLETION_BOUNDARY.md by this
original forward graph invalidates the necessary synchronization proof.

The corresponding tempting linear argument fails for the same reason.
With f=(1,2,2), W=span(e_1-e_2) is invariant and contains ker(M_f).
Yet e_0-e_1 lies outside W and maps INTO W, so the induced action on
Q^3/W is noninjective. Kernel containment does not give an invertible
quotient. The earlier observability theorem uses trivial kernel
INTERSECTION and injectivity ON its invariant space; that proof is
unaffected.

## A smaller terminal-graph witness beyond n steps

The graph F_L of pairs MERGED by original words of length<=L is a
different graph. TERMINAL_KERNEL_COMPONENT_STAGNATION.md already
refutes permanent stagnation and the cutoff n-1. Furthermore the
retained Figure3 family has finite n9 witnesses with a specified state
requiring12 steps, which already rules out a universal cutoff n.
The present independently found n6 example makes this failure smaller:

    a=(2,3,4,1,0,5),         b=(0,5,3,2,3,1).

It is binary SC, with ranks6 and5. In pair order01,02,03,04,05,12,13,
14,15,23,24,25,34,35,45 the exact merge distances are

    6,2,3,3,7,7,10,4,9,5,1,9,6,8,8.

Through length6 state5 is isolated; the other five states form one
component. F_7 is connected. Its exact state5 compress-with-another
threshold and graph connectivity threshold are both7>n. Full subset
BFS independently gives its reset threshold and original reset word
in the certificate; its exact threshold is19, below the square25. No all-n
terminal lower bound or arbitrary-alphabet state minimum is claimed.

## Verification and continued research

The generator covers all labeled binary maps at n2..4, with every
forward partition/depth/forest cost streamed into a semantic hash.
The checker uses repeated FULL-class-image partition joins, rather
than forward-edge propagation, and independently reconstructs the
minimum-depth forest. The chain counterfamilies are checked through
n4096, including literal a powers on small scopes and all shortest
words on very small scopes. For the n6 terminal witness the checker
enumerates EVERY original word through length10, reconstructs all
pair distances and component layers, and performs ordinary set BFS.
The report verifies66281 complete binary inputs,45 chain parameters
throughn4096,1558 literal reset letters and252 small-chain words. The
n6 checker uses2046 literal words and56 full-image vertices. Twelve
corruptions are rejected. Registry113/197 preserves112 and appends only
this generator/replay/checker, not a full113 rerun. These scopes do not supply a universal
quadratic proof.

The continued literature attack inspected [Volkov2023](https://arxiv.org/pdf/2306.13317)'s known primitive
defect-one synchronizability theorem and two 2026 preprints:
[Miccinesi's extension certificates](https://arxiv.org/pdf/2609.21603)
and [one-cluster annular descent](https://arxiv.org/pdf/2607.19675).
Neither was treated as an unrestricted Cerny proof. A seeded exploratory
attack of the latter's binary annular membership relation found no
counterexample in205813 samples/301750 controls (n4..12, binary, tested
filtration indices1..4 and skipped once the preceding cycle space was
full), with exact rational
rechecking specified for candidate failures. This is a negative finite
search in ignored native_build, NOT an independent universal proof,
novel theorem, or new registered check. Its limitation is that distinct
cycle eigenspaces and multiple control letters need separate treatment.
