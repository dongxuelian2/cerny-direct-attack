"""Positive/negative controls checking every supplied letter is actually used."""
from copy import deepcopy
import json
from pathlib import Path
from alphabet_check import bfs, certificate, verify

ROOT = Path(__file__).resolve().parent

def main():
    saved = json.loads((ROOT/"binary_obstruction_witness.json").read_text())
    rows, S = saved["rows"], saved["S"]
    tests = []
    for name, third, expected in (
        ("identity", list(range(11)), 9),
        ("duplicate", rows[1], 9),
        ("constant", [0]*11, 1)):
        z = certificate(deepcopy(rows)+[list(third)], S, 1)
        assert z is not None and z["value"] == expected and verify(z)
        if name == "constant":
            word, _ = bfs(z["rows"], S, lambda T: len(T)<8)
            assert word == "c"
        tests.append(dict(third_letter=name, expected=expected, verified=True))
    control = json.loads((ROOT/"ternary_control_n5.json").read_text())["witness"]
    assert control["r"] == 0 and control["compression"] == 10 and verify(control)
    # Relabel the known value-nine example to S={0,...,7}; add identity.
    order = S+[q for q in range(11) if q not in S]
    labels = {q: i for i, q in enumerate(order)}
    fixed = [[labels[row[q]] for q in order] for row in rows]+[list(range(11))]
    (ROOT/"alphabet_fixed_control.json").write_text(json.dumps(fixed)+"\n")
    fixed[2] = [0]*11
    (ROOT/"alphabet_fixed_negative.json").write_text(json.dumps(fixed)+"\n")
    report = dict(verified=True, third_letter_controls=tests,
                  compression_control_n5_verified=True,
                  scope="Verification controls only; no alphabet-separation claim.")
    (ROOT/"alphabet_audit.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report))

if __name__ == "__main__":
    main()
