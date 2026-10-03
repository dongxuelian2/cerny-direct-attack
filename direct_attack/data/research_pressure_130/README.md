# Discovery-only pressure, not registered completeness checks

The saved Python files are byte copies of the ignored native_build discovery
scripts at execution time. The JSON files explicitly transcribe actual tool
output fields; they are not invented subprocess captures. Original execution
was python -m direct_attack.native_build.probe_exact_cycle_entry n, and
python -m direct_attack.native_build.search_short_weak_stationarity 4.

To reproduce discovery after a fresh checkout, copy these four scripts into
the ignored direct_attack/native_build directory and use those module paths
from the repository root. The weak-stationarity discovery requires NumPy;
the new independent theorem checker requires only Python standard library.
The remaining imports reference tracked repository code. No negative search
completeness, floating feasibility or all-parameter conjecture is certified
by this archive. It is excluded from the formal verification registry.

The family discovered at n4 was generalized and audited separately in
WEAK_STATIONARY_LINEAR_COST_COUNTERFAMILY.md and its exact checker. The
general exact-cycle-entry question remains OPEN, with no independent full
implementation/coverage audit. The actual-cost theorem and the refuted
worst-formula bridge remain as established at the preceding checkpoint.
