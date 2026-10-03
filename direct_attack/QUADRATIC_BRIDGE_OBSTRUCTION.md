# One extra state already forces a quadratic kernel bridge

**PROVED (paper), NOVELTY OPEN.** This is a negative structural result, not
an improvement of a general reset upper bound. It isolates why the linear
kernel bridge cannot be used at the neighboring, larger rank. The obstruction
occurs in the classical circular Cerny family.

For every integer h>=1 put n=6h. Use states Z/nZ and letters

    qa=q+1 mod n;  (n-1)b=0;  qb=q otherwise.

Let S={0,2h,4h}. Partition Q into the two intervals
F0={0,...,3h-1}, F1={3h,...,6h-1}. There is an actual rank-two word u whose
two fibers are exactly F0,F1 (constructed below). The exact shortest length
of a bridge v satisfying |Svu|<2 is

    6h^2+2h = n^2/6+n/3.                                    (QB)

Thus no universal O(n) bound exists for the bridge v even when |S|=3,
rank(u)=2, and A is strongly connected, synchronizing, binary and circular.
S is also reachable from Q; this is not an unreachable-subset obstruction.
In particular, the tested candidate

    |v| <= (|S|-rank(u)+1)(n-rank(u)+1)

fails for all h>=2 in this family, and already has a separate C7 witness
with exact distance 13 rather than its proposed 12.
No state-minimality is claimed until the six-state rank-excess case is audited.

## Full lower bound: repeated hits on one original trajectory

For any word prefix let A be its number of a's. For each original state
q in {0,2h,4h}, let B_q count the b's at which its current trajectory is
n-1. Its image is congruent to q+A+B_q modulo n: a always advances one
position and b does so precisely at n-1.

Suppose all three final counts B_q are <=h. Put y_q=q+A+B_q. The differences

    y_(2h)-y_0 = 2h+B_(2h)-B_0,
    y_(4h)-y_(2h) = 2h+B_(4h)-B_(2h),
    n+y_0-y_(4h) = 2h+B_0-B_(4h)

lie in [h,3h] and sum to n. Thus the images are distinct and these are
their cyclic gaps. Every gap is at most 3h. But a subset contained in an
interval of 3h states has a gap at least n-(3h-1)=3h+1. It cannot miss a
fiber. Every successful bridge therefore has B_q>=h+1 for some fixed
original q.

After each counted b hit of q its trajectory is 0. Before the next counted
hit it must reach n-1. No intervening b changes this trajectory (otherwise
it would be another counted hit). Hence there are at least n-1 a's between
consecutive counted hits. Before its first hit there are at least 2h-1 a's:
the possible initial states are 0,2h,4h. These intervals are disjoint, so

    #a >= (2h-1)+h(n-1),  #b >= h+1.

Their sum is 6h^2+2h. Original labels remain tracked after a collision;
the argument allows collisions, ineffective b's and extra rotations.

## Matching upper bound

Take v=a^(2h-1)b(a^(n-1)b)^h. After its first b the subset is
{0,2h-1,4h-1}. After j further blocks, 0<=j<=h, it is
{0,2h-1-j,4h-1-j}. At j=h this is {0,h-1,3h-1}, contained in F0. At h=1
the duplicate 0 is removed as set semantics require. The length is
2h+hn=6h^2+2h. This proves the exact formula including h=1.

## Actual kernel word, with the right composition order

For i in Z/nZ define

    e_i=a^((n-1-i) mod n) b a^((i+1) mod n).

Its transformation sends i to i+1 and fixes every other state. Concatenate
e_0 e_1 ... e_(3h-2), followed by e_(3h) ... e_(6h-2). This sends F0 to 3h-1
and F1 to 6h-1; these targets are distinct and fixed throughout the opposite
block's merges. Its fibers are exactly the claimed partition. The word has
length (n-2)(n+1); its length is not asserted to be minimal. We do not add u
as a new letter: doing so changes the search alphabet and invalidates the
gap lower bound.

For reachability of S, concatenate the local e_i's inside each of the three
cyclic intervals ending at 0,2h,4h. Each interval collapses to its endpoint,
and these endpoints are not changed by the other intervals' maps. The
certificate stores this actual reach word and the independent checker
maps Q through it. No shortest-rank reach assertion is needed for the
obstruction theorem.

## Independent audit and interpretation

The computer experiment works on the complete transition-closed collection
of all nonempty subsets of size <=3, rather than a 2^n graph. A saved
Bellman potential plus a target-reaching word certifies each exact bridge
distance, independently of the trajectory argument. Kernel words are verified by
mapping every original state. See bridge_obstruction.py and check_bridges.py.
The h=1..10 instances (n=6..60) agree with the exact formula. The checker
also rejects deliberately corrupted potentials and kernel transformations.

The ordinary |S|=rank(u) bridge remains linear. This theorem concerns
|S|=rank(u)+1. A hypothetical splice with a larger plateau image therefore
cannot simply replace the singleton-rich mechanism with a constant-excess
linear bridge. It does not refute other averaged, fiber-aware, or amortized
bridges.
