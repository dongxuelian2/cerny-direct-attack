"""Exact complete middle-rank image-extension layer of the alternating family."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time


ROOT=Path(__file__).resolve().parent.parent


def build():
    source=ROOT/'direct_attack/alternating_extension.cpp';digest=hashlib.sha256(source.read_bytes()).hexdigest()
    binary=ROOT/'direct_attack/native_build'/('alternating_'+digest[:16]+'.exe')
    if binary.exists():return binary
    compiler=shutil.which('g++');assert compiler is not None
    argv=[compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',str(source),'-o',str(binary)]
    r=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True);assert r.returncode==0,(r.stdout,r.stderr)
    report=dict(argv=argv,stdout=r.stdout,stderr=r.stderr,returncode=r.returncode,source_sha256=digest,
                binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
    (ROOT/'direct_attack/data/alternating_native_build.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return binary


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--max-n',type=int,default=23)
    ap.add_argument('--out',default='direct_attack/data/alternating_extension_layer');args=ap.parse_args()
    out=Path(args.out);out.mkdir(exist_ok=True);binary=build();records=[]
    for n in range(5,args.max_n+1,2):
        argv=[str(binary),str(n)];start=time.monotonic()
        r=subprocess.run(argv,capture_output=True,text=True,encoding='ascii');assert r.returncode==0,(r.stdout,r.stderr)
        c=json.loads(r.stdout);m=(n-1)//2;c['rows']=[[q-q%2 for q in range(n)],[(q+1)%n for q in range(n)]]
        i,rotation=c['missing_index'],c['rotation']
        # Q a b a=F. F b^(2i+2) a=E\{2i}, i<m; F=E\{2m}.
        c['reach_word']=[0,1,0]+([] if i==m else [1]*(2*i+2)+[0])+[1]*rotation
        c['argv']=argv;c['stdout']=r.stdout;c['stderr']=r.stderr;c['seconds']=time.monotonic()-start
        c['scope']='All reachable images of cardinality (n-1)/2, not all reachable ranks or all automata.'
        (out/f'n{n}.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        record={key:c[key] for key in ['n','rank','images_at_rank','max_cost','missing_index','rotation','seconds']}
        records.append(record);print(json.dumps(record),flush=True)
    (out/'summary.json').write_text(json.dumps(dict(arguments=vars(args),records=records),indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
