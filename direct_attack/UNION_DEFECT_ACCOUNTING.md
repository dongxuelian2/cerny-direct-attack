# Quantifying the two losses in image-capacity union transfer

**PROVED on paper, elementary identity; priority OPEN.** This is a general
conditional image-extension lemma, not a new n-only synchronization bound.
Let R be the family of actual Q-images, rho(X)=max{|V|:V in R,V subset X},
rho(empty)=0, and Delta(X)=|X|-rho(X). For an ACTUAL word w define

    F_w(X)=rho(pre_w(X))-|X|,
    I=S intersect T, U=S union T,
    m_w(I)=|I\Qw|.

For any S,T (no reachability assumptions are needed for the identity),

    F_w(S)+F_w(T)
      = F_w(U)+|pre_w(I)|-|I|
        +Delta(pre_w(U))-Delta(pre_w(S))-Delta(pre_w(T)).

Proof: preimages preserve unions and intersections, so their cardinalities
satisfy inclusion-exclusion; substitute rho=cardinality-Delta and apply
inclusion-exclusion also to S,T. Each nonempty state fiber contains at
least one source, hence |pre_w(I)|-|I|>=-m_w(I). Consequently, if

    F_w(U)>m_w(I)+Delta(pre_w(S))+Delta(pre_w(T))-Delta(pre_w(U)),

then F_w(S)>0 or F_w(T)>0. For reachable S,T this means the SAME word
image-extends one component, so e(S)<=|w| or e(T)<=|w|. The source image
exists by rho's definition; no ordinary fiber is declared reachable for
free. Conversely, if w image-extends U but neither component, its positive
capacity gain is at most the right-hand defect budget. An actual chosen
endpoint V with |V|-|U|=g satisfies the same necessary g bound, because
g<=F_w(U). This does not by itself bound how such losses accumulate along
a reset construction.

The strict inequality is necessary in general. The earlier n3 union
obstruction has S={1},T={2},w=b=[1,2,1], F_w(U)=1, missing overlap 0,
Delta(pre_w(S))=1, the other defects 0. Its failure is entirely image
availability. The completely reachable n4 obstruction has S={0,3},
T={2,3},w=aa, F_w(U)=1, missing overlap 1, all defects 0. Its failure
is entirely target omission. Both saturate this accounting inequality.

On completely reachable inputs every Delta is zero. A union capacity
gain exceeding the number of omitted overlap states therefore transfers.
The known proper-onto extension union lemma is contained in the case of
zero omitted overlap. These deductions reconstruct the combinatorial
mechanism rather than claiming a novel general union principle. The
unrestricted into-image route still needs control of BOTH loss terms.

check_union_defects.py uses ordinary sets, actual-word transformation
closures and independently enumerated image capacities. It checks the
identity and sufficient condition at every tested proper union, and
verifies both equality obstructions. Its finite counts do not prove the
general lemma: the displayed inclusion-exclusion proof does. No Lean result.
