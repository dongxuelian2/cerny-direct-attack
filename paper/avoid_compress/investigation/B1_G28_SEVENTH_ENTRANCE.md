# Seventh entrance in E6/F7/G28, with pair-output capacity

9 October 2026. Conditional at n=13, |S|=9, ac(S,{3})=12,
B0/C14/D5/E6/F7/G28. The seventh geometry and four crossed-fiber
exclusions below hold for every finite alphabet. The H19 exclusion
is binary only. No extremal F value follows from this reduction.

## Fresh seventh and exact Boolean space

Put A={3}, B={0}, C={1,4}, D={5}, E={6}, F={7}, G={2,8},
K={1,2}, O=Q minus A. B1_SIXTH_ENTRANCE.md and its literal inventory
give pre(F) in {A,B,C,D,E,F,G}, with no additional companion in this
geometry. The earlier preimage descriptions are similarly common.

Every actual image through five meets G once, and each preimage R
of G meets every actual image through four once. All these images
are collision-free nine-sets. A preimage containing3 equals A:
otherwise a different point in it is absent from all such images,
contradicting strong connectivity reaching every state from S within
four letters. The same argument makes distinct one-count fibers
incomparable. If all pre(G) were known fibers, their nonempty proper
nine-state union would be backward closed. Thus a fresh H exists.

The annihilator of V4 has dimension8 and restricts injectively to O.
Its restriction contains 1_O and the seven one-count fibers B,C,D,E,F,G,H.
The first seven columns (before H) are independent: the known six
fibers are disjoint, and their remainder has two S points. A Boolean
one-count column in this seven-column span must have constant coefficient
zero and exactly one private coefficient equal to one, hence be known.
Fresh H is independent and completes the eight-column basis. Every
outside pre(G) is a Boolean one-count column in this span; the one-count
condition on coefficients is 8*c0+sum(c_i)=1.

Some original letter maps G to the singleton F. Therefore each pre(G)
is a merging clique within TWO letters, not necessarily an immediate
kernel clique. K covering P5 implies |H minus K|<=1 and |H|<=3.
The target capacity of pre(G) is2, and the remaining output field is
{9,10,11,12}, of capacity4. Neither individual state2 nor8 is declared
mandatory just from one-count on G.

## All seven geometries and every companion

| H | labels | actual nine-set family | additional Boolean fibers | binary field pairs |
| --- | ---: | ---: | --- | ---: |
| 9 | 4 | 12 | 10,11,12 (uncovered) | 1094 |
| 12 | 1 | 12 | 4,8 (uncovered) | 0 |
| 18 | 1 | 12 | 2,4 (covered) | 0 |
| 19 | 4 | 12 | none | 48 |
| 24 | 1 | 12 | 1,8 (covered) | 0 |
| 29 | 4 | 12 | none | 243 |
| 129 | 4 | 9 | none | 0 |

State9 represents any of the four remaining fresh points. All19 labels
and Boolean companions are retained BEFORE deterministic cuts. The
crossed companions satisfy chi_R=chi_C+chi_G-chi_H. The uncovered
fibers are not merging cliques under the K cover, but the covered
companions18/24 must be explicitly treated.

For residual H9,H19,H29, common pre(G) in {A,B,C,D,E,F,G,H} is valid
after rejecting the uncovered H9 remainder. Indeed, H9 gives seven
disjoint one-count cells plus a one-count remainder; exactly these are
Boolean one-count columns. For H19/H29, H overlaps respectively C/G
with both private cells and an intersection. A constant coefficient1
would force private coefficients to be0 or-1, with both overlapping
coefficients unable to equal-1. At most six coefficients are negative,
so 8*c0+sum(c_i) cannot be1. Constant coefficient0 yields one known
or H column. No common-fiber assertion discards the crossed companions.

## Four all-alphabet crossed-fiber exclusions

For a letter X with pre_X(G)=H meeting both C and G, disjointness
forces pre(A),pre(B) to be the two singleton inputs0,3. It forces
pre(C)=D5, pre(D)=E6, and pre(E)=F7. Now every possible pre(F) among
A,B,C,D,E,F,G intersects an assigned input: the five singletons were
used and both C,G meet H. No nonempty pre(F) remains. This contradicts
the earlier preimage description, independently of target capacities,
incoming-state counts or alphabet size.

This excludes H12,H18,H24,H129 and the crossed companions18,24 (and
48, independently already uncovered). All7 labelled crossed H choices
are checked as complete individual field tuples,5040 tuples per label,
none disjoint. Unrestricted admission retains H9,H19,H29, twelve labels.

## Binary H19: two explicit three-letter witnesses

Let X supply H={1,9} as pre(G), and let L have pre(B)=C. Both exist
in the earlier entrance flag. Their roles are distinct because H meets C;
for a binary alphabet they are the only letters. The literal fields force

    X permutes0,3; X5=gamma in C; X6=5; X7=6;
    X2=X8=7; X1,X9 in G.

The remaining inputs I={4,10,11,12}, all outside K, biject to
R={9,10,11,12}. For L, pre(C)={u} with u in {0,3,5}; put Lu=delta.
The six input fields pre(A),pre(C),pre(D),pre(E),pre(F),pre(G)
use all P={0,3,5,6,7} and G. Specifically pre(F),pre(G) are G and
the remaining singleton of P in either order. Its ordinary inputs R
therefore permute R. These facts are checked on all48 original H19
field pairs. Strong connectivity forces {gamma,delta}=C; otherwise
one C state has no incoming edge under either original letter.

If gamma=1, take x in I with Xx=9. The protected pair {5,x} follows

    {5,x} X = {1,9}, then X maps it into G, then X merges G to7.

Thus X^3 merges it. If gamma=4,delta=1, take q in R with Lq=9.
Then {u,q} L = {1,9}, and X^2 merges it to7. Thus LX^2 merges a
protected pair. Both contradict P7 isolation of the mandatory core P.
In particular, no individual isolation of2,8 or9 is needed here.

The complete normalized thirteen-state control retains all protected
assignments, both locations of the G input pair, and every ordinary
permutation. It contains6912 L rows and384 X rows,2,654,208 coupled
pairs. Half omit an incoming C state; each other pair has the displayed
literal three-letter protected witness. The normalized pool enlarges
some earlier field restrictions and so cannot miss an actual target.
This control verifies the symbolic proof at actual n13, not by extrapolation.

## Independent check and scope

The independent checker imports no generator. It checks all19 labelled
geometries and every outside3 mask by augmented ranks modulo100003;
Boolean minors have order<=9 and absolute value<100003, so these are
exact rational ranks. Exact coefficients, every actual nine-set family,
each mandatory intersection, every companion, and all capacity2 parent
field extensions are reconstructed. Every actual family point in its
intersection is isolated in P7 by MANDATORY_CORE_ISOLATION.md.

Consequently binary E6/F7/G28 retains H9/H29:two geometries/eight labels,
1337 necessary seventh field pairs, still covering all365 parent sixth
pairs. The unrestricted seventh keeps H9/H19/H29:three geometries/twelve
labels. H19's binary exclusion is not transferred to larger alphabets.
The whole G28/E6/F7 geometry is not excluded by this admission alone;
other sixth branches and both F(13,9,1) intervals[11,12] remain.

Run enumerate_b1_g28_seventh.py followed by check_b1_g28_seventh.py
with Python>=3.10 and assertions enabled. This is an auxiliary
conditional certificate; the accepted article and109-file release
supplement remain unchanged.
