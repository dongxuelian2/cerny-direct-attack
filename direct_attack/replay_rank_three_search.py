"""Deterministic replay of frozen rank-three seeds, counters and every retained array."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def main():
    base=Path('direct_attack/native_build').resolve();base.mkdir(exist_ok=True);records=[]
    roots=sorted(Path('direct_attack/data').glob('rank_three_extension_n*'))+sorted(Path('direct_attack/data').glob('rank_bounded_extension_n*'))
    for root in roots:
        frozen=json.loads((root/'summary.json').read_text());a=frozen['arguments']
        with tempfile.TemporaryDirectory(prefix='rank3_replay_',dir=base) as temporary:
            out=Path(temporary).resolve();assert out.parent==base
            module='rank_bounded_extension_search' if 'rank' in a else 'rank_three_extension_search'
            argv=[sys.executable,'-m','direct_attack.'+module]
            keys=['n','count','seed','restart']+(['rank','limit','seed_count'] if 'rank' in a else [])
            for key in keys:argv+=['--'+key.replace('_','-'),str(a[key])]
            for key in ['family_seed','elite','permutation_mutations']:
                if a.get(key):argv+=['--'+key.replace('_','-')]
            argv+=['--out',str(out)];started=time.monotonic()
            r=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',errors='replace')
            (root/'replay_stdout.txt').write_text(r.stdout,encoding='utf-8');(root/'replay_stderr.txt').write_text(r.stderr,encoding='utf-8')
            assert r.returncode==0,r.stderr
            replay=json.loads((out/'summary.json').read_text())
            for key in ['seeds','counts','best','records']:assert replay[key]==frozen[key],(root,key)
            assert json.loads((out/'input_seeds.json').read_text())==json.loads((root/'input_seeds.json').read_text())
            for name in frozen['records']:
                x=json.loads((root/name).read_text());y=json.loads((out/name).read_text())
                assert {k:v for k,v in x.items() if k!='scope'}=={k:v for k,v in y.items() if k!='scope'},(root,name)
            record=dict(argv=argv,cwd=str(Path.cwd()),returncode=r.returncode,seconds=time.monotonic()-started,
                        verified=True,records=len(frozen['records']),input_sha256=hashlib.sha256((root/'input_seeds.json').read_bytes()).hexdigest(),
                        boundary='Literal replay outputs retained; initial generation stdout was not saved for rank3 n12/20/30/40. Rank3 n63 and rank4/5 also retain initial generation output.')
            (root/'replay_run.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');records.append(dict(root=str(root),**record))
            print(json.dumps(dict(root=str(root),verified=True,seconds=record['seconds'])),flush=True)
    Path('direct_attack/data/rank_three_replay_checks.json').write_text(json.dumps(dict(verified=True,records=records),indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
