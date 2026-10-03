# Exact policy for one permutation and unitary letters

Status: **PROVED (paper proof)**, with independent finite model checking below.
No new general reset upper bound, no Lean verification, novelty **OPEN**.

Let A be a strongly connected synchronizing complete DFA with n>=2 states.
Its alphabet consists of ONE permutation a (arbitrary cycle structure) and
any finite nonempty collection of unitary letters u=(s->t), s!=t, fixing
every other state. Duplicate letters are immaterial. Composition is on
the right: S(xy)=(Sx)y. Inverse actions are taken in the opposite order.
Identity a is allowed. Pure unitary alphabets are covered by adjoining an
identity letter, which never occurs in any shortest reaching/extension word.

Write R={Qw:w in Sigma*}. For nonempty S in R, let
e(S)=min{|v|:Tv subset S, T in R, |T|>|S|}. All eligible larger T at this
minimum participate in G(S)=e(S)+min G(T) and W(S)=e(S)+max W(T), with
G(Q)=W(Q)=0. Let d(Q,S) be the shortest word reaching S EXACTLY.

**Theorem.** R contains every nonempty subset, and

    G(S)=W(S)=d(Q,S) for EVERY nonempty S subset Q.

In particular P=min_q G({q})=rt(A). Every shortest-extension parent choice
is optimal for its fixed target S. This is not a claim that all endpoint
states have the same reset length, nor that max_q W({q}) equals rt(A).

## 1. Complete reachability, proved without assuming arbitrary predecessors

Let o be the order of a. Form the directed graph Gamma whose edges are
all conjugates of the unitary edges by a^t, 0<=t<o. The word
a^t u a^(o-t) is a unitary map with the corresponding conjugated edge.
Thus a acts as an automorphism of Gamma. Let Z be the union of terminal
strongly connected components of Gamma. This nonempty set is closed
under a and all units. Strong connectivity of A forces Z=Q. Consequently
EVERY Gamma component is terminal and no Gamma edge joins components.

Each unit preserves every component, while a permutes them. If Gamma
had two or more components, states in different components would remain
in different components under every word, contradicting synchronization.
Gamma is therefore strongly connected.

For any desired nonempty S, measure the shortest Gamma distance to S.
For each q outside S choose an edge q->p decreasing that distance by one.
Apply the corresponding conjugated units in decreasing distance order.
They fix all roots in S and move every other state to some root. This
gives an actual word taking Q onto S. No short-length estimate is used.
This argument also establishes the known PU complete-reachability fact;
the same argument works with a finite permutation group in place of <a>.

## 2. Shortest inverse trajectories and proper reaching

Put D(S)=min{|w|:Qw subset S}. This is finite. Consider a shortest inverse
trajectory from S to Q. For a unit u=(s->t), its inverse either adds s
(t in S,s notin S), deletes s (s in S,t notin S), or fixes S.
If an occurrence fixes or deletes, omit it. Every preimage map is
inclusion-monotone, so the resulting trajectory still ends at Q and is
strictly shorter. Thus EVERY unit in a shortest trajectory grows by one;
permutations preserve cardinality. There are exactly n-|S| units.

Each growing inverse unit is proper: u(u^-1(S))=S. The same holds for
permutations. Composing these equalities shows that the associated forward
word reaches S exactly. Hence D(S)=d(Q,S), including S=Q (both zero).

## 3. Characterization of ALL shortest extension parents

An extension word of minimum length e(S) can have no fixing/deleting unit:
omitting it leaves a larger final preimage by monotonicity, contradicting
minimality. Nor can it have a growing unit before its last letter, because
that prefix already extends S. Its inverse sequence therefore is

    a^-1 repeated t0 times, followed by c^-1,

where t0 is the earliest nonnegative time at which ANY unit grows the
rotated S. Therefore e(S)=t0+1. Complete reachability from section 1 is
essential when identifying actual-image capacity with full preimages.

For every winning forward word c a^t0, its full preimage T has size |S|+1
and is actual. An eligible winning larger image must be contained in
this T; its larger size forces equality. Thus this describes ALL parents,
without ignoring any capacity tie or allowing an unreachable subset.

## 4. Exchange for an ARBITRARY shortest extension choice

Fix ANY such c and t0. Take a shortest inverse S-to-Q trajectory of length
L=D(S). Before its first unit it follows the same unique path a^-t, with
t>=t0. Insert c^-1 after the first t0 inverse permutation steps, leaving
all original letters in place. At insertion the new trajectory contains
the old set. Inclusion remains true through every later preimage.

