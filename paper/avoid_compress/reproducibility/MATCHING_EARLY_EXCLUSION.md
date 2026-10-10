# Excluding three disjoint early pairs at tight codimension-three compression

Suppose a synchronizing automaton on n>=6 has an (n-3)-subset of shortest
compression length 10. The credited Frankl--Pin refinement and strict pair
closure growth give |P_h|=h for h=1,2,3. Consider the case

    P1={01}, P2={01,23}, P3={01,23,45}.

Every letter is a permutation or has rank n-1 and the common kernel 01.
For every letter f, inverse pairs of 01 lie in P2 and inverse pairs of 23
lie in P3. These statements mean all two-point preimages, not a chosen
preimage.

## Eight projected images

Every (n-3)-set whose pairs avoid P3 has a hole set containing exactly one
point from each of 01,23,45. There are eight such hole sets, indexed by
(x,y,z) in {0,1}^3, namely {x,2+y,4+z}. The initial set is one of them.
Each can be relabeled to the first hole set by independently swapping the
endpoints of the three pairs. This preserves the ordered early-pair type.

A permutation sends a hole set H to f(H). For a rank-(n-1) letter with
missing output d, H contains exactly one endpoint of its kernel. Its new
holes are {d,f(2+y),f(4+z)}. The image still has n-3 points. Mark the action
as EXIT if those holes fail to contain one endpoint of each early pair.
Such an image contains a P3 pair and hence compresses within three further
letters. Thus compression length 10 would require first exit distance at
least 7 from the initial projected image.

Synchronization requires exit to be reachable from every projected image:
otherwise its entire image orbit stays in the eight sets of cardinality
n-3, making a reset impossible. The shortest exit distance from each
projected image is consequently at most 8 (erase repeated vertices on a
shortest exit path).

## Complete action projection, independent of n and alphabet size

Only f(0),...,f(5) and, for a singular letter, d affect the eight actions.
At most six distinct external labels occur among these values. Relabel
them to 6,...,11. The six distinguished labels 0,...,5 stay fixed. Thus
enumerating these values among twelve labels gives a superset of every
possible projected action for every n>=6. Small n simply realizes a
subset of this superset.

For a permutation, enumerate all injective six-tuples (12P6=665280).
The inverse pairs of 01 and 23 must both occur among the six distinguished
sources and satisfy the constraints above. Exactly 896 core cases pass.

For a singular letter, f(0)=f(1), and f(0),f(2),...,f(5) are distinct.
Choose these five images and then a different d (12P5 times 7 =665280).
If d is in an output pair its two-point preimage is empty. If the kernel
image is in a present output pair, its two inverse edges share an endpoint;
they cannot both be in the matching P2 or P3. Otherwise the unique inverse
pair must be one of the specified matching pairs. Exactly 6272 cases pass.

An independent inverse-case classification obtains the same cases:

* d in 01: inverse 23 is 23 or 45; 4032 core cases;
* d in 23: inverse 01 is 23; 2016 core cases;
* d outside 01 union 23: inverse 01 is 23 and inverse 23 is 45; 224 cases.

The permutation and singular cases yield exactly 177 distinct action
profiles. The independent checker extends the inverse cases to literal
twelve-state rows and computes all eight subset images directly. All 177
profiles coincide. Literal n=6,7 pools (111 and 407 letters) are included.

## Exact finite alphabet check

Let d(v) be the shortest exit distance in an arbitrary selected alphabet
of the 177 profiles. If all eight values are finite, their maximum is at
most 8 and every integer from 1 to that maximum occurs: a shortest exit
path descends one level at each step. Normalize the initial vertex to 0.
If d(0)>=7 there are exactly 30240 possible distance vectors:

* maximum 7 and d(0)=7: levels 1,...,7 with one duplicate, 20160 vectors;
* maximum 8 and d(0)=7 or 8: one of each level 1,...,8, 10080 vectors.

For each vector include ALL profiles satisfying

    d(v) <= 1 + d(f(v)), with d(EXIT)=0.

This includes every letter of an alphabet having that distance vector.
Under any included word to EXIT the inequality gives length >=d(v), so
adding all such profiles does not invalidate the lower bound. If the union
of allowed actions cannot make every vertex reach EXIT, no alphabet with
that vector is possible.

The complete check finds no vector for which all eight vertices reach
EXIT. Python constructs multiset permutations and uses reverse BFS; C++
independently scans all base-eight label vectors and uses repeated Boolean
exit closure. Both check 30240 vectors with zero candidates. Each accepts
the artificial eight-vertex chain, a positive control with first distance 8.
This is exhaustive arithmetic enumeration, without a SAT solver or any
bound on the selected alphabet size.

Hence in every synchronizing alphabet of these actions the first exit
distance is at most 6. Appending a P3 merging word of length at most 3
compresses the original subset within 9, a contradiction. The disjoint
early-pair type is therefore impossible for tight compression 10.

## Reproduction and limits

Build and run matching_cube_profiles.cpp to matching_cube_profiles.json.
Run check_matching_cube.py against that report. Run audit_matching_cube.py
to generate an independent text profile list, then build/run
audit_matching_distances.cpp on that list. Reports matching_cube_check.json,
matching_cube_audit.json and matching_distance_audit.json contain the counts.