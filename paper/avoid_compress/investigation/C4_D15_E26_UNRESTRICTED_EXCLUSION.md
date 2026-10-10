# Unrestricted B0/C4/D15/E26 exclusion

Conditional at (13,9,1), equality12, B={0}, C={4}, D={1,5},
E={2,6}, and K={1,2} covering P5. This fourth geometry is impossible
for every finite alphabet. Neither whole D15 third type nor a numerical
F value is determined by this fourth cut.

Put H={0,3,4}, W=Q-(H union D union E), O=E union W, R=Q-K.
The complete fourth classification has sixteen individual fields and
no additional covered Boolean companions. Both suppliers M0 with
preC=D and T0 with preD=E exist; one letter may supply both, and is
not omitted. Since M0 collapses D into singleton C, pair15 is in P1.
The two E inputs under T0 enter D and merge under T0M0, so26 is in P2.
Write G0={15,26}, a matching on L=D union E.

Assume synchronization. TWO_COVER_P3_CLASSIFICATION.md says P3 is
matching, path4 or triangle after deletion of isolates. It contains
G0, so it is G0 with at most one crossing edge between D and E.
In particular every P3 edge has both endpoints in L.

If P2 contained the crossing edge, its three-edge path would have
exactly three independent n-2-sets. All edges belong to P2; the P5
cover and FINITE_INDEPENDENT_IMAGE_TRAP.md forbid synchronization.
Consequently P2=G0 exactly.

We now prove the pair recurrence cannot add anything at depth3.
The inverse pairs of15 already lie in P2, since15 belongs to P1.
For inverse pairs of26, the complete sixteen fields give four
exhaustive classes (preimages here are exact sets):

* F: preC is a singleton of H and preD=D. The H inputs permute H,
  the D inputs enter D, and the O inputs enter O. Both inverse inputs
  of an E edge therefore lie in O=E union W. A P3 edge with these
  inputs must have both endpoints in L, hence must be26.
* M: preC=D and preD={p}, p in H. D enters C, the two other H
  inputs supply A,B, p enters D, and O enters O. Inverse E inputs
  again lie in O, giving only26.
* T: preC is a singleton of H and preD=E. H permutes H, E enters
  D, and all inverse E inputs lie in D union W. The only possible
  P3 inverse E pair is15.
* MT: preC=D and preD=E. D enters C, E enters D, two H inputs
  supply A,B, and the remaining H input and W enter O. Every inverse
  E input lies in H union W, disjoint from L. There is no inverse E
  pair at all, since such a pair would be a P3 edge outside L.

Thus all inverse pairs of G0 lie in G0, and P1 is contained in G0.
The recurrence P_(j+1)=P1 union all letter inverse pairs of P_j
therefore stabilizes at P2=P3=G0. Induction gives P_j=G0 for every
j>=2. A pair outside this proper matching never merges, contradicting
synchronization.

The argument uses exact fields, suppliers, synchronization and the P5
cover. Mandatory H isolation, SC, binary incoming capacity and S
reachability are unnecessary for this conditional obstruction. The
P3 classification is applied only after its two-cover/synchronization
hypotheses hold. No extra edge-cardinality cap is assumed. The overlap
of the M and E suppliers is retained throughout.

Independent raw-row generators match the complete small individual
domains. Complete binary/ternary supplier alphabets are tested, including
alphabets where one letter supplies both D and E. Every synchronizing
control has a directly checked outside-K pair merged within five; no
SC filter is used for this statement. Nonsynchronizing cover controls
have literal image-closure or stabilized-pair-graph certificates.
Samples support the uniform paper argument and prove no negative
theorem. Structural boundary examples are not attaining F witnesses.
