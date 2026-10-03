"""Replay frozen seed-budget covers/searches and compare all mathematical records."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def main():
    base=Path('direct_attack/native_build').resolve();base.mkdir(exist_ok=True);records=[]
    for root in sorted(Path('direct_attack/data').glob('seed_budget_*')):
        path=root/'summary.json'
        if not path.exists():continue
        frozen=json.loads(path.read_text())
        if 'arguments' not in frozen:continue
        a=frozen['arguments']
        with tempfile.TemporaryDirectory(prefix='seed_budget_replay_',dir=base) as temporary:
            out=Path(temporary).resolve();assert out.parent==base
            seed=root/'input_seeds.json'
            if seed.exists():(out/'input_seeds.json').write_bytes(seed.read_bytes())
            argv=[sys.executable,'-m','direct_attack.seed_budget_attack']
            for key in ['n','alphabet','count','seed','restart','mode','objective']:argv+=['--'+key,str(a[key])]
            if 'minimum_kappa' in a:argv+=['--minimum-kappa',str(a['minimum_kappa'])]
            argv+=['--out',str(out)];started=time.monotonic()
            r=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',errors='replace')
            (root/'replay_stdout.txt').write_text(r.stdout,encoding='utf-8');(root/'replay_stderr.txt').write_text(r.stderr,encoding='utf-8');assert r.returncode==0,r.stderr
            replay=json.loads((out/'summary.json').read_text())
            for key in ['counts','best','records','histogram']:assert replay[key]==frozen[key],(root,key)
            for name in frozen['records']:
                x=json.loads((root/name).read_text());y=json.loads((out/name).read_text());assert x==y,(root,name)
            if seed.exists():assert (out/'input_seeds.json').read_bytes()==seed.read_bytes()
            record=dict(argv=argv,cwd=str(Path.cwd()),returncode=r.returncode,seconds=time.monotonic()-started,verified=True,
                        witnesses=len(frozen['records']),frozen_seed_sha256=hashlib.sha256(seed.read_bytes()).hexdigest() if seed.exists() else None)
            (root/'replay_run.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');records.append(dict(root=str(root),**record))
            print(json.dumps(dict(root=str(root),verified=True,seconds=record['seconds'])),flush=True)
    Path('direct_attack/data/seed_budget_replay_checks.json').write_text(json.dumps(dict(verified=True,records=records),indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
