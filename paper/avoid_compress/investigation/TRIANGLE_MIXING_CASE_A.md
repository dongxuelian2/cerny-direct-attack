# Necessary exclusion of one mixing singular letter in early triangle type

Assume shortest compression length 10 for an (n-3)-subset of a
synchronizing automaton, with P1={01}, P2={01,02}, P3={01,02,12}.
Every letter is a permutation or has rank n-1 and kernel 01.

Let C={0,1,2}. The three-hole sets covering P3 are C itself and
{i,j,x}, with {i,j} contained in C and x outside C. Every image reached
within six letters must have one of these hole sets: otherwise it
contains a P3 pair, compressing within at most three more letters.

A singular letter has missing output 0 or 1. Indeed, if both 0 and 1
are present, their inverse pair is either disjoint from the kernel or
consists of two overlapping edges 0z,1z; neither is contained in
P2={01,02}. Its inverse pair of 01 is consequently empty. Since P2
contains the new pair 02, there is a permutation g with g^{-1}(01)=02.
The inverse pair of 02 is a different edge in P3, so g permutes C and
its complement. Also g(01) differs from 01.

Suppose a singular letter f omits 0, has f(0)=f(1)=c in {1,2}, and
has f(2) outside C. Let v be the unique preimage of {1,2} minus {c};
it lies outside C. Direct computation of the holes gives the domain

    D_f = {C, {0,2,v}, {1,2,v}}
          union {{0,1,x}: x outside C}

of P3-covering hole sets whose f-images also cover P3. Since g sends
01 to a different core pair, among the last family at most one member
has its g-image in D_f: its external point must be g^{-1}(v). The other
three members contribute at most three. Thus

    |D_f intersection g^{-1}(D_f)| <= 4.

Every image of the original subset reached within four letters lies
in this intersection. Its f- and gf-images must cover P3, since they
are reached within respectively five and six letters. But the family
of distinct images reachable within i letters grows strictly with i
until it contains a compressed image. A plateau would be a finite
family invariant under every letter, contradicting synchronization.
Thus at least five distinct images are reached within four letters,
contradicting the four-element intersection bound.

No such Case A singular letter exists in an automaton of the assumed
tight compression type. This exclusion uses synchronization, not strong
connectivity or reachability of the initial subset. It applies to every
n where the displayed assumptions hold and to any finite alphabet.
It is only one necessary exclusion, not a compression-nine theorem.

audit_triangle_mixing.py checks all Case A letters f and all required
permutations g in the literal complete n=6,7 pools using actual subset
images. It verifies the domain exactly and the intersection bound.
The other cases are proved in TRIANGLE_EARLY_EXCLUSION.md.
