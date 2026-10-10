# Unrestricted-alphabet B0/C4/D125/E6 exclusion

Conditional at(13,9,1), ac(S,{3})=12, B0,C4,D125,E6, strong connectivity
and synchronization. This is a fourth-geometry exclusion, not an F value
or alphabet separation. It does not exclude E16/E126 or the whole D125
third geometry for unrestricted alphabets.

Write A={3}, B={0}, C={4}, D={1,2,5}, O=Q-(A union B union C union D),
e=6, K={1,2}, J={0,3,4,6}. The complete Boolean one-count classification
has preA in{A,B}, preB in{A,B,C}, preC in{A,B,C,D}, and preD in{A,B,C,D,{e}}.
There are16 individually admissible fields, not just the eight binary-active
fields. Each letter is injective outside K because K covers P5. J is
mandatory through seven, hence isolated in P7. No binary capacity bound
is used below.

The output groups A,B,C,D,O are disjoint, so the first four preimage groups
are disjoint as well. This gives the following exhaustive letter classes.

(1) If preD=D, the preimages of A,B,C are three distinct singletons in
A union B union C. The letter permutes these three states, maps D into D,
and permutes O (outside-K injectivity on |O| inputs). All kernels are in D.
Call these letters D-preserving.

(2) If preD is a singleton p in A union B union C, preA/preB use the
other two singletons, forcing preC=D. The letter collapses D into C,
permutes O, and has no mixed D/outside kernel. Its image contains all O.

(3) If preD={e} and preC=D, the two singleton preA/preB groups leave
one protected input and O-{e} as the |O| free inputs of the O-output group.
Injectivity outside K makes these map bijectively onto O. Kernels lie in D.

(4) If preD={e} and preC is a singleton, preA/preB/preC permute A union
B union C. All D inputs map to O. The free D input5 and O-{e} are exactly
|O| free inputs mapping injectively onto O, so the image contains all O.
Any kernel outside D is a mixed pair {k,x}, k in D, x in O.

Thus every letter either preserves D or enters D from exactly one p in J.
Every entering letter L has QL containing all O; D-preserving letters
permute O. All kernels outside D can occur only in class(4).

Suppose some class(4) letter T merges k in D with x in O. Strong connectivity
makes every D state reachable from Q-D. On any such path consider the last
entrance into D. That entrance uses a letter L from p in J; the remaining
suffix stays in D and hence uses only D-preserving letters. For k choose
a shortest such suffix u. Since D has three states, |u|<=2. Then pLu=k,
and QLu still contains O because QL contains O and u permutes O. Choose
q with qLu=x. Since k is in D and x is in O, q is distinct from p.
The pair {p,q} merges under LuT, length at most four, contradicting J's
P7 isolation. Notice that this uses surjectivity of QL onto O, not a
claim that every entering letter preserves O. Arbitrary entering-letter
prefixes are not asserted to preserve O.

Consequently every letter's kernels lie in D. All preD fibers are D or
singletons, so CLOSED_MERGING_BLOCK.md traps every mergeable pair inside D.
Synchronization is impossible. This proves the unrestricted E6 exclusion.

The counting proof of the four classes works for any |O|>=1; the auxiliary
abstract statement uses the same three-state D, three protected singleton
states, e in O and outside-K injectivity. Strong connectivity plus
synchronization under this abstract field schema forces a pair touching J
to merge within four. We make no global F claim from that statement.

Independent controls reconstruct all120 preimage tuples and their16 exact
fields, every individual row at n7,8,9 by a different input recursion,
and materialize short merging witnesses in sampled larger alphabets.
A literal strongly connected synchronizing n8 control has earliest J-pair
merging distance four, so dropping the P4 isolation condition would be
invalid. This is a structural boundary control, not an attaining F example.
All source and sample hashes are retained. The paper proof, not sampled
failures, is the all-alphabet certificate.
