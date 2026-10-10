# Uniform two-block construction: proof and adversarial case audit

For p>=4, t>=2 and k>=0, construct disjoint sets
P={p_0,...,p_(p-1)}, X={x_1,...,x_t}, Y={y_1,...,y_t}, {z},
H={h_1,...,h_k}. Letter a swaps the last two P states, fixes the other
P states and H, and cycles x_1,...,x_t,y_1,...,y_t,z.
Letter b maps p_i to p_(i-1) for i>=1; subdivides the edge p_0 -> y_1
by the H chain; increases X and Y indices when below t; maps x_t,y_t
to p_(p-1); and fixes z. Set S=P union X union H and A={p_0} union H.
Then all structural requirements hold and

    ac(S,A)=min(p+2t,3t+2).

Here n=p+2t+1+k, s=p+t+k and r=k+1, hence n-r=p+2t and m=n-s=t+1.
Consequently for all m>=3 and q=n-r>=2m+2 the binary construction attains
min(q,3m-1). In particular F_bin=F=U=q on 2m+2<=q<=3m-1.
For larger q it is only a lower bound. Together with the separately proved
cofinal region, exactness holds throughout q<=3m-1, m>=3; the existing
codimension-three family extends that face to q=9. No unrestricted upper
bound 3m-1 or global equality with this family is claimed.

## Compression lower bound in the unpadded base

Initially k=0. Put L=3t+2 and rho_i=min(i,p-2). Give diagonal pairs
potential zero and the following symmetric potentials on distinct pairs:

| pair | D |
| --- | --- |
| P-P, P-X, X-X | L |
| x_i,y_j, j=i | t-i+1 |
| x_i,y_j, j>i | 2t-i+1 |
| x_i,y_j, j<i | L-j |
| x_i,z | 2t-i+1 |
| y_i,y_j, i<j | L-j |
| y_i,z | 2t+1 |
| p_i,y_j | min(L,max(L-j,2t+3+rho_i)) |
| p_i,z | min(L,2t+2+rho_i) |

For every pair E and original letter l, D(E)<=1+D(E l).
The following ledger checks every type, including all index boundaries.
Clipping at L cannot increase a positive difference. Swapping the last
two P indices preserves rho; under b, rho decreases by at most one.

* P-P: a preserves type; b either preserves type or gives P-Y with j=1,
  whose potential is at least L-1.
* P-X: a stays in type unless x_t crosses to y_1, again potential >=L-1.
  Under b, p_i with i>=1 stays P-X or becomes P-P. For i=0 and j<t,
  the image is {y_1,x_(j+1)} with potential L-1; for j=t it is
  {y_1,p_(p-1)} with potential >=L-1.
* X-X: a stays in type unless the larger index is t, when the target
  X-Y potential is L-1. Under b a crossing gives P-X, potential L.
* P-z: a gives P-X, potential L; b with i>=1 decreases rho by <=1,
  and i=0 gives Y-z, potential 2t+1, exactly one below 2t+2.
* P-Y, a: for j<t the L-j term decreases by one and rho is unchanged.
  For j=t the source is min(L,2t+3+rho_i) and the target is
  min(L,2t+2+rho_i), differing by at most one.
* P-Y, b: for i>=1,j<t both terms decrease by <=1; j=t gives P-P.
  For i=0,j<t the source is exactly L-j (since j<=t-1) and the
  target {y_1,y_(j+1)} has L-j-1. For i=0,j=t, the source 2t+3
  is <=L and the target P-Y at j=1 has potential >=L-1.
* X-Y, j=i: a or b increments both indices and decreases potential
  by one. The last a boundary gives Y-z with a larger potential; the
  last b boundary is the unique kernel pair, of potential one, merging.
* X-Y, j>i: incrementing both or crossing y_t to z under a gives
  2t-i, one below the source. Under b the y_t boundary gives P-X.
* X-Y, j<i: incrementing both gives L-j-1. The x_t boundary under
  a gives {y_1,y_(j+1)} with that same value; under b it gives P-Y
  with potential >=L-j-1.
* X-z: a with i<t gives X-X; i=t gives {x_1,y_1} of potential t,
  one below the source t+1. Under b, i<t decreases the value by one,
  and i=t gives P-z with a larger value.
* Y-Y: both indices increment unless the larger is t. Under a that
  boundary gives Y-z of potential 2t+1=L-t-1. Under b it gives
  P-Y at index <=t, with potential at least L-t.
* Y-z: a always gives potential 2t, exactly one less; b preserves
  type unless y_t enters P, when the target potential is >=2t+2.
* Diagonal pairs have zero and remain diagonal, trivially satisfying the inequality.

Every distinct pair in P union X has potential L. Telescoping along a
merging word gives |w|>=D(E), since its final potential is zero. Every
compressing word merges some initial pair, so compression needs >=L letters.
This proof uses symbolic inequalities for arbitrary p,t, not a finite grid.

## Avoidance lower bound in the unpadded base

Use singleton P-cells and t color cells, giving x_i and y_i color i,
and z color 1. Let C be the incidence matrix. T_a swaps the last two
P-cells and cycles the colors; T_b cycles
p_0,1,...,t,p_(p-1),...,p_1. With row-action matrices D_l and a state
column f_z and color rows e_i, both original letters satisfy

    D_l C = C T_l + f_z (e_1-e_2).

