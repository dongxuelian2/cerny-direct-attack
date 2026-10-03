# An unbounded penalty for insisting on a largest seed

**PROVED on paper.** For every n=6h, h>=1, the strongly connected
three-letter DFA below has rt=P=2, maximum actual one-letter merge capacity
kappa=3, and largest-seed best-policy budget F_kappa=n-2.
Thus F_kappa-P=n-4 and F_kappa/P=(n-2)/2 are unbounded. This refutes every
universal fixed additive or multiplicative approximation to P obtained by
insisting on maximum seed cardinality. It does not refute the OPEN bound
F_kappa<=(n-1)^2, the global policy square conjecture, or Cerny.

Use right actions on Q={0,...,n-1}, put j=n-4, and define

    a(q)=q mod 2, except a(j+1)=0;
    b(q)=q+1 mod n;
    c(0)=c(1)=0, c(q)=(q-1) mod 3 for q>=2.

All letters have unit cost. Here P=min_q G({q}), where G is the exact
all-shortest-phase reachable-image policy. F_kappa is 1 plus the least
G(T) among actual images of maximum size merged by ONE LETTER.

## Complete reachable images and the short reset

The full actual image family R={Qv} consists of Q, all singletons, every
cyclic adjacent pair {q,q+1}, every cyclic distance-two pair {q,q+2},
and every cyclic consecutive triple {q,q+1,q+2}. Its size is 4n+1.

These images are reachable: Qa={0,1}, Qab^3c={0,2}, Qc={0,1,2}, and
Qac={0}; appending powers of b supplies every rotation. The listed family
is closed: b rotates it, a maps every nonempty set to a nonempty subset of
{0,1}, and c maps it to a nonempty subset of {0,1,2}. Every such subset
belongs to the listed family. This proves both completeness and closure.
The cycle b makes the DFA strongly connected. The word ac resets in two
letters, and none of a,b,c is constant, so rt=2. For U={0,1}, e(U)=1
via Qa=U and G(U)=1, while Uc={0}. The policy ac costs 2; rt<=P proves
P=2 as well. No reachability word is being treated as free.

## The unique maximum merge source

All proper actual images have rank <=3; Q is not merged by a single letter.
The letter b merges none. The alternating 0/1 pattern of a has just one
monochromatic cyclic triple: T={j,j+1,j+2}, all three mapped to 0.
The changed odd position j+1 creates a run of exactly three zeros, with
ones on both sides; the even cycle has no additional boundary run.

The letter c has no monochromatic cyclic triple. Away from positions 0,1
its values cycle 0,1,2. The four exceptional triples beginning at n-2,
n-1,0,1 have value patterns (0,1,0), (1,0,0), (0,0,1), (0,1,2),
respectively, because n is divisible by 3. Hence kappa=3, and T is the
UNIQUE actual maximum-cardinality merge source.

## The full into-T transport lower bound

Because T has rank 3 and every other proper actual image has rank <=3,
Q is its only larger actual image. Consequently

    e(T)=G(T)=W(T)=min{|w|: Qw subset T}.

The word cb^j maps Q ONTO T and has length j+1=n-3. To prove it shortest,
allow a word to end at ANY nonempty subset of T, including a singleton.
Suppose a word of length ell<j+1 transports Q into T. It must contain a
letter a or c, since powers of b preserve Q. Write it as v x b^r, where
x is its last letter from {a,c}; let t=|vx|>=1 and J=Qvx.
Then J is a nonempty subset of {0,1,2}, and ell=t+r<=n-4 gives r<=n-5.
Thus translating J by r does not wrap around the n-cycle.

If t=1 or 2, J contains 0: the one-letter images are {0,1} and {0,1,2};
the two-letter possibilities ending in a or c are aa,ac,ca,cc,ba,bc,
whose images are respectively {0,1},{0},{0,1},{0,1},{0,1},{0,1,2}.
Landing inside T therefore requires r>=j, so ell>=j+1, a contradiction.
If t>=3, min J<=2, and landing inside T requires r>=j-2. Again
ell>=3+j-2=j+1, a contradiction. This covers all prefixes, further rank
drops, and strict terminal containment; it does not assume a rank-3 endpoint.

It follows that e(T)=G(T)=W(T)=n-3, and

    F_kappa=1+G(T)=n-2.

The forced-seed reset cb^j a attains that value. For every fixed K or C,
choose an eligible n with n>2K+2 or n>C+4, respectively. Then
F_kappa>K P or F_kappa>P+C. The obstruction concerns this selection rule,
not the existence of another square-bounded policy.

## Parameter and verification boundaries

The divisibility condition matters. At n=6h+2, the triple {n-1,0,1}
is c-monochromatic. It is an actual maximum merge source, but Qa={0,1}
lies inside it, so its G is 1 and F_kappa=2. The saved n8,n14,n20 controls
explicitly prevent promotion of this theorem to all even n.

The generator and independent checker cover ten eligible cases n6..60
and those three controls. Every saved e/G/W/forward entry is recomputed
using ordinary ALL-SOURCE forward BFS; the full closed family, unique
maximum source, exact words and three deliberately corrupted certificates
are checked. Arbitrary-n claims follow from the proof above, not from
finite enumeration. No new Lean theorem; literature priority is OPEN.
