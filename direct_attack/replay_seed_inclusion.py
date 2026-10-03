"""Replay the frozen inclusion search and compare all retained mathematical data."""
import hashlib,json
from pathlib import Path
import subprocess,sys,tempfile,time


def main():
    root=Path('direct_attack/data/seed_inclusion');frozen=json.loads((root/'summary.json').read_text());a=frozen['arguments']
    base=Path('direct_attack/native_build').resolve();base.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='seed_inclusion_replay_',dir=base) as temporary:
        out=Path(temporary).resolve();assert out.parent==base
        seed=root/'input_seeds.json';(out/'input_seeds.json').write_bytes(seed.read_bytes())
        argv=[sys.executable,'-m','direct_attack.seed_inclusion_attack','--count',str(a['count']),'--seed',str(a['seed']),'--out',str(out)]
        started=time.monotonic();r=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (root/'replay_stdout.txt').write_text(r.stdout,encoding='utf-8');(root/'replay_stderr.txt').write_text(r.stderr,encoding='utf-8');assert r.returncode==0,r.stderr
        replay=json.loads((out/'summary.json').read_text())
        for key in ['counts','best_gap','records','certificates']:assert frozen[key]==replay[key]
        for name in frozen['records']+frozen['certificates']:assert json.loads((root/name).read_text())==json.loads((out/name).read_text()),name
        assert seed.read_bytes()==(out/'input_seeds.json').read_bytes()
        report=dict(verified=True,argv=argv,cwd=str(Path.cwd()),returncode=0,seconds=time.monotonic()-started,
                    frozen_seed_sha256=hashlib.sha256(seed.read_bytes()).hexdigest(),records=len(frozen['records']),certificates=len(frozen['certificates']))
        (root/'replay_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report),flush=True)


if __name__=='__main__':main()
