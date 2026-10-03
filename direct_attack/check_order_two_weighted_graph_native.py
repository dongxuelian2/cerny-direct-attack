"""Build/capture the independent factoradic/literal checker, outside old registry."""
from pathlib import Path
import argparse
import json
import os
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser();p.add_argument('path',type=Path);args=p.parse_args()
    data=ROOT/args.path;assert json.loads(data.with_suffix('.counter.json').read_text()) is None
    source=ROOT/'direct_attack/check_order_two_weighted_graph_native.cpp'
    binary=ROOT/'direct_attack/native_build/check_order_two_weighted_graph_native.exe'
    metadata=ROOT/'direct_attack/data/order_two_weighted_graph_check_build.json'
    valid=False
    if binary.exists() and metadata.exists():
        old=json.loads(metadata.read_text());valid=old['source_sha256']==digest(source) and old['binary_sha256']==digest(binary)
    if not valid:
        compiler=os.environ.get('CXX','g++')
        build=capture([compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',source,'-o',binary])
        metadata.write_text(json.dumps(dict(source_sha256=digest(source),binary_sha256=digest(binary),build=build),indent=2)+'\n',encoding='utf-8')
    record=capture([binary,data]);record.update(source_sha256=digest(source),binary_sha256=digest(binary),data_sha256=digest(data))
    data.with_suffix('.check.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(record['stdout'],end='')


if __name__=='__main__':main()
