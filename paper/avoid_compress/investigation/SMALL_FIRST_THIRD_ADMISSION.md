# Complete B1/B2 third-preimage admission at (13,9,1)

9 October 2026. Necessary structural inventory, outside the release.

The earlier binary B3 exclusions leave 29 original joint B,C records,
with |B|=1 or 2. For each record, a fresh preimage D of C is covered
by H={0,1,2}, incomparable with B,C, and has |B union C union D|<=6.
A nine-set containing a=3 must meet B,C,D once. The third-space
annihilator requires the four columns 1,chi_B,chi_C,chi_D to be independent.

There are 235 geometric third orbits under the full stabilizer of H,a,B,C.
The orbit of D is specified by its membership counts in the eight
H/B/C cells. Equivalent cell counts are sufficient as well as necessary
because permutations within each cell are independent. Literal enumeration
of all 79 covered D sets and all 495 nine-sets containing a independently
checks their orbit sizes and their feasible initial-set counts.

Every other outside preimage R of C lies in the same four-column span
and meets every feasible initial nine-set once. We retain every Boolean
R satisfying these requirements and the cover/nonnesting conditions.
Thirty geometric orbits admit additional fibers besides B,C,D. For example
B={0,4}, C={1,5}, D={0,5}, R={1,4} satisfy chi_R=chi_B+chi_C-chi_D.
The nine-set {0,1,3,6,7,8,9,10,11} meets all four once. This is a
geometric control, not an automaton equality witness. A universal common
third fiber is not assumed.

For a binary pair of letters we enumerate all possible preimages of
A,B,C: pre(A) is A or B, pre(B) is A,B or C, and pre(C) is A or any
admitted outside R. Each input's membership signature must correspond
to a nonempty output membership cell. Singleton output cells give forced
kernel pairs, whose union must have size at most four and be covered by H.
The two letters must use B as pre(A), C as pre(B), and the chosen D as
pre(C). Their combined numbers of available predecessors in each output
cell must at least equal the cell size. For overlapping B,C we also use
the already proved forbidden crossing of the fixed row's pre(C)=B.

These necessary tests retain 182 third orbits and 965 unordered letter
profile pairs. Profiles are counted with the chosen D; these counts are
not numbers of distinct automata. The independent checker forms actual
possible output sets for each input and uses integer augmented rank and
literal nine-set intersections, independently of the generator's rational
coefficient calculation. It reproduces all admission records.

B2_FOUR_POINT_SECOND_EXCLUSION.md then symbolically excludes the original
joint record b2_mixed_c12, B={0,4}, C={0,1,2,5}. Only D={1,6} and
D={1,2,6} have admitted binary profiles. The required outside predecessors
of 6 produce an uncovered pair merged by L M F M whenever 6 enters
D intersect H; otherwise that nonempty intersection has no incoming
transition from its complement. Both alternatives contradict equality.

check_small_first_third.py audits the complete R-kernel partitions
(4,140+877+877=5,894), all 108 core assignments, and every short-pair or
backward-closure case. This audits the symbolic proof; it is not a scan of
all completed transition tables. Both extrema remain in [11,12]. Binary
joint cases decrease to 28, while unrestricted cases remain 43. Combined
with the preceding |B|<=2 restriction, binary equality now also requires
|C|<=3, since |B|=1 already gives |C|<=3 and the only B2/C4 orbit is
the one just excluded. No new F value or numerical separation is asserted.
