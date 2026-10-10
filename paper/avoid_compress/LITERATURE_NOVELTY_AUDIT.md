# Literature and novelty audit

Checked on 7–8 October 2026. Target: the cardinality-face and two-block constructions and the complete computer-assisted codimension-three theorem, with binary, strongly connected, synchronizing witnesses and an actual reachable image. This audit reports the sources inspected and the claim boundaries; absence of a search hit is not a proof of priority.

## Primary-source comparison

| Source inspected | Relevant location | Treatment in the manuscript |
| --- | --- | --- |
| [Szykuła, Synchronizing Automata: Open Problems (2026), arXiv v1](https://arxiv.org/pdf/2608.24245v1), EPTCS 451, 33–47, [DOI](https://doi.org/10.4204/EPTCS.451.3) | Section 2.2, pp. 35–36: Lemma 3, Figure 2 and Open Problem 4 | Cite as the question being partially answered; acknowledge the existing pair case |
| [Szykuła, STACS 2018, published PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol096-stacs2018/LIPIcs.STACS.2018.56/LIPIcs.STACS.2018.56.pdf), [publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2018.56) | Lemma 2, pp. 56:4–56:5 | Original avoid-or-compress upper bound, explicitly credited and reproved |
| [Szykuła, arXiv:1702.05455v5](https://arxiv.org/pdf/1702.05455v5), [version record](https://arxiv.org/abs/1702.05455); also [v1](https://arxiv.org/pdf/1702.05455v1) | Lemma 2 in both inspected versions; v5 open-problem section | Check numbering and distinguish its different Open Problem 4 |
| [Ferens, Szykuła and Vorel, MFCS 2021](https://drops.dagstuhl.de/storage/00lipics/lipics-vol202-mfcs2021/LIPIcs.MFCS.2021.46/LIPIcs.MFCS.2021.46.pdf), [publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2021.46) | Definition of k-avoidance; discussion on p. 46:6 | Cite the nearby sharpness discussion; do not claim all local sharpness examples were previously unknown |
| [Volkov, Synchronization of finite automata (2022)](https://www.mathnet.ru/eng/rm10005) | Section 3.3, avoiding-word methods and multiplicity/linear-algebra background | Contextual cross-check only; not needed in the short-paper bibliography |
| [Volkov, List of Results on the Černý Conjecture and Reset Thresholds](https://arxiv.org/pdf/2508.15655), [version record](https://arxiv.org/abs/2508.15655) | Index and references to synchronization bounds | Broader cross-check; its reset-threshold focus does not establish absence of local sharpness results |

Rechecked on 9 October 2026: the DROPS publisher record and exported BibTeX use the singular, *Shortest Reset Word*, whereas the article PDF heading and arXiv title use the plural, *Shortest Reset Words*. The manuscript and its BibTeX now consistently follow the article PDF's plural title. Both title variants identify the same DOI; the singular publisher metadata is not treated as an error. The MFCS author name is Vojtěch Vorel; all diacritics are encoded in LaTeX/BibTeX.

## Version and definition checks

1. The survey's Lemma 3 labels the original result “Rephrased Lemma 1”. In the published 2018 article, and in both inspected arXiv versions v1 and v5, the needed bound is Lemma 2. The manuscript therefore cites **2018 Lemma 2** and **2026 Lemma 3**, without silently reproducing the mismatched numbering. No explanation for the mismatch is assumed.
2. The survey's Open Problem 4 is the two-cardinality avoid-or-compress question. Open Problem 4 in the 2018 extended arXiv paper concerns compressing a specified state with another. The new paper identifies the **2026** question, and does not answer the older question under the same number.
3. The original local condition is `A` not contained in `Sw`: at least one protected state is absent. In the MFCS k-avoiding problem, an entire set is disjoint from `Qw`. These are different predicates. Neither a long word avoiding all of a set nor a long reset word proves the local lower bound here.
4. The survey's existing Figure 2 is the `r=1` first-face construction, after relabeling. It already supplies the `s=2,r=1` sharpness case. That specialization is explicitly credited; its existence, its binary alphabet and the general upper bound are not presented as discoveries.

## Close prior sharpness passage: MFCS 2021, p. 46:6

The paragraph preceding Section 2.1 reports a related series with a fixed-state avoiding-or-compressing alternative and the expression `n-|S|+1`, citing 2018 Lemma 3. It does not give a full transition specification for that reported series or state the simultaneous `(s,r)` classification and reachable-image restrictions proved here. We have not reconstructed that unspecified series and do not certify disjointness of all its special cases from the first-face examples.

The printed bound should not be imported literally as a uniform bound on the present invariant. In the paper's already-proved second-face instance `n=4,r=1,M=3`, take states `p_0,u_1,u_2,u_3`, `S={p_0,u_1,u_2}`, `A={p_0}`. Its rows in that order are

```text
a = [0,2,3,1]
b = [1,0,2,0]
```

The empty word and all six words of lengths one and two preserve cardinality three and contain state zero; `aab` compresses to `{0,1}`. Thus the present local invariant equals 3, whereas `n-|S|+1=2`. This finite instance is included in the reproducibility data. It identifies a definition/notation/statement issue in interpreting the older prose, not a claimed new theorem about that publication. The safe editorial treatment is to cite the passage as related prior sharpness discussion, avoid a first-ever claim for the first face, and base every mathematical assertion on an explicit definition and proof. Clarification of the unspecified earlier family would strengthen a priority assessment, but is not needed for the correctness of this manuscript's statements.

## Search coverage

General web and arXiv-directed searches were made using the exact author/title/arXiv identifiers and combinations of:

- `avoid-or-compress`, `avoiding or compressing`, `sharp`, `tight`;
- `Szykuła`, `Szykula`, `Open Problem 4`, `2026`;
- `cardinality`, `cardinalities`, `cardinality gap`;
- the expressions `n-|A|` and `n-|S|+1` in avoiding-word context.

The direct-primary-source route was more useful than the phrase searches, several of which returned irrelevant material or no useful exact match. The 2026 survey's references led to the 2018 lemma and the 2021 near-prior passage. Metadata was checked against arXiv version records and publisher BibTeX records. The inspected primary sources and useful results above were used for claim comparison; aggregator summaries, unrelated Open Problem 4 results and unverified external announcements were not used as mathematical evidence.

No inspected source states the complete second-face theorem for all proper-image state counts or the every-fixed-pair larger-gap arithmetic progression with all four structural requirements. This is a **bounded search result**, not an exhaustive citation-database search, an author confirmation, or a certificate of global publication priority. Unindexed papers and unpublished constructions are outside its coverage.

## Current contribution and literature checks

The current paper is a partial answer. It gives the two cardinality faces, the cofinal larger-gap sharpness family, the codimension-one and -two equalities, the two-block exact band, and the complete codimension-three equality F_bin=F=min(n-r,9). The latter uses a computer-assisted, all-state-count structural proof; it is no longer only a binary finite obstruction. No absolute priority claim or alphabet separation is asserted.

The compression refinement is explicitly credited to Kisielewicz, Kowalski and Szykuła, *Experiments with Synchronizing Automata*, CIAA 2016, LNCS 9705, 176–188, DOI 10.1007/978-3-319-40946-7_15. Its Theorem 1 and Frankl–Pin sequence convention were inspected in the author-hosted primary PDF: https://jakubkowalski.tech/Publications/Kisielewicz2016ExperimentsWith.pdf. The needed sequence construction uses three holes excluding endpoints of later pairs, exactly equivalent to each later pair being absent from every earlier subset; it does not transpose or reverse the published convention. The refinement is an input, not a claimed new result.

On 8 October 2026 additional searches specifically examined codimension-three subset compression, nine-letter compression of an (n-3)-subset, strongly connected sharp Frankl–Pin bounds, and the 2026 question. Primary texts rechecked were the 2026 survey (Section 2.2, Lemma 3 and Open Problem 4), the 2016 refinement, and *Synchronizing Times for k-sets in Automata*, Electronic Journal of Combinatorics 29(3), P3.41 (2022), https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i3p41/pdf/. The latter distinguishes synchronization of a given subset to one state from the Frankl–Pin one-step compression bound. No inspected passage supplied the present uniform nine-letter compression theorem for arbitrary (n-3)-subsets under strong connectivity and synchronization. This is a bounded primary-source audit, not a priority certificate or an exhaustive database search.

The familiar length-nine result reducing the full state set by three states is a different operation and is not used as a bound for compressing an arbitrary (n-3)-set. The five-state compression-ten boundary control also prevents silently extending the new compression theorem from n>=6 to n=5. The avoid-or-compress consequence nevertheless holds at n=5 by separately verified binary witnesses and n-r<=4.

The proposed formula is refuted for arbitrary alphabets as well as for binary alphabets at every n>=11, s=n-3, 1<=r<=n-10. Both maxima equal nine there and the proposed upper is ten. Other parameters are not all determined; no complete solution of Open Problem 4 or all-parameter replacement formula is claimed.

## Repository provenance

Original source repository commit: 187c0b1df7e1074bbc1843668caaeb1e2c5dded1. The named initial face and all-gap notes were matched against their original generators. The separate existing repository paper is unchanged. Public dissemination of the repository may precede this manuscript; dates here do not establish publication priority. SOURCE_PROVENANCE.json records original hashes and current proof hashes.

## Current exact-region consolidation

The paper now determines m<=3 and m>=4,q<=3m-1, where m=n-s,q=n-r. The cofinal construction removes the former arithmetic-progression restriction and gives q at every n>=2s-r-1 for s-r>=3. Its proof and all structural requirements were checked directly, including the M=2g boundary. The codimension-one and -two constructions meet the existing compression bounds; those upper bounds are not claimed as new. No first-ever claim is made for these families or their special cases. The inspected literature above does not certify disjointness from every unpublished construction.

Additional graph-span and early-pair synthesis work stays outside the submitted article and release. Its own research note credits the standard span method and the Hajnal intersection-union mechanism. Failed restricted construction searches and solver timeouts do not change any exact value or constitute literature evidence. The remaining all-parameter region is m>=4,q>=3m; (13,9,1) remains unproved at value 11 or 12.