The final term is an outer product. Initially S=P union X contains one
state per cell. Iteration gives the exact trajectory multiplicity identity

    chi_S D_w C = 1 + sum_i mu_i (e_1-e_2) T_suffix,

where mu_i>=0 counts trajectories at z just before the ith letter.
The formula remains true after collisions.

No trajectory from S reaches z before t+1 steps. From X its increasing
U-index requires at least t+1 steps; any P entrance into y_1 costs at
least one step and then at least t further steps to reach z. Departing U
through b cannot shorten this. Thus mu_i>0 requires i>=t+2.

In the prescribed cell graph, color 2 needs t-1 letters to enter P at
p_(p-1), and p-1 more to reach p_0. The only P interchange is between
the adjacent last two points and cannot shorten the descending path.
Hence a negative correction reaches p_0 only with suffix length >=p+t-2,
requiring total length >=(t+2)+(p+t-2)=p+2t. Before that length the
p_0 coordinate is >=1, proving its presence. Positives need not be bounded.

## Attaining words

After a^(2t)b, the missing P state is p_(p-1). Applying a makes p_(p-2)
missing. This state is the unique b^(p-2)-preimage of p_0. Therefore
a^(2t)b a b^(p-2) omits p_0 and has length p+2t.

The U portion after a^(2t)b is {x_2,...,x_t,y_1,z}. After a^t it contains
x_t (from z) and y_t (from x_t, which exists in this set since t>=2).
The following b merges them. Thus a^(2t)b a^t b compresses at length L.
These two words prove ac=min(p+2t,L) together with both lower bounds.

## Protected subdivision and all structural requirements

For every old T containing p_0, (T union H)a'=Ta union H and
(T union H)b'=Tb union H. Each proper prefix of a shortest old unsafe
word contains p_0. Induction through the first unsafe step transfers the
event, and all new states remain present. Thus the local value and the
corresponding attaining word are preserved with A={p_0} union H.

Let B=P union H union Y, s=|B|=p+t+k and E=B union {z}. Letter b cycles
B in the order p_0,H,y_1,...,y_t,p_(p-1),...,p_1. Qb^t=E. The a-cycle
connects every remaining state to B and vice versa, so the automaton is
strongly connected.

On E, d=a^(2t)b^s fixes P union H, cycles y_1 -> y_t -> ... -> y_1,
and sends z to y_t. Therefore e=d^t fixes B and sends z to y_1. This
gives Qb^t e=B and Ba^(t+1)=S, so b^t e a^(t+1) is a reaching word.

The word a^(2t+1) fixes U and H and interchanges the last two P states,
adjacent on the b-cycle. Along with b it generates Sym(B), with inverses
realized by positive powers. Further,
Ba=(B minus {y_1}) union {z}, Bab=(B minus {y_2}) union {z}, and
Babe=B minus {y_2}. For t>=2, y_1 remains in the latter intermediate B
image, so the retraction of z creates a collision. Permutations send any
pair in a current image into that kernel; repeat abe after suitable
permutations to synchronize B. Prepend b^t e to synchronize Q.
No auxiliary input letter or uncharged macro is introduced.

## Equivalent canonical prefix form used by the paper and release

Reverse the H chain and place it before the old P chain. This gives a single
P-chain of size p'=p+k, with A={p'_0,...,p'_(r-1)}, r=k+1. In this form
there is no separate H block: a swaps the last two P' points and cycles
X,Y,z; b sends p'_0 to y_1 and shifts the other P' points down.
The hypothesis is p'>=r+3, t>=2, and the result is

    n=p'+2t+1, s=p'+t, ac(S,A)=min(n-r,3t+2).

The pair-potential ledger applies directly with p' replacing p. In the cell
graph, color 2 first enters P' at p'_(p'-1) after t-1 letters, and needs
p'-r further letters to reach the nearest A point p'_(r-1). Thus its distance
to A is p'+t-r-1. Combined with the first-error position t+2, no protected
coordinate can be lost before n-r. The avoider is
a^(2t)b a b^(p'-r-1), of length n-r, whose missing point is p'_(r-1).
All powers are nonnegative; the hypothesis makes the last exponent >=2.
The same compression word, retraction, reaching word and adjacent
transposition establish the other claims. The release generator/checker use
this canonical prefix form and have no dependency on exploratory modules.

## Finite implementation audit

The finite symbolic-potential audit checked 618999 pairs and 1237998 letter
inequalities through t=40, including small p, p=t+1,t+2,t+3, and large p.
The separate ordinary subset-BFS probe checked 105 cases through t=8,
including k=0,1,2, both parities of t and the clipped range p=t+3.
These checks support the implementation. The universal theorem rests on
the preceding exhaustive symbolic case ledger, matrix delay and structural proof.

The release's canonical-prefix generator supplies 221 records through n=65.
The independent checker rebuilds transitions from named states and verifies
216 values by ordinary subset BFS. The five larger instances use complete
finite pair-potential and signed cell-delay certificates instead; it checks
every original-letter inequality and exact incidence identity and both graph
distances. All instances have checked actual reaching/attaining/reset words
and structural macro actions. Its totals are 68744 pair checks, 137488 letter
inequalities and eight deliberately corrupted records rejected. No generator
module is imported by the checker. The uniform proof does not depend on
whether these finitely many implementation checks passed.
