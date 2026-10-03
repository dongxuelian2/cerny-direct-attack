"""Capture only OPEN unpaired short-tail pressure, excluding solved forms."""
from pathlib import Path
import argparse
import json
from .weighted_class_reset_native import ROOT,capture,digest


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--M',type=int,required=True);parser.add_argument('--sample',type=int,default=0);args=parser.parse_args()
    src=ROOT/'direct_attack/short_tail_unpaired_weighted_pressure.cpp';binary=ROOT/'direct_attack/native_build/short_tail_unpaired_weighted_pressure.exe'
    meta=ROOT/'direct_attack/data/short_tail_unpaired_weighted_build.json'
    if not(meta.exists() and binary.exists() and json.loads(meta.read_text())['source_sha256']==digest(src)
           and json.loads(meta.read_text())['binary_sha256']==digest(binary)):
        compiler=Path('<CXX_BIN>/g++.exe')
        version=capture([compiler,'--version']);build=capture([compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',src,'-o',binary])
        meta.write_text(json.dumps(dict(source_sha256=digest(src),binary_sha256=digest(binary),compiler=version,build=build),indent=2)+'\n',encoding='utf-8')
    stem='short_tail_unpaired_weighted_M'+str(args.M)+('_sample'+str(args.sample) if args.sample else '')
    out=ROOT/'direct_attack/data'/ (stem+'.json');argv=[binary,args.M,out]
    if args.sample:argv.append(args.sample)
    run=capture(argv);run.update(source_sha256=digest(src),binary_sha256=digest(binary),output_sha256=digest(out))
    out.with_name(stem+'_capture.json').write_text(json.dumps(run,indent=2)+'\n',encoding='utf-8')
    print(run['stdout'].strip())


if __name__=='__main__':main()
