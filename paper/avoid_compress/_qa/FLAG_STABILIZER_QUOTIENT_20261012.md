# Conditional simultaneous-alphabet child transports

At a flag node let L be its complete active literal-letter pool, R_j its
obligatory domains, and v_0,...,v_k its actual prefix images. The permitted
next-image inventory is C. A checked generator p must fix every old image,
each known forced image, the fixed states and premise graphs. Conjugation
is defined by f'(p(q))=p(f(q)). It must give a bijection of L fixing every
R_j as a set, and p must permute C.

For any actual alphabet E contained in L, apply this same p to every
letter. The conjugated alphabet still lies in L and meets all R_j. Words
have unchanged lengths and their images are relabeled by p; old images
are fixed. Strong connectivity, synchronization, reachable-image status,
alphabet size and the safety predicate are preserved. All products of
checked generators have these properties.

Suppose a prospective next image y is transported to representative z.
Conjugation sends letters mapping v_k to y to letters mapping v_k to z.
It also sends span(v_0,...,v_k,y) to span(v_0,...,v_k,z), because p fixes
the old characteristic rows and acts linearly by a coordinate permutation.
Consequently the filtered child letter pool, its new obligatory domain
and its rank-growth condition are transported correctly. A rejected
representative child therefore rejects every child explicitly transported
to it. This is an alphabet-independent conditional statement, not an F
bound or an all-parameter result.

The implementation starts with adjacent transpositions in cells agreeing
on all old and forced-image columns, outside conservative fixed-state
sets. Every proposed generator is verified on all active literal rows,
all required groups, all premise edges and the complete choice inventory.
Only successfully checked involutions are used. Each child stores a
sequence mapping it to its representative. Exact child coverage, row
transport digests and every stated invariant are independently replayed.
No node acquires safety at depth 12; a depth-11 survivor remains a candidate.
