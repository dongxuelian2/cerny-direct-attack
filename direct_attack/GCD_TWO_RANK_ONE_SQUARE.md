# Arbitrary rank-one tails at gcd(M,L)=2

Date:2026-10-03. **PROVED (paper), ALL parameters in the stated class.**
Independent finite controls are **COMPUTATIONALLY VERIFIED** separately.
The all-n theorem is not FORMALLY VERIFIED. General Cerny remains OPEN.
No novelty claim or reduction from arbitrary automata.

Let ORIGINAL b cycle C=Z_M and fix r, M>=3. ORIGINAL a has rank M,
doubled output r, a(r)=0, omitted output L in1..M-1, and any two
distinct kernel inputs K in the core. Every other core input maps
bijectively to C\{0,L}. If gcd(M,L)=2 and the automaton is synchronizing,
there is ONE ORIGINAL reset of length<=M^2=(n-1)^2. At M>=6 the proof
establishes synchronization without assuming it. Tail height and all
cycle structure of a are unrestricted. Larger alphabets inherit the
bound when the specified binary pair itself satisfies the theorem.

Together with KERNEL_ROOT_RETURN_SQUARE.md this proves the square bound
for ALL gcd(M,L)<=2 forms in this moving-root/doubled-b-fixed-state class
(the tiny nonsynchronizing M2 form is vacuous). If a(r)=r instead, the
same fixed doubled root has the elementary bound1+M(M-1): choose a b^j
to move its omitted output outside the current proper root subset at
each step. No coprimality condition is needed in that fixed-root case.

## The only new case is a late return

Put g=2 and t=M/2. For M>=6, t>=3. A two-point kernel set cannot
be invariant under translation L, whose orbits have length t. Thus
some J in K has L+J outside K. If any such J<=M-2, the previous
kernel-return criterion J+g<=M already proves the bound.

The remaining case has unique admissible J=M-1 and other kernel input

    H=M-1-L,       K={H,J}.

Both H,J are odd, since M,L are even; H is positive. The literal
f=a b^J a, of cost M+1, fixes r and has full defect

    D(f)=e_r+e_0-e_L-e_z,       z=a(L-1) in C\{0,L}.

Let p=a^-1(M-L). This is a core state outside K, so p<=M-2.
The actual root inverse of f is {r,p}. The paid original seed
v=a b^p f has length p+M+2 and exact root inverse {r,H,J}.
Its designated first extension a b^J has length M, root retained,
and inverse {r,H,J,p}. In particular the next core size is THREE.

## Root stages and their potentially excessive cost

Nonwhole core subsets extend by ONE, with root retained, using an
original a b^j of cost<=M. A proper nonempty whole core subset is
exactly ONE parity class, of size t. It extends by ONE under f b^s,
where s=0 or1 is the smallest shift with z+s outside that class.
Its cost is M+1+s. There is at mostONE such stage in the full core
size sequence2,3,...,M-1.

If no whole stage occurs, the total cost is at most

    p+M+2+M(M-2)=M^2-M+p+2<=M^2.

If it occurs with shift s, the preliminary bound is

    p+M+2+(M-3)M+(M+1+s)=M^2-M+p+3+s.

For p<=M-4 this is already<=M^2. The two extreme p values are
paid by two compulsory savings in distinct stages, as follows.

## First saving when p=M-2

After the designated first extension the core is {H,J,p}. H,J are
odd and p is even. The sole even point p has p+L outside this set,
since L is a nonzero even shift. The next nonwhole step can therefore
use j=p, of cost M-1, saving ONE versus M. This is the stage of
core size THREE; taking the smallest boundary is at least as cheap.

## Second saving after the costly whole step

Only s=1 can need this second payment. The target whole subset U
contains z, since shift0 failed, and has size t. After f b it has
core size t+1. Both kernel points H,J occur in that preimage or
both fail to occur: f b maps each to core point1.

Write E for the even points of this new core set.

* E cannot be empty, because the core has t+1 points and there are
  only t odd points.
* If 0<|E|<t, translation L cycles all even points, so an even
  boundary j exists. It satisfies j<=M-2 and yields cost<=M-1.
* If |E|=t, there is exactlyONE odd point. Both kernel points
  therefore fail to occur, so that point is not J=M-1. It is a
  boundary of cost<=M-2.

In every case the next root extension costs<=M-1, saving at leastONE.
This step exists: t+1<M at M>=6. It is distinct from the core-size
THREE saving above, because t+1>=4.

Now p=M-3 needs onlyONE saving when s1, and the post-whole step
supplies it; s0 was already within square. For p=M-2, s0 needs
ONE saving supplied at core size3, while s1 needsTWO, supplied by
the two distinct steps. All paid factors form the SAME actual reset.
Thus no case exceeds M^2. No return word has been priced as one letter.

## M4 and scope

At M4, L2, a kernel set that is not an opposite pair has a return
J<=2 and is covered by the previous criterion. If K is an opposite
pair, the partition {0,2},{1,3},{r} is preserved by both original
letters, and each induces a permutation of its THREE blocks.
The remaining nonkernel pair necessarily maps to {1,3}, r maps to
{0,2}, and K maps to {r}. Consequently these cases cannot synchronize.
This handles every synchronizing M4 input; gcd2 has no other smaller M.

The independent checker tests2446 literal late-return inputs, including
COMPLETE1488 new forms M6/M8,78809372 particle controls and53700 root
stages. It checks592 critical first savings and96 post-expensive-whole
savings explicitly, all2446 compatible reset words through n257, and
seven rejected corruptions. Larger controls force the extreme p values
instead of relying only on random permutations.

This removes ALL gcd2 arbitrary-tail gaps in the stated class. It does
not remove the c0 opposite-pair order-two gap when M/2>2 (there g=M/2),
larger-g arbitrary kernel gaps, or the general Cerny gap. The new weighted
extension route for order two is CONJECTURED, not used in this proof.