Every original unit grew on the old trajectory, so its target t belongs
to the new set as well. It therefore grows or fixes the new set; it cannot
delete. The inserted unit grows by one. The final set contains Q and is
Q. There were n-|S|+1 units, and exactly n-|S| actual increases; exactly
ONE original unit must be neutral. Delete that occurrence. It is after
the insertion; deleting a neutral operation leaves the later trajectory
unchanged. The resulting word has length L and starts with the prescribed
inverse phase a^-t0,c^-1.

Its remaining inverse suffix takes T to Q in L-e(S) steps. Conversely
any T-to-Q inverse word can follow that phase. Consequently

    D(S)=e(S)+D(T) for EVERY winning larger parent T.

Downward induction on |S| now gives G(S)=W(S)=D(S)=d(Q,S). This avoids
an unproved lexicographic convergence assumption. It works for t=t0 too,
and for a chosen c different from the original first unit. The sole
permutation assumption ensures the earliest rotation lies on the ORIGINAL
permutation prefix; with multiple permutations that implication fails.

## 5. Sharp limitation: two permutations

Four states, letters

    a=[0,1,3,2], b=[1,2,0,3], c=[2,1,2,3].

This is SC, synchronizing, completely reachable; rt=6, P=7. Its shortest
reset is c b c b a c, ending at 2. The optimal last phase c has parent
{0,2}. That pair has e=2 and unique winning parent {0,1,2}, via forward
word c b. Its tail cost is G({0,1,2})=4, so G({0,2})=6, whereas its true
reaching length is 5 (c b c b a). Then G({2})=1+6=7>6.
All three endpoint alternatives are checked; the failure is GLOBAL P,
not only a badly chosen endpoint or tie. See the full saved arrays and
independent ordinary forward/reverse BFS certificate.

State minimum is four WITHIN arbitrary permutation/unit alphabets:
all nonempty subsets of the 6 distinct permutations and 6 distinct units
at n=3 are exhausted (3969 designations), and at n=2 (9). Alphabets with
no units cannot synchronize for n>=2. Pure units attain every target in
n-|S| steps by the forest construction, so are exact as well. Duplicates
do not affect shortest costs. This is a finite complete class minimum,
not an unrestricted-DFA minimum claim. Alphabet minimum three follows
on all n: two permutations cannot synchronize, one permutation plus a
unit is covered above, and pure units are exact. n=1 is trivial.

## 6. Validation and attribution

The machine-readable summary is authoritative. Specifically n2..6
test 6,189,20475,9450,49775 inputs, accepting 4,117,14780,2160,7751.
n<=4 cover every nonempty unit subset and every permutation cycle type;
n5/6 cover unit subsets of sizes 1,2,3 only. Every accepted FULL array
has G=W=forward, and every input is checked with two native algorithms.
The independent checker replays ordinary reverse BFS for every n<=4
designation and retained larger samples; separate ALL-SOURCE BFS audits
the counterexample and retained arrays. The separate positive-polynomial
proof SINGLE_PERMUTATION_UNIT_SQUARE.md now establishes e<=n-c+1 and the
square bound for all n; finite patterns alone are not used as proofs.
No large permutation-order running time is bounded by the exchange proof.

Szykula--Vorel, *An Extremal Series of Eulerian Synchronizing Automata*
(DLT 2016), section 3, Proposition 3 and Lemma 5, already prove straight
shortest words and immediate-unit greediness for ALL PU alphabets:
https://ktiml.mff.cuni.cz/~vorel/bib/VO7conf.pdf . The deletion/insertion
mechanism here rederives that known method. Phase-cost and all-target,
all-tie exactness with one permutation is an explicitly restricted
corollary/extension; its publication priority is OPEN, not claimed new.
Ferens--Szykula (2026), DOI 10.1145/3798283, confirms known PU complete
reachability and existing quadratic class bounds. None is a new general
Cerny bound. The four-state counter distinguishes immediate-letter
greediness (known to hold even there) from shortest-WORD phase policy.
COMMUTING_UNIT_POLICY_OBSTRUCTION.md further refutes replacing the one
permutation by mutually commuting permutations: two such letters and two
units give rt8,P9 at n6. Commutativity does not make the shorter branch
a prefix of the original permutation path. Its exact class minimum and
finite scope are stated separately; the one-permutation proof is unaffected.
