# Hyperplane support and actual-letter guards of a full history

Date: 2026-10-02. **PROVED (paper)**, with explicitly conditional
consequences below. General Cerny and the unrestricted ALL/SOME shortest
history cost/rank assertions remain **OPEN**. No novelty or formal proof
is claimed. These are refinements of FULL_HISTORY_BOOLEAN_CAPACITY.md;
they count actual full histories and never assume their spans invariant.

Let w be ANY globally shortest reset, L its length, and W the real span
of ALL its singleton inverse suffix indicators, including the initial
singleton and Q. Write d=dim W and c=number of singleton vectors in W.
The earlier proof gives L<=|W intersect {0,1}^n|-c-1.

## A codimension-one refinement

Suppose d=n-1. Write W=ker alpha, alpha nonzero. Since W contains Q,
sum alpha_i=0; since it contains a singleton, some alpha_i=0.
Moreover its Boolean vertices span W, by the definition of the history.
Let s be the number of nonzero alpha_i. The singleton count is EXACTLY
c=n-s. Support one is impossible. Support two gives alpha proportional
to e_i-e_j, hence a partition space with one double block.

Support three cannot occur: its only zero-sum Boolean patterns on those
three coordinates are 000 and111. Their span has dimension one, whereas
the restriction of ker alpha has dimension two.

At support four, every proper nonempty zero-sum subset is a pair and
its complementary pair is also zero-sum. With at most one such pair
partition, the Boolean span has dimension at most two on the support,
too small for the required dimension three. Two distinct pair partitions
force alpha proportional, up to coordinate order, to (1,1,-1,-1).
Indeed their two perfect matchings form a four-cycle, and opposing
coefficients along each edge force equal absolute values. Conversely
this normal has six Boolean support patterns spanning its hyperplane.
Thus in this case

    |V(W)|=6*2^(n-4), c=n-4,
    L<=3*2^(d-2)-d+2.                                  (1)

At s>=5, flip the bits at negative coordinates. Zero-sum support
patterns become subsets of s POSITIVE weights with one fixed sum.
They form an antichain. The standard Sperner chain-count proof gives
at most binom(s,floor(s/2)) such subsets: a subset of size k belongs
to k!(s-k)! permutation chains; an antichain meets each chain at most
once. The middle-layer density is at most5/16 for every s>=5.
For completeness, the densities at5/6 equal5/16; the density at an
odd successor2k+1 is (2k+1)/(2k+2) times that at2k, and at2k+2 it
stays equal to the preceding odd density. Consequently

    |V(W)|<=5*2^(d-3), L<=5*2^(d-3)-2.                 (2)

For d>=4, (1) is the larger bound: their difference is
2^(d-3)-d+4>0. A nonpartition codimension-one history therefore has
L<=3*2^(d-2)-d+2. This is a SPACE/counting bound, not an assertion
that a DFA realizes the extremal count.

In the first unsupported proper-rank case n6/d5 it gives L<=21,
instead of22. More sharply, either the normal is (1,1,-1,-1,0,0)
up to scaling/order, or L<=14. The latter case has support five,
since a singleton rules out support six. At sign split1/4 there
are only empty/full patterns. At split2/3, let a,b be the two
positive weights. With three negative absolute weights summing a+b,
let T count their subsets summing a. Complementation counts equally
many subsets summing b. There are2+2T zero-sum patterns, and T<=3
by the same three-element antichain bound. Thus V has at most16
vertices, c=1, and L<=14. Equality L21 in the balanced case would
require visiting EVERY Boolean vertex except zero and the unused
free singleton. Its realizability is still **OPEN** here.

## Necessary guards from letters that do not preserve a partition span

Now suppose W is the partition space on d blocks, c of them singletons.
For every original letter a that does NOT preserve W, choose states
p_a,q_a in one source block whose images land in DIFFERENT destination
blocks U_a,V_a. Such witnesses exist exactly when a fails to preserve
the partition space under inverse images.

If S is a union of blocks and a^(-1)S is again a union of blocks, its
destination-block bits MUST satisfy x_(U_a)=x_(V_a): the two source
states must have identical membership in a^(-1)S. These equations
are necessary guards, not sufficient conditions or free transitions.

Assume EVERY letter fails to preserve W. Build the undirected graph H
on the d blocks with one chosen edge U_a V_a per letter. At each
nonterminal history vertex, the next actual letter has its guard
satisfied. Q also satisfies every guard. Thus ALL history vertices
belong to the Boolean cube minus the proper two-colorings of H.

