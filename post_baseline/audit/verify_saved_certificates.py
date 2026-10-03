from collections import Counter
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT))
from src.check_certificate import check, read_json

for label, base, expected in (
    ("baseline", PROJECT / "reference_results", 83),
    ("post-baseline reproduction", PROJECT / "post_baseline" / "reproduction", 83),
    ("post-baseline reconnaissance", PROJECT / "post_baseline" / "reconnaissance", 76),
):
    json_files = sorted(base.rglob("*.json"))
    certificates = [
        (path, read_json(path))
        for path in json_files
        if read_json(path).get("schema") == "orion.sync-certificate.v1"
    ]
    verified = [(path, check(obj)) for path, obj in certificates]
    kinds = Counter(result["kind"] for _, result in verified)
    skipped = [path.relative_to(base).as_posix() for path in json_files
               if read_json(path).get("schema") != "orion.sync-certificate.v1"]
    print(f"{label}: json={len(json_files)} certificates={len(verified)} "
          f"verified={len(verified)} kinds={dict(kinds)} non_certificate_json={skipped}")
    if len(verified) != expected:
        raise SystemExit(f"Expected {expected} certificates for {label}")
