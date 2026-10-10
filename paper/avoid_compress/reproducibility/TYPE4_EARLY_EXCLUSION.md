# Disjoint-tail early-type-4 exclusion at codimension three

**Claim.** For n>=5, a synchronizing automaton cannot have an (n-3)-set
of shortest compression length ten with

    P1={01}, P2={01,02}, P3={01,02,34}.

No alphabet-size, strong-connectivity or image-reachability hypothesis is
needed for this exclusion. SHORT_PAIR_STRUCTURE.md gives the credited
short-pair refinement. Write C={0,1,2,3,4} and G={3,4}. The three-hole
sets covering P3 form H: the seven core holes

    013,014,023,024,034,123,124

and 03x,04x for x outside C. Every image reached within six letters must
have holes in H. The distinct images reached within i letters grow
strictly until compression, giving |R_i|>=i+1 for i<=9. Equality at a
step would make all reached uncompressed images invariant under every
letter, contrary to the existence of a reset word.

## All compatible letters

Every letter is a permutation or a rank-(n-1) transformation with common
kernel 01. Inverse pairs of 01 belong to P2 and inverse pairs of 02
belong to P3. Permutations have core prefix A=(0,1,2) or B=(0,2,1);
they fix 0 and preserve the pair 12. An inverse pair 34 of 02 cannot
occur in a permutation: its inverse pair of 01 is 01 or 02 and would
be disjoint from 34, whereas the target pairs intersect at 0.

A singular letter omits 0 or 1, by the inverse-pair 01 test. If it
omits 1, its kernel image cannot be 0 or 2: that would produce both
0x and 1x as inverse pairs of 02, incompatible with P3. Its unique
inverse pair of 02 must therefore be 34. It has one of the core rows

    (c,c,t,0,2), (c,c,t,2,0),  c,t>=3, c!=t.

A singular letter omitting 0 has unrestricted distinct nonzero images
on the common kernel and the other core states. Some missing-1 letter
is necessary, because only such a letter can add the new pair 34 to
P3. Call it d. Swapping 3 and 4 if needed, write d=(c,c,t,0,2) on C.
This relabeling preserves the whole early-pair type.

## The domain of d has six images

Let D be the holes in H whose d-images also have holes in H. The hole
034 always has d-image holes 012, so is absent. Core holes 013,014
survive exactly when c is in G; holes 023,024,123,124 survive exactly
when t is in G. An outside 03x or 04x survives exactly when dx is in
G. Among the two outputs in G, every one not occupied by c or t has
one outside preimage. Thus, writing a=[c in G], b=[t in G],

    |D|=2a+4b+2(2-a-b)=4+2b.

This exact count also follows by direct complement-of-image substitution.
For example, 013 has holes {1,c,0}, 014 has {1,c,2}; 023 and 123
have {1,t,0}, 024 and 124 have {1,t,2}; outside holes have {1,0,dx}
or {1,2,dx}. In each case the remaining condition is to meet G.

All images reached within five letters belong to D; hence |D|>=6.
We must have t in G and |D|=6, so every D-image is reached within five
letters. In particular EVERY letter sends EVERY D-image to an H-image,
because the resulting depth is at most six.

There are exactly two domain shapes:

* c in G: c,t are the two members of G and
  D_closed={013,014,023,024,123,124};
* c outside C: let v be the unique outside preimage under d of the
  other member of G. Then
  D_mixing={023,024,123,124,03v,04v}.

The second shape requires n>=6. The first is already meaningful at n=5.

## Complete finite projections

For each domain project every compatible letter to its six successor
indices, with EXIT=-1 for an H-image outside the domain. These are
projections of actual subset images: for a permutation f the new holes
are f(H); for a singular common-kernel letter with missing output e they
are {e} union f(H) when H contains both 0 and 1, and {e} union
f(H minus {0,1}) otherwise. Each new hole set has cardinality three.

