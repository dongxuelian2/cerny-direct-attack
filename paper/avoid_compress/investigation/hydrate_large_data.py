"""Restore checksum-bound inventories and QA evidence to their original paths."""
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    assert __debug__, 'Keep assertions enabled'
    manifest = json.loads((ROOT / 'large_data_manifest.json').read_text(encoding='utf-8'))
    archive_hashes = {}
    for name, record in manifest['files'].items():
        target = (ROOT / name).resolve()
        archive = (ROOT / record['archive']).resolve()
        assert target.is_relative_to(ROOT.parent) and archive.is_relative_to(ROOT.parent)
        if archive not in archive_hashes:
            archive_hashes[archive] = digest(archive)
        assert archive_hashes[archive] == record['archive_sha256']
        if target.exists():
            assert target.stat().st_size == record['bytes'] and digest(target) == record['sha256'], name
            continue
        temp_path = None
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive) as z, tempfile.NamedTemporaryFile(dir=target.parent, suffix='.tmp', delete=False) as f:
                temp_path = Path(f.name)
                assert z.getinfo(record['member']).file_size == record['bytes']
                with z.open(record['member']) as source:
                    for block in iter(lambda: source.read(1024 * 1024), b''):
                        f.write(block)
            assert digest(temp_path) == record['sha256'], name
            temp_path.replace(target)
        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()
    print(json.dumps({'status': 'pass', 'large_inventories': len(manifest['files'])}))


if __name__ == '__main__':
    main()
