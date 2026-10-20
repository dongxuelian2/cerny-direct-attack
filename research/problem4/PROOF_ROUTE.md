# Linear proof route for Open Problem 4

**Status:** reader-facing dependency map and a preliminary audit, **not** a substitute for the complete mathematical arguments and program domains in the [archival source](../../archive/legacy/PROOF.md). A displayed computation count alone does not establish a theorem.

## 0. Definitions and the target

Let \(\mathcal A=(Q,\Sigma,\delta)\) be a finite deterministic strongly connected synchronizing automaton. Original input letters are counted individually. For a reachable image \(S=Qv\), \(|S|=s\), and \(\varnothing\ne A\subsetneq S\), \(|A|=r\), put

\[
\operatorname{ac}(S,A)=\min\{|w|:\ A\not\subseteq Sw\text{ or }|Sw|<s\}.
\]
Let \(c(S)\) be the shortest compressing word length, \(m=n-s\), \(q=n-r\), and let \(P_h\) join all pairs compressible in at most \(h\) original letters. Its minimum vertex-cover size is \(\tau(P_h)\).

**Key reduction:** an s-set survives pure compression through length h iff its m-point complement covers all edges of P_h; hence
\[
\exists |S|=n-m: c(S)>h\quad\Longleftrightarrow\quad \tau(P_h)\le m.
\]
The original avoid-or-compress bound is \(\operatorname{ac}(S,A)\le q\).

## 1. General sharpness and the universal lower construction (paper)

