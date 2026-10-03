"""Native graph pressure with literal command/hash captures."""
from pathlib import Path
import argparse
import json
import os
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--M',type=int,default=12)
    parser.add_argument('--trials',type=int,default=0)
    args=parser.parse_args()
    source=ROOT/'direct_attack/order_two_weighted_graph_pressure.cpp'
    binary=ROOT/'direct_attack/native_build/order_two_weighted_graph_pressure.exe'
    metadata=ROOT/'direct_attack/data/order_two_weighted_graph_pressure_build.json'
    valid=False
    if metadata.exists() and binary.exists():
        prior=json.loads(metadata.read_text());valid=prior['source_sha256']==digest(source) and prior['binary_sha256']==digest(binary)
    if not valid:
        compiler=os.environ.get('CXX','<CXX_BIN>/g++.exe')
        build=capture([compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',source,'-o',binary])
        metadata.write_text(json.dumps(dict(source_sha256=digest(source),binary_sha256=digest(binary),build=build),indent=2)+'\n',encoding='utf-8')
    label='complete' if args.trials==0 else 'sample'+str(args.trials)
    out=ROOT/('direct_attack/data/order_two_weighted_graph_M'+str(args.M)+'_'+label+'.tsv')
    counter=out.with_suffix('.counter.json')
    run=capture([binary,args.M,args.trials,out,counter])
    out.with_suffix('.capture.json').write_text(json.dumps(dict(source_sha256=digest(source),binary_sha256=digest(binary),
        residual_tsv_sha256=digest(out),counter_sha256=digest(counter),run=run),indent=2)+'\n',encoding='utf-8')
    print(run['stdout'],end='')


if __name__=='__main__':main()
