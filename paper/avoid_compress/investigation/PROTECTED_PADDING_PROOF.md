# Exact codimension-four bands n-r=10 and 11

There are binary strongly connected synchronizing witnesses with actual
reachable S for

    F_bin(r+10,r+6,r)=F(r+10,r+6,r)=10, r>=1,
    F_bin(r+11,r+7,r)=F(r+11,r+7,r)=11, r>=1.

The lower proof uses a complete finite twelve-state base certificate and
a parameter-uniform set-image lifting argument. The upper is the known
avoid-or-compress bound. The r=1 instance of the ten-band is the separately
checked (11,7,1) witness in frontier_certificates.json.

## Finite base (computer-assisted)

Use P={p_0,...,p_4}, U={u_1,...,u_7}. Letter a fixes p_0,p_1,p_2,
swaps p_3,p_4 and cycles U. Letter b maps p_i to p_(i-1) for i>=1,
p_0 to u_4, u_1 to u_2 to u_3 to p_4, u_4 to u_5 to u_6 to p_4,
and fixes u_7. Put S=P union {u_1,u_2,u_3}.

In coordinates p_0,...,p_4,u_1,...,u_7 the rows are

    a=[0,1,2,4,3,6,7,8,9,10,11,5],
    b=[8,0,1,2,3,6,7,4,9,10,4,11].

The complete 62-state short-image certificate proves every word of length
<=10 preserves |S| and contains p_0, and every word of length <=9 also
contains p_1. The word a^6 b a^3 b compresses at length eleven;
a^6 b a b^2 omits p_1 at length ten.
Thus ac(S,{p_0})=11 and ac(S,{p_0,p_1})=10.
protected_padding_base.json records every short-image set, its level and
both successors below level ten. The independent checker rebuilds the
whole BFS without reading this certificate.

## Protected edge lifting

Insert k>=0 states H={h_1,...,h_k} on the b-edge p_0 -> u_4:
p_0 -> h_1 -> ... -> h_k -> u_4. Fix H under a, and leave all other
old transitions unchanged. Put S'=S union H and A'=A union H.

For every old subset T containing p_0,

    (T union H)a' = Ta union H,
    (T union H)b' = Tb union H.

Indeed the new chain has all its internal states covered, and its last
state supplies the former b-image of p_0. Every safe old prefix contains
p_0. Induction therefore lifts all prefixes through the first old unsafe
word, preserving both cardinality loss and protected-state omission.
Consequently ac(S',A')=ac(S,A), including attainment by the same word.

## Structural requirements for every k

Let B=P union H union {u_4,u_5,u_6}; b cycles B in the order
p_0,h_1,...,h_k,u_4,u_5,u_6,p_4,p_3,p_2,p_1.
Put s=|B|=8+k and E=B union {u_7}. Then Qb^3=E.
The a-cycle on U connects all outside states to B; b cycles B, proving
strong connectivity.

Set d=a^6 b^s. On E it fixes P union H and acts by
u_4 -> u_6 -> u_5 -> u_4, u_7 -> u_6. Hence e=d^3 fixes B and sends
u_7 to u_4. Thus Qb^3 e=B and Ba^4=S'; the actual reaching word is
b^3(a^6 b^s)^3 a^4.

On B, f=ae cycles u_4,u_5,u_6 and swaps p_3,p_4.
Therefore f^3 is the transposition of p_3,p_4, two adjacent b-cycle points.
The words b and f^3 generate the full symmetric group on B. Inverses are
positive powers on B, so no extra input letters are introduced.
Moreover Ba=(B minus {u_4}) union {u_7}, whence
Bab=(B minus {u_5}) union {u_7}; applying e compresses B to B minus {u_5}.
Thus h=abe is a compressing transformation of B.
Use permutations of B to send any pair in the current image into h's
colliding fiber and apply h. Iterating synchronizes B. Prepending b^3 e
synchronizes Q. Every permutation and compression is an original-letter word.

For A={p_0}, r=k+1, n=r+11 and |S'|=r+7.
For A={p_0,p_1}, r=k+2, n=r+10 and |S'|=r+6.
The two lengths meet n-r, and the compression upper is 15 at codimension
four. This establishes the stated exact bands; it asserts nothing at
n-r>=12. The independent checker audits all r through twenty and all
macro actions, reaching words, exact local lengths and literal resets.

## Smaller protected subsets in the same eleven-valued automaton

For any n>=12, choose k=n-12 and any r-element subset of {p_0} union H
containing p_0, where 1<=r<=k+1=n-11. Every short image through depth ten
contains {p_0} union H. The same length-eleven word compresses the image.
Consequently ac=11 for every such choice, proving F_bin(n,n-4,r)>=11.
This is not an upper bound eleven when n-r>11. The checker independently
recomputes all 210 such parameter choices through n=31.
