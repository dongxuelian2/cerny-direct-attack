"""Seal/check canonical Git-index contents, independent of checkout line endings.

Stage all submission changes before --write. The manifest excludes itself;
the containing Git commit binds the manifest and its own identity externally.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'submission/SHA256.json'


def index_hashes(env):
    raw = subprocess.check_output(['git', 'ls-files', '-s', '-z'], cwd=ROOT, env=env)
    entries = []
    for record in filter(None, raw.split(b'\0')):
        metadata, filename = record.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        assert stage == b'0' and mode in (b'100644', b'100755'), record
        path = filename.decode('utf-8')
        if path != TARGET:
            entries.append((path, oid))
    hashes = {}
    process = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT, env=env,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for path, oid in entries:
            process.stdin.write(oid+b'\n')
            process.stdin.flush()
            header = process.stdout.readline().split()
            assert header[0] == oid and header[1] == b'blob'
            remaining = int(header[2])
            digest = hashlib.sha256()
            while remaining:
                chunk = process.stdout.read(min(remaining, 1024*1024))
                assert chunk
                digest.update(chunk)
                remaining -= len(chunk)
            assert process.stdout.read(1) == b'\n'
            hashes[path] = digest.hexdigest()
    finally:
        process.stdin.close()
        assert process.wait() == 0
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    env = os.environ.copy()
    n = int(env.get('GIT_CONFIG_COUNT', '0'))
    env['GIT_CONFIG_KEY_'+str(n)] = 'safe.directory'
    env['GIT_CONFIG_VALUE_'+str(n)] = ROOT.as_posix()
    env['GIT_CONFIG_COUNT'] = str(n+1)
    hashes = index_hashes(env)
    if args.write:
        (ROOT/TARGET).write_text(json.dumps(hashes, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    else:
        expected = json.loads((ROOT/TARGET).read_text(encoding='utf-8'))
        assert hashes == expected, 'Canonical index manifest mismatch'
        subprocess.run(['git', 'diff', '--exit-code'], cwd=ROOT, env=env, check=True)
        extra = subprocess.check_output(['git', 'ls-files', '-z', '-o', '--exclude-standard'], cwd=ROOT, env=env)
        assert not extra, 'Untracked submission files are not sealed'
    print('CANONICAL_GIT_BLOBS_SHA256='+str(len(hashes))+' PASS')


if __name__ == '__main__':
    main()
