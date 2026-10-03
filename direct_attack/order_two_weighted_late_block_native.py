"""New late-block attack; native proposal counts exploratory, retained edges literal."""
from pathlib import Path
import argparse
import json
import os
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser();p.add_argument('--M',type=int,required=True)
    p.add_argument('--trials',type=int,default=1000000);p.add_argument('--seed',type=int,default=2026100331);args=p.parse_args()
    source=ROOT/'direct_attack/order_two_weighted_late_block_pressure.cpp'
    dependency=ROOT/'direct_attack/order_two_weighted_graph_pressure.cpp'
    binary=ROOT/'direct_attack/native_build/order_two_weighted_late_block_pressure.exe'
    metadata=ROOT/'direct_attack/data/order_two_weighted_late_block_build.json'
    valid=False
    if binary.exists() and metadata.exists():
        old=json.loads(metadata.read_text());valid=old['source_sha256']==digest(source) and old['dependency_sha256']==digest(dependency) and old['binary_sha256']==digest(binary)
    if not valid:
        compiler=os.environ.get('CXX','<CXX_BIN>/g++.exe')
        build=capture([compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',source,'-o',binary])
        metadata.write_text(json.dumps(dict(source_sha256=digest(source),dependency_sha256=digest(dependency),
            binary_sha256=digest(binary),build=build),indent=2)+'\n',encoding='utf-8')
    out=ROOT/('direct_attack/data/weighted_late_block_M'+str(args.M)+'_sample'+str(args.trials)+'_seed'+str(args.seed)+'.tsv')
    counter=out.with_suffix('.counter.json');run=capture([binary,args.M,args.trials,args.seed,out,counter])
    out.with_suffix('.capture.json').write_text(json.dumps(dict(run=run,source_sha256=digest(source),
        dependency_sha256=digest(dependency),binary_sha256=digest(binary),data_sha256=digest(out),counter_sha256=digest(counter)),indent=2)+'\n',encoding='utf-8')
    print(run['stdout'],end='')


if __name__=='__main__':main()
