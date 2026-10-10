# A common entrance fiber for the protected set

8 October 2026. This is auxiliary structure at equality n-|A|, for arbitrary
finite alphabets. It gives no new extremal value and is outside the
manuscript release. It generalizes SINGLETON_PREDECESSOR_FLAG.md.

## Proposition

Let a strongly connected synchronizing automaton satisfy
ac(S,A)=t=n-r, where r=|A|>=1 and g=|S|-r>=3. Then there is a nonempty
set B contained in Q minus A with |S intersect B|=1 such that, for every
letter ell and protected output a in A, the preimage ell^(-1)(a) is
either a singleton {p} with p in A, or exactly B. At least one letter
uses B. In a letter using B, exactly one protected output receives B;
the other r-1 receive distinct protected singleton predecessors, and
exactly one protected input is sent outside A. A letter not using B
permutes A and has no outside predecessor of a protected output.

For g=2 the corresponding proven description permits B and its
complement (Q minus A) minus B, each meeting S in one point, in place
of only B. At most two protected outputs can receive outside fibers
in the same letter. No assertion for g=1 is made.

Initial-set reachability is not used. If |P1|<=4, a letter using B
merges all its pairs, giving |B|<=3 in the g>=3 case.

## Proof

Put s=|S| and let V_i be the real span of characteristic trajectory rows
chi_S D_w for |w|<=i. The equality flag gives dim V_i=i+1 for
0<=i<=t-1. In particular the annihilator K of V_(t-2) has dimension
n-(t-1)=r+1. It contains the r independent columns

  h_a=s e_a-1,  a in A.

Their independence follows by inspecting a coordinate outside A and
then the coordinates in A. For each letter ell and a in A it also
contains d_(ell,a)=chi_(ell^(-1)(a))-e_a. Indeed every word w of length
at most t-2 and its extension w ell are safe. Their characteristic
image rows contain each protected state once, so multiplication by
d_(ell,a) has value zero. Safety guarantees no collision; using set
images without that fact would not justify this linear identity.

Every protected preimage C is nonempty and |S intersect C|=1. If it
contains p in A and another point q, then every image through depth
t-2 omits q, or the next letter would collide p and q. But every state
is reached from some state of S within n-s steps by strong connectivity,
and n-s<=t-2 when g>=2. Thus such a preimage is exactly {p}. Every other
protected preimage is a nonempty subset of Q minus A.

Restrict columns in K to O=Q minus A. The span of the h_a restricts to
the one-dimensional space of constant columns; hence the image of K
under restriction has dimension at most two. An outside preimage C
restricts d_(ell,a) to its Boolean indicator chi_C. Some outside
preimage B must occur: otherwise every letter permutes A, making the
proper nonempty A closed, contrary to strong connectivity. Also B is
proper in O, since |S intersect B|=1 while |S minus A|=g>=2.
Therefore the restricted space has basis 1_O,chi_B.

The only Boolean vectors in span{1_O,chi_B} are 0,1_O,chi_B and
chi_(O minus B): their values are constant separately on the two
nonempty parts B and O minus B. A protected outside preimage cannot be
empty or O, by its intersection size one. If g>=3 it also cannot be
O minus B, since that set meets S in g-1>=2 points. Thus B is the only
outside preimage. For g=2 both complementary fibers are allowed.

Distinct outputs in a deterministic letter have disjoint preimages,
so B can be used by at most one protected output (at most two outputs
for the complementary-fiber case). If B is used, all the other r-1
outputs have distinct predecessors in A. The one remaining protected
input cannot have an output in A, and is the unique input sent outside.
Without B, all r protected outputs have their distinct predecessors in
A and the restriction is a permutation. Finally binomial(|B|,2)<=|P1|
gives the stated size bound. QED.

## Controls and scope

The singleton audit completely covers all first-letter conjugacy types
paired with every labelled second letter at n=4,5,6. It checks all
relevant initial subsets, including unreachable ones, without stopping
when an extremal value is attained. At n=6 there are 6,065,280 row pairs,
2,759 singleton equality instances, including 1,025 with |S|>=4.
An independent literal-set checker reproduces the n=4 counts and checks
22 singleton frontier certificates. It verifies the g=2 counterexample
with n=4, S={0,1,3}, A={1}, rows [0,2,1,1] and [1,2,3,0]: preimages
of 1 are {2,3} and {0}, and the local value is three. S is reachable.

The general checker independently recomputes the exact value and the
annihilator restrictions on every applicable frontier certificate;
this includes 67 witnesses with g>=3 and protected sizes through seven.
These checks support the proof above and do not extrapolate a finite
classification to arbitrary alphabets or n. General search failures
using the entrance-fiber condition remain diagnostics, never uppers.

## Protected-pair isolation

For any strongly connected synchronizing automaton and any nonempty
A subsetneq S, put m=n-|S| and let d_A be the minimum shortest merging
length among pairs with at least one endpoint in A. Then

  ac(S,A)<=m+d_A.

Choose such a pair {a,q}, with a in A. A path from some input in S
reaches q in at most m steps. If that word is unsafe, the required
avoid-or-compress word is already at most m long. Otherwise its image
contains both a and q, so appending a shortest merging word compresses
it within m+d_A steps. Synchronization makes every pair distance finite.
No reachable-image assumption is used.

Consequently equality ac(S,A)=n-r forces every pair touching A to have
merging distance at least |S|-r. Thus A is isolated in P_(|S|-r-1).
The checker verifies this on all 112 applicable frontier certificates.
At (13,9,1), A is isolated in P7. A cover of P5 can therefore be selected
and enlarged to three vertices outside A; the canonical protected state
3, outside the cover {0,1,2}, alone covers all witnesses up to relabeling.
The old protected-state-0 slice is redundant, not a proved empty slice.
