from direct_attack.runtime import compile_source
"""Build/load an exact native image-policy scorer; retain Python certificates."""
import atexit
import json
from pathlib import Path
import subprocess
from direct_attack.core import strongly_connected

ROOT=Path(__file__).resolve().parents[2]
_process=None


def build():
    return compile_source("native_policy.cpp")


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
