# A second common entrance fiber at singleton equality

Auxiliary necessary structure for Problem 4; no new extremal value.
This note is outside the manuscript and supplementary release.

Let a strongly connected synchronizing automaton have S of size s>=5,
A={a}, and ac(S,{a})=t=n-1. The first entrance-fiber proposition supplies
a nonempty B subset Q minus {a}, meeting S once, such that every letter
has preimage of a equal to {a} or B, and some letter uses B.

Then there is a nonempty C subset Q minus {a}, distinct from B, such that

* each letter has preimage of B equal to {a}, B or C;
* some letter uses C, and |S intersect C|=1;
* neither B nor C contains the other;
* every image Sw with |w|<=t-3 meets C once; every image with
  |w|<=t-2 meets B once.

Initial-set reachability is unnecessary. If |B|=1, C is a one-step
collision clique. Otherwise C is a two-step collision clique. At
(n,s,r)=(13,9,1), the proved |P1|<=4 and cover(P5)<=3 therefore give
|B|<=3, |C|<=4 (improved to |C|<=3 when |B|=1), and |B union C|<=5.

## Proof

Use row trajectories chi_S D_w and V_i=span_R of trajectories with
|w|<=i. Equality gives dim V_i=i+1 through i=t-1, and all these
trajectories are collision-free characteristic rows containing a.
For a letter whose preimage of a is B, safety of w followed by that
letter shows |Sw intersect B|=1 through depth t-2.

For a letter ell put D=ell^(-1)(B). Every image through depth t-3
meets D once. In particular D is nonempty and |S intersect D|=1.
If a belongs to D, every such image already contains a, so it omits
every point in D minus {a}. Strong connectivity reaches each state
from S within m=n-s steps, and m<=t-3 since s>=4. Thus D={a}.
Otherwise D is a subset of O=Q minus {a}.

Thus each D is {a} or is contained in O. The outside preimages
cannot all equal B. Indeed, if every preimage of B
were {a} or B, then ell^(-1)({a} union B) would be contained in
{a} union B for every letter. Its nonempty complement could never
reach this proper nonempty set, contradicting strong connectivity.
The set is proper since S minus {a} has at least four points and
only one of them belongs to B. Choose an outside preimage C different
from B. It meets S once.

The annihilator K of V_(t-3) has dimension three and contains

  h_a=s e_a-1,   h_B=s chi_B-1,   h_C=s chi_C-1.

Here 1 denotes the all-one column. The restrictions to O of these
columns span {1_O,chi_B,chi_C}. This space has dimension three:
the only Boolean vectors in span{1_O,chi_B} are 0,1_O,chi_B and
chi_(O minus B); C is neither empty nor O nor B nor its complement,
because it meets S once and |S intersect O|>=4. Consequently these
three columns form a basis of K. Any outside preimage D of B has
h_D=s chi_D-1 in K, so chi_D belongs to span{1_O,chi_B,chi_C}.

Both B and C meet every image through depth t-3 once. If B were
properly contained in C, these images would all omit C minus B;
if C were properly contained in B, they would all omit B minus C.
Strong connectivity and m<=t-3 exclude both possibilities. Also
B union C is proper in O: its intersection with S has at most two
points whereas |S intersect O|>=4.

If B and C intersect, all four membership cells on O are nonempty.
A Boolean vector in their affine span is one of 0,1,B,O minus B,
C,O minus C: its four cell values are Boolean and their opposite
sums agree. Among these, only B and C meet S once. If B and C are
disjoint, their three membership cells are nonempty and the Boolean
vectors in the span are the eight unions of these cells. The remainder
meets S in s-3>=2 points; the two other cells each meet S once.
Again only B and C are permitted. This proves the common-fiber claim.
The role of s>=5 is essential to this last argument; no assertion for
s=4 is made here.

If B is a singleton, a letter using C maps its points to that single
state and merges each pair in C immediately. If |B|>=2, some letter
maps the whole B to a; appending it after a letter with preimage C
of B merges every pair in C in at most two steps. Thus C is the
stated collision clique. At the thirteen-state parameter a cover of
P5 has size at most three, so |C|-1<=3. B itself is a clique in P1,
and binomial(|B|,2)<=4. Finally an independent set in the union of
the two cliques B and C has size at most two. Its induced graph
therefore needs at least |B union C|-2 cover vertices, proving
|B union C|<=5. These are necessary cuts, not a new upper on F.

## Audit

check_second_entrance.py recomputes ordinary subset and pair distances,
the three-dimensional annihilator, all admitted preimages, and the
boundary restrictions on applicable known equality certificates. It
also verifies the elementary Boolean-cell classification literally.
Finite controls support the symbolic proof; neither they nor a bounded
solver run certify absence of an extremal automaton.
