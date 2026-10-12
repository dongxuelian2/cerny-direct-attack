# Conditional rejection using the real flag of an entire literal pool

Auxiliary thirteen-state proof. Let T have nine states and contain alpha=3.
Assume alpha is avoidable from Q and every word of length at most eleven
is safe from T. This is a necessary model for the manuscript domain at
(13,9,1), target twelve, and for its qualified folded counterpart. No new
F value, folded synchronization or folded reachable image is asserted.

Fix characteristic rows b_0,...,b_11, with b_0=chi_T, and let
W_i=span_R(b_0,...,b_i). The finite audit checks dim W_i=i+1, that all
b_i have total nine and alpha-coordinate one, and that every literal
action in the specified pool maps W_i into W_(i+1) for i<11. Consequently
W_11=H={x:sum x=9x_alpha}. These are statements about complete counting
rows chi_B D_f; the audit does not require safety of b_11 f at depth twelve.

For an actual alphabet E inside this pool, let V_i be the actual trajectory
row span from T through length i. The checked filtration implies V_i is
contained in W_i for i<=11. Under the safe-word premise V_i is in H. A
plateau V_i=V_(i+1) stabilizes forever under E, contrary to a word avoiding
alpha from Q, which also avoids it from T and has total nine. Hence
dim V_i>=i+1, so V_i=W_i for all i<=11.

For every i<11 some actual letter must map b_i outside W_i. If every
letter mapped b_i inside W_i, the earlier basis rows would also map
inside W_i by the checked filtration, causing a plateau. At i=11 the
same argument applies to H: the earlier basis rows already map inside H,
so some actual letter maps b_11 outside H. Its counting row has total
nine, hence this means alpha multiplicity differs from one. Define the
twelve growth domains by these exact tests. Every qualifying alphabet
must meet each of them. The argument does not require the b_i themselves
to be actual word images for that alphabet; it uses equality of spans.

The existing literal word conflicts are valid under the same premise.
An unsafe word of length at most eleven directly contradicts safety.
A word u of rank below nine compresses T. For rank exactly nine and
length at most six, every Tw with |w|<=5 is a transversal of its nine
fibers, since |Twu|=9. Their rows span a space of dimension at most
13-9+1=5, while the preceding no-plateau argument gives dim V_5>=6.
This contradiction is the standard row-span/transversal method, not a
novelty or priority claim. It needs no unproved folded reset word.

A finite cover tree checks all alphabets meeting the twelve growth
domains against these literal conflicts. Before using it at a native
node, every active transformation must literally belong to the audited
pool and its initial image must equal T. The growth domains replace
dependence on a particular choice of subsequent characteristic images.
Complete original-prefix and whole-geometry replay are still separate
requirements. No other geometry or numerical extremum follows from the
pool certificate alone.
