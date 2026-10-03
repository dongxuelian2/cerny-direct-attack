# Exact contiguous-anchor quotient formula

Status: **PROVED** by the paper argument below. No Lean status is implied.

## Main theorem

For every integer r>=2 and n>=r+2, let L=floor(log2(r-1)). Then

    B_r(n)=3n+Lr-2^(L+1)-3 = 3n+E(r)-2r-3.

Here E(r) is the minimum external path length of a full binary tree with
r leaves. Thus the conjecture is closed for all parameters. The proof has
two independently checkable parts: the general genealogy lower bound, and
a deterministic capacity2 construction. This file supplies the latter in
full detail; `GENEALOGY_LOWER_BOUND.md` supplies the former.

## Lower bound (summary of the separate full proof)

Lift any quotient path to labelled particles, permitting free permutations
inside the hidden block. Its n-1 effective b letters create a binary
genealogy. Count every other letter in a separate clock. Successive merge
events differ by at least2. A merged particle at0 needs at least r such
letters to merge again as the n-1 particle, and r+1 to merge again as the0
particle. Reverse the genealogy. The kth split clock is therefore at least

    t_1=0,
    t_k=max(t_(k-1)+2, t_floor(k/2)+r+(k mod2)).

The recurrence solves to

    t_k=2(k-1)+max_{0<=d<=floor(log2 k)}(d*r-2^(d+1)+2).

At k=n-1>=r, the maximum is Lr-2^(L+1)+2. Adding the n-1 effective letters
gives the lower bound in the theorem. Ineffective b letters are included
in the clock; they are not silently discarded.

## The exact capacity2 construction

Put K=r+1 and C=Lr-2^(L+1). For every positive integer i define

    F(i)=min_{d>=0}(2^(d+1)*i-d*r).

The minimum exists: the expression eventually increases without bound.
Define K split clocks

    s_i=C+F(i),  1<=i<=K,       A=s_K=C+2K.

These clocks have elementary properties proved next. The construction
starts at a singleton at0 in the **reverse** capacity2 quotient. At clock0
split it by reversing b, obtaining two particles at0,n-1. For t=1,...,A,
reverse a once, choosing the hidden input bit u_t=1 exactly when t is one
of s_2,...,s_K, and u_t=0 otherwise. When u_t=1, immediately reverse b to
split the particle at0 into particles at0,n-1.

There are no ineffective b letters. We prove every step feasible at
capacity2, and the final vertex is the full set with hidden count2.

### Arithmetic properties of the clocks

For fixed i, consecutive d expressions differ by 2^(d+1)*i-r. Thus
the minimizing d is where these differences change sign. It follows that

* F(1)=2^(L+1)-Lr, so s_1=0;
* F(i)=2i whenever 2i>=r;
* F(i+1)>=F(i)+2, since every affine expression has slope at least2;
* if 2p<=r, F(2p)=F(p)+r. Indeed a minimizing index for F(p) can be
  chosen at least1 (the d=1 term is no larger than the d=0 term), and
  reindexing d+1 in F(2p) gives the identity.

Consequently s_(i+1)>=s_i+2. For every even index 2p<=K,

    s_(2p)-s_p = r,

except when r is odd and 2p=r+1, where F(p)=2p and F(2p)=4p, giving

    s_(2p)-s_p = r+1.

In particular every such difference lies in {r,r+1}.

### Ordered releases and buffer feasibility

A reverse split at clock s_i produces a particle at0 and one at n-1.
Under subsequent reverse a steps, the latter exits into the hidden block
after r-1 steps and is available as an input after r steps; the former
exits after r steps and is available after r+1. Later splits only fill an
empty n-1 site, so do not alter these trajectories. The exact input-ready
times are s_i+r and s_i+r+1.

Include the initial root's ready time q_1=0. Since split clocks differ
by at least2, all ready times are strictly ordered in parent-pair order:

    q_(2p)=s_p+r,     q_(2p+1)=s_p+r+1.

For 2<=k<=K, the clock properties give q_k<=s_k: even k follows directly,
and odd k follows from s_(2p+1)>=s_(2p)+2>=s_p+r+2. Thus no input is
requested before a particle is available.

For 2<=k<=K+1 they also give s_(k-1)<=q_k. If k=2p, use
s_(2p-1)<=s_(2p)-2<=s_p+r-1. If k=2p+1, use
s_(2p)<=s_p+r+1. At k=2, s_1=0<=r. For the endpoint k=K+1,
check separately that q_(K+1)=A=s_K: if r=2p use
s_(p+1)+r=C+2r+2; if r=2p+1 use s_(p+1)+r+1=C+2r+2.

Finally q_(K+2)=A+1. To check explicitly:
if r=2p, q_(r+3)=s_(p+1)+r+1=C+2r+3;
if r=2p+1, q_(r+3)=s_(p+2)+r=C+2r+3.
In both cases A=C+2r+2. The F values used here are in the F(i)=2i regime.

Let R(t) count ready times q<=t, and N(t) count split clocks s<=t.
For every integer 0<=t<=A, the preceding interlacing and endpoint identity
prove

    N(t)<=R(t)<=N(t)+1.

Before the reverse a at time t>=1, hidden occupancy is

    j_(t-1)=R(t)-N(t-1).

This formula counts particles which have exited the window minus those
already consumed as split inputs. An exit occurs one clock before its
ready time. The root's dummy ready event and its split at0 cancel in this
count; the root is not being treated as a physical hidden particle.
If u_t=1, N(t)=N(t-1)+1 and the interlacing gives 1<=j<=2.
If u_t=0, N(t)=N(t-1) and it gives 0<=j<=1. These are exactly the reverse
rotation realizability inequalities

    u_t<=j_(t-1)<=1+u_t

at hidden capacity2. This establishes validity inductively, not merely
nonnegative particle counts. At a split time the previous input was0,
because clocks differ by at least2. Therefore the first two bits just
after reverse a are10, so reversing b is also feasible.

### The endpoint is full

For every i>r/2, F(i)=2i and hence s_i=C+2i. All these last split clocks
are spaced exactly2. A split fills two consecutive stream slots, at times
s_i and s_i-1. There are at least ceil(r/2)+1 such terminal splits, so
they fill all r stream slots A,A-1,...,A-r+1. Thus the final anchor word
is all ones. The process started with one particle and performed K=r+1
splits, so it has r+2 particles; exactly two must be hidden. Equivalently
R(A+1)-N(A)=2, by q_(K+2)=A+1 and strict ordering of releases.

We have constructed a reverse path from a singleton to the full set at
capacity2. Reversing its edges yields a forward quotient path of length

    A+K = C+3K = (L+3)r-2^(L+1)+3.

This equals the proved lower bound at n=r+2.

## Arbitrary hidden capacity

For m=n-r>=2, prepend m-2 forward baa cycles, taking the all-one window
from hidden count m to2. A path valid at capacity2 embeds into every larger
capacity, as proved in `GENERAL_STABILIZATION.md`. Total length is

    3(m-2)+(L+3)r-2^(L+1)+3 = 3n+Lr-2^(L+1)-3.

This completes the all-parameter equality.

## Relation to external path length

With h=ceil(log2 r)=L+1, the minimum external path length is
E(r)=(h+1)r-2^h=(L+2)r-2^(L+1). This is the independent binary-tree
fact proved in `AFFINE_CERTIFICATES.md`. Therefore the displayed closed
formula is exactly 3n+E(r)-2r-3. The proof above derives the same dyadic
constant from a genealogy scheduling recurrence; it does not assume a
cost-preserving identification of arbitrary quotient paths with optimal
prefix codes.
