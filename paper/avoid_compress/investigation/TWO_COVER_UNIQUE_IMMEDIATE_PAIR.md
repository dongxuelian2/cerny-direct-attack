# Unique immediate pair under a two-state P5 cover

For n>=4, if a complete synchronizing automaton has a two-state set K
covering P5, P1 consists of exactly one pair. The alphabet is any finite
alphabet. This is a direct consequence of the known compression
refinement, not a new compression theorem or F value. SC and initial
image reachability are unnecessary.

Let R=Q-K, |R|=n-2>=2. The cover says no word of length at most five
compresses R. Synchronization makes R compressible. If two distinct
immediate pairs e1,e2 existed, their synchronizing height would be one,
and they admit an (n-2)-subset Frankl-Pin sequence of length two.
Choose an endpoint x of e2 outside e1 and another y outside e1 with
y!=x; n>=4 ensures the latter exists. Set T1=Q-{x,y}, which contains
e1 and omits an endpoint of e2. Choose any (n-2)-set T2 containing e2.
The two sets/pairs satisfy the sequence conditions.

Kisielewicz, Kowalski and Szykula, Experiments with Synchronizing
Automata, CIAA2016, Theorem1 (PDF p3) gives for every compressible
t-set the upper bound binomial(n-t+2,2)-p(P)+h(P). At t=n-2,
p(P)>=2 and h(P)=1, this is at most6-2+1=5, contradicting the cover.
The source theorem requires compressibility, not SC. P1 is nonempty
because synchronization at n>=2 needs a singular letter, so it has
exactly one edge.

Primary source checked again on10October2026:
https://kot.rogacz.com/Publications/Kisielewicz2016ExperimentsWith.pdf
The relevant theorem and sequence argument already appear in
BINARY_OBSTRUCTION_PROOF.md; this note only applies them to an
auxiliary (n-2)-set. No priority claim is made for the refinement or
this immediate consequence. It constrains automata, not just letters
in a binary alphabet, and does not assert a numerical F maximum.

The n>=4 condition matters: at n3, Q-K is a singleton and need not
compress, even when the automaton synchronizes. Checks retain this
boundary. Every singular letter now has rank n-1 and the same sole
kernel pair; any larger kernel would give multiple immediate pairs.

Complete n4 binary controls independently verify the refinement on
every compressible pair, including nonsynchronizing automata, and
the unique-edge consequence in the fixed-cover synchronizing cases.
All ordered distinct-pair two-step sequences are literally checked
through n13. These controls support the cited theorem/application;
they are not a new theorem proved by finite sampling.
