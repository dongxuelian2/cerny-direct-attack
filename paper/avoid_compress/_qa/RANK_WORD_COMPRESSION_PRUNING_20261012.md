# Existing transversal method: conditional compression pruning

Let |Q|=n, |S|=s>=2, and assume S is compressible. If a word u has
rank exactly s and length h, then S compresses within n-s+h+1 letters.

Put m=n-s. Suppose all words of length <=m+h+1 preserve |S|. The s
fibers of u partition Q. Each Sv for |v|<=m+1 is a transversal, since
|Svu|=s. Their trajectory rows lie in the space T whose fiber sums
are equal. Its dimension is m+1. For V_i=span{chi_S D_v:|v|<=i}, an
early plateau gives invariance and permanent containment in T, impossible
because a compressed trajectory has support <s and an empty fiber.
Thus V_m=T. Every generator of V_m maps into T under each letter, so
T is invariant, giving the same contradiction. This includes m=0.

If rank(u)<s, u itself compresses S. At (13,9,1), compression length
>=12 therefore forbids every word of rank <=9 and length <=6.
This requires eventual compressibility; it does not require S reachability.

No novelty claim: the transversal persistence argument is Pin's 1978
Corollaire 4, *Utilisation de l'algebre lineaire en theorie des automates*,
AFCET-SMF, pp.85-92. Primary author-uploaded text:
https://www.researchgate.net/publication/29616908_Utilisation_de_l%27algebre_lineaire_en_theorie_des_automates
Berlinkov--Szykula also cite its rank-word application:
https://arxiv.org/pdf/1412.8363 (p.14).

This is an auxiliary reuse of existing theory, outside the article and
publication package. It does not determine a numerical F value.
