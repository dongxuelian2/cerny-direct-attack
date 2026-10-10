# Singleton B and a two-point C completing the H-cover

9 October 2026. Conditional binary exclusion at (13,9,1), outside the
article/release. Assume ac(S,{3})=12 with |S|=9, strong connectivity
and synchronization. Normalize H={0,1,2}, B={0}, C={1,2}.

All short images contain 3,0 through depth ten and meet C once
through nine. The established H-cover of P5 and isolation of 0 in
P6 imply that C itself covers P5: an edge cannot use 0. Thus no pair
outside C merges within five letters. Each letter is injective on
Q minus C. Also both protected states 3,0 are isolated in P6.
Put R={4,...,12}, J=R minus {4}. Initial reachability is unnecessary.

The complete third inventory has exactly two orbits, D={4} and
D={1,4}, with fourteen and three earlier letter-profile pairs. They
are common third fibers in this geometry. To see this directly, an
outside preimage of C lies in span{1,chi_B,chi_C,chi_D}. The remainder
outside B,C,D meets S at least five times, so its Boolean coefficient
is zero. The private cells B, C minus D, D minus C make the other
coefficients Boolean. Since S meets B,C,D once, their sum is one.
Thus every preimage of C is A={3},B,C or D; no extra Boolean fiber
is omitted. D is a collision clique within two steps, since C itself
is an immediate collision pair under a C-merging letter.

## D={1,4}

The C-merging letter L has pre(B)=C, pre(C) a protected singleton,
and pre(3) the other protected singleton. Write p for its protected
predecessor of delta in C. It maps R to R bijectively: all nine R
inputs are outside C, their outputs lie in the nine-state R, and
outside injectivity forbids collisions. The other letter F permutes
{0,3}, has pre(C)=D, and sends {2} union J into R. Its restriction
to J is injective. These descriptions cover all three admitted pairs.

If delta=1, choose x=L^{-1}(4) in R. The protected pair {p,x}
follows L to {1,4}, F into C, and L to 0. Word L F L merges it
within three letters. Hence delta=2.

Write gamma=F4. If gamma=2, incoming C targets force F1=1;
state 1 then has only its own F-loop and no other incoming transition,
contradicting strong connectivity. (F1=2 would leave 1 with no input.)
Thus gamma=1. If some x in J has Fx=4, the pair {4,x}, outside C,
follows F to D, then F L merges it in three letters. Hence F(J)
avoids 4 and is exactly J, bijectively.

If F2 is in J, let r be its J predecessor under F and choose
x=L^{-1}(r) in R. Then {p,x} follows L to {2,r} and merges by F
in two letters. Therefore F2=4. Finally choose x=L^{-1}(4) again.
The protected pair {p,x} follows L F^2 to {1,F1}, contained in C
or already singleton. A further L merges it. Word L F^2 L has length
four, contradicting protected-pair isolation. All possibilities fail.

## D={4}

Put G={the pair12}. If both letters merge C to B, each has only
that immediate kernel: outside-C injectivity and pre(B)=C exclude
any C-to-outside collision. Each pre(C) is a singleton in {A,B,D},
so G is backward closed. This is incompatible with synchronization.

Otherwise let L be the C-merging letter and F the other one. If
pre_F(C)=C, its kernel is contained in G: C maps into C, protected
states permute, and R maps bijectively into R. The fresh D supplier
must be L, with pre_L(C)=D. Its kernel is exactly G, and its preimage
of C is singleton. Again G is backward closed and synchronization fails.

The remaining possibility is pre_F(C)=D. L has a singleton preimage
of C in {A,B,D}; write delta for its output. Incoming C targets force
F4=beta, where {delta,beta}=C. F permutes {0,3}, sends C union J
into R, and is injective on J. Under L every R output has an
outside-C predecessor: its R-inputs are R if pre_L(C) is protected,
or J union the unused protected input if pre_L(C)=D. There are nine
such outside-C inputs into R, mapped bijectively. Its sole predecessor
of delta is outside C too (protected or4).

If Fdelta=Fq for any q in J, choose outside-C L-predecessors of
delta and q. Their pair merges by L F, contradicting the C-cover.
Thus Fdelta has no J predecessor. If Fdelta=Fbeta, then the only
immediate F kernel is G, as is L's; singleton preimages of C again
make G backward closed. Exclude this nonsynchronizing alternative.

Consequently Fdelta is distinct from every other R-input output.
There are ten inputs C union J into nine R targets, with F injective
on J. Thus Fbeta=Fq for a unique q in J. This is the extra kernel;
its nine blocks map bijectively onto R. Put r=Fdelta; then F(J)=R
minus {r}. If q is not r, choose an outside-C F-predecessor x in J
of state q. The pair {4,x} follows F to {beta,q}, and a second F
merges it, contradicting the cover. Hence r=q.

Let u=L^{-1}(delta), and choose v=L^{-1}(4), both outside C and
distinct. Their pair follows L to {delta,4}, F to {q,beta}, and F
to a singleton. Word L F^2 has length three. This final contradiction
exhausts all fourteen admitted D={4} profile pairs. The unused
protected input mapping into R is included; no ordinary permutation
or injection is fixed in any case.

## Scope and independent controls

Both profiles are excluded, hence the whole binary joint b1_in_c4.
No unrestricted exclusion is made. No F value or alphabet separation
follows; both extrema at (13,9,1) remain in [11,12]. This statement
is only the conditional thirteen-state equality exclusion, not a
generalization of the earlier k>=3 covered-C proposition to k=2.

The checker independently regenerates the outside-C injective kernel
cover, preserving every original profile pair and every possible
ordinary output assignment symbolically. Complete normalized smaller
row controls verify the explicit word witnesses and backward-closed
graphs. Their local pair premises are imposed, not inferred from
equality for smaller subset sizes. Complete thirteen-state single-letter
injection/permutation controls verify the predecessor-port arguments;
none of these is a full thirteen-state transition-pair scan.

The two profiles have170/42 row-kernel patterns and497/54 compatible
kernel pairs. Seventeen singleton-D kernel configurations already have
the universal backward-closed G obstruction. Complete smaller controls
have752,11,952,301,824 row assignments at n=6,7,8. The checker evaluates
each explicit proof word literally, and separately checks all inverse
pairs of G in the closed cases. All362,880 R-output permutations and
all362,880 J-output injections at n=13 verify the predecessor ports,
including the unused protected input in the moving-L row. No thirteen-
state pair of ordinary permutations is fixed or assumed representative.
