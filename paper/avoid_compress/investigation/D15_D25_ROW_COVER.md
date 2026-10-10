# Complete remaining binary fourth row domains in B0/C14

Conditional at n=13, |S|=9, ac(S,{3})=12, B0,C14,K12 covering
P5. Remaining binary third types are D15 and D25. Their complete
fourth inventory supplies seven E types at D15 and three at D25,
with42 and56 admitted field pairs. Every Boolean companion is
retained: D15/E24 has companion25 and D15/E25 has companion24.
All allowed preD columns and original third-field pairs are included.

Output signatures use A3,B0,C14,D. At D15 the shared C/D state1
and the private4 and5 are singleton atoms; the ordinary atom is
{2,6,7,8,9,10,11,12}. At D25, C14 and D25 are disjoint two-point
atoms, and the ordinary atom is6..12. Never replace overlapping
or paired outputs with independent singleton targets. Python generates
all atomwise outside-K injections and guard assignments avoiding
mandatory outputs; native recursion independently assigns every input.

The literal initial nine-set family contains3 and meets B,C,D,E
once. It contains every actual image through seven and automatically
meets the listed companion once. Its intersection is P7-isolated
by the mandatory-core theorem. Outside-K pairs cannot merge through
five. Pure-letter masks require rank nine and3 through eleven,
and family membership through seven. The largest family has60 sets;
64-bit masks and a bit59 control prevent truncation.

When E contains6, fix0..6 and permute7..12 (720 bijections).
Otherwise fix0..5 and permute6..12 (5040 bijections). Each chosen
group fixes every known fiber and companion and preserves every
input/output atom. First-letter orbit normalization is exact: all
group elements are enumerated, the least conjugate is selected, and
an explicit permutation witness is emitted for each retained row.
For an orbit member f^g and g0 mapping f to the least row, the cached
witness k satisfies k(g(q))=g0(q). Cache clears at each geometric
type; the group table is keyed by its fixed-state count.

The second letter remains fully labelled. Simultaneous conjugation
of both letters and S therefore proves coverage of every actual pair.
The independent forward scanner does not choose canonical rows: it
checks every emitted bijection, every pointwise row equation, every
transported initial mask, and membership in the full retained field.
Every group element and every companion identity is independently
checked. Reverse pair BFS and forward scalar relaxation use different
connectivity and pure-letter algorithms. Positive candidates require
ordinary-set avoid-or-compress BFS, reset and reaching words before
changing any F value. A negative needs all actual row domains and
complete fourth/third coverage; no missing-companion shortcut is allowed.

These binary pair domains do not exclude unrestricted alphabets.
For larger alphabets all individually admissible fourth fields, rather
than just binary-active ones, must be retained. An optional positive
search among three or more supplying letters has no negative force.
Any attaining candidate it finds must be independently checked under
all four structural requirements, including actual image reachability.
