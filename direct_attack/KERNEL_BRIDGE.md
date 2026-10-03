# Kernel bridge (independent reconstruction of Pin 1978)

Status: **PROVED**, not **FORMALLY VERIFIED**. No improvement to the best
general asymptotic synchronization bound is claimed.

Let A be a complete synchronizing DFA with n states and arbitrary finite
alphabet. Words act on the right: S(uv)=(Su)v. Let u have rank k, 2<=k<=n.
For every k-subset S there exists a word v of length at most n-k+1 such that

    |S v u| < k.                                             (KB)

Neither strong connectivity nor reachability of S from Q is required. The
bound counts v only; the compression word is vu and costs |u|+n-k+1.

Stronger form: A need not synchronize Q. It suffices that S is compressible.
The fibers may be ANY partition into k nonempty blocks, whether or not they
come from a word. Some word of length <=n-k+1 sends S to a set missing a
block. To recover the word vu, the rank-k map u must be an actual word of A.

## Complete proof

Work over the rationals. For each letter a let M_a have entry (p,q) equal to
1 exactly when pa=q. Thus M_uv=M_u M_v. Write [S] for the row indicator
vector of S, and R=Qu. The k nonempty fibers F_q={p:pu=q}, q in R, partition Q.
Define the linear subspace

    W={x in Q^n : sum_(p in F_q) x_p is the same for all q in R}.

The k-1 equality constraints are independent: the linear map sending x to
its k fiber sums is surjective, since every fiber is nonempty. Consequently
dim W=n-k+1.

For any word v, x=[S]M_v is a nonnegative integer vector of total mass k.
If x lies in W, each fiber sum is exactly 1. Conversely, if |Svu|=k, every
fiber contains at least one image of an original member of S. The k fiber
sums are positive integers with total k, and hence all equal 1. Therefore

    [S]M_v lies outside W  <=>  |Svu|<k.                      (1)

This equivalence uses multiplicity vectors, not just image indicators. It
remains valid if S has already compressed under v.

Let L_i=span{[S]M_v: |v|<=i}. Then L_0 has dimension 1 and L_i is an ascending
chain. If L_i=L_(i+1), then L_i M_a is contained in L_i for every letter a;
induction gives L_j=L_i for every j>=i. Thus the chain cannot stop growing
before it contains the whole orbit span.

For a word z compressing S, [S]M_z has support size <k, so it misses at
least one of the k fibers. Its total mass is still k, so its fiber sums
cannot all be equal. Thus it does not lie in W. Hence the orbit span is
not contained in W. Put D=dim W. If all words of length <=D had vectors in W,
then L_D would be contained in W. Either the chain stabilized earlier,
contradicting the reset vector, or dim L_D>=D+1, contradicting dim W=D.
Some v of length <=D therefore satisfies (1). This proves (KB).

## Consequences and limits

Define lambda_r=min{|u|: |Qu|<=n-r}, lambda_0=0. For k=n-r>=2,

    c(S):=min{|w|: |Sw|<|S|} <= lambda_r+r+1,  |S|=k.        (2)

If a word attaining lambda_r has rank <k, apply it directly; otherwise apply
(KB). This also gives the same bound for all subsets of size >=k, by choosing
a k-subset and preserving its collision. Combining (2) with Pin--Frankl gives
the automaton-dependent bound

    rt(A) <= sum_(r=0)^(n-2) min{(r+1)(r+2)/2,lambda_r+r+1}.  (3)

Skipping ranks only reduces this positive sum. The lambda values in (3)
exclude the reset threshold lambda_(n-1), so the formula is not literally
the reset-distance tautology. However, large low-rank lambda values make it
revert to the cubic Pin--Frankl estimate. It gives NO new uniform coefficient.

For the saved four-state bottleneck automaton a=(0,0,1,3), b=(3,1,3,2),
lambda_2=2 and the pair {0,3} needs 5 letters. Thus (2) is sharp there:
2+(4-2)+1=5. The original bridge length n-k+1=3 is also sharp with u=aa and
S={0,3}: no bridge of length <=2 compresses Svu; v=bab does.

**KNOWN, not novel.** Pin's 1978 paper, Corollary 4, states precisely the
short-transversal persistence assertion whose contrapositive gives (KB),
including arbitrary partitions. Proposition 5 gives the rank recurrence
2|u|+n-k+1. The proof above independently reconstructs those mechanisms.
Source: [Pin, Utilisation de l'algebre lineaire en theorie des automates,
Corollary 4 and Proposition 5](https://www.irif.fr/~jep/PDF/AlgebreLineaire.pdf).
Formula (3) is a direct combination with Pin--Frankl, not a new general bound.

## Audit

- k=1 excluded: no nonempty singleton can be compressed.
- n=1 handled separately by the empty reset word.
- u may be empty at k=n; then a non-permutation letter provides v of length 1.
- S is arbitrary, including unreachable subsets.
- The order is v followed by u. Reversing this order is not authorized.
- W is linear, while the actual orbit has fixed total mass k. Both facts are
  used; replacing integer occupancy by a real probability vector loses (1).
- Stabilization is invariant under right multiplication by every letter.
- An eventual compression vector ensures escape without global synchronization.
- This proof does not assert that v itself compresses S.
