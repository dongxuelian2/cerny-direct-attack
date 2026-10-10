# Finite independent-image trap

Auxiliary obstruction only. Let G be a graph on Q whose edges belong
to P_h, h>=1. Let K be a state set, a=|Q-K|>=2, and let N be the
number of G-independent a-element subsets. Suppose K covers P_(h+N).
Then the automaton is not synchronizing, for any finite alphabet.
Neither strong connectivity nor a reachable-image hypothesis is needed.

Put R=Q-K. The cover makes R independent in G, so N>=1. Every Rw
for |w|<=N has cardinality a: a collision would merge a pair outside K
within N<=h+N. Such an image is independent in G. Otherwise lift an
edge of G to two R inputs and append its merging word of length at
most h, contradicting the P_(h+N) cover.

All these short images belong to the N-element family I of independent
a-sets. Let F be the images reached within N-1. If F is not closed
under letters, some image X outside F is reached in N steps (a
shorter prefix would already put X in F). Its shortest reaching word
has length N. The N+1 prefix images along this shortest path are
distinct, yet all belong to I. This is impossible. Thus F is closed,
every reachable image of R belongs to I, and all have size a>=2.
A reset word for Q would reset R, which is impossible.

The count is of independent sets of the precise size a, not edges,
span dimension, or independent sets of every size. No claim is made
that every member of I occurs. Singleton R is excluded essentially.
This is an elementary subset-graph obstruction, with no priority claim.

The cases used in C4/D15 have a=n-2 and isolated states outside the
displayed active graph. Literal independent-set enumeration confirms:

* triangle126 with pendant edge15: N=2 (omitted pairs12 and16);
* path5-1-6-2: N=3 (omitted pairs12,16,56);
* path6-1-5-2: N=3 (omitted pairs12,15,56);
* star1-{5,6} and disjoint edge2-x, x not in {1,2,5,6}: N=2
  (omitted pairs12 and1x).

In each case every independent n-2-set includes all isolated states;
the count therefore does not depend on their number. With edges in
P2, N<=3 fits the established P5 cover. This lemma is a necessary
conditional obstruction, not an all-parameter formula or a new F value.
