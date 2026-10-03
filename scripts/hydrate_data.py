"""Restore pinned scientific release data; reject unknown or altered members."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--asset', type=Path, help='Offline scientific-data.zip')
    args = parser.parse_args()
    manifest = json.loads((ROOT/'archive/assets.json').read_text(encoding='utf-8'))
    meta = next(a for a in manifest['assets'] if a['name'] == 'scientific-data.zip')
    if args.asset:
        data = args.asset.read_bytes()
    else:
        url = ('https://github.com/' + manifest['repository'] + '/releases/download/'
               + manifest['release_tag'] + '/' + meta['name'])
        with urllib.request.urlopen(url, timeout=120) as response:
            data = response.read(meta['bytes']+1)
    if len(data) != meta['bytes'] or hashlib.sha256(data).hexdigest() != meta['sha256']:
        raise ValueError('Release asset length/SHA-256 mismatch')
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = zf.namelist()
        if len(names) != len(set(names)) or set(names) != set(manifest['scientific_files']):
            raise ValueError('Unexpected, duplicate, or missing ZIP member')
        # Validate every member before writing anything.
        files = []
        for name in names:
            target = (ROOT/name).resolve()
            if ROOT.resolve() not in target.parents:
                raise ValueError('Unsafe archive path')
            content = zf.read(name)
            if hashlib.sha256(content).hexdigest() != manifest['scientific_files'][name]:
                raise ValueError('Member SHA-256 mismatch: '+name)
            if target.exists() and target.read_bytes() != content:
                raise ValueError('Refusing to overwrite different scientific data: '+name)
            files.append((target, content))
        for target, content in files:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    print('PASS: restored '+str(len(files))+' checksum-verified scientific files')


if __name__ == '__main__':
    main()
