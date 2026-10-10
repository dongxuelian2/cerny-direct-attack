# Typed third entrances in the disjoint three-point/two-point case

9 October 2026. Necessary structure at (13,9,1), any finite alphabet.
No new extremal value and no joint second-entrance orbit exclusion.

Normalize H={0,1,2}, a=3, B={0,1,4}, C={2,5}, and suppose
ac(S,{a})=12, |S|=9. The entrance lemmas give each letter's preimage
of a as A={3} or B, of B as A,B or C, and of C as A or an outside
Boolean fiber in the third entrance space. Some outside preimage D
of C is distinct from B,C. The union B,C is disjoint.

Because the three output sets A,B,C are pairwise disjoint, their
input preimages under each letter must be pairwise disjoint. The
possible first two preimage pairs are exactly

  (A,B), (A,C), (B,A), (B,C).

Every pair includes B or C. Therefore its third preimage D must
avoid B or avoid C. A third preimage meeting both is impossible.
This is a constraint on each actual row, not an alphabet-size bound.

Combining this constraint with the proved H cover, incomparability
of B,C,D, and a nine-set meeting all three once leaves exactly,
up to permuting equivalent ordinary points and exchanging 0,1,

  D={6}, {0,6}, {2,6}, {0,1,6}.

Indeed, a D disjoint from B is contained in {2,5} union {6,...,12}.
Incomparability with C requires a new ordinary point, while the
H-cover allows at most one point outside H, excluding 5 together
with a new point. This leaves {6} or {2,6}. A D disjoint from C
is contained in {0,1,4} union {6,...,12}. Incomparability with B
again requires a new ordinary point; the cover then excludes 4.
This leaves {6}, {0,6} or {0,1,6} up to exchanging 0,1.
Each case has an admissible nine-set, as checked independently.
There are 35 labelled sets in these four orbits, compared with
65 labelled sets in the earlier twelve-orbit geometric admission.

The third entrance is common in these specific cases. To see this,
let an outside preimage R of C have indicator

  chi_R = alpha*1 + beta*chi_B + gamma*chi_C + delta*chi_D.

The remainder outside B,C,D contains several points outside H,
on which chi_R takes the constant value alpha. The cover condition
|R minus H|<=1 forces alpha=0. There is a private B point (4), a
private C point (5), and a private D point (6). Thus beta,gamma,delta
are each Boolean. Counting R on the actual S, which meets B,C,D
once, gives beta+gamma+delta=1. Consequently R is B,C or D.
Each letter's preimage of C is therefore A,B,C or this same D.
No common-third-fiber statement outside these profiles is asserted.

For a binary alphabet and D meeting B, the letter using D as
preimage of C must fix a and have preimage C of B: the other
possible preimage pair (A,B) intersects D in B. Call it F. The
other letter M must use B as preimage of a. Its preimage pair for
B,C is either (A,C) or (C,A). There are no other profiles; D meets
B, so it cannot be used by a moving letter. Both these profiles
are treated for D={0,1,6} in C3_D9_BINARY_EXCLUSION.md.
For D={0,6}, C3_D4_PROFILE_I_EXCLUSION.md and
C3_D4_BINARY_EXCLUSION.md exclude both binary moving profiles.
Binary c3 retains only the disjoint third entrances {6} and {2,6}.
The unrestricted typed admission remains all four profiles.

The old third inventory deliberately remains geometric and retains
all twelve entries. The new checker applies the disjoint input types
independently and records the four actual-row-compatible entrances.
This reduction does not exclude the c3 second-entrance orbit itself.
