# Excluding the remaining singleton third entrance in B1/C3 mixed

9 October 2026. Symbolic binary exclusion at (13,9,1), outside the release.

Normalize H={0,1,2}, a=3,b=4,B={4},C={0,1,5}, and singleton D={6}.
Suppose ac(S,{a})=12, |S|=9 in a binary strongly connected synchronizing
automaton. H covers P5 and |P1|<=4 by the earlier established reductions.
No initial-image reachability assumption is used.

BINARY_SINGLETON_FIRST_SECOND_COVER.md gives the complete row profile:
the unique C-merging letter L has pre_L(B)=C, pre_L(C)=D and a protected
singleton as preimage of a. The other protected input maps into R=Q minus
({a,b} union C)={2,6,...,12}. F permutes {a,b} and has pre_F(C)=C.
The same proposition makes L noninjective outside C. Its C triangle and
the pair budget therefore leave exactly one outside-C block {2,q},
where q is ordinary. q cannot be 6 since L6 belongs to C and L2 to R.
Normalize q=7 and J={8,...,12}. Write E={2,q}, G=binomial(C,2) union {E}.

All seven R-input blocks of L contain an outside-H point: the other
protected input, E and the five J singletons. They inject into the eight
R targets and miss one target mu. Pulling E back under L gives an outside
pair in two steps if both endpoints are used, so mu is 2 or q.

F's restriction R->R has either singleton blocks, or the sole E block
and other singletons; any other collision would add a pair outside G.
In the latter case its seven blocks all contain outside-H points and
miss one R target nu. Pulling E under F similarly forces nu in E.
Then G contains all kernels and is backward closed under both letters:
L's preimage of C is a singleton and its preimage of E is empty at one
endpoint; F's preimage of C is C, and its preimage of E is empty at one
endpoint. The pair {a,b} outside G can never merge, contradicting
synchronization. Thus F restricts to a permutation of R.

Only input 2 among R lies in H. Pulling E under F therefore forces
F2 in E; otherwise an outside pair merges by F L. If F2=q and Fq differs
from 2, then F^2(2) is outside E. Both points of F^(-2)(E) are outside H
and merge by F^2 L, of length three. Hence Fq=2. F now permutes E, so
the same graph G is backward closed under F, and the L argument is
unchanged. Synchronization is again impossible.

The last possibility is F2=2. If mu=2, no L input maps to 2 and only
the self-loop 2F=2 enters that state, contrary to strong connectivity.
Thus mu=q. If Fq=q, the same incoming-self-loop contradiction holds at
q. Otherwise x=F^(-1)(q) differs from q and belongs to R minus {2}.
Both output points 2,x are used by L and have outside-H predecessors
y,z. Their image under L is {2,x}, under F is E, and the final L
merges them. The word L F L has length three, contradicting the cover.

All possibilities are excluded symbolically. The argument leaves F's
C map arbitrary, including singular maps, and leaves all unspecified
ordinary injections and permutations arbitrary. The independent audit
checks the full R-kernel partitions and permutations, graph closure, and
an entire small normalized row family by literal forward pair BFS.
These controls do not replace the thirteen-state symbolic argument.

This removes b1_out_c5_third2. With the earlier sole-new-point-2 proof,
B1/C3 mixed retains D={0,6},{2,6},{0,1,6},{0,2,6},{0,1,2,6}. These
are original inventory labels; the kernel partner q here is a distinct
marked point, not the singleton D point 6. Binary typed third cases
decrease to 168 with 927 letter pairs. Joint cases stay 26/43 and both
extrema stay [11,12]. No new F value or alphabet separation is asserted.
