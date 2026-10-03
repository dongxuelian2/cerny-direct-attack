"""Fully replay all short-reset adaptive streams, including initial RNG advancement."""
import hashlib,json
from pathlib import Path
import subprocess,sys,tempfile,time


def main():
    base=Path('direct_attack/native_build').resolve();base.mkdir(exist_ok=True);records=[]
    for root in sorted(Path('direct_attack/data').glob('short_reset_policy_n*')):
        frozen=json.loads((root/'summary.json').read_text());a=frozen['arguments']
        with tempfile.TemporaryDirectory(prefix='short_reset_replay_',dir=base) as temporary:
            out=Path(temporary).resolve();assert out.parent==base;seed=root/'input_seeds.json';(out/'input_seeds.json').write_bytes(seed.read_bytes())
            argv=[sys.executable,'-m','direct_attack.short_reset_policy_attack']
            for key in ['n','rank','alphabet','count','seed','restart']:argv+=['--'+key,str(a[key])]
            argv+=['--out',str(out)];started=time.monotonic();r=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',errors='replace')
            (root/'replay_stdout.txt').write_text(r.stdout,encoding='utf-8');(root/'replay_stderr.txt').write_text(r.stderr,encoding='utf-8');assert r.returncode==0,r.stderr
            replay=json.loads((out/'summary.json').read_text())
            for key in ['counts','max_policy','records','histogram']:assert frozen[key]==replay[key],(root,key)
            for name in frozen['records']:assert json.loads((root/name).read_text())==json.loads((out/name).read_text()),(root,name)
            assert seed.read_bytes()==(out/'input_seeds.json').read_bytes()
            record=dict(argv=argv,cwd=str(Path.cwd()),verified=True,returncode=0,seconds=time.monotonic()-started,
                        witnesses=len(frozen['records']),seed_sha256=hashlib.sha256(seed.read_bytes()).hexdigest())
            (root/'replay_run.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');records.append(dict(root=str(root),**record));print(json.dumps(records[-1]),flush=True)
    Path('direct_attack/data/short_reset_replay_checks.json').write_text(json.dumps(dict(verified=True,records=records),indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
