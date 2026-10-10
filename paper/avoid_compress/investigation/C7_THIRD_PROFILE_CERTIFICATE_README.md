# Binary c7 symbolic exclusion certificate

This auxiliary package contains the symbolic exclusion of b3_mixed_c7
at (13,9,1), its necessary row normalization, native scan source and
completed ordinary/sanitized scan receipts, and an independent checker.
It does not determine F(13,9,1), whose interval remains [11,12]. It
does not exclude unrestricted alphabets or the disjoint c3 branch.
It is separate from the article's unchanged 109-file supplement.

Read C7_THIRD_PROFILE_EXCLUSION.md and C7_THIRD_PROFILE_NORMALIZATION.md.
The proof gives a short-pair/backward-closure dichotomy without depending
on first-level flags, an exhaustive search result or a numerical histogram.
Antecedent notes supply the first three entrance statements and the
five-pair endpoint argument. Historical native scans referenced in the
antecedent singleton note are not used in this proof or reproduced here.

Python 3.10+ with its standard library suffices for the independent audit:

```sh
python check_c7_third_profile.py
```

It must report status pass, 240 n=13 moving types covering 40,320 labelled
moving rows, 27,216,000 completed native n=13 assignments, 2,016 literal
n=9 typed-function assignments, seven proof cases and 30/43 remaining
binary/unrestricted joint cases. The checker directly enumerates the
labelled moving-row cover and the initial sets; it independently enumerates
small full functions, uses forward pair BFS and tests both pair closures.
It compares all fields except elapsed seconds between the supplied full
ordinary and sanitizer receipts. It does not independently re-enumerate
all 27 million n=13 F assignments in Python.

Optional full native reproduction, with clang++ or an equivalent C++17
compiler (commands shown for Windows):

```powershell
clang++ -std=c++17 -O3 probe_c7_third_profile.cpp -o probe.exe
.\probe.exe 9 c7_third_profile_pairs_n9.json --pairs
.\probe.exe 13 c7_third_profile_pairs_n13.json --pairs
clang++ -std=c++17 -O1 -g '-fsanitize=address,undefined' probe_c7_third_profile.cpp -o sanitized.exe
.\sanitized.exe 9 c7_third_profile_pairs_n9_sanitized.json --pairs
.\sanitized.exe 13 c7_third_profile_pairs_n13_sanitized.json --pairs
python check_c7_third_profile.py
```

Native counts are deterministic; elapsed seconds and consequently source
hashes of newly generated receipts will change. CHECKSUMS.txt authenticates
the original distributed bytes. No SAT solver, timeout result, floating
rank tolerance or reachability cutoff is used in the exclusion proof.
