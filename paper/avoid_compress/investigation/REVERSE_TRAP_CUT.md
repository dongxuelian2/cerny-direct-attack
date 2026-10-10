# Safe reverse trap cut for a partially assigned second letter

The first letter a is complete. In the inverse enumeration a set D of
output fibers of b has been assigned completely: no future assignment can
add any source to b^{-1}(q) for q in D. Start at 0 and take the reverse
closure R under a and the already assigned b-fibers. If R is a proper
subset of Q and R is contained in D, discard this branch.

Indeed, a^{-1}(R) is contained in R by reverse closure. Also b^{-1}(R)
is contained in R, and these fibers are complete. Every completion has
the same property. Thus no state outside R can reach 0, so the automaton
cannot be strongly connected. If a reachable reverse vertex has an
unassigned b-fiber, the code returns "open" immediately: this sacrifices
pruning and does not exclude a completion. If R=Q it also returns open.

This cut includes the earlier zero-state cut but adds closures of several
states. The separate zero-state test remains for speed. The second code
uses repeated numeric transition scans; the first uses a queue with the
explicit inverse fibers. Both disable the cuts in unpruned orbit-export
mode. No new maximum is asserted before their complete runs are audited.
