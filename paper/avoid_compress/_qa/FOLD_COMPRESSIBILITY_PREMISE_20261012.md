# A compressibility premise for the necessary folded model

Auxiliary premise audit only. No numerical maximum, alphabet separation,
new construction or synchronization of the fold is claimed.

Let a complete strongly connected N-state automaton have a subset T of
size t>=2, with alpha in T. Assume alpha is avoidable from Q and
ac(T,{alpha})>N-t. Then T is compressible, even if the full automaton
is not synchronizing and T is not a reachable image.

To prove this, take a word z with alpha not in Qz and consider its state
transformation f. The f-orbit of alpha has a tail of length h>=1 followed
by a cycle of length d>=1: alpha cannot be on the cycle, because it has
no f-predecessor. Set p=f^d(alpha). Then p differs from alpha, and
f^h(p)=f^(h+d)(alpha)=f^h(alpha). Thus z^h merges alpha and p.

Strong connectivity supplies a path from a point of T to p of length
at most N-t. Indeed, a shortest path from the set T to p has no repeated
vertices, and after its initial vertex every vertex lies outside T.
Let its label be v. The assumed lower bound makes v safe: Tv contains
alpha and p and has t points. Appending z^h compresses Tv. Hence T is
compressible. This is only an existence argument; it gives no useful
short upper bound and does not assert that every pair merges.

In the qualified fold at N=13,t=9, ac=12, the previous avoidability and
strong-connectivity premises therefore suffice for eventual
compressibility. The existing transversal/rank-word lemma may now be
applied to T: no word of length at most six can have rank at most nine.
For rank below nine it compresses T directly; for rank nine the existing
bound is N-t+|u|+1<=11. This is exactly the previously used conditional
rank-word rule, with its missing folded compressibility premise supplied.

No historical certificate is enlarged or reinterpreted by this note.
The new premise does not repair the unproved synchronization or reachable
image status of the folded model. The proof uses ordinary functional
graphs and shortest paths; no novelty or priority claim is made.

The companion audit enumerates every unordered binary transition pair
through four states, including repeated letters. It checks avoiding
words, a literal merging partner, all applicable subsets and paths, and
eventual compression by independent ordinary subset BFS. These controls
support the argument; they are not extrapolated as a finite upper proof.
