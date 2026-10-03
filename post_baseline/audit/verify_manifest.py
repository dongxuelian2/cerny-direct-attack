from pathlib import Path
import hashlib
import json
import subprocess

PROJECT = Path(__file__).resolve().parents[2]
BASELINE = 'b36adeac34a5088a7e2cd588f8c55221d04bd6eb'
manifest = PROJECT / "MANIFEST.sha256"
listed = {}
for line in manifest.read_text(encoding="utf-8").splitlines():
    if line.strip():
        digest, rel = line.split("  ", 1)
        listed[rel] = digest.lower()

tracked = subprocess.check_output(
    ["git", "-C", str(PROJECT), "-c", "core.quotepath=false",
     "ls-tree", "-r", "--name-only", BASELINE],
    text=True, encoding="utf-8"
).splitlines()
baseline_files = set(tracked) - {"MANIFEST.sha256"}
listed_paths = set(listed)
missing_from_manifest = sorted(baseline_files - listed_paths)
manifest_not_tracked = sorted(listed_paths - baseline_files)
bad_hashes = []
preparation_overrides = []
csv_serialization = []
worktree_eol = []
renamed_paths = []
migrations = json.loads((PROJECT / 'submission/PATH_MIGRATIONS.json').read_text(encoding='utf-8'))
allowed_overrides = {'README.md', 'START_HERE.md', 'REPRODUCIBILITY.md', 'STATUS.json', 'src/lean_export.py', 'start_windows.bat'}
for rel, expected in listed.items():
    # The original manifest seals the imported baseline, not later submissions.
    # Preserve its exact evidence and separately report current preparation edits.
    original = subprocess.check_output(['git', '-C', str(PROJECT), 'show', BASELINE + ':' + rel])
    if hashlib.sha256(original).hexdigest().lower() != expected:
        # Git normalized five imported CSVs to LF; the ZIP manifest hashes CRLF.
        # Accept only exact reconstruction of the sealed bytes, and report it.
        restored = original.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
        if rel.endswith('.csv') and hashlib.sha256(restored).hexdigest().lower() == expected:
            csv_serialization.append(rel)
        else:
            bad_hashes.append((rel, 'BASELINE_BLOB_HASH_MISMATCH'))
    current_rel = migrations.get(rel, rel)
    path = PROJECT / current_rel
    if current_rel != rel:
        # Historical manifest names stay unchanged; renamed manuals must match
        # the exact imported bytes, with no content or serialization changes.
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected, rel
        renamed_paths.append((rel, current_rel))
    if not path.is_file():
        bad_hashes.append((rel, "MISSING"))
    elif hashlib.sha256(path.read_bytes()).hexdigest().lower() != expected:
        if rel in allowed_overrides:
            preparation_overrides.append(rel)
        elif path.read_bytes().replace(b'\r\n', b'\n') == original.replace(b'\r\n', b'\n'):
            worktree_eol.append(rel)
        else:
            bad_hashes.append((rel, "UNDECLARED_WORKTREE_HASH_MISMATCH"))

current_files = {
    path.relative_to(PROJECT).as_posix()
    for path in PROJECT.rglob("*")
    if path.is_file() and ".git" not in path.parts
}
added_files = current_files - set(tracked)
print(f"MANIFEST_ENTRIES={len(listed)} TRACKED_BASELINE_FILES={len(baseline_files)} "
      f"HASH_ERRORS={len(bad_hashes)} UNLISTED_BASELINE={len(missing_from_manifest)} "
      f"MANIFEST_NOT_BASELINE={len(manifest_not_tracked)} POST_BASELINE_FILES={len(added_files)}")
print('DOCUMENTED_SUBMISSION_PREPARATION_OVERRIDES', preparation_overrides)
print('BASELINE_CSV_CRLF_RECONSTRUCTION', csv_serialization)
print('WORKTREE_EOL_EQUIVALENCE', worktree_eol)
print('BYTE_IDENTICAL_ASCII_PATH_MIGRATIONS', renamed_paths)
print('Imported baseline hashes are checked against immutable Git blobs; final-package hashes are in submission/SHA256.json.')
if bad_hashes or missing_from_manifest or manifest_not_tracked:
    print("HASH_ERRORS", bad_hashes[:10])
    print("UNLISTED_BASELINE", missing_from_manifest[:10])
    print("MANIFEST_NOT_BASELINE", manifest_not_tracked[:10])
    raise SystemExit(1)
