"""Reproducible native full-class pressure with literal build/run capture."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent.parent


def capture(argv):
    start, clock = datetime.now(timezone.utc).isoformat(), time.monotonic()
    result = subprocess.run(list(map(str,argv)), cwd=ROOT, capture_output=True,
                            text=True, encoding='utf-8', errors='replace')
    record = dict(argv=list(map(str,argv)), cwd=str(ROOT), start_utc=start,
                  seconds=time.monotonic()-clock, returncode=result.returncode,
                  stdout=result.stdout, stderr=result.stderr)
    assert result.returncode == 0, record
    return record


def ensure_build():
    source = ROOT/'direct_attack/class_reset_pressure.cpp'
    binary = ROOT/'direct_attack/native_build/class_reset_pressure.exe'
    metadata = ROOT/'direct_attack/data/class_reset_native_build.json'
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if binary.exists() and metadata.exists():
        old = json.loads(metadata.read_text())
        if old['source_sha256'] == source_hash and old['binary_sha256'] == hashlib.sha256(binary.read_bytes()).hexdigest():
            return binary
    compiler = shutil.which('g++')
    assert compiler is not None
    compile_record = capture([compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',source,'-o',binary])
    version = capture([compiler,'--version'])
    data = dict(source_sha256=source_hash,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
                compile=compile_record,compiler_version=version)
    metadata.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return binary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=1000000)
    ap.add_argument('--seed', type=int, default=20261017)
    ap.add_argument('--limit', type=int, default=150000)
    ap.add_argument('--profile-mode', choices=['small','large'], default='large')
    ap.add_argument('--out', type=Path, default=Path('direct_attack/data/class_reset_pressure_large.json'))
    args = ap.parse_args()
    binary = ensure_build()
    record = capture([binary,'--trials',args.trials,'--seed',args.seed,'--limit',args.limit,
                      '--profile-mode',args.profile_mode,'--out',args.out])
    record['note'] = 'small explicitly reconstructs the initial twelve-profile protocol; large uses twenty-one profiles'
    target = args.out.with_name(args.out.stem+'_generation_capture.json')
    target.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(record['stdout'].strip())


if __name__ == '__main__':
    main()
