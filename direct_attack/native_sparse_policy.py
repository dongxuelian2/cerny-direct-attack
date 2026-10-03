"""Exact sparse reachable-image multi-source policy kernel (n<=63)."""
import atexit
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parent.parent
_process=None


def build():
    folder=ROOT/'direct_attack/native_build';folder.mkdir(exist_ok=True)
    source=ROOT/'direct_attack/native_sparse_policy.cpp';digest=hashlib.sha256(source.read_bytes()).hexdigest()
    binary=folder/('sparse_policy_'+digest[:16]+'.exe')
    if binary.exists():return binary
    compiler=shutil.which('g++');assert compiler is not None,'g++ or retained executable required'
    argv=[compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',str(source),'-o',str(binary)]
    r=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    assert r.returncode==0,(r.stdout,r.stderr)
    version=subprocess.run([compiler,'--version'],capture_output=True,text=True,encoding='utf-8',errors='replace')
    report=dict(argv=argv,cwd=str(ROOT),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,
                compiler_version=version.stdout,source_sha256=digest,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
    (ROOT/'direct_attack/data/sparse_policy_build.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return binary


def profile(rows,details=False,limit=200000,seed_budget=False):
    global _process
    n=len(rows[0]);assert 2<=n<=63 and all(len(row)==n for row in rows)
    if _process is None:
        _process=subprocess.Popen([str(build())],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                  text=True,encoding='ascii',bufsize=1)
        def close():
            if _process.poll() is None:_process.stdin.close();_process.wait(timeout=2)
        atexit.register(close)
    assert not (details and seed_budget),'Seed-summary and full-array protocol modes are separate'
    mode=2 if seed_budget else int(bool(details))
    _process.stdin.write(' '.join(map(str,[n,len(rows),mode,limit]+[q for row in rows for q in row]))+'\n');_process.stdin.flush()
    line=_process.stdout.readline()
    if not line:raise RuntimeError('Sparse kernel terminated: '+str(_process.poll()))
    fields=list(map(int,line.split()));status=fields[0]
    if status==0:return None
    if status==-4:return dict(truncated=True,n=n,limit=limit)
    assert status==1,fields
    out=dict(n=n,rows=rows,best_policy=fields[1],worst_policy=fields[2],rt=fields[3],reachable=fields[4],
             max_extension=fields[5],extension_start=fields[6],max_proper_rank=fields[7],truncated=False)
    if seed_budget:
        assert len(fields)==14,fields
        out.update(kappa=fields[8],seed_best=fields[9],anchor_best=fields[10],anchor_worst=fields[11],
                   seed_image=fields[12],anchor_image=fields[13])
    if details:
        e={};best={};worst={};forward={}
        for _ in range(out['reachable']):
            S,c,g,w,f=list(map(int,_process.stdout.readline().split()))
            assert S not in forward;forward[S]=f
            if c>=0:e[S]=c
            best[S]=g;worst[S]=w
        out.update(extension=e,best=best,worst=worst,forward=forward)
    return out


if __name__=='__main__':print(build())
