# Saturated two-guard image trap

Auxiliary obstruction, not an exact value of F. Let n>=4 and let K,Z
be disjoint two-element state sets. Write P_h for the unordered pairs
merged by a word of length at most h. Suppose K covers P4 and every
pair with one endpoint in K and one in Z belongs to P2. Then the
automaton is not synchronizing. The alphabet is any finite alphabet;
strong connectivity and initial-image reachability are unnecessary.

Put R=Q-K and C=Q-Z. Every Rw for |w|<=2 has cardinality n-2,
otherwise w merges a pair outside K. It contains no K-Z pair:
lifting that pair through w and then applying its merging word would
merge a pair outside K within four. An independent set of cardinality
n-2 in the complete bipartite graph between K and Z must be exactly
R or C. Indeed it cannot meet both K and Z, and either complement
has exactly n-2 points. This also holds at n=4.

Consequently every first image of R is R or C. If no letter takes R
to C, R is invariant under every letter. Otherwise choose a letter t
with Rt=C. For every letter l, Cl=Rtl is R or C by the preceding
two-letter argument. Thus {R,C} is invariant, with every image of R
having n-2>=2 states. A reset word for Q would reset R, a contradiction.

Only the explicit K-Z seed pairs and the P4 cover are used. This
lemma must not be inferred from an edge-count cap, nor applied to a
non-saturated bipartite graph. Independent finite controls enumerate
all rows injective on R at n4 and all ordered one/two-letter alphabets
on that domain; an explicit strongly connected nonsynchronizing
control checks that the hypotheses need not contradict connectivity.
