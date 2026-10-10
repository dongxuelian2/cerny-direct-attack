# The singleton fifth F2 is impossible in E6

9 October 2026. Conditional exclusion at n=13, |S|=9,
ac(S,{3})=12, for every finite alphabet. Fix B0,C14,D5,E6 and
the fresh fifth F2 of B1_FIFTH_ENTRANCE.md. No whole E6 branch,
new F value or numerical alphabet separation is asserted.

## Correct depth and rank

Every image through six contains2. Thus ac(S,{2})>=7, and the
protected-pair bound ac(S,{2})<=4+d_2 implies d_2>=3. The point2
is isolated in P2. This is not P3 isolation; the earlier one-point
P3 compression-cover floor does not apply.

Strip2 from K={1,2}, which covers P5. The singleton {1} covers P2.
In particular every letter is injective on Q minus {1}, so has rank
at least12. Any nontrivial kernel consists of exactly one pair {1,q}:
a triple or two nontrivial blocks would collide two inputs outside1.
The set U={0,2,3,5,6} is isolated in P2. This follows from the
earlier depth bounds for0,3,5,6 and the just established bound for2.
Hence q is4 or is in J={7,8,9,10,11,12}.

## A short pair-graph argument

In a strongly connected automaton, if a singleton {c} covers P2,
then P1 has at most one edge. To prove this, suppose P1 contains
distinct edges {c,u},{c,v}. Every letter ell is injective outside c,
so T=(Q minus {c})ell has n-1 points. Also T is independent in P1:
a collision edge in T would have distinct predecessors outside c
forming an edge of P2, contradicting the singleton cover. The only
independent (n-1)-set in a graph containing those two edges is
Q minus {c}. Indeed, an (n-1)-set containing c omits only one state
and cannot omit both u and v. Thus every letter preserves Q minus
{c}, contradicting strong connectivity. This elementary argument
uses no synchronization premise or n=13 restriction.

Apply it with c=1. The earlier C-supplying letter maps C={1,4}
to0, so pair14 is an immediate kernel. It must therefore be the
only edge of P1. Let G
be the singleton pair-graph edge14. It is backward closed: each
letter has pre(C) equal to A3,B0,C14 or D5. A singleton pre(C)
supplies no distinct inverse pair, and a C14 pre(C) supplies only
the edge14 when its two outputs differ. All immediate collisions
are in G, so the reverse pair search never leaves G. The automaton
would not synchronize, contradicting the hypothesis. This already
proves the conditional exclusion.

## Independent expanded incoming argument

As an adversarial cross-check, the same contradiction can be obtained
without using the short graph observation. If every letter kernel
were empty or14, the backward-closure argument above would contradict
synchronization. Some letter R therefore has kernel {1,q}, q in J.

Fix that letter R and its q. Consider any letter ell supplying an
incoming transition to1. Its pre(C) is A3,B0,C14 or D5.

If pre(C) is a singleton {u}, u in {0,3,5}, then ell(u)=1 and4
is absent from the image. Rank at least12 makes4 its only absent
output. Consequently q has a predecessor x, distinct from u.
The pair {u,x} follows ell R to a singleton, contradicting the
P2 isolation of the protected point u.

Suppose pre(C)=C and ell(4)=1. If ell(1)=1, output4 is absent;
again rank at least12 ensures q is present. If ell(1)=4, the
restriction to C is a permutation. Any collision would involve1,
but every input outside C maps outside C, so1 cannot collide with
one of them or with4. Thus ell is a permutation of Q and q is
again present. In both cases choose x with ell(x)=q. This x is
outside C. The pair {4,x} is outside the cover {1}, yet ell R
merges it in two steps, contradicting that {1} covers P2.

The only remaining way to supply1 is pre(C)=C, ell(1)=1,
ell(4)=4. Its preimage of1 is exactly {1}. Letters not supplying1
have empty preimage of1. Thus every letter's preimage of the
nonempty proper set {1} is contained in {1}. No state outside1
can reach1, contradicting strong connectivity. QED.

The proof uses synchronization to obtain R, strong connectivity
for the final incoming contradiction, and only length-two pair
premises afterward. It does not require a binary alphabet, choose
ordinary permutations or assume outside-C injectivity at an earlier
depth. Outside-{1} injectivity is derived here after P2 isolation
of2 has been proved.

## Complete individual-letter controls

The generator enumerates the five disjoint output fields A,B,C,D,E
and their remaining field at n=7,8,9,13. Its row templates cover
all known nonempty preimages, including letters unused by any
binary parent pair. It assigns all injective outputs for inputs
outside1 and all allowed outputs for1, retaining both the C kernel
and every ordinary {1,q} kernel. It checks the protected immediate
kernel restrictions. No fixed ordinary permutation is substituted.

The independent checker reconstructs these assignments by selecting
the immediate kernel first and then injecting its quotient blocks
into the permitted target fields. It imports neither the generator
nor the fifth checker. For every full letter and every q in J it
evaluates the two displayed witnesses literally whenever that letter
supplies1 from a predecessor other than1. It also checks the inverse
closure of G. These are full individual-letter controls for the
symbolic proof, not a full thirteen-state transition-pair scan.

The singleton cover of P2 by itself is permissible: on three states,
letters [1,2,0] and [0,2,2] are strongly connected and synchronizing,
with P1={12}, P2={01,12}. This literal control guards against the
invalid claim that one-point P2 covers are impossible. It has a
different preimage structure from the thirteen-state branch.

Run enumerate_b1_e6_f2_letters.py, then check_b1_e6_f2.py, with
Python>=3.10 and assertions enabled. These auxiliary files are
outside the unchanged109-file accepted manuscript supplement.
