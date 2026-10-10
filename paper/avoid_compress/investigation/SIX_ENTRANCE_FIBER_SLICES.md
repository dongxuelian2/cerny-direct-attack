# Six normalized entrance-fiber cases at (13,9,1)

Investigation only. This is a complete necessary case admission for a
twelve-step witness, not an exclusion of any of the cases.

9 October update: the geometric inventory below remains intact. The
separate symbolic proofs BINARY_NEAR_EQUAL_ENTRANCE_EXCLUSION.md and
BINARY_SINGLETON_SECOND_ENTRANCE_EXCLUSION.md exclude b3_in for binary
automata. Five binary first-fiber cases remain; all six unrestricted
cases remain. This is not a numerical alphabet separation.

The proved span refinement gives a three-vertex cover H of P5, after
enlarging a smaller cover if necessary. Protected-pair isolation makes
the protected point a isolated even in P7, so H can be chosen outside a.
Relabel H={0,1,2} and a=3. The entrance-fiber proposition gives B outside
a with |S intersect B|=1; some letter maps all of B to a. Thus B is a
clique in P1, and the proved |P1|<=4 gives 1<=|B|<=3. Since H covers P1,
at most one point of B lies outside H.

Permutations within H and within Q minus (H union {a}) leave this
normalization intact. They give exactly the following six orbits:

| Case | Canonical B | Number of labelled B sets |
|---|---|---:|
| b1_out | {4} | 9 |
| b1_in | {0} | 3 |
| b2_mixed | {0,4} | 27 |
| b2_in | {0,1} | 3 |
| b3_mixed | {0,1,4} | 27 |
| b3_in | {0,1,2} | 1 |

The total is 70. Relabel S along with the automaton; its membership is
not otherwise prescribed. For |B|>=2 a letter using B is singular and
can be named first. For |B|=1 the first singular letter may either use B
or fix a, and both are admitted. No permutation companion, fixed whole
kernel, or prescribed rank is imposed on the remaining alphabet.

run_fiber_slices.py applies the first two local equality levels, the
exact five-level image-cover constraint, common B, and two levels of
protected-pair isolation. run_second_fiber_slices.py additionally uses
the independently proved common second fiber C. The latter carries
forward necessary safe-word and pair-trap constraints from the former;
it does not silently convert their timeouts into exclusions.

The geometric orbit normalization works for arbitrary finite alphabets.
The executable batches use two or three letters only. Even a complete
negative for both of these alphabet sizes would not exclude larger
alphabets. Currently the reports are bounded synthesis diagnostics;
their status must not be read as an upper certificate. Ordinary BFS,
including S reachability, is required for every positive.

No claim that the old protected-point-inside-cover slice is empty is
made. It is redundant because a cover outside the isolated point can
be selected. Each of these six cases remains admitted unless a separate
complete proof or certificate excludes it.
