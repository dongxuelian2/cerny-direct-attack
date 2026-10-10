# A closed merging block

Let D be a nonempty proper state subset. Suppose for every letter ell:
(1) every immediate kernel pair lies in binom(D,2), and
(2) ell^{-1}(D) is contained in D or has at most one state.
Then every pair mergeable by any word lies in binom(D,2). The automaton
is not synchronizing. This criterion holds for arbitrary finite
alphabets and needs no strong connectivity or initial-image assumption.

Proof. The pair recurrence is P_(h+1)=P1 union the letter inverse pairs
of P_h. Condition(1) gives P1 subset binom(D,2). If a distinct pair
maps to a distinct pair in D, its endpoints lie in ell^{-1}(D). By(2)
they must both lie in D; the alternative singleton preimage cannot
contain a distinct pair. Induction proves P_h subset binom(D,2).
A pair with an endpoint outside proper D never merges. If some letter
collapses all D, equality P_h=binom(D,2) holds for every h>=1.

At(13,9,1), B0,C4,D125,E6, all outside preD fibers are precisely B,C,D,E;
preD can also be A={3}. Only D has cardinality greater than one.
K12 covers P1 and is contained in D, so every letter is injective
outside D. A letter M supplying preC=D collapses D into C4 and has
no mixed D/outside kernel. The common-block trap excludes both letters
having preC=D. Strong connectivity requires incoming coverage of all
three D states. If both preD fibers were singletons, only two D states
could have incoming edges. Hence the other letter F must have preD=D.
The required E6 supplier is M, with preD=E6. Exact preD=D for F means
D/outside images are disjoint, and its only kernels are inside D.
Thus F^{-1}(D)=D and M^{-1}(D)=E6, satisfying the closed-block criterion.
The entire binary E6 branch is therefore excluded on paper, independently
of the complete row scans. This does not exclude unrestricted E6,
where additional letters with other field columns are admissible.

The nine formal binary E6 field pairs are independently checked to
have exactly the M/F structure above. Finite controls normalize D012,
c3,e4, enumerate all M collapsing D to c with preD=e and injectivity
outside D, and all F with preD=D and injectivity outside D, at n5..7.
Every ordered M/F pair is tested by reverse pair BFS, with separately
selected direct forward pair checks; some controls are strongly connected
but none synchronizes. Boundary controls show failure when the kernel,
preD or proper-subset hypothesis is omitted. These finite controls
support the uniform proof; they are not an all-parameter F theorem.
