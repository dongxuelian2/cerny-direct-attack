"""Replay the frozen seven-state native adversarial experiment exactly."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def main():
    source=Path('direct_attack/data/image_extension_policy_broad_n7')
    saved=json.loads((source/'summary.json').read_text());a=saved['arguments']
    with tempfile.TemporaryDirectory(prefix='cerny_policy_replay_') as directory:
        temp=Path(directory).resolve()
        assert temp.parent==Path(tempfile.gettempdir()).resolve()
        shutil.copyfile(source/'input_seeds.json',temp/'input_seeds.json')
        argv=[sys.executable,'-m','direct_attack.image_policy_broad']
        for key in ['n','alphabet','count','seed','restart']:argv+=['--'+key,str(a[key])]
        argv+=['--objective',a.get('objective','global'),'--out',str(temp)]
        start=time.monotonic();r=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',errors='replace')
        assert r.returncode==0,(r.stdout,r.stderr)
        actual=json.loads((temp/'summary.json').read_text())
        for key in ['counts','seeds','seed_max','best_policy','best_rt_at_policy_peak','records']:
            assert actual[key]==saved[key],key
        files=sorted(p.name for p in source.glob('witness_*.json'))
        assert files==sorted(p.name for p in temp.glob('witness_*.json'))
        for name in files:
            before=json.loads((source/name).read_text());after=json.loads((temp/name).read_text())
            for key,value in before.items():assert value==after[key],(name,key)
        report=dict(argv=argv,seconds=time.monotonic()-start,stdout=r.stdout,stderr=r.stderr,
                    returncode=r.returncode,certificates_matched=len(files),counts_matched=True,verified=True)
        Path('direct_attack/data/policy_broad_replay.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(dict(certificates_matched=len(files),counts_matched=True,verified=True)))


if __name__=='__main__':main()
