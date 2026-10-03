# Exact policy solver for completely reachable inputs

native_complete_policy.cpp is an additional algorithm, not a replacement
for the unrestricted solver. It accepts only when forward BFS from Q
reaches all 2^n-1 nonempty subsets. Incomplete inputs return rejection.
The guard is essential: arbitrary subsets cannot silently be treated as
reachable images. Inputs currently have n<=22. Build metadata and source
hash are retained in data/complete_policy_build.json; binaries are ignored.

## Exact reverse search

For each letter construct the inverse map on every subset, and its reverse
CSR graph. An edge is the reversal of X -> letter^-1 X. For a fixed rank
k, every set X containing a larger image T is an extension goal. Its
distance-zero tail label is min G(T) (or max worst(T)) over such contained
T. A subset zeta transform computes these labels. Reverse multi-source BFS
then labels every starting subset by the first distance to a goal, with
min/max tail at that exact distance. FIFO levels ensure all equally short
parents update the tail before a vertex is popped. No longer transport is
substituted for a shortest extension. Descending k ensures all target tail
values are already known. The resulting distance and tail give exact e,
G and worst for each rank-k image.

When every letter has rank >=n-1, an inverse edge increases size by at
most one. First growth from k is then to k+1, whose only contained larger
image is itself. Using just rank-(k+1) goals suffices, without a zeta
transform; reverse propagation needs only sizes <=k. This is a proved
algorithmic specialization, not a universal extension-length estimate.

The general time bound is O(n^2 2^n+n |alphabet| 2^n), and the
permutation/unit-defect specialization O(n |alphabet| 2^n); memory is
O(|alphabet| 2^n). These bounds concern finite exact computation, not reset
word upper bounds. The older all-source forward-transport solver can use
O(n 4^n) time on completely reachable inputs.

## Independent checks

audit_complete_policy.py compares all e/G/worst entries with the older
forward-transport algorithm. Among 8023 tested inputs, 1262 pass complete
reachability and 6761 are rejected. Complete small binary covers through
n4 and all distinct-letter ternary triples at n3 include 1200 accepted
inputs also checked by ordinary-set policy certificates. The other 62
accepted inputs include arbitrary extra transformations at n6/8/10 and
both alphabets of the shortcut family at n12. Full-vector and singleton
protocol modes agree. Rejection counts describe this finite suite only.

check_shortcut_family.py independently uses ordinary frozenset inverse BFS
and a memoized all-tie rank recursion through n22. This different sparse
algorithm compares the compact finite-family records rather than trusting
the new native solver's output. Its guard tests and reset witnesses are
separate from the policy computation. No new FORMALLY VERIFIED statement.
