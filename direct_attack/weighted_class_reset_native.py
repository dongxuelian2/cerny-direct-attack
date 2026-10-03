"""Separate reproducible weighted-return pressure wrapper with literal captures."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent.parent
COMPILER = os.environ.get('CXX') or shutil.which('g++')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def capture(argv):
    start, clock = datetime.now(timezone.utc).isoformat(), time.monotonic()
    result = subprocess.run(list(map(str, argv)), cwd=ROOT, capture_output=True,
                            text=True, encoding='utf-8', errors='replace')
    record = dict(argv=list(map(str, argv)), cwd=str(ROOT), start_utc=start,
                  seconds=time.monotonic()-clock, returncode=result.returncode,
                  stdout=result.stdout, stderr=result.stderr)
    assert result.returncode == 0, record
    return record


def ensure_build():
    assert COMPILER, 'Set CXX to a C++11 compiler or put g++ on PATH'
    source = ROOT/'direct_attack/weighted_class_reset_pressure.cpp'
    binary = ROOT/'direct_attack/native_build/weighted_class_reset_pressure.exe'
    metadata = ROOT/'direct_attack/data/weighted_class_reset_native_build.json'
    binary.parent.mkdir(parents=True, exist_ok=True)
    source_hash = digest(source)
    if binary.exists() and metadata.exists():
        old = json.loads(metadata.read_text())
        if old['source_sha256'] == source_hash and old['binary_sha256'] == digest(binary):
            return binary
    version = capture([COMPILER, '--version'])
    compile_record = capture([COMPILER, '-O3', '-std=c++11', '-static-libgcc',
                              '-static-libstdc++', source, '-o', binary])
    metadata.write_text(json.dumps(dict(source_sha256=source_hash,
                        binary_sha256=digest(binary), compile=compile_record,
                        compiler_version=version), indent=2)+'\n', encoding='utf-8')
    return binary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trials', type=int, default=250000)
    parser.add_argument('--seed', type=int, default=20261021)
    parser.add_argument('--mode', choices=['search', 'tiny'], default='search')
    parser.add_argument('--out', type=Path, default=Path('direct_attack/data/weighted_class_reset_pressure.json'))
    args = parser.parse_args()
    binary = ensure_build()
    record = capture([binary, '--trials', args.trials, '--seed', args.seed,
                      '--mode', args.mode, '--out', args.out])
    record['source_sha256'] = digest(ROOT/'direct_attack/weighted_class_reset_pressure.cpp')
    record['binary_sha256'] = digest(binary)
    record['output_sha256'] = digest(ROOT/args.out)
    args.out.with_name(args.out.stem+'_generation_capture.json').write_text(
        json.dumps(record, indent=2)+'\n', encoding='utf-8')
    print(record['stdout'].strip())


if __name__ == '__main__':
    main()
