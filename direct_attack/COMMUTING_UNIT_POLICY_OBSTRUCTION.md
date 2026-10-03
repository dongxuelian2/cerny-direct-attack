# Commuting permutations do not rescue shortest-phase policy optimality

Status: **REFUTED**, exact ordinary ALL-SOURCE and reverse BFS audit.

The attempted weakening of SINGLE_PERMUTATION_UNIT_POLICY.md was:
"Replace one permutation by any set of mutually commuting permutations,
retaining unitary letters; then the GLOBAL P still equals rt."

Six states suffice. Use letters in this order:

    a=[0,1,2,3,5,4], b=[1,2,3,0,5,4],
    c=[4,1,2,3,4,5], d=[0,1,2,3,1,5].

a and b commute; c is (0->4), d is (4->1). The DFA is SC, synchronizing,
and completely reachable (63 nonempty images). Exact rt=8, P=9; a
shortest reset is c d b c b b c d, ending at1. Full singleton reaching
lengths are [11,8,9,10,10,11], while G is [12,9,10,11,10,11]. Every
singleton is worse than the global rt, so choosing another endpoint
does not eliminate the policy failure. W is [12,9,10,11,13,14].

The critical target S={0,1,4} (mask19) has e(S)=2. Its ONLY winning
larger actual parent is T={0,1,4,5} (mask51), via forward d a. Since
G(T)=5, G(S)=7. But its exact Q-reaching distance is6, attained by
c d b c b b. Parent {0,1,4} then wins the one-letter c phase into
{1,4}; that pair wins the one-letter d phase into {1}, giving P=9.

In inverse reading, the globally optimal prefix for mask19 waits for
b^-2 then c^-1, a three-letter expansion. The shortest expansion uses
a^-1 then d^-1, a different two-letter route with a more expensive tail.
Commutativity does not put the shorter permutation route on the original
path. Consequently the unit insertion in the one-permutation proof cannot
be made at the shorter route without paying for additional permutations.

State minimum6 is certified ONLY in the stated restricted class of TWO
distinct commuting permutation letters plus one to three distinct unit
letters: complete labeled covers at n2..5 test 3,246,14304,486000 inputs,
accepting 3,171,7536,161940, with no P>rt. Ordinary set BFS audits every
small accepted input n<=4; all486000 n5 inputs are checked with two
native algorithms. The counter has ordinary ALL-SOURCE and reverse BFS
e/G/W/forward arrays, and ALL critical parent ties are enumerated.
No state minimum across arbitrary numbers of commuting generators or
arbitrary unit alphabets is asserted. No general alphabet-minimum claim.

The original n6 adaptive search terminated on its first refutation; it
was not a complete cover. Its initial terminal stdout was not persisted,
and that exploratory count is not reported as a durable exhaustive result.
The saved counter and complete smaller covers have literal reproduction
commands, child stdout/stderr, summaries and independent checks.

This does not refute Cerny: rt8<25. It also does not refute a possible
cycle-orbit-sensitive EXTENSION bound for commuting PU alphabets (OPEN).
It refutes the proposed exact policy compatibility bridge. Known
immediate-letter greediness for all PU automata is not shortest-phase
greediness; Szykula--Vorel's DLT2016 Lemma5 remains valid.
