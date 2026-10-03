# Nearest permutation completions: a general necessary theorem and a sharp failure

Date: 2026-10-01. **PROVED (paper)** for arbitrary finite alphabets and
all n, with the scopes below. Priority **OPEN**. General Cerny **OPEN**.
No **FORMALLY VERIFIED** claim. Virtual permutations are NEVER charged
as original letters or asserted to belong to the original monoid.

## General completion theorem

For a map f:Q->Q of rank r, a nearest permutation completion p agrees
with f on exactly r states: choose one representative in each fiber,
keep its f-image, and biject the other n-r sources onto the n-r missing
targets. These are EXACTLY the permutations minimizing Hamming distance
from f. Denote their set C(f). For a permutation f, C(f)={f}.
Given an arbitrary DFA, form the VIRTUAL group

    G=< C(a): a is an ORIGINAL letter >.

**Theorem.** If the DFA is synchronizing, G=S_n.

**Proof.** For any two states x,y in one fiber of a letter f, and any
p in C(f), the completion p' obtained by interchanging its x,y source
values is again in C(f). Their quotient p' p^(-1) is the transposition
(x,y). Thus G contains every original kernel-pair transposition.

Let E consist of all images of these kernel pairs under G, and let
the components of the undirected graph (Q,E) be C_1,...,C_t. G preserves
E and permutes these components. For any completion p of f, write

    f=e p,       e(q)=p^(-1)(f(q)).                         (1)

The map e sends every f-fiber to its selected representative. All of
its moves are within one graph component, because every fiber pair is
an initial edge. Consequently e fixes component MEMBERSHIP, and f
induces the SAME permutation of components as p. Original permutation
letters do so as well. Every original word therefore permutes the t
components. A reset word forces t=1.

Transpositions along a connected graph generate S_n: a spanning tree
and conjugations along its paths give any pair transposition. Every edge
transposition in E is a conjugate of an original kernel transposition
and belongs to G. Hence S_n is contained in G, proving equality. The
n1 case is immediate. No strong connectivity assumption is required.

This theorem is about a virtual GROUP, not reset-word membership or
length. It does not invoke a theorem about an ORIGINAL primitive group.
The distinction matters: for example the original-transitive-group
bound of [Zhu2024](https://arxiv.org/pdf/2407.08135) assumes actual
permutational generators, which the completions need not be.

## Exact subset compatibility, not arbitrary permutation control

For any map f and subset S, f is injective on S if and only if there
exists p in C(f) agreeing with f on EVERY point of S.

If f is injective, select all S-points as their fiber representatives,
choose one representative for every other fiber, and fill missing
targets as above. Conversely agreement with a permutation gives
injectivity. Therefore EVERY rank-neutral original step has a compatible
completion on its CURRENT image, even for arbitrary corank.
The compatible choice can change with the image. It does not permit
choosing arbitrary completion effects: all compatible choices have
the SAME action f on that image. A rank-dropping step has no such
permutation restriction on the full image.

For a corank-one f with kernel {x,y}, its two completions agree on
S if both x,y are outside S; exactly one agrees if precisely one is
in S; neither agrees if both are in S. This is an exact online token
description, not an additional alphabet. Ignoring its compatibility
condition destroys the original synchronization problem.

## A binary SC counterfamily for EVERY n>=3

Take states 0,...,n-1 and ORIGINAL letters

    a=(0,1) as a transposition, fixing all other states;
    0b=1b=2; qb=q+1 for 2<=q<n-1; (n-1)b=0.

The b-cycle is 0,2,3,...,n-1, and state1 enters it; a reaches1 from0.
This proves strong connectivity. The partition

    {0,1}, {2}, {3},...,{n-1}

is an ORIGINAL congruence. On its n-1 classes a is the identity and b
is a full cycle. Thus EVERY original word has rank at least n-1. Since
b has rank n-1, the minimum rank is EXACTLY n-1, not1.
The complete actual-image closure is just

    Q, Q\{0}, Q\{1}.

Indeed a exchanges the last two images and b sends either to Q\{1}.
Thus nonsynchronization holds at ALL word lengths, not only a BFS cutoff.

Yet the two nearest completions of b are

    p_plus: change 0b to1,     p_minus: change 1b to1.

p_plus is the FULL n-cycle 0,1,2,...,n-1. Together with original a it
generates S_n, by conjugating (0,1) around that cycle. The virtual
completion group is therefore S_n for every n>=3, although no original
word even makes a second rank drop. This REFUTES the converse of the
general theorem in binary SC corank-one automata, and REFUTES transfer
of synchronization from the virtual permutation group.

Neither completion belongs to the original transition monoid, at ANY
positive length. Any word containing b has rank at most n-1 and cannot
be a permutation. The words without b give only identity and a, while
p_plus and p_minus are different from both for n>=3. This is a membership
failure, stronger than an unbounded inverse cost. At n2 every singular
letter is already a reset, so n3 is minimal for this counterexample
over any finite alphabet.

## General signed-error form and the remaining proof target

For ANY nearest completion p of f, its deterministic row matrix has
the exact form

    M_f=P+sum_(q not selected) e_q^T (e_(f(q))-e_(p(q))).   (2)

All coefficients are nonnegative, but each summand is SIGNED. Iterating
these identities yields the same type of source-weighted error expansion
used in AVOID_COMPRESS_ALL_GAPS.md. Unlike that construction, an arbitrary
DFA need not have a common error direction or useful distance separation.
Moreover P is a virtual permutation unless represented by an actual word.
Neither (1), (2), full G, nor subset compatibility proves a quadratic cost.

The next substantive target is a bound using only COMPATIBLE original
steps and paid rank drops. Replacing original singular letters by their
completions, assuming their inverse words exist, or importing an actual
transitive-group bound into this virtual group are all invalid shortcuts.

## Independent finite scope

permutation_completion_boundary.py records all-map completion controls,
complete designated binary rank-n/rank-(n-1) scopes, and counterfamily
certificates. The independent checker defines nearest completions by
enumerating EVERY permutation and maximizing agreement, without importing
the generator. It compares every fiber retraction/transposition identity,
independent set-image BFS and FULL group enumeration, SC and exact family
closure. Small counterfamily scopes additionally enumerate the entire
original transition monoid and exclude both completions. Corruptions are
rejected. The report gives the exact COMPUTATIONALLY VERIFIED finite scope;
the preceding arguments supply the all-n paper theorem and failure.

The completed finite report checks ALL 3412 maps at n2..5 and ALL their
24570 nearest completions, 104328 subset-compatibility controls, 79198
kernel swaps and 604308 signed-error coordinates. ALL 28816 designated
labeled binary inputs at n2..4 use 604128 independently enumerated group
elements and 231504 set-image vertices. The 45 counterfamily parameters
run through n4096; eight complete original monoids at n3..10 have 104
elements in total. Eleven deliberate corruptions are rejected.
Registry112/196 preserves the prior111-check record and appends this
generator, deterministic replay and independent checker. Not a full112
rerun, arbitrary-alphabet census, formal proof, or new reset bound.
