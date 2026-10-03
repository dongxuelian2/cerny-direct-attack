"""Retain a literal Bellman best case, not an exhaustive pressure theorem."""
from pathlib import Path
import argparse
import json
import os
from .weighted_class_reset_native import capture, digest

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--M', type=int, default=12)
    parser.add_argument('--trials', type=int, default=50000)
    args = parser.parse_args()
    source = ROOT/'direct_attack/order_two_weighted_pressure.cpp'
    binary = ROOT/'direct_attack/native_build/order_two_weighted_pressure.exe'
    compiler = os.environ.get('CXX', '<CXX_BIN>/g++.exe')
    metadata = ROOT/'direct_attack/data/order_two_weighted_pressure_build.json'
    if not metadata.exists() or not binary.exists() or json.loads(metadata.read_text())['source_sha256'] != digest(source):
        build = capture([compiler, '-O3', '-std=c++11', '-static-libgcc', '-static-libstdc++', source, '-o', binary])
        metadata.write_text(json.dumps(dict(source_sha256=digest(source), binary_sha256=digest(binary), build=build), indent=2)+'\n', encoding='utf-8')
    out = ROOT/('direct_attack/data/order_two_weighted_pressure_M'+str(args.M)+'.json')
    run = capture([binary, args.M, args.trials, out])
    out.with_name(out.stem+'_capture.json').write_text(json.dumps(dict(run=run,
        source_sha256=digest(source), binary_sha256=digest(binary), output_sha256=digest(out)), indent=2)+'\n', encoding='utf-8')
    print(run['stdout'], end='')


if __name__ == '__main__':
    main()
