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
    large_data = json.loads((INV / 'large_data_manifest.json').read_text(encoding='utf-8'))
    archive_hashes = {}
    for name, record in large_data['files'].items():
        archive = (INV / record['archive']).resolve()
        assert archive.is_relative_to(ROOT), name
        if archive not in archive_hashes:
            archive_hashes[archive] = digest(archive)
        assert archive_hashes[archive] == record['archive_sha256'], name
        h = hashlib.sha256()
        with zipfile.ZipFile(archive) as z:
            assert z.getinfo(record['member']).file_size == record['bytes'], name
            with z.open(record['member']) as source:
                for block in iter(lambda: source.read(1024 * 1024), b''):
                    h.update(block)
        assert h.hexdigest() == record['sha256'], name
        hashes[name] = h.hexdigest()

    def source_hash(name):
        if name not in hashes:
            target = (INV / name).resolve()
            assert target.is_relative_to(ROOT), name
            hashes[name] = digest(target)
        return hashes[name]

    latest_name = manifest['auxiliary_audit']
    latest = json.loads((INV / latest_name).read_text(encoding='utf-8'))
    for name, expected in latest['source_sha256'].items():
        assert source_hash(name) == expected, 'Latest source binding: ' + name
    bindings = 0
    audit_count = len(latest['passed_audits'])
    assert audit_count == len(set(latest['passed_audits'])) == manifest['auxiliary_audits']
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
    # Include adopted QA certificates, while excluding unrelated local QA builds.
    archives = sorted({ROOT / name for name in manifest['files']
                       if name.endswith('.zip') and ROOT / name != INV / historical['archive']})
    for path in archives:
        with zipfile.ZipFile(path) as z:
            assert len(z.namelist()) == len(set(z.namelist())) and z.testzip() is None, path.name
    active = json.loads((INV / 'active_research.json').read_text(encoding='utf-8'))
    assert active['current_auxiliary_audit'] == latest_name
    assert active['workers'] == []
    frontier = manifest['research_frontier']
    assert active['b3_third_cover']['combined_unrestricted_remaining_geometries'] == frontier['unrestricted_geometries']
    assert active['b3_third_cover']['unrestricted_remaining_B3_geometries'] == frontier['unrestricted_B3_geometries']
    assert active['small_first_third_admission']['remaining_binary_typed_orbits'] == frontier['binary_types']
    assert active['small_first_third_admission']['remaining_binary_profile_pairs'] == frontier['binary_profiles']
    assert active['small_first_third_admission']['remaining_geometric_after_joint_and_third_exclusions'] == frontier['binary_geometries']
    assert active['joint_fiber_cases']['unrestricted_remaining_orbits'] == frontier['unrestricted_joints']
    assert active['joint_fiber_cases']['binary_remaining_orbits'] == frontier['binary_joints']
    print(json.dumps({'status': 'pass', 'snapshot_files': len(manifest['files']),
                      'paper_checksum_entries': checks, 'auxiliary_audits': audit_count,
                      'source_bindings': bindings, 'latest_bound_sources': len(latest['source_sha256']),
                      'historical_receipts': len(frozen_hashes), 'validated_archives': len(archives) + 1,
                      'archived_large_inventories': len(large_data['files']),
                      'latest_auxiliary_audit': latest_name, 'research_frontier': frontier,
                      'unresolved_interval': [11, 12]}, indent=2))


if __name__ == '__main__':
    main()
