# A forbidden backward crossing and the remaining three-point profile

9 October 2026. Conditional binary equality structure, outside release.

## Backward crossing

At ac(S,{a})=t=n-1, s>=5 in a binary strongly connected synchronizing
automaton, suppose the first two entrances B,C overlap. Name the
moving letter M and the other letter F. The first two entrance lemmas
force M^(-1)(a)=B, M^(-1)(B)={a}, F^(-1)(a)={a}, F^(-1)(B)=C.
Then

  F^(-1)(C) cannot equal B.

Suppose otherwise. If aM belongs to C, the third-entrance argument
gives M^(-1)(C)={a}. Under each letter the preimage of the proper
union {a} union B union C is then contained in that union, contrary
to strong connectivity. If aM is outside C, put U=B intersect C.
Then M^(-1)(U) is empty, since a is the sole predecessor of B and
its image is outside C. Also F^(-1)(U)=F^(-1)(B) intersect
F^(-1)(C)=C intersect B=U. The proper nonempty U has no incoming
transition from its complement, again contradicting strong connectivity.
This proves the assertion without a collision-pair cap or S reachability.

## Rank obstruction when |B|=3 and |C minus B|=2

At the thirteen-state target, |P1|<=4. The moving letter has its
three-point B block and at most one further two-point block, so
rank(M)>=n-3. If M^(-1)(C)={a}, the image of M can contain only a,
beta=aM, and points outside {a} union B union C. Since |B union C|=5,
this would give rank(M)<=n-4. Thus M^(-1)(C) is an outside third
entrance D disjoint from B. The cover H and incomparability with C
force, after relabeling its new outside point to 6,

  D={6} or D={2,6}.

Both have private points for B,C,D, namely 4,5,6. Any other preimage
R of C has indicator alpha*1+beta*chi_B+gamma*chi_C+delta*chi_D.
The constant coefficient is zero: the remainder outside B,C,D has
at least two points outside H, whereas R can contain at most one.
The private-point values beta,gamma,delta are Boolean, and meeting
S once forces beta+gamma+delta=1. Therefore each outside preimage
of C is B,C or D: the third entrance is common in these two cases.

## Forced profile for C={0,2,5}

For the retained b3_mixed_c7 case, F^(-1)(C)=B is excluded above.
It cannot be C: then F would map three points of C into the singleton
B intersect C={0}, adding three collision pairs outside B, contrary
to |P1|<=4. Hence F^(-1)(C)=D. If D={6}, no input under F can reach
B intersect C, since C intersect D is empty. M also misses that
intersection, because aM is outside C. Strong connectivity rules it out.

Consequently every binary equality realization of b3_mixed_c7 must,
up to the stated relabeling, satisfy exactly

  M^(-1)(C)=F^(-1)(C)={2,6}.

This is a necessary profile, not an exclusion of b3_mixed_c7 or a
new F value. The disjoint case b3_mixed_c3 is not covered by the
backward-crossing lemma and must not inherit this profile.
