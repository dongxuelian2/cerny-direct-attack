# Complete seventh entrance admission in E26/F7

Conditional at n=13, |S|=9, ac(S,{3})=12, B={0}, C={1,4},
D={5}, E={2,6}, F={7}, K={1,2} covering P5.
The sixth branches considered here are precisely G={8},{1,8},{2,8}.
This is an investigation-only necessary classification, not an extremal
value or an assertion of automaton existence.

Every collision-free image through five meets G once. Thus every
preimage of G meets every image through four once. A preimage containing
3 equals {3}; otherwise the four-step images omit another state, contrary
to strong connectivity reaching every state from S in at most four steps.
Distinct one-count fibers are incomparable for the same reason.

The complete earlier sixth Boolean inventory has no companions in these
three branches. Every preimage of F is one of A,B,C,D,E,F,G. If all
preimages of G were also known, the nonempty proper union of these fibers
would be backward closed under every letter, contradicting strong
connectivity. Hence some letter supplies a fresh H.

Equality gives dim V4=5. The annihilator has dimension eight; restriction
to O=Q minus {3} is injective. The columns 1_O,B,C,D,E,F,G are independent.
The earlier complete Boolean inventory shows that a fresh one-count H is
outside their span. Therefore 1_O,B,C,D,E,F,G,H is a basis of this
restricted annihilator. Every further preimage of G is a Boolean column
in this span with one-count functional 8*c0+sum(ci)=1. All such columns
are retained explicitly before cover and incomparability tests.

G is a clique in P1 because F is a singleton and a letter maps G to F.
Every preimage of G is consequently a clique in P2. The P5 cover gives
|H minus K|<=1 and |H|<=3. No separate isolation is asserted for either
endpoint of E or of the overlapping G pairs.

The literal family contains all nine-subsets containing3 and meeting
each of B,C,D,E,F,G,H once. It includes every actual image through four.
Its intersection is therefore a mandatory core through four and is
isolated in P7 by MANDATORY_CORE_ISOLATION.md.

Each letter is recorded by the seven preimages of A,B,C,D,E,F,G. A source
can map only to an output with the same seven-bit membership signature.
The exact output atoms retain C/G's shared1 and E/G's shared2. Empty
input atoms are allowed. Singleton output atoms force kernel pairs;
these must meet K, avoid the mandatory core, and number at most four.
For binary pairs the two incoming capacities must cover every output
atom, their combined forced pairs must number at most four, and one
letter must supply H. Those binary conditions are not all-alphabet cuts.

The independent checker imports no generator. It enumerates every
literal H and all outside3 subset masks, checks augmented ranks modulo
100003, and checks the generator's rational coefficients literally.
All Boolean minors have order at most nine and square absolute value
at most 9^9<100003^2; the modulus is verified prime. Modular rank thus
equals rational rank. Full 5040-tuples of earlier individual fibers
are separately checked for every fresh or covered companion preimage,
without binary incoming-capacity constraints. These controls establish
whether an individual preimage is impossible for every alphabet.

The inventory and checker do not by themselves exclude a whole G, F, E,
third or joint geometry. A field admission is not a complete transition
row or an equality model. The manuscript and release are unchanged.

## Completed classification

For the three canonical G shapes, the complete classification has
23 geometric orbits and59 labelled H choices (7/19,8/20,8/20).
The independent checker tests241,605 outside3 masks and39,365 augmented
ranks. Every coefficient vector has eight entries; every Boolean fiber
is unique. All covered companions and output overlaps are retained.

| G | all-alphabet impossible H | binary admitted H | binary field pairs |
| --- | --- | --- | ---: |
|8|12,16,24,129|9,19,29|1250|
|18|12,16,24,28,29,129|9|48|
|28|12,16,24,129|9,18,19|120|

Digits denote state sets, not numbers. G18/H19 and G28/H29 have
individual supplying fields, but zero binary incoming-capacity pairs;
they are not all-alphabet exclusions. The full5040-tuple controls,
without binary capacity conditions, verify every individual cut.
G8/H16,H24 permit the mutual companion24,16. G18/H16,H24,H28 and
G28/H16,H18,H24 have two covered companions each. All those companions
are explicitly tested, including G28/H18 where H18 itself remains.
Uncovered remainders are also present in the complete Boolean lists.

The unrestricted survivors are G8/H9,H19,H29 (3orbits/12labels),
G18/H9,H19 (2/8), G28/H9,H18,H19,H29 (4/13). These are necessary
fields, not actual extremal automata. Canonical G uses8 as an ordinary
representative; permutations of8-12 and then of its four remaining
ordinary points transport the entire geometry and row checks to all
literal G/H labels while fixing A,B,C,D,E,F,K.

For each of the nine unrestricted survivors the independent checker
also supplies a literal single-letter row, reconstructed by inputwise
recursion and checked against the exact target atoms, P7/P5 pure powers,
and a safe initial nine-set through eleven (family membership through
four). This verifies that the supplying-letter domain itself is
nonempty, including binary-capacity-zero H19 at G18 and H29 at G28.
A single letter is not an automaton or a full equality witness.
