# A third entrance space, without assuming a common third fiber

9 October 2026. Auxiliary necessary structure; no new extremal value.

Let a strongly connected synchronizing automaton over any finite
alphabet satisfy ac(S,{a})=t=n-1 with s=|S|>=5. Write B,C for the
first two common entrances from ENTRY_FIBER_FLAG.md and
SECOND_ENTRANCE_FIBER.md. Then some letter has a preimage D of C
outside {a}, distinct from B,C, with the following properties:

* Each letter's preimage of C is either {a} or a nonempty subset R
  of O=Q minus {a}. Every image through depth t-4 meets R once.
* D is incomparable with B and C. Any two distinct one-count fibers
  among B,C and the outside preimages of C are incomparable.
* The restrictions of the four-dimensional trajectory annihilator
  to O have basis 1_O,chi_B,chi_C,chi_D. Every outside preimage R of
  C has indicator in this span. This does not in general force R=D.
* Each outside preimage of C is a collision clique in P3. If H
  covers P5, it contains all but at most one point of each such fiber.

No initial-set reachability assumption is used.

## Proof

For a letter ell, every image Sw with |w|<=t-4 meets ell^(-1)(C)
once, because Sw ell meets C once through depth t-3. Safety ensures
these are collision-free characteristic rows. A preimage containing
a must be {a}: otherwise all those images would omit another point
of that preimage, contrary to strong connectivity reaching every
point from S within m=n-s<=t-4 steps.

At least one preimage D is outside {a},B,C. Otherwise the preimage
under every letter of the proper nonempty union {a} union B union C
would be contained in that union, using also the already proved
preimage descriptions of a and B. Its complement could not reach
it. The union is proper because it meets S in at most three points
and s>=5. Every outside preimage meets S once. If two such one-count
fibers, including B,C, were properly nested, images through depth
t-4 would omit their difference, again contradicting m<=t-4.

Equality gives dim V_(t-4)=t-3=n-4, so its annihilator has dimension
four. It contains h_a=s e_a-1 and h_X=s chi_X-1 for X=B,C,D. Their
restrictions to O span 1_O,chi_B,chi_C,chi_D. The first three are
independent. The Boolean classification used in the second-entrance
proof shows that only B and C among Boolean vectors in
span{1_O,chi_B,chi_C} can meet S once when s>=5. Thus D supplies the
fourth independent column. Any other preimage R has h_R in the same
annihilator, proving the span assertion. A letter taking R into C,
followed by a word of length at most two merging a specified pair
in C, merges that pair of R in at most three steps.

## Thirteen-state inventory and a warning

For H={0,1,2}, a=3, B={0,1,4}, the three remaining second entrances
are {2,5}, {0,2,5}, {0,1,2,5}. A possible D is nonempty, has at most
one point outside H, is incomparable with B,C, and admits a nine-set
containing a and meeting B,C,D once. Also |B union C union D|<=6:
the union of three collision cliques has independence number at
most three, and its vertex cover has size at most three.

Exact Boolean-column enumeration gives, for these fixed B,C:

| C | D orbits | Labelled D sets | Orbits allowing an additional fiber |
|---|---:|---:|---:|
| {2,5} | 12 | 65 | 4 |
| {0,2,5} | 16 | 64 | 2 |
| {0,1,2,5} | 8 | 59 | 0 |

The common-third-fiber claim must not be extrapolated from the last
row. For example B={0,1,4}, C={0,2,5}, D={0,1,5}, R={0,2,4} satisfy
chi_R=chi_B+chi_C-chi_D. All four meet the nine-set
{0,3,6,7,8,9,10,11,12} once, are incomparable, and satisfy the cover
cuts. This is a geometric/linear control, not an automaton equality
witness or a counterexample to a stronger full-automaton theorem.

enumerate_third_entrance.py enumerates the stabilizer cell counts
and solves the four-column Boolean equations over exact rationals.
The independent checker enumerates labelled D sets, each possible
covered R, literal nine-set intersections and exact augmented ranks.
No geometric admission or solver timeout is treated as exclusion.