The first two cardinality faces and a cofinal family attain q. For m≥3 a single **original-binary** two-block construction supplies, in the appropriate q-range,
\[
F_{\rm bin}(n,n-m,r)\ge\min(q,3m-1).
\]
Choose t=m−1≥2, p'≥r+3; let P={p₀,…,p_{p'−1}}, X={x₁,…,x_t}, Y={y₁,…,y_t}, {z}, with S=P∪X and protected A={p₀,…,p_{r−1}}. Letter a swaps the last two P-states, fixes the remaining P and cycles (x₁,…,x_t,y₁,…,y_t,z). Letter b shifts the P-chain backward (p₀→y₁), shifts the X/Y chains forward, sends x_t,y_t to p_{p'−1}, and fixes z.

Two matching actual words are \(a^{2t}ba^tb\), which compresses in 3t+2 steps, and \(a^{2t}bab^{p'-r-1}\), which avoids A in n−r steps. The **lower** proof requires a pair-potential inequality for every original letter and a signed cell-incidence invariant for every short word, plus explicit synchronization, strong connectivity and reachability witnesses. Merely giving attaining words does not establish a lower bound.

Read: [uniform two-block proof](../../archive/legacy/PROOF.md#problem4-two-block-proof), [first faces](../../archive/legacy/PROOF.md#problem4-defect-two-proof), and [cofinal witnesses](../../archive/legacy/PROOF.md#problem4-cofinal-proof). The manuscript includes a diagram of the t=3,p'=7,r=1 instance.

## 2. The small-codimension exception m=3

For m=1,2,3 the established extrema are min(q,3m), not one uniform min(q,3m−1). In particular m=3 has value min(q,9). This is a **genuine obstruction** to stating the conjecture for m≥3. Its binary 9-step lower example is separate from the m≥4 two-block family.

Read: [codimension-three upper](../../archive/legacy/PROOF.md#problem4-codimension-three-upper-proof) and [binary lower](../../archive/legacy/PROOF.md#problem4-codimension-three-proof).

## 3. Codimension four: exact 11 (computer-assisted upper)

For every legal n,r:
\[
F_{\rm bin}(n,n-4,r)=F(n,n-4,r)=\min(q,11).
\]
For n≥11 it suffices to prove that **every** (n−4)-set compresses by 11, without assuming reachability. Contradict c(S)≥12 and split using the vertex cover of P₇:

1. τ(P₇)≥4: a reduction gives **91** early graph cores, all excluded.
2. τ(P₇)=3: the structure forces τ(P₉)=4; the classification gives **117** graph classes and **10,142** named necessary domains, all excluded.

The projection from any actual automaton to a named domain must preserve actual state identity across letters; joint pair/row distances, quotient connectivity, and same-letter squares provide **necessary** tests. No SAT model is taken as an automaton. For n≤10, q≤9 gives the upper bound directly. The binary construction and small-q families supply equality.

Read: [full codimension-four chain](../../archive/legacy/PROOF.md#problem4-four-exact-eleven). Counts and reductions still need an independent archival certificate audit.

## 4. Codimension five: exact 14 (computer-assisted upper plus a paper exception)

For every legal n,r:
\[
F_{\rm bin}(n,n-5,r)=F(n,n-5,r)=\min(q,14).
\]
For n≥16 suppose c(S)≥15. The P₉ vertex-cover split yields:

| Necessary branch | Full finite coverage | Reported outcome |
|---|---:|---|
| τ(P₉)=5 | 2,294 early cores | no candidate |
| τ(P₉)=4, 11-point early support | 90 cores / 3,595 domains | excluded in disjoint component runs + supplementary paper reduction |
| τ(P₉)=4, support 5–10 | 4,568 cores / 3,245,386 domains | 38,398 static rejections and 3,206,988 dynamic checks |

**Important:** the complete lower-support run reported **3,206,987 UNSAT domains and one SAT relaxation survivor**, not zero survivors. The survivor is core=447/domain=0, K₄,₄ on eight named points, rows {012,013,456,457} (using the corresponding bitmasks 7,11,112,176).

**Final paper lemma:** if P_h is complete multipartite on V, with isolated J, and each part has an intersecting, connected covering family R whose R∪J sets are P_{h+1}-independent, then every permitted original letter preserves P_h-nonedges. A noncomplete short-pair layer of a synchronizing automaton must admit some letter mapping an outside nonedge into the layer, a contradiction. Two intersecting triples in each part certify the K₄,₄ survivor. This is *not* a claim that the SAT relaxation itself was UNSAT.

For n≤15 the general q bound suffices. Binary witnesses attain min(q,14). Read: [last full exclusion](../../archive/legacy/PROOF.md#problem4-five-exact-fourteen), [multipartite lemma](../../archive/legacy/PROOF.md#problem4-multipartite-overlap-exclusion), [eleven-point closure](../../archive/legacy/PROOF.md#problem4-five-fifteen-eleven-excluded).

## 5. Structural satellites — useful, but NOT hidden dependencies

- Full-cycle letter class: a separately proved exact formula min(s−r+1, 2m+1) with a binary construction, including noncoprime cases. This does **not** prove the unrestricted optimum. [Proof](../../archive/legacy/PROOF.md#problem4-full-cycle-exact).
- Quadratic exit-letter sparsification preserves shortest exit lengths for a **complete** family D, requiring no synchronizing selected subalphabet. [Proof](../../archive/legacy/PROOF.md#problem4-quadratic-exit-sparsification).
- Large-m cover and critical-graph arguments are conditional branches, not an unconditional linear compression bound. [Proof](../../archive/legacy/PROOF.md#problem4-large-codimension-cover-improvement).
- Negative attempts, extra core classification, and obsolete incremental thresholds (m=5 upper 18,17,16,15) stay in the [archival notebook](../../archive/legacy/PROOF.md) and are not steps a reader must follow to understand the final theorem.

## 6. End point and conjecture

The proven parameter region now includes m≤5 and (for larger m) q≤3m−1. The remaining region begins at m≥6, q≥3m. We **conjecture**, but have not proved,
\[
F_{\rm bin}(n,n-m,r)=F(n,n-m,r)=\min(q,3m-1)\quad (m\ge4).
\]
The stronger pure compression bound c(S)≤3m−1 for n≥3m+1 is a **separate** conjecture, not logically equivalent to the displayed exact extremum. See [CONJECTURE.md](CONJECTURE.md). Experiments near the binary witness and scans of restricted transition families are not unrestricted upper-bound certificates.
