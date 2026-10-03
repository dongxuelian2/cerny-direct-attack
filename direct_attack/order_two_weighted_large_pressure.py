"""New M18/M20 exploratory scope; preserve the smaller-source capture hashes.

The only source transformation raises the mask-safe size guard from 16 to20.
No result about every proposal is certified; retained Bellman peaks are checked.
"""
from pathlib import Path
import argparse
import json
import os
from .weighted_class_reset_native import capture, digest

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--M', type=int, choices=(18, 20), required=True)
    p.add_argument('--trials', type=int, default=3000)
    args = p.parse_args()
    original = ROOT/'direct_attack/order_two_weighted_pressure.cpp'
    source = ROOT/'direct_attack/native_build/order_two_weighted_large_pressure.cpp'
    binary = source.with_suffix('.exe')
    guard = 'if(M<6 || M>16 || M%2)'
    text = original.read_text()
    assert text.count(guard) == 1
    transformed = text.replace(guard, 'if(M<6 || M>20 || M%2)')
    source.write_text(transformed, encoding='utf-8')
    compiler = os.environ.get('CXX', '<CXX_BIN>/g++.exe')
    metadata = ROOT/'direct_attack/data/order_two_weighted_large_pressure_build.json'
    if not metadata.exists() or not binary.exists() or json.loads(metadata.read_text())['generated_source_sha256'] != digest(source):
        build = capture([compiler, '-O3', '-std=c++11', '-static-libgcc', '-static-libstdc++', source, '-o', binary])
        metadata.write_text(json.dumps(dict(original_source_sha256=digest(original),
            generated_source_sha256=digest(source), transformation=dict(old=guard,new='if(M<6 || M>20 || M%2)'),
            binary_sha256=digest(binary), build=build), indent=2)+'\n', encoding='utf-8')
    out = ROOT/('direct_attack/data/order_two_weighted_pressure_M'+str(args.M)+'.json')
    run = capture([binary, args.M, args.trials, out])
    out.with_name(out.stem+'_capture.json').write_text(json.dumps(dict(run=run,
        original_source_sha256=digest(original), generated_source_sha256=digest(source),
        binary_sha256=digest(binary), output_sha256=digest(out)), indent=2)+'\n', encoding='utf-8')
    print(run['stdout'], end='')


if __name__ == '__main__':
    main()
