"""Restore checksum-bound historical command receipts; never rerun their commands."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parent


def main():
    manifest = json.loads((ROOT / 'historical_receipts_manifest.json').read_text(encoding='utf-8'))
    archive = ROOT / manifest['archive']
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == manifest['archive_sha256']
    contents = {}
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == len(manifest['files'])
        assert set(z.namelist()) == set(manifest['files'])
        for name, expected in manifest['files'].items():
            path = PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and len(path.parts) == 1
            data = z.read(name)
            assert hashlib.sha256(data).hexdigest() == expected, name
            target = ROOT / name
            if target.exists():
                assert target.read_bytes() == data, 'Existing receipt differs: ' + name
            contents[name] = data
    for name, data in contents.items():
        target = ROOT / name
        if not target.exists():
            target.write_bytes(data)
    print(json.dumps({'status': 'pass', 'historical_receipts': len(contents), 'commands_rerun': 0}))


if __name__ == '__main__':
    main()
