"""Independent native inverse policy solver; completeness is checked exactly."""
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
    source=ROOT/'direct_attack/native_complete_policy.cpp';digest=hashlib.sha256(source.read_bytes()).hexdigest()
    binary=folder/('complete_policy_'+digest[:16]+'.exe')
    if binary.exists():return binary
    compiler=shutil.which('g++');assert compiler is not None,'g++ or the retained executable is required'
    argv=[compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',str(source),'-o',str(binary)]
    r=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    assert r.returncode==0,(r.stdout,r.stderr)
    version=subprocess.run([compiler,'--version'],capture_output=True,text=True,encoding='utf-8',errors='replace')
    report=dict(argv=argv,cwd=str(ROOT),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,
                compiler_version=version.stdout,source_sha256=digest,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
    (ROOT/'direct_attack/data/complete_policy_build.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return binary


def profile(rows,details=False):
    global _process
    n=len(rows[0]);assert all(len(row)==n for row in rows)
    mode=2 if details=='singletons' else int(bool(details))
    if _process is None:
        _process=subprocess.Popen([str(build())],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                  text=True,encoding='ascii',bufsize=1)
        def close():
            if _process.poll() is None:_process.stdin.close();_process.wait(timeout=2)
        atexit.register(close)
    _process.stdin.write(' '.join(map(str,[n,len(rows),mode]+[q for row in rows for q in row]))+'\n');_process.stdin.flush()
    line=_process.stdout.readline()
    if not line:raise RuntimeError('Native complete solver terminated: '+str(_process.poll()))
    fields=list(map(int,line.split()));status=fields[0]
    if status==0:return None
    assert status==1,fields
    out=dict(n=n,rows=rows,best_policy=fields[1],worst_policy=fields[2],rt=fields[3],reachable=fields[4],
             local_excess=fields[5],local_start=fields[6],unit_defect=bool(fields[7]))
    if mode==1:
        N=1<<n;e,best,worst=[list(map(int,_process.stdout.readline().split())) for _ in range(3)]
        assert len(e)==len(best)==len(worst)==N
        out.update(extension={s:e[s] for s in range(N) if e[s]>=0},best={s:best[s] for s in range(N) if best[s]>=0},
                   worst={s:worst[s] for s in range(N) if worst[s]>=0})
    if mode==2:
        e,best,worst=[list(map(int,_process.stdout.readline().split())) for _ in range(3)]
        assert len(e)==len(best)==len(worst)==n
        out.update(singleton_extension=e,singleton_best=best,singleton_worst=worst)
    return out


if __name__=='__main__':print(build())
