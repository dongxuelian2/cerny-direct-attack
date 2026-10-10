# A uniform lower bound at codimension three

For n>=10 and 1<=r<=n-5, there is a binary strongly connected synchronizing
automaton with reachable S of size n-3 and ac(S,A)=min(n-r,9).
Together with the first face (r=n-4), this proves

    F_bin(n,n-3,r) >= min(n-r,9).

When n-r<=9 the known upper bound agrees, so F_bin=F=n-r.
This does not prove an upper bound nine in the remaining compression range.

Put L=n-5>=5. Let T={x_0,...,x_(L-2),z}, K={v,y,c,t}, and add d.
Letter b cycles T, cycles v,y,c,t, and fixes d.
Letter a swaps z,y and c,d, sends t to z, and fixes the other states.
Set S=T union {v,t}. The same reaching word abbbabaabb works for every L:
its holes are successively
{t}, {v}, {y}, {c}, {t,d}, {v,d}, {v,t,c}, {v,t,d}, {v,y,d}, {y,c,d}.
The a-interchanges join the b-cycles and d, proving strong connectivity.

The complete 17-row short-image table in BINARY_OBSTRUCTION_PROOF.md
is unchanged for every L>=5: it only uses z,x_0,x_1,x_2 from T.
It proves preservation of cardinality through length eight, and that the
first possible missing T-states are z at depth five, x_0 at six,
x_1 at seven, x_2 at eight. No other T-state is absent through depth eight.
The words ababa b^j, j=0,1,2,3, attain those four avoidance depths.
The word ababbbaba compresses at length nine.

For r<L choose the last r of x_0,...,x_(L-2); for r=L choose all of T.
If r<=L-4, all chosen states have index at least three and ac=9.
If r=L-3,L-2,L-1,L, the respective first omitted protected state is
x_2,x_1,x_0,z, giving ac=8,7,6,5. These values equal min(n-r,9).

Here is a synchronization proof valid for every L>=5, including all residues
modulo four. Put N=lcm(L,4), so b^N is the identity. The unit e=a^2 sends
t to y. Conjugates b^(N-i)e b^i merge all opposite pairs in K.
Rotate a d--K pair to {d,v}; a takes it to the opposite pair {c,v}.
The pair {c,z} maps by a to {d,y}. The word b^4 a b^(N-4) takes {d,z}
to {c,z}: z b^4=x_3 (which exists since L>=5), while the final exponent
fixes c and returns the T-point to z. Therefore every d--T pair merges.
An adjacent K-pair rotates to {c,t} and a takes it to {d,z}.
For a T--K pair, rotate its K-point to c; if its T-point is z use {c,z},
otherwise a takes it to a d--T pair. Finally rotate one point of a
T--T pair to z and apply a, giving a T--K pair.
Every pair merges. Iteratively merging two points of the current full-set
image gives an original-letter reset.

No inverse letters are introduced: every conjugate uses nonnegative powers
of b. The bound is a uniform lower construction and becomes an exact value
only where it meets an independently known upper bound. In particular it
does not assert that F_bin or F is nine for all n-r>=10.
