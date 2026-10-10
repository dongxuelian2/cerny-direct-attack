# Singleton second-entrance certificate

This package certifies only the binary B3 / singleton-C branch exclusion
at (13,9,1) stated in SINGLETON_THREE_KERNEL_EXCLUSION.md. The first
unresolved extremal value still lies in [11,12]; this is not a complete
Problem 4 answer. The package is auxiliary and is not part of the
unchanged paper's 109-file supplementary release.

Read LOCALIZED_BINARY_ENTRANCE_KERNEL.md for the complete normalization,
then SINGLETON_THREE_KERNEL_EXCLUSION.md for the finite proof and scope.
The included antecedent proof notes establish the equality flags and
entrance restrictions; no SAT answer is used.

Requirements: Python 3.10+ (standard library only) and a C++17 compiler.
The reference compiler was clang 22.1.7 targeting x86_64-w64-windows-gnu.

From this directory, on a POSIX shell:

```sh
clang++ -O3 -std=c++17 probe_singleton_three_kernel.cpp -o probe
for n in 9 10 11 12 13; do
  ./probe "$n" "singleton_three_kernel_n$n.json"
done
clang++ -O1 -g -std=c++17 -fsanitize=address,undefined probe_singleton_three_kernel.cpp -o probe_sanitized
for n in 9 13; do
  ./probe_sanitized "$n" "singleton_three_kernel_sanitized_n$n.json"
done
python check_singleton_three_kernel.py
```

Equivalent PowerShell commands:

```powershell
clang++ -O3 -std=c++17 probe_singleton_three_kernel.cpp -o probe.exe
foreach ($n in 9,10,11,12,13) {
  .\probe.exe $n "singleton_three_kernel_n$n.json"
}
clang++ -O1 -g -std=c++17 '-fsanitize=address,undefined' probe_singleton_three_kernel.cpp -o probe_sanitized.exe
foreach ($n in 9,13) {
  .\probe_sanitized.exe $n "singleton_three_kernel_sanitized_n$n.json"
}
python check_singleton_three_kernel.py
```

The n=13 run must complete all 180 moving conjugacy types and
43,545,600 row/initial-set assignments. It retains 162,091 strong,
synchronizing and protected-isolated assignments, with delay counts
110,327 at four, 44,264 at five and 7,500 at six. The checker independently
verifies the moving cover by marked cycles, all assignment counts,
all 3,456 n9 rows by literal BFS, and agreement with both sanitized runs.
Timing fields may differ. Smaller-n scans are enumerator controls;
the tested histogram is not a uniform upper bound on F.

CHECKSUMS.txt authenticates the distributed bytes. Rerunning the native
programs changes timing fields and therefore changes report hashes;
the mathematical counts and independent checker must still agree.
