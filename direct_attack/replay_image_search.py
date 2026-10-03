"""Replay one archived adversarial search in an isolated temporary directory."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def main():
    source=Path('direct_attack/data/image_extension_adversarial_n8')
    saved=json.loads((source/'summary.json').read_text());a=saved['arguments']
    with tempfile.TemporaryDirectory(prefix='cerny_image_replay_') as directory:
        temp=Path(directory).resolve()
        assert temp.parent==Path(tempfile.gettempdir()).resolve()
        shutil.copyfile(source/'input_seeds.json',temp/'input_seeds.json')
        argv=[sys.executable,'-m','direct_attack.image_extension_adversarial',
              '--n',str(a['n']),'--count',str(a['count']),'--seed',str(a['seed']),'--out',str(temp)]
        started=time.monotonic();r=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',errors='replace')
        assert r.returncode==0,(r.stdout,r.stderr)
        actual=json.loads((temp/'summary.json').read_text())
        for key in ['counts','best','records']:assert actual[key]==saved[key],key
        files=sorted(p.name for p in source.glob('n*_cost*.json'))
        assert files==sorted(p.name for p in temp.glob('n*_cost*.json'))
        for file in files:assert json.loads((source/file).read_text())==json.loads((temp/file).read_text()),file
        report=dict(argv=argv,seconds=time.monotonic()-started,stdout=r.stdout,stderr=r.stderr,
                    returncode=r.returncode,certificates_matched=len(files),counts_matched=True,verified=True)
        Path('direct_attack/data/image_search_replay.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(dict(certificates_matched=len(files),counts_matched=True,verified=True)))


if __name__=='__main__':main()