If H is bipartite with k connected components, including isolated
vertices, it has exactly2^k proper two-colorings. Let t be the number
of singleton blocks whose one-hot Boolean vectors are such colorings.
The allowed union has2^d-2^k vertices and c-t singleton vectors.
Excluding zero and every singleton other than the start proves

    L <= 2^d-2^k-c+t-1.                                (3)

The initial singleton is allowed because an actual next letter exists;
this also handles c-t explicitly. If H is not bipartite, this argument
reduces to the earlier partition bound; it gives no further saving.
The graph contains NO loops, since destination blocks differ.

For a binary alphabet, if both letters fail to preserve W, the graph
is bipartite. Equal guard edges give k=d-1 and t<=2, so
L<=2^(d-1)-c+1. Distinct edges give k=d-2 and t<=1, so

    L <= 3*2^(d-2)-c.                                  (4)

Disjoint guard edges have t=0 and save one further step. At n6/d5,
the partition has c4 singleton blocks. Hence (4) gives L<=20;
equal edges give L<=13. Therefore ANY binary n6/d5 partition-history
counter to L<=20 must have at least ONE original letter preserving
that partition space. This does NOT show that the other letter does,
or that the partition is a congruence.

For arbitrary alphabets, odd guard cycles can eliminate the counting
saving. No arbitrary-alphabet extension of (4) is asserted.

## Conditional quotient consequence, with the final route paid

If EVERY letter preserves a proper partition history space, its blocks
form a genuine d-state quotient. The reset endpoint q lies in a
singleton block. A shortest quotient reset has length rt(quotient);
from its endpoint block there is a route to {q} of length at most d-1,
because the original word w proves reachability. Lifting the reset
and then this route resets the original DFA. Thus unconditionally

    rt(original)<=rt(quotient)+d-1.                    (5)

IF Cerny holds for that smaller quotient, (5) gives
L<=d(d-1)<=(n-1)(d-1), since d<n. The condition is explicit; this is
not a proof of smaller-state Cerny within this note. It does not cover
the one-preserving/one-nonpreserving binary case left by (4).

## Verification and remaining attack

Checkpoint124 update: the formerly EXPLORATORY n6 covering prefilter
has now been independently replayed on ALL distinct-row binary inputs,
including NON-SC cases. ALL first-map conjugation orbits are checked.
Together with the37-case integer-minor audit, the cost/rank inequality
is COMPUTATIONALLY VERIFIED for ALL synchronizing n6 DFAs over at most
two letters and ANY shortest reset. The initial per-case account below
records checkpoint122; BALANCED_HISTORY_SATURATION_RIGIDITY.md gives
the complete upgrade. New fixed-row n7/n8 and third-letter n6 pressure
remains separately EXPLORATORY. The general mathematical gaps remain.

The independent controls enumerate integer-normal hyperplane vertices,
check exact real ranks, exhaust guard graphs on up to six blocks, and
check the integer middle-layer/length comparisons. They verify the
recorded finite data, not an unrestricted DFA census or a formal proof.
There are142 integer normals (74 Boolean-spanning hyperplanes),6004
normal-model vertices,11 balanced models/24564 vertices,33861 nonempty
graphs,2096696 admissible singleton profiles,1830 density comparisons
and61 length comparisons. Eight corruptions are rejected.

A NEW proper-history query on the previous binary n6 covering universe
retains all423 covering records with rt>=21, belonging to37 state/
alphabet isomorphism classes. Its reset-count totals match the previous
census; those totals are NOT recounted as new research evidence. The
new ALL-shortest subspace search excludes rank<=5 in all37 classes,
already within the first few inverse steps. The complete prefilter
and class-completeness claim remain **EXPLORATORY**. A separate independent
checker DOES verify ALL shortest histories of EACH of the37 retained
cases. It computes all forward Q-images, then distances into every target
subset; these are independent of the inverse-BFS implementation. Every
optimal inverse prefix branch terminates at a nonzero exact integer
six-by-six minor, at depth at most6. There are4736 literal subset/letter
controls,2037 forward image vertices,205 prefix nodes,168 prefix edges
and43 full-rank minor certificates. Three corruptions are rejected.
This finite37-case statement is **COMPUTATIONALLY VERIFIED**; it does
not by itself verify that the covering prefilter missed no other class.

The mathematical gaps are now more explicit: the balanced n6/d5
nonpartition saturation, the partition case with one preserving letter,
odd guard cycles for larger alphabets, and all higher-rank ranges.
Invariance of a whole orbit span remains different from membership
of the vectors in a SINGLE shortest history. No new general square
bound follows from this note.
