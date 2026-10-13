"""Complete permutation-plus-corank-one binary cover, with centralizer reduction."""
import argparse
import json
from pathlib import Path
import subprocess
import time
from direct_attack.native_policy import build
from direct_attack.image_extension_policy import profile
from direct_attack.check_image_policy import verify


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--n',type=int,required=True)
    ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    argv=[str(build()),'--rank-cover',str(args.n)];started=time.monotonic()
    process=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='ascii',bufsize=1)
    records=[]
    for line in process.stdout:
        item=json.loads(line);records.append(item);print(line.rstrip(),flush=True)
        if item['event']=='refutation':
            c=profile(item['rows']);assert c['best_policy']==item['best_policy'] and c['rt']==item['rt']
            saved=json.loads(json.dumps(c));verify(saved)
            (out/'witness_000.json').write_text(json.dumps(saved,indent=2)+'\n',encoding='utf-8')
    stderr=process.stderr.read();returncode=process.wait();assert returncode==0,stderr
    report=dict(arguments=vars(args),argv=argv,returncode=returncode,stderr=stderr,
                records=records,result=records[-1],seconds=time.monotonic()-started,
                scope='Complete binary permutation + rank-(n-1) covering; counts overlap, not isomorphism classes.',
                reduction='For each permutation cycle type, one missing-image representative per distinct cycle length suffices by its centralizer action.')
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}))


if __name__=='__main__':main()
