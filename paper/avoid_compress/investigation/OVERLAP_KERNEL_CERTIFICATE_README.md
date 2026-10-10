# Three-point entrance / one-new-point overlap certificate

This auxiliary package certifies only the binary conditional exclusion
at (13,9,1) in OVERLAP_THREE_KERNEL_EXCLUSION.md. The extremal interval
remains [11,12]; unrestricted alphabets and other entrance shapes are
not excluded. It is outside the unchanged paper's 109-file supplement.

Read OVERLAP_THREE_KERNEL_NORMALIZATION.md for the complete six-shape
row cover. The included antecedent notes prove the equality flags,
entrance restrictions, localized kernel, and four-pair cap. The tail
counts and marked-cycle orbit counts are independently checked.

Requirements: Python 3.10+ (standard library) and a C++17 compiler.
Reference compiler: clang 22.1.7, x86_64-w64-windows-gnu.

POSIX commands, run from the extracted directory:

```sh
clang++ -O3 -std=c++17 probe_overlap_three_kernel.cpp -o probe_overlap_three_kernel
python run_overlap_kernel_scans.py 9
python run_overlap_kernel_scans.py 13
clang++ -O1 -g -std=c++17 -fsanitize=address,undefined probe_overlap_three_kernel.cpp -o probe_overlap_three_kernel_sanitized
python run_overlap_kernel_scans.py 9 --sanitized
python run_overlap_kernel_scans.py 13 --sanitized
python check_overlap_three_kernel.py
```

PowerShell uses .exe output names and quotes the sanitizer option:

```powershell
clang++ -O3 -std=c++17 probe_overlap_three_kernel.cpp -o probe_overlap_three_kernel.exe
python run_overlap_kernel_scans.py 9
python run_overlap_kernel_scans.py 13
clang++ -O1 -g -std=c++17 '-fsanitize=address,undefined' probe_overlap_three_kernel.cpp -o probe_overlap_three_kernel_sanitized.exe
python run_overlap_kernel_scans.py 9 --sanitized
python run_overlap_kernel_scans.py 13 --sanitized
python check_overlap_three_kernel.py
```

Each n=13 normal/sanitized batch must complete all six shapes and
32,659,200 row/initial-set assignments. Of these, 89,992 are strong,
synchronizing and protected-isolated; their tested delays are all four,
never twelve. The checker independently covers all moving orbits,
all tail counts, and all 4,320 n=9 rows by forward pair and subset BFS.
The header's exact provenance from the preceding native probe is also
checked. No generic SAT search, sampling or time cutoff is used.

CHECKSUMS.txt records the distributed bytes. Reruns change timing fields
and report hashes; the exact mathematical counts must still agree.
The four-step histogram is not an upper bound on F or on larger n.
