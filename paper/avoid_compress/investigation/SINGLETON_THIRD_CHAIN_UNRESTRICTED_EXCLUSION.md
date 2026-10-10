# Complete singleton third-chain obstruction at (13,9,1)

Assume strong connectivity, synchronization, |Q|=13, |S|=9 and
ac(S,{a})=12. Then c(S)>=12, m=4, dim V_i=i+1 through i=11,
and every point mandatory through depth4 is isolated in P7.
Suppose a two-state K covers P5, and the first three entrances
B={b},C={c},D={d} are distinct singletons outside {a}.
Their common exact fields are pre(a) in {a,B}, pre(B) in {a,B,C},
and pre(C) in {a,B,C,D}, by the established singleton Boolean
inventory. These conditions are impossible for arbitrary alphabets.
S need not be an initial reachable image for this auxiliary obstruction.

## Abstract singleton-inverse version of the kernel obstruction

The graph argument in TWO_COVER_PROTECTED_KERNEL_OBSTRUCTION.md
uses S only to prove that every singleton fiber pre_f(e) is a P7
isolate. Therefore its same matching, path and growth proof gives:
in a synchronizing n>=4 automaton with a two-state P5 cover, if
e is its unique immediate pair, every singleton pre_f(e) is a P7
isolate, and some letter collapses e to a state outside e, there is
a contradiction. No strong connectivity or S premise is needed
once the singleton-isolation condition is given. Distinct-edge
inverse graphs and immediate kernel pairs remain separate.

## Two finite-dimensional facts

First, let a seven-state core J be mandatory through depth4, and
let a pair e outside J be one-count through depth4. If e is the
unique immediate pair, any singleton pre_f(e)={p} has p outside e:
the two e inputs have the same output, so either both belong to
that vertex fiber or neither does. Safety and the one-count property
make p mandatory through depth3. If p were outside J, every image
through3 would be J plus p plus one e endpoint, because |S|=9.
There would be at most two such images, giving dim V3<=2, whereas
equality gives dim V3=4. Thus p is in J and is P7-isolated.
The abstract singleton-inverse obstruction excludes any supplier
collapsing this pair to a singleton of J outside e.

Second, an eight-state core J mandatory through4 is impossible.
Every image through3 is J plus one variable state. These rows are
linearly independent for distinct variable states, so dim V3=4
forces exactly four distinct variable states. For a letter f and
target j in J, its exact fiber meets every one of these images once.
If it meets J, it can contain only that core point: any further
point would give an immediate pair incident to a P7 isolate.
If it avoids J, it contains all four variable states, hence has
at least six immediate kernel pairs, contradicting unique P1.
Every j consequently has a singleton preimage in J under every
letter. Each letter permutes J, contradicting synchronization.

## Growing the singleton chain without assuming common fibers

Write J={a,b,c,d} initially. The entrance depth of the last singleton
is8. Every letter's preimage of that singleton is nonempty and meets
every image through7 once. A fiber meeting J must be a singleton
of J, because J is P7-isolated. If every such fiber lay in J, J
would be a proper backward-closed set, using the earlier exact
fields; strong connectivity forbids this. Choose a fresh fiber R
outside J. Since it maps to a singleton, unique P1 forces |R|<=2.

At one-count depths7,6,5 a pair R is impossible by the uniform
kernel obstruction: it maps outside itself, c(S)>=m+8, and its
one-count prefix is at least m+1. A singleton R in K is impossible
by mandatory P7 isolation and the one-cover compression floor.
Thus each surviving fresh fiber is a singleton outside J union K.

It remains essential to control all other letters' fibers, not just
this chosen supplier. After adding a fresh singleton, for each of
the first three new depths7,6,5 the annihilator has exactly the
dimension of the known singleton columns. On Q minus {a}, its
basis is 1 plus the indicators of the known outside singleton
states. A Boolean column in this span has ordinary-cell value c0
in {0,1} and singleton values v_i in {0,1}; its one-count condition
is (8-l)c0+sum v_i=1, with l=4,5,6 known outside singletons.
For c0=1 the left side is at least2; for c0=0 exactly one v_i is1.
Hence every outside one-count fiber is an already known singleton;
the {a} fiber is allowed separately. This checks all companions and
suppliers and proves the required common-column conclusion here.
It is not extrapolated to pair or overlapping-fiber geometries.

Accordingly the core grows from4 to5 to6 to7 singletons, mandatory
through depths7,6,5 respectively, while every earlier preimage
stays in the enlarged core. A fresh fiber of the last singleton
exists again by backward closure. It is outside the seven-state core,
has size at most two, and is one-count through4. If it is a pair,
the first finite-dimensional fact and abstract obstruction exclude
it. If it is a singleton, the enlarged eight-state mandatory core
is excluded by the second fact. No case remains.

## Scope and controls

The ordinary-cell complement becomes a valid one-count column at
l=7; the proof never uses the l<=6 classification at that boundary.
The checker retains this control, exhausts every labelled eight-core
and four-variable family, and checks all seven-core/pair/singleton
placements. It also follows every labelled ordinary singleton
prefix and every covered last fresh fiber for the three current
singleton third types. Historical equality, mandatory and cover
lemmas are explicit premises; no binary capacity shortcut is used.

This excludes both complete C4/D5 third types and the third type
B4/C5/D0, independently of alphabet size. Combining the complete
five-D inventory and earlier cuts excludes the whole joints B0/C4
and B4/C0. Other three-cover joints remain. No new numerical value
of F(13,9,1), alphabet separation or complete answer follows yet.
