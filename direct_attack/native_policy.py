"""Build/load an exact native image-policy scorer; retain Python certificates."""
import atexit
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from direct_attack.core import strongly_connected

ROOT=Path(__file__).resolve().parent.parent
_process=None


def build():
    folder=ROOT/'direct_attack/native_build';folder.mkdir(exist_ok=True)
    source=ROOT/'direct_attack/native_policy.cpp';digest=hashlib.sha256(source.read_bytes()).hexdigest()
    binary=folder/('image_policy_'+digest[:16]+'.exe')
    if binary.exists():return binary
    compiler=shutil.which('g++')
    if compiler is None:raise RuntimeError('g++ unavailable; existing Python solver remains usable')
    argv=[compiler,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',
          'direct_attack/native_policy.cpp','-o',str(binary.relative_to(ROOT))]
    result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    version=subprocess.run([compiler,'--version'],capture_output=True,text=True,encoding='utf-8',errors='replace')
    report=dict(argv=argv,cwd=str(ROOT),stdout=result.stdout,stderr=result.stderr,
                returncode=result.returncode,compiler_version=version.stdout,source_sha256=digest)
    if result.returncode:raise RuntimeError(json.dumps(report))
    report['binary_sha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
    (ROOT/'direct_attack/data/native_build.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return binary


def profile(rows,details=False):
    global _process
    n=len(rows[0]);N=1<<n
    if not strongly_connected(rows):return None
    if _process is None:
        _process=subprocess.Popen([str(build())],cwd=ROOT,stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='ascii',bufsize=1)
        def close():
            if _process.poll() is None:
                _process.stdin.close();_process.wait(timeout=2)
        atexit.register(close)
    line=' '.join(map(str,[n,len(rows),int(details)]+[q for row in rows for q in row]))+'\n'
    _process.stdin.write(line);_process.stdin.flush()
    answer=_process.stdout.readline()
    if not answer:raise RuntimeError(f'native process terminated: {_process.poll()}')
    fields=list(map(int,answer.split()));status=fields[0];summary=fields[1:]
    if status==0:return None
    if status!=1:raise RuntimeError(f'native scorer rejected input with status {status}')
    out=dict(n=n,rows=rows,best_policy=summary[0],worst_policy=summary[1],rt=summary[2],reachable=summary[3],
             local_excess=summary[4],local_start=summary[5])
    if details:
        e,best,worst=[list(map(int,_process.stdout.readline().split())) for _ in range(3)]
        assert len(e)==len(best)==len(worst)==N
        out.update(extension={s:e[s] for s in range(N) if e[s]>=0},
                   best={s:best[s] for s in range(N) if best[s]>=0},
                   worst={s:worst[s] for s in range(N) if worst[s]>=0})
    return out


if __name__=='__main__':print(build())
