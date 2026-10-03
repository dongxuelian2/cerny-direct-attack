# Protected-point cycle insertion

Status: **PROVED** (paper); finite instances **COMPUTATIONALLY VERIFIED**.
Not formalized. Priority of this construction and its applications is **OPEN**.
Use right actions: S(uv)=(Su)v. This result is an obstruction to proposed
compression bounds, not an upper bound or a counterexample to Cerny.

## General theorem

Let A be a strongly connected synchronizing binary DFA on Q, with letters
a,b. Assume a is a permutation, a fixes p, b(p) != p, and S is Q-reachable,
p in S, |S|>=2. Write c=min{|w|: |Sw|<|S|}. Assume p belongs to Sw for
every word of length strictly less than c. Let M be the order of a.

For any t>=0 with gcd(t+1,M)=1, add new states N={q_1,...,q_t}, replace
a's loop at p with (p,q_1,...,q_t), and let b fix N. The resulting DFA is
strongly connected and synchronizing. Its reachable set S'=S union N has
exact compression cost c. Its corank equals that of S.

### Short-word invariant

For any w of length <=c, induction on prefixes gives

    S'w = Sw union N.

The assertion is immediate for b. For a, the preceding old image contains
p because that prefix has length <c. The new cycle sends the complete set
{p} union N onto itself; the other old transitions agree. Thus the lifted
and old ranks differ by exactly t through the first compression. Every
word of length <c preserves rank and an old shortest compression word
still compresses. This proves equality, not just a lower bound.

### Reachability and connectivity

Choose a positive L with L=0 mod(t+1) and L=1 mod M, which exists by
coprimality. Replace each occurrence of a in any old word by a^L. The
encoded word acts like the old word on Q and fixes every new state. An
encoded full-Q reach word for S therefore reaches S'. Encoded old state
paths connect all old states. The new cycle connects p to every new state
and every new state to p, so the whole lifted graph is strongly connected.

### Full-Q synchronization

Pick z in Q distinct from p. Strong connectivity allows an old reset word
followed by a state path that resets Q to z. Encode that word as V. Then
QV={z} and NV=N. Start by applying V to the full lifted Q. If a new state
q remains in its image, apply a^j with qa^j=p, then b, then V. The sole
selected cycle member reaching p moves into old Q under b, since b(p)!=p;
all other selected new states remain new and distinct. The old selected
state z stays old and avoids p during a^j, since it belongs to a different
permutation cycle. Finally V resets all old images to z. Exactly one new
image disappears. Repeat t times. This constructs a reset word; no claim
that this word is shortest is needed.

## Reachable corank-three application

The independently checked twelve-state base has

    a=[2,5,8,4,1,7,3,6,9,0,10,11]
    b=[0,6,4,10,7,3,1,5,11,4,2,8]
    S=Q\{2,8,11}, p=10.

The permutation a has order 12. The word baaababbaa reaches S from Q;
aabaaabab compresses S in 9 steps. All shorter words preserve its size
and retain p. The exact pair-distance Bellman certificate, independent
set checks and the literal words are stored in
data/near_full_n12_r3/protected_witness.json. The independent checker uses
no search or lift-constructor imports.

For every n=12+t with gcd(t+1,12)=1, the theorem therefore supplies a
strongly connected synchronizing DFA and a Q-reachable (n-3)-set with
c(S')=9. There are unbounded such n.

For an unrounded universal harmonic proposal

    c(T) <= C n(n-|T|+1)/(|T|-1),

the family requires C >= 9(n-4)/(4n), hence **C>=9/4** in the limit.
In particular C=2 is false for all eligible n>36 (the saved n=46 instance
is one example). For the rounded proposal with a ceiling, every fixed
C<2 fails eventually. This family does **not** refute rounded C=2:
ceil(8n/(n-4))>=9. No statement about minimality of the C=2 counterexample
or nonexistence of stronger bases is asserted.

## Limit of the protected-point approach

The known avoid-or-compress lemma gives c(S)<=|Q|-1 whenever a singleton
p persists in every shorter image in a strongly connected synchronizing DFA. Apply it with
A={p}: a word of length <=|Q|-1 either avoids p or compresses S. If
c(S)>|Q|-1, neither outcome is possible, a contradiction. Thus this
method cannot preserve a superlinear bottleneck from a fixed protected
base. This is a consequence of known theory, not a new avoiding bound.
Here p is avoidable: synchronization followed by a state path reaches an
old state different from p. This checks the avoiding lemma's hypothesis.

Primary source: [Szykula, Improving the Upper Bound on the Length of the
Shortest Reset Words (2018)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol096-stacs2018/LIPIcs.STACS.2018.56/LIPIcs.STACS.2018.56.pdf).
