# Necessary short-pair structure for tight compression

This is a direct consequence of the credited Frankl--Pin refinement, not
an asserted exact formula. It applies to arbitrary finite alphabets.
Put m=n-s and T=binom(m+2,2). Let P_h be the pairs merging in at most h letters.
If some s-subset has shortest compression length T, then

    |P_h| <= h    for every 1<=h<=m.

Proof: any q<=m+1 distinct pairs admit an s-subset Frankl--Pin sequence
of length q, in any chosen order, indexed i=0,...,q-1. For its ith pair E_i, choose a hole set
H_i of size m disjoint from E_i, containing an endpoint outside E_i of
each later pair. Each later pair is distinct and thus has such an endpoint.
There are at most q-i-1<=m required endpoints. Fill H_i outside E_i;
n-2>=m since s>=2. Then S_i=Q minus H_i contains E_i and fails to contain
every later pair, giving the required sequence. This is exactly the
standard convention E_i is not contained in S_j for j<i: S_j was chosen
to omit an endpoint of its later pair E_i. No reversal of the sequence
or change of the Frankl--Pin convention is needed.

If |P_h|>=h+1 for h<=m, choose h+1 of those pairs, so p(P_h)>=h+1.
The bound T-p(P_h)+h from CIAA 2016 Theorem 1 yields compression <=T-1,
contradicting tightness. Merging words shorter than h can be padded with
arbitrary original letters, so the refinement's height convention agrees.

At codimension three, any length-ten compression witness therefore has
at most 1,2,3 merged pairs within respectively 1,2,3 letters, irrespective
of alphabet size. This explains a safe synthesis prune. It does not prove
nonexistence of such a witness or a general compression upper bound nine.
