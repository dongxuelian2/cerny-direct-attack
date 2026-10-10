# Complete fourth row cover for D12 and D24

Conditional at n=13, |S|=9, ac(S,{3})=12, B0,C14 and K12
covering P5. This new calculation targets D12,D24 and all their
binary fourth fields; it does not assume either branch is excluded.

For each D the remaining E geometries are5,15,25. Every supplying
letter and all original third pairs are included in the frozen fourth
inventory. D24/E15 has Boolean companion25, and D24/E25 has
companion15. These are present in the permitted preD columns and
their complete field pairs. No common-E or missing-companion shortcut
is used. Their one-count equations follow from those for C,D,E;
the literal initial family contains every actual image through seven.

The output atoms are six sets:0,1,2,3,4 and5..12. Their four-bit
membership signatures differ: C/D share1 at D12 and4 at D24.
Input atoms are reconstructed from literal preA,preB,preC,preD sets,
not from a disjoint-target assumption. Every actual row is injective
outside K; collisions cannot touch mandatory points. Python generates
atomwise outside-K injections and guard assignments, while C++ uses
per-input recursion. Sorted raw-row hashes establish their agreement.
For every atom with o outputs, t outside-K inputs, p mandatory inputs
and h guard inputs, the domain size is (o)_t*(o-p)^h; t>o gives zero.
All eight-million-row individual domains are complete necessary domains.

Initial families have56 forms for E5 and42 for E15,E25. Pure-letter
cuts check mandatory P7 isolation and outside-K P5 nonmerging. The
initial-mask calculation requires rank nine and3 through eleven,
and family membership through seven. Two distinct algorithms compute
these cuts and masks independently. Python here checks raw-domain
completeness; it does not duplicate the native pure-letter checks.
All masks use uint64_t, including a bit55 control and actual high masks.

Fix0..5 and permute6..12. All5040 bijections preserve A,B,C,D,E,
K, every companion, every field atom, and the initial family. Enumerate
the whole group to select the least conjugate of the first row f.
For every g the conjugate obeys f'(g(q))=g(f(q)). The second letter
is left fully labelled, so a pair(f,h) is represented by(f',g h g^-1).
Both rows and the initial subset are conjugated together in this
coverage argument. Transported initial masks are recomputed and checked.

An exact orbit cache does not change the algorithm. If g0 carries f
to its least representative, a row obtained via another g has witness
k defined by k(g(q))=g0(q). This is g0 composed with g^-1 and sends
that orbit member to the same representative. All5040 group members
are inserted. Cache hits return such an explicit pointwise witness;
the cache is cleared for each geometric type. No graph canonicalizer,
assumed orbit size or stochastic representative selection is used.

The independent scanner checks every emitted bijection fixes0..5,
every row-conjugacy equation, preservation of all literal initial-image
masks, and membership of the representative in the same complete
retained row field. It does not choose representatives itself. Reverse
pair BFS and forward scalar relaxation independently check coupled
P5/P7 constraints and synchronization; connectivity uses two different
algorithms. A final negative requires both complete scans to exclude
all necessary candidates, and whole-third coverage additionally requires
the frozen fourth alternatives. If candidates survive, further audits
are required; merely running these programs proves no exclusion.
