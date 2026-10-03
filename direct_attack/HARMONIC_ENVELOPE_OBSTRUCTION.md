# Reachable almost-full subsets attain the six-step bound at unbounded n

**PROVED (paper, with explicit finite base); novelty OPEN.** There are
strongly connected synchronizing binary DFAs for infinitely many n, with a
Q-reachable subset S of size n-2 whose shortest compression length is exactly
6. Thus Pin--Frankl's corank-two bound is attained even at unbounded n.

In particular the tempting harmonic estimate

    c(S) <= ceil(n(n-|S|+1)/(|S|-1))                         (H1)

is **REFUTED**, with state-minimal witness n=8 over ANY alphabet. Summing
this estimate would give O(n^2 log n), so the failure blocks a concrete
subcubic route. The counterexample concerns actual reachable images, not
only arbitrary subsets.

## Explicit eight-state base

On Q0={0,...,7}, take

    a=(6,7,1,3,0,5,4,2), b=(0,4,2,7,5,6,3,4),
    S0={0,1,3,4,5,6}=Q0\{2,7}.

a has cycles (0,6,4), (1,7,2), and fixed states 3,5. The directed graph
is strongly connected. The following actual words suffice for the proof:

    Q0 (baabaa) = S0;
    |S0 (aabaab)|=5;
    Q0 (baababaababbaababbaababbbaabbbbabaaba)={0}.

To audit that no word of length <=5 compresses S0, write a set by its bitmask
sum_(q in S) 2^q. The sets first reached at each distance from S0 are:

| distance | masks |
|---|---|
| 0 | 123 |
| 1 | 249 |
| 2 | 125 |
| 3 | 237 |
| 4 | 126, 221 |
| 5 | 95, 187, 189, 252 |

Every listed set has size six and contains state 3. Direct multiplication by
the two displayed letters checks the table inductively. Together with the
six-letter word aabaab this proves c(S0)=6. The independent checker also
tests every one of the 63 words of length <=5, not just a selected path.

For n<=7 and every 2<=k<=n, the H1 right side is at least
binom(n-k+2,2), so Pin--Frankl proves H1 for all such n over arbitrary
alphabets. At n=8,k=6 it is ceil(24/5)=5. Hence n=8 is state minimal.

## Padding that preserves the bottleneck

Let n>=8 and 3 not divide d=n-7. Add N=n-8 states 8,...,n-1. The letter b
fixes each added state. Replace a's fixed point 3 by the cycle

    (3,8,9,...,n-1), of length d=N+1,

leaving its other cycles unchanged. Put S_n=Q_n\{2,7}=S0 union new states.

As long as the base image contains 3, applying a to an image enlarged by ALL
new states gives exactly its old a-image union all new states: the new cycle
is entirely occupied. Applying b always has that property. The base table
therefore lifts every word of length <=6, because its prefixes through length
5 contain 3. No word of length <=5 compresses S_n, and aabaab compresses it
to n-3. Thus c(S_n)=6 for every parameter of this family.

Strong connectivity is preserved. The only changed old edge is the a-loop
at 3; removing a self-loop cannot destroy paths among old states. New states
are connected to those old paths through the added cycle.

## Synchronization and reachability are not assumed

Choose L=d if d=1 mod 3, and L=2d if d=2 mod 3. Then L=0 mod d and
L=1 mod 3. The word a^L acts on Q0 exactly as the original a and fixes all
new states. Encode any old word by replacing every a with a^L and keeping b.
The encoded 37-letter reset word displayed above, call it V, maps Q0 to 0
and fixes every new state. The encoded baabaa maps Q_n precisely to S_n.

To reset Q_n, start with V, whose image is {0} union new states. Pick a new
state q still in the current image. Some a^j, 1<=j<=N, sends q to 3. The old
state 0 stays in its old three-cycle, and hence does not enter the new cycle.
Applying b sends 3 to old state 7 and fixes every remaining new state.
Applying V then resets all old images to 0, leaving the others unchanged.
Exactly one new image has been removed. Repeating this step at most N times
resets Q_n. This supplies an actual reset word; its length is not asserted
minimal, and its long length is not a lower bound on rt.

## Quantitative limits of the harmonic route

On these subsets, n(n-|S_n|+1)/(|S_n|-1)=3n/(n-3) tends to 3,
whereas c(S_n)=6. Therefore any uniform UNROUNDED envelope
c(S)<=C*n(n-|S|+1)/(|S|-1) needs C>=2. With a ceiling, every C<5/3 fails
for sufficiently large members of the family. A larger constant envelope,
which could still imply subcubic total cost, remains **OPEN**; this argument
does not refute it.

Eleven finite instances through n=60 retain the full transition rows, S,
actual reach/reset words and the shortest compression word. A separate set
checker verifies every short word, strong connectivity, full-Q reset and
reachability. The all-n proof is the simulation and padding argument above.
No new Lean theorem or new general upper bound follows from this family.
