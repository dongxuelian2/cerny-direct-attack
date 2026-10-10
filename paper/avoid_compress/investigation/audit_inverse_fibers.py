"""Compile an independent harness against the actual numeric cover methods.

No method is copied into this checker. The original root entry point is
omitted, and audit_inverse_fibers.cpp is appended to the declaration prefix.
The original cover and included independent source are never modified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--compiler',default='clang++')
    ap.add_argument('--build-dir',type=Path,required=True)
    ap.add_argument('--out',type=Path,default=ROOT/'inverse_fibers_audit.json')
    ap.add_argument('--sanitize',action='store_true');args=ap.parse_args()
    compiler=shutil.which(args.compiler)
    assert compiler is not None,f'Compiler not found: {args.compiler}'
    source=ROOT/'compression_decision_inverse_zero_fibers.cpp'
    harness=ROOT/'audit_inverse_fibers.cpp'
    text=source.read_text(encoding='utf-8');marker='int main(int argc,char**argv)'
    assert text.count(marker)==1
    prefix=text[:text.index(marker)]
    assert 'bool possible()' in prefix and 'bool synchronizing()' in prefix
    build=args.build_dir.resolve();build.mkdir(parents=True,exist_ok=True)
    generated=build/'inverse_fibers_audit_generated.cpp'
    generated.write_text(prefix+'\n'+harness.read_text(encoding='utf-8'),encoding='utf-8')
    binary=build/('inverse_fibers_audit.exe' if sys.platform=='win32' else 'inverse_fibers_audit')
    flags=['-std=c++17','-O2'] if not args.sanitize else ['-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer']
    subprocess.run([compiler,*flags,'-I',str(ROOT),str(generated),'-o',str(binary)],check=True)
    result=subprocess.run([str(binary)],check=True,capture_output=True,text=True)
    data=json.loads(result.stdout)
    assert data['status']=='pass' and data['random_cases']==1000
    assert data['sizes']==[5,8,12,13,16] and data['positive_control_compression']==10
    data['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (source,ROOT/'compression_decision_extended_independent.cpp',harness)}
    data['sanitizers_enabled']=args.sanitize
    args.out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data))


if __name__=='__main__':main()
