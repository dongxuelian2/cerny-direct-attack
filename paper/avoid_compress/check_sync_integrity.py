"""Check the shipped Problem 4 snapshot and historical evidence without new research."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
INV = ROOT / 'investigation'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    assert __debug__, 'Keep assertions enabled; do not use Python -O'
    manifest = json.loads((ROOT / 'SYNC_SHA256.json').read_text(encoding='utf-8'))
    for name, expected in manifest['files'].items():
        target = (ROOT / name).resolve()
        assert target.is_relative_to(ROOT), name
        assert target.is_file() and digest(target) == expected, name

    historical = json.loads((INV / 'historical_receipts_manifest.json').read_text(encoding='utf-8'))
    archive = INV / historical['archive']
    assert digest(archive) == historical['archive_sha256']
    frozen_hashes = {}
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == len(historical['files'])
        assert set(z.namelist()) == set(historical['files'])
        assert z.testzip() is None
        for name, expected in historical['files'].items():
            actual = hashlib.sha256(z.read(name)).hexdigest()
            assert actual == expected, name
            frozen_hashes[name] = actual

    hashes = dict(frozen_hashes)

    def source_hash(name):
        if name not in hashes:
            target = (INV / name).resolve()
            assert target.is_relative_to(ROOT), name
            hashes[name] = digest(target)
        return hashes[name]

    latest = json.loads((INV / 'AUXILIARY_AUDIT_20261010_22.json').read_text(encoding='utf-8'))
    for name, expected in latest['source_sha256'].items():
        assert source_hash(name) == expected, 'Latest source binding: ' + name
    bindings = 0
    assert len(latest['passed_audits']) == len(set(latest['passed_audits'])) == 119
    for name in latest['passed_audits']:
        audit = json.loads((INV / name).read_text(encoding='utf-8'))
        assert audit['status'] == 'pass', name
        for source, expected in audit['source_sha256'].items():
            assert source_hash(source) == expected, (name, source)
            bindings += 1
    assert bindings == latest['current_audit_source_bindings_verified']

    checks = 0
    for folder, name in [(ROOT, 'SHA256SUMS.txt'), (ROOT / 'release', 'ARCHIVE_SHA256SUMS.txt')]:
        for line in (folder / name).read_text(encoding='utf-8').splitlines():
            expected, relative = line.split('  ', 1)
            assert digest(folder / relative) == expected, relative
            checks += 1
    assert checks == 121
    for name, expected in latest['accepted_artifact_sha256'].items():
        assert digest(ROOT / name) == expected, name
    archives = sorted((INV / 'certificates').glob('*.zip')) + sorted((ROOT / 'release').glob('*.zip'))
    for path in archives:
        with zipfile.ZipFile(path) as z:
            assert len(z.namelist()) == len(set(z.namelist())) and z.testzip() is None, path.name
    active = json.loads((INV / 'active_research.json').read_text(encoding='utf-8'))
    assert active['current_auxiliary_audit'] == 'AUXILIARY_AUDIT_20261010_22.json'
    assert active['workers'] == []
    assert active['b3_third_cover']['combined_unrestricted_remaining_geometries'] == 137
    assert active['b3_third_cover']['unrestricted_remaining_B3_geometries'] == 1
    print(json.dumps({'status': 'pass', 'snapshot_files': len(manifest['files']),
                      'paper_checksum_entries': checks, 'auxiliary_audits': 119,
                      'source_bindings': bindings, 'latest_bound_sources': len(latest['source_sha256']),
                      'historical_receipts': len(frozen_hashes), 'validated_archives': len(archives) + 1,
                      'unresolved_interval': [11, 12]}, indent=2))


if __name__ == '__main__':
    main()
