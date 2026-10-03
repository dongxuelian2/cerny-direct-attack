# Distance stabilization does not stabilize the optimal word language

Status: **PROVED**, with a small explicit obstruction and independent
concrete-subset verification. The main distance formula remains true.

Let Opt_r(m) be the set of shortest quotient letter words at hidden capacity
m. Padding proves (baa) Opt_r(m) is contained in Opt_r(m+1), m>=2, because
the distances differ by exactly3. The tempting reverse inclusion is false.

## Smallest anchor count where padding-language equality can fail

For r=5 define

    w=(baa)^2 b a^3 b a^2 b a^5 b,    |w|=20.

Then w is **not** a quotient path to a singleton at capacity2 (n=7), but
baa w **is** an optimal quotient word at capacity3 (n=8), length23.
The proved formula gives B5(7)=20 and B5(8)=23, so this is a strict
optimal-language enlargement, rather than a distance-formula failure.

For r=2,3,4 the optimal word is unique for every capacity>=2, by the
normal-form rigidity theorem. Hence r=5 is the smallest anchor count at
which this padding-language equality fails in the proved regime.

## Explicit reverse obstruction at capacity2

Every b in a putative shortest path is effective. The final goal is0, so
reverse w begins with the singleton at0 and must split there at clocks

    0,5,7,10,12,14.

Each split after0 requires reverse input1 at its clock. An input at the
immediately preceding clock must be0, otherwise the split has first bits11
instead of10. Starting from the root split, hidden occupancy is0 before
clocks1..4, forcing inputs0 there. Clock5 has the first mandatory input.
Clock6 is immediately before a split and hence has input0; clock7 is
mandatory1. The hidden count after clock7 is0, forcing inputs0 at8,9.
Clock10 is mandatory1, clock11 is immediately before a split and has
input0, and clock12 is mandatory1. The hidden counts after each clock
(including its scheduled split) are

    t: 0 1 2 3 4 5 6 7 8 9 10 11 12
    j: 0 0 0 0 1 1 1 0 0 1  1  2  2.

At clock13, the split at14 forces input0, but hidden count2 requires
input1 by the exact capacity2 realizability condition u<=j<=1+u. This is
a contradiction. No representative choices avoid it: all earlier inputs
have been forced by empty hidden storage or the split's preceding zero.
This proves w is impossible at capacity2.

## Matching capacity3 witness

Reverse baa w has split clocks

    0,5,7,10,12,14,16.

Use reverse input1 at exactly these nonzero split clocks and input0
otherwise. The same count2 at13 is now permitted: capacity3 requires
u<=j<=2+u. All subsequent splits are legal and the final state is the
all-one five-anchor word with hidden count3. Here is the remainder:

    after t=13: j=2,  x=30;
    after t=14 and split: j=2, x=31;
    after t=15: j=3, x=30;
    after t=16 and split: j=3, x=31.

The integer window x has its bit0 at anchor0, bit1 at n-1. The earlier
counts and direct shift/merge rules verify every edge. Thus the forward
word is valid from the full n=8 feature. It has optimal length23.

## Meaning

The optimal value stabilizes at capacity2, while the set of optimal words
can still enlarge at capacity3. The forced literal baa prefix of an optimum
does not force its reached feature to be the full capacity2 feature:
alternative witness choices can leave a different distribution behind it.
The explicit greatest clock schedule remains realizable and canonical;
other optimal schedules can depend on capacity.

`optimal_language.py` checks both words by directly enumerating concrete
subsets, constructing labelled quotient relations, and propagating **all**
possible feature states along the proposed word. It does not import the
count/window transition implementation. The earliest-schedule greedy
failure in `earliest_capacity_two.py` first appears at r5 for this same
blocking mechanism; that greedy rule is an exploratory failure, not a
replacement for the proved uniform construction.
