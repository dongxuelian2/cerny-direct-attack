# Complete reachability and modular capacity do not repair union transfer

**REFUTED, state-minimal n=4 over ANY alphabet:** even in a completely
reachable binary DFA, e(S union T)<min(e(S),e(T)) can hold for a proper
union. Thus neither availability of all larger images nor modularity of
rho suffices to transfer the proper-extension union argument to our
image-extension policy.

    a=[2,0,0,1], b=[1,2,3,0],
    S={0,3}, T={2,3}, U={0,2,3},
    e(S)=3, e(T)=3, e(U)=2.

All 15 nonempty subsets are actual images, with independently checked
reach words. The word aa has Q aa={0,2}, strictly inside U. Hence
pre_aa(U)=Q, while pre_aa(S)={1,2} and pre_aa(T)={0,3}. It image-extends
U and neither component. The independently exact costs also show that no
OTHER word of length <=2 can image-extend either component. The obstruction
therefore defeats both same-word and bounded-cost transfer.

At n<=3 every proper union has size <=2. If one component is the union,
transfer is immediate. Otherwise its nonempty components are two disjoint
singletons. If pre_w(U) contains a larger reachable image, its cardinality
is at least 3, so one singleton fiber has size >=2. In a completely
reachable automaton any two states in that fiber form a reachable image,
and the same word image-extends that singleton. This proves minimum n4
over arbitrary alphabets. The fixed-cycle binary scans at n2/3 are checks,
not the basis for arbitrary-alphabet minimality.

The distinction from [Ferens--Szykula, Lemma 3.2](https://arxiv.org/pdf/2208.05956)
is the onto condition. Their properly extending word has a larger
predecessor mapping ONTO the union. Here aa omits state 3 of U. In a
completely reachable DFA rho is cardinality and therefore modular, but
that omitted overlap still gives a negative intersection contribution.
The cited proper-extension lemma remains valid. The precise route requiring
union transfer for maps INTO an image is unavailable even in this stronger
reachability class. This example is not a counterexample to the global
policy square or to Cerny; priority of the specific policy obstruction OPEN.
