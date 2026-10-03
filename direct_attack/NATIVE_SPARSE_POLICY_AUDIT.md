# Exact sparse policy solver on the full reachable-image graph

The solver accepts unrestricted alphabets and image families at 2<=n<=63.
It enumerates the ENTIRE forward closure R={Qw}, including Q, with uint64
masks. A configurable vertex limit returns status -4 and a `truncated`
rejection; it never returns a policy value for an incomplete graph. Every
singleton must be reachable. This is equivalent here to synchronization
plus strong connectivity: a reset followed by a state path proves one
direction, and reachable singleton images prove synchronization and paths
from every state to every target for the other. Other inputs are rejected.

## Exact distances and all future-policy ties

For each existing proper rank k in descending order, run forward BFS with
ALL reachable images T of size >k as distance-zero sources. Source T has
already computed tails G(T),W(T); Q has tails zero. At each vertex U,
retain the shortest distance d(U) from those sources and the minimum and
maximum source tail over ALL paths of exactly that shortest distance.
All distance-zero sources are queued before any distance-one vertex, so
FIFO BFS completes every parent-layer update before processing a child.
Equal-distance edges propagate both min and max tails, without dropping ties.

For an actual rank-k image S, minimize d(U) over reachable U subset S.
This minimum equals e(S): every larger image and word T w subset S remains
in R at every prefix, and every graph path describes an actual word.
Moreover, for any winning source T, its own distance into S must equal
the global minimum; a shorter path would contradict that minimum. Hence
the winning source tails give precisely

    G(S)=e(S)+min G(T),  W(S)=e(S)+max W(T),

over all larger T having shortest transport cost e(S). Rank jumps, strict
terminal subsets, intermediate rank drops and both future-tail ties are
included. A path passing another larger source cannot be a shortest path
from the whole source set, since that suffix starts at distance zero there.

Containment is tested either by all nonempty submasks of S (if fewer) or
by scanning R. No ordinary subset is silently treated as reachable.
The first forward enumeration also gives exact full-Q distances and rt.

For M=|R|, alphabet size s and d existing proper ranks, construction costs
O(snM). Policy BFS costs O(dsM); containment costs
O(sum_(S proper in R) min(M,2^|S|)) in expected hash-table time. Memory
is O(sM+n s) plus hash-table storage. If all nonpermutation letters have
rank <=r, then every proper image has size <=r, d<=r and M<=1+sum_(j=1)^r
binom(n,j). This explains why much larger n can be scored exactly here.
It proves no universal synchronization bound.

Protocol mode 0 retains the original summary, mode 1 retains all arrays,
and new mode 2 appends exact actual merge capacity kappa, best unrestricted
one-letter seed budget, best/worst largest-seed budgets and attaining best
source masks. The wrapper rejects combining array and seed-summary modes.
Graph-limit or nonsynchronizing rejection precedes any partial summary.
check_first_drop independently reconstructs every seed metric and verifies
selected masks as actual one-letter sources. F=P is proved on paper.

## Independent verification

audit_sparse_policy compares every e/G/W value with the older full-cube
forward solver on complete binary coverage through n4, ternary n3, retained
inputs <=12 and random rank-three inputs. All 1303 small accepted binary
cases additionally have ordinary inverse-set certificates. Four cases
n16,33,40,63 have a separate ordinary-set ALL-SOURCE forward BFS for every
entry. Explicit graph-limit rejection, nonsynchronizing rejection and
subsequent protocol recovery are checked. Literal counters are in
data/sparse_policy_checks.json; later stored inputs can increase the counts.

The two parameter-family checkers independently recompute EVERY saved
e/G/W/forward entry at n4..63, verify full ordinary-set image closures and
actual full-Q/extension words. The search checker independently recomputes
every entry in all 48 rank-three/four/five retained peaks, up to 2784 images, and
extracts actual larger-image extension words. Corrupted field tests reject
each tested change. None of these finite checks replaces an arbitrary-n
paper proof. Build metadata retains compiler, literal argv, source and binary
SHA256 values; binaries are regeneratable ignored files. No Lean addition.
