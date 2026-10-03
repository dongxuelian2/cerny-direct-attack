"""Build, run, and capture the new weighted target without changing old scorers."""
from pathlib import Path
import argparse
import json
import os
from .weighted_class_reset_native import capture, digest

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--M', type=int, default=10)
    parser.add_argument('--samples', type=int, default=0)
    args = parser.parse_args()
    source = ROOT/'direct_attack/order_two_weighted_extension.cpp'
    binary = ROOT/'direct_attack/native_build/order_two_weighted_extension.exe'
    compiler = os.environ.get('CXX', '<CXX_BIN>/g++.exe')
    binary.parent.mkdir(exist_ok=True)
    metadata = ROOT/'direct_attack/data/order_two_weighted_extension_build.json'
    if not metadata.exists() or not binary.exists() or json.loads(metadata.read_text())['source_sha256'] != digest(source):
        build = capture([compiler, '-O3', '-std=c++11', '-static-libgcc', '-static-libstdc++', source, '-o', binary])
        metadata.write_text(json.dumps(dict(source_sha256=digest(source), binary_sha256=digest(binary), build=build), indent=2)+'\n', encoding='utf-8')
    label = 'M'+str(args.M)+('_sample'+str(args.samples) if args.samples else '_complete')
    path = ROOT/('direct_attack/data/order_two_weighted_'+label+'.tsv')
    counter = path.with_suffix('.counter.json')
    run = capture([binary, args.M, path, counter, args.samples])
    receipt = dict(source_sha256=digest(source), binary_sha256=digest(binary),
                   witness_sha256=digest(path), counter_sha256=digest(counter), run=run)
    path.with_suffix('.capture.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(run['stdout'], end='')


if __name__ == '__main__':
    main()
