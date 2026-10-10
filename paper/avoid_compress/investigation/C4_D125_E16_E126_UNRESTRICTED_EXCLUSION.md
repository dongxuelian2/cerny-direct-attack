# Unrestricted C4/D125/E16 and E126 exclusions

Conditional at (13,9,1), equality ac(S,{3})=12, with B={0}, C={4},
D={1,2,5}, K={1,2} covering P5. The fresh fourth fiber is either
E={1,6} or E={1,2,6}. Both conditional geometries are excluded for
arbitrary finite alphabets. No numerical F value is asserted here.

Put A={3}, H=A union B union C, O=Q-(H union D), e=6, R=Q-K.
The complete fourth classification gives, for each letter ell,
preA in {A,B}, preB in {A,B,C}, preC in {A,B,C,D}, and
preD in {A,B,C,D,E}. These exact preimage groups are pairwise disjoint.
There are 12 individual fields for each E, all included. No binary
incoming capacity bound or binary-active field restriction is used.
There are no omitted Boolean companions in either geometry.
The fresh D and E have suppliers M,T with preC(M)=D and preD(T)=E.
This existence is part of the entry flag, not inferred from a sample.
M collapses D into the singleton C. Thus binom(D,2) is contained in P1.

Disjointness gives three exhaustive letter classes.
(F) preD=D: preA/preB/preC are the three distinct singletons of H;
    H is permuted, D maps into D, and O is permuted.
(M) preD is a singleton in H: preA/preB occupy the other two H
    inputs, forcing preC=D; O is permuted.
(T) preD=E: since E meets D, preC cannot be D, so preA/preB/preC
    are the three H singletons. The free input 5 and O-{e} are
    exactly |O| inputs that map into O. They are outside K and so
    map injectively onto O. Guard 2 may also map into O for E16.
Every letter therefore satisfies O subset R ell. Injectivity outside K
follows from the P5 cover; we use no retracted pair-count bound.

For E126, T sends all of {1,2,e} into D and M collapses D.
Both {1,e} and {2,e} merge under TM, of length two. By the universal
free-image trap (d=2), K covering P3 and e in R ell for every ell
imply that R is forward invariant. Strong connectivity is impossible.

For E16, {1,e} merges under TM. The one-target trap, using the P3
cover, forbids every transition R -> 1. Strong connectivity forces
an edge 2 -> 1: along a path from R to 1, consider the first arrival
at 1; its predecessor cannot be in R or be 1, so it must be 2.
Its letter F must have preD=D: input 2 is not in E16 or any H singleton.
Class F permutes O, so there is x in O with xF=e. The pair {2,x}
then merges under FTM in at most three letters. All letters have x in
R ell. The one-target trap at d=3, using the P4 cover, now forbids
every transition R -> 2 as well. Hence R is forward invariant, again
contradicting strong connectivity.

Only covers P3/P4 are needed in these arguments, and both follow from
the accepted P5 cover. Mandatory-core isolation is not used here.
The E16 argument permits a different sentinel x for target 2; it does
not assume F fixes e or arbitrary prefixes preserve O.

Equivalently, every strongly connected alphabet with the complete
field schema, outside-K injectivity, and D/E suppliers admits a word
merging a pair in R within four (E16) or three (E126). Construct it
directly: an edge R->1 yields LTM with both inputs in R; otherwise
choose F:2->1, an edge L:R->2, and x=F^{-1}(e) in O, obtaining LFTM.
For E126 use any edge R->K and append TM. Universal coverage of O
supplies the other R input of each displayed word.

Independent controls reconstruct all 120 preimage tuples, all 12
fields per geometry, and every individual row at n7,8,9 by a different
recursion. Complete binary ordered alphabets with both suppliers and
seeded larger alphabets are checked by literal graphs and reverse pair
BFS; constructive words are evaluated directly. Sampling is not the
negative certificate: the paper argument covers arbitrary alphabets.
These exclusions, together with the separately proved E6 exclusion,
will imply the whole unrestricted C4/D125 third exclusion only after
an independent composition check verifies all fourth alternatives.
