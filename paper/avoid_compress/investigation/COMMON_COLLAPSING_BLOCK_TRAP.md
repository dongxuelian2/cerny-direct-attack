# A common collapsing block traps the pair closure

Let a complete deterministic automaton have n states and a nonempty
finite alphabet. Let2<=|D|<n and c not in D. Suppose every letter has
exact preimage ell^{-1}({c})=D, and some K contained in D is a vertex
cover of P2, the pairs mergeable within two letters. Then

    P_h = binom(D,2) for every h>=1.

In particular the automaton is not synchronizing. Strong connectivity
and initial-image reachability are not needed for this necessary cut.

Proof. Every letter collapses D to c. A mixed D/outside-D pair cannot
collide, by the exact-preimage assumption. An outside-D pair cannot
collide because both endpoints lie outside K, which covers P1 subset P2.
Thus P1 is precisely binom(D,2), and each letter is injective on Q-D.
For a letter ell, R=ell^{-1}(D) is disjoint from D because c not in D.
If |R|>=2, a pair outside K maps into D and is then merged by any
second letter, contrary to the P2 cover. Hence |R|<=1 for every letter.
The usual pair recurrence P_(h+1)=P1 union all letter inverse pairs
of P_h now stays at binom(D,2): no distinct pair can map into D.
Since D is proper, at least one pair involving Q-D never merges.
This proves the conclusion for arbitrary finite alphabets.

All assumptions are essential to this proof. Omitting the P2-cover
condition admits[2,2,3,3],D01,c2, reset aa. Omitting c outside D admits
[0,0,1],D01,c0,K01, reset aa. Omitting the common-preimage condition
admits a=[2,2,0],b=[1,2,0],D01,c2,K01, reset aba.
The independent checker verifies these literal boundary controls.

At(13,9,1) in the B0/C4 joint, K12 covers P5 and hence P2. For D12
or D125, K is contained in D and4 is outside D. Therefore the two
letters cannot both have preC=D. In each complete eight-row parent
inventory this excludes exactly five originally admitted odd/odd
pairs: (1,7),(3,5),(3,7),(5,7),(7,7). The cut also forbids any larger
alphabet in which every letter has that same preC; it does not exclude
those third geometries for unrestricted alphabets, where a different
letter can be included. No numerical alphabet separation follows.

The uniform proof above is authoritative. Independent finite checks
normalize c=n-1 and D=0..d-1 at3<=n<=6,2<=d<n. They enumerate every
outside-D injection into Q-c and every two/three-letter tuple after
the necessary |pre(D)|<=1 condition. Relabelling supplies every labelled
choice. Literal pair closure and selected separate forward pair searches
confirm the trapped clique; these finite checks do not replace the
all-n proof. Both numerical extrema at(13,9,1) remain unclassified.
