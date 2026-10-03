# A constant-length word shortcut worsens the policy for infinitely many n

**PROVED on paper:** for every n>=6 the SC binary base below has rt=P=n,
but adjoining a unit-cost label for its existing length-seven word gives
rt=n and P>=n+1. The transformation monoid and all reachable images stay
unchanged. This is an obstruction to policy monotonicity, not to Cerny.
Priority of this precise family remains OPEN. Right actions are used.

Let Q={0,...,n-1}, n>=4, and

    a=[1,0,0,2,3,...,n-2], b(q)=q+1 mod n,
    u=b b a b b b a, c(q)=q u.

For n>=5, c(0)=c(n-1)=2, c(q)=q+3 for 1<=q<=n-5,
c(n-4)=1, c(n-3)=0, c(n-2)=3. For n=4 it is [2,0,1,2].
Both nonpermutations have rank n-1 and image V=Q\{n-1}; their only
double fibers are {1,2} for a (target 0) and {0,n-1} for c (target 2).
Adding c changes word costs, while it cannot change the generated monoid.

## All nonempty subsets are actual images, and extend within n

Induct downwards on subset size. For a nonempty proper S choose a cyclic
boundary h outside S with d=h+1 inside S. Let r=d and Y=S b^(-r).
Then 0 belongs to Y and n-1 does not. Hence |a^-1Y|=|Y|+1 and
(a^-1Y)a=Y. By induction T=a^-1Y is an actual image (or Q).
The word a b^r, of length <=n, maps T ONTO S. This proves complete
reachability and e(S)<=n for every proper S in the binary base. The
augmented automaton has the same image family and no larger extension
cost. Strong connectivity follows from b. Thus the sufficient square
condition in ANCHORED_IMAGE_PROFILE.md applies to both automata.
This reconstruction of an extension mechanism is not claimed as a new
general complete-reachability theorem.

## Exact reset threshold and base policy

The word a^(n-2) b a resets Q to 0, with length n. Each letter can drop
rank by at most one. A reset shorter than n would therefore have exactly
n-1 steps, every step a rank drop. Its first a or c gives V. Since n-1
is absent from V and every subsequent a-image, c cannot drop rank there;
b never drops rank. The subsequent steps must all be a. Its repeated
images end at {0,1}, which a swaps. This excludes such a reset, proving
rt=n in both alphabets for every n>=4.

For the base, {0} has extension cost 1 via the image {1,2} and a.
The pair {1,2} has extension cost 2 via {0,1,2} and ab: its one-letter
inverse images have size <=2. For S_k={0,...,k-1}, 3<=k<n, the one-letter
inverse a^-1 S_k=S_(k+1) is an image. These phases cost
1+2+(n-3)=n. Since rt<=P, this proves P_base=n.

## A critical three-image requires another neutral step

Now n>=6, and T={0,n-4,n-1}. For any subset X,

    |a^-1X|-|X|=1_(0 in X)-1_(n-1 in X),
    |c^-1X|-|X|=1_(2 in X)-1_(n-1 in X),
    |b^-1X|-|X|=0.

Any word carrying Q into T of length <=n-2, read inversely from T to Q,
would need net gain n-3. These unit-defect letters allow no decrease and
at most ONE neutral step within that budget. Initially T contains n-1,
so no positive step is possible. Its possible first neutral steps are:

* a^-1T={1,2,n-3}, which excludes 0 and includes 2;
* b^-1T={n-1,n-5,n-2}, still containing n-1;
* at n=6, c^-1T={0,3,n-1}, still containing n-1. For n>=7
  c^-1T has size 2, so it is a forbidden decrease.

After the first a step, the only positive next step is c. That step
introduces n-1, yielding a four-set still smaller than Q. Another neutral
step is then necessary before any further growth. The other neutral
choices already retain n-1 and permit no growth. All possibilities
contradict the budget. Consequently D(Q,T)>=n-1, where D allows the
terminal Q-image to be a subset of T. At n=5 the analogous guard DOES
reach Q; the excluded boundary is necessary.

## Every initial singleton costs more than n

Because all subsets are reachable and each inverse edge gains at most
one, a shortest image extension from rank k first reaches exactly rank
k+1. Its endpoint must be that whole inverse image: no larger contained
image exists at that first distance. Every policy chain from a singleton
therefore has n-1 phases, each with positive cost.

In the augmented alphabet singleton 0 has e=1 with the ONLY endpoint
{1,2} (via a). That pair has e=1 with the ONLY endpoint T (via c).
Thus G({0})=2+G(T)>=n+1, since the policy constructs an actual transport
Q into T and G(T)>=D(Q,T).

Singleton 2 has e=1 with the ONLY endpoint {0,n-1} (via c). This pair
has e=2 and ONLY first-growth endpoint T, through inverse a then inverse
c. Inverse b retains n-1 and cannot grow at the next step; inverse c
decreases to a singleton, which cannot grow to rank 3 in one step.
Thus G({2})=3+G(T)>=n+2.

Every other singleton has e>=2. If e>=3, its first cost plus n-2
remaining positive phases already gives >=n+1. If e=2, its intermediate
inverse prefix must be a singleton, and the next step grows only at
target 0 or 2. Its first endpoint is therefore {1,2} or {0,n-1}, whose
values just proved give total >n. This proves P_augmented>=n+1.

## Exact finite data and boundaries

For n=4,...,22 the exact augmented P values are

    5,5,9,9,13,13,17,17,21,21,25,25,29,29,33,33,37,37,41.

The apparent formula 2n-3 for even n and 2n-5 for odd n>=5 is
**CONJECTURED**, not an arbitrary-n theorem. In particular an unbounded
policy gap is not proved by the lower bound n+1. The n4 failure is the
state-minimal word-shortcut witness in ALPHABET_POLICY_OBSTRUCTION.md;
n5 has P=rt=5. A different shortcut b^2 a b^(n-1) a gives P=n in the
tested n5..12, so replacing the fixed three b's by that parameter rotation
does not preserve the observed failure.

The full-cube native solver and an independent ordinary-set sparse inverse
all-tie recursion agree on EVERY saved singleton e/G/worst value through
n22. The older forward-transport kernel additionally agrees through n12.
Independent closed graphs exclude all reset words of length <n and all
critical transports of length <=n-2 for the saved cases. Paper proofs,
not finite graphs, establish the arbitrary-n claims above. No Lean result.
