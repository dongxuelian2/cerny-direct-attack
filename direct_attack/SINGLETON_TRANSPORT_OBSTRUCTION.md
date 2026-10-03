# Singleton target transport does not preserve greedy policy cost

**I6 — REFUTED, binary-minimal n=4 in the SC synchronizing scope.**
The proposed directed-edge inequality is G({q x})<=G({q})+1 for every
state q and letter x. Such an inequality would let a good reset target
control the costs at other targets. It is valid for the Cerny policy
formula but fails generally.

    a=[0,0,1,1], b=[1,2,3,0], q=0, x=b.

All singleton best/worst costs are [2,4,5,6]. The actual reset word aa
has length 2 and ends at 0. Appending b resets to 1 in length 3, while
G({1})=4>G({0})+1=3. Independent ordinary-set forward BFS gives exact
shortest reset-to-1 distance 3. The global policy minimum is still 2.

The failure mechanism is explicit. For target {1}, the shortest extension
word is a, of length 1, with reachable larger preimage {2,3}; that
image's policy tail costs 3. The word ab of length 2 can instead choose
the reachable image {0,1}, whose policy tail costs 1. Taking a longer
first phase saves overall transport cost. The appended reset aab is
therefore not a shortest-extension policy for its final target.

Complete binary covers at n=2 and n=3 pass (9 and 182 overlapping inputs).
The n=4 cover stops at its first refutation after 873 inputs; it is not
a complete four-state failure enumeration. Duplicate letters reduce to
unary and cannot be SC synchronizing for n>=2. No arbitrary-alphabet
minimality is asserted. Stored full arrays are independently checked by
inverse BFS, and check_singleton_transport.py separately verifies the
edge, both full-Q words and the exact target distance.

## The unrestricted transport recurrence is exact but not a bound

Let delta(T,S) be the shortest word sending T into S, and define
F(Q)=0 and F(S)=min_{reachable T, |T|>|S|}(delta(T,S)+F(T)).
Then F(S) equals the shortest full-Q transport distance D(Q,S).
The construction of phase words gives D<=F. The allowed choice T=Q
gives F<=delta(Q,S)=D. This identity is valid for every reachable S
in a synchronizing automaton, but supplies no bound in n: the direct
Q choice already contains the original shortest-word problem.
The unresolved task is a cheaper globally compatible family of phases,
not merely removing the shortest-phase restriction from exact search.
