# Sharpness of the Avoid-or-Compress Bound for Reachable Images

Current seven-page mathematical paper: **partial answer to Szykuła 2026 Open Problem 4**. The complete-answer objective remains active. Author: Qichao Wang, Hebei University of Technology.

Put m=n-s and q=n-r. Both maxima are determined for every parameter with m<=3: one for m=0 and min(q,3m) for 1<=m<=3. For m>=4 and q<=3m-1 both maxima equal q. Every lower witness is binary, strongly connected and synchronizing, with S an actual reachable image. The cofinal construction proves q for every fixed s-r>=3 and n>=2s-r-1, strengthening the former progression-only range.

The proposed formula U=min(n-r,binom(n-s+2,2)) is false: both maxima equal nine rather than ten at n>=11,s=n-3,r<=n-10. The complete codimension-three upper is computer-assisted, for arbitrary finite alphabets, n>=6, and does not require S to be reachable. No alphabet separation is established.

The region m>=4,q>=3m is not determined as a whole. The smallest unknown (13,9,1) remains in [11,12]. The complete finite frontier through n=12 and the four additional n=13 points are unchanged. No search failure or solver timeout is treated as an upper bound.

## Deliverables and reproduction

main.tex and main.pdf give the seven-page article. references.bib contains the same four records as the embedded references. The computer-assisted proof requires the accompanying proof supplement, beginning with CODIMENSION_THREE_UPPER_PROOF.md. All newly incorporated cofinal and low-codimension construction proofs are included in the article, with expanded notes and independent checks in the supplement.

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    python -B reproducibility/check_codimension_three_upper.py --rerun --compiler clang++ --build-dir ../upper-build
    python -B reproducibility/generator.py
    python -B reproducibility/checker.py
    python -B reproducibility/check_cofinal.py
    python -B reproducibility/check_boundary.py
    python -B reproducibility/check_defect_two.py
    python -B reproducibility/check_codimension_three.py
    python -B reproducibility/two_block_family.py
    python -B reproducibility/check_two_block.py
    python -B reproducibility/verify_certificates.py
    python -B reproducibility/verify_frontier.py

Python >=3.10 and C++17 with assertions enabled suffice; no solver is needed. The supplement has exactly 109 directly relevant source, proof, data and report files. Search code, solver logs, historical covers and auxiliary pruning research stay outside it. The source archive contains main.tex, references.bib and anc/reproducibility.zip. The submission bundle also contains the audits, validation, provenance, release builder and SHA-256 hashes. These archives have been checked against the shipped files.

LITERATURE_NOVELTY_AUDIT.md records a bounded primary-source audit, not a priority guarantee. PROOF_AUDIT.md and VALIDATION.json state exact mathematical and computational scopes. No account submission or complete-solution claim is made; the article includes an AI-assistance disclosure.