The projections are complete for every n by the following bounded
description of all relevant partial rows.

### Closed domain: five represented input states

Use output labels 0,...,6. A permutation has prefix A or B and injective
images on states 3,4. The requirement on holes 013 and 014 actually
forces both these images to belong to G. For a missing-1 singular row,
the same domain requirements force c and t into G, so its whole core
row preserves C. For a missing-0 row write it (c,c,t,u,z) on C, where
c,t,u,z are distinct and nonzero. The six hole tests require G to meet
each of {c,u},{c,z},{t,u},{t,z}. Since these four outputs are distinct,
both members of G must occur. At most two fresh outside labels are
needed. Thus labels 0,...,6 include every relevant partial row, including
ones not extendible at the smallest n; extra rows only enlarge the
candidate set and do not weaken a negative proof.

Complete enumeration yields 33 profiles on D_closed.

### Mixing domain: six represented input states

Relabel v=5 and use output labels 0,...,8. Core holes 023 and 024 force
every compatible permutation to preserve G, so its row has prefix A/B,
a permutation of 3,4, and an arbitrary outside image of state 5.

For a missing-1 row, those same holes force its image of state 2 into
G. Holes 035,045 then force its image of state 5 to be the other member
of G. Its kernel image is therefore outside C. These give all missing-1
partial rows (c,c,t,0,2,x) or (c,c,t,2,0,x), where c>=5 and {t,x}=G.

For a missing-0 row write (c,c,t,u,z,x), with five distinct nonzero
outputs. The hole conditions require G to meet each of {t,u},{t,z},
{u,x},{z,x}. Thus both members of G occur among t,u,z,x, and at most
three fresh outside output labels remain among the five distinct outputs.
The nine labels 0,...,8 therefore cover every relevant partial row.

Complete enumeration yields 37 profiles on D_mixing.

## Exit distances and contradiction

Synchronization forces every domain vertex eventually to exit: otherwise
a reset word could not reduce its image cardinality. Every finite shortest
exit distance in a six-vertex graph is at most six. If the initial vertex
had distance six, a shortest exit path would use all vertices with distinct
distances 1,...,6. For each of their 720 permutations d, include all
profiles p satisfying

    d(i)<=1+d(p(i)), d(EXIT)=0,

and test whether every vertex can exit. These enlarged profile graphs
contain every actual alphabet having those exit distances. In BOTH domains,
every one of the 720 vectors fails the test. Hence the first exit takes
at most five letters. Leaving D fails its defining d test; appending d
and then a P3 merging word of length at most three compresses the original
set within 5+1+3=9, contradicting the assumed compression ten.

## Independent verification and reproduction

type4_reduced_actions.py uses the structural row templates above and
reverse exit closure. audit_type4_actions.cpp independently enumerates
literal forward partial rows, checks the early inverse pairs directly,
and searches forward from each domain vertex. It does not use the Python
templates or reports. Every profile, every underlying-row closure flag,
all 720 vectors and both zero-candidate results agree. The Python exit
checker also accepts an artificial six-vertex chain as a positive control.

audit_type4_domains.py independently computes ordinary subset images for
every compatible missing-1 letter from the complete n6/n7 letter pools.
It verifies the exact 4+2b count, both domain shapes and the complete
letter classification. These finite controls support the symbolic count;
the parameter range is not extrapolated from them.

From the supplementary directory, using standard-library Python >=3.10
and a C++17 compiler:

    python -B type4_reduced_actions.py
    clang++ -O2 -std=c++17 audit_type4_actions.cpp -o type4_audit
    ./type4_audit type4_actions_independent.json
    python -B audit_type4_domains.py

Use .exe names on Windows and keep assertions enabled. The finite pool
files are generated by early_pair_alphabet_pool.py. The native audit
also passed -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer
with an identical report. The data are type4_reduced_actions.json,
type4_actions_independent.json and type4_domain_audit.json. They are included in the proof supplement.