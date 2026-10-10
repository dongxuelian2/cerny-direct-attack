"""Build and run an independent complete paired-seventh row audit.

Requires a C++17 compiler (CXX, clang++, or g++). No generator imports.
Small proof-case histograms are matched against the Python literal audit;
the n13 runs completely exhaust each normalized paired geometry.
"""
from pathlib import Path
from math import factorial
import hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent

def main():
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if compiler is None:raise RuntimeError('C++17 compiler required; set CXX')
    dest=ROOT.parent/'_qa'/'paired_seventh_cpp';dest.mkdir(parents=True,exist_ok=True)
    exe=dest/('check_paired_seventh_rows.exe' if os.name=='nt' else 'check_paired_seventh_rows')
    source=ROOT/'check_paired_seventh_rows.cpp'
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic']
    build=subprocess.run([compiler,*flags,str(source),'-o',str(exe)],capture_output=True,text=True)
    if build.returncode:raise RuntimeError(build.stdout+build.stderr)
    assert not build.stderr,build.stderr
    python=json.loads((ROOT/'b1_e6_f7_g8_seventh_audit.json').read_text(encoding='utf-8'))
    assert python['status']=='pass'
    def H(mode):return {12:[1,2],19:[1,9],24:[2,4],129:[1,2,9]}[mode]
    runs=[];controls=0
    for mode in (12,19,24,129):
        for n in (10,11,13):
            command=subprocess.run([str(exe),str(n),str(mode)],capture_output=True,text=True)
            if command.returncode:raise RuntimeError(command.stdout+command.stderr)
            assert not command.stderr,command.stderr
            report=json.loads(command.stdout);assert report['status']=='pass'
            assert (report['n'],report['H'])==(n,mode)
            k=n-8;expected=768*k*factorial(k)**2
            if mode in (19,24):expected*=k
            assert report['left_rows']==192*k*factorial(k)
            assert report['right_rows']==4*factorial(k)*(k if mode in (19,24) else 1)
            assert report['complete_normalized_row_pairs']==expected
            assert sum(report['proof_cases'].values())==expected
            if n!=13:
                control=next(v for v in python['complete_literal_controls'] if v['n']==n and v['H']==H(mode))
                assert control['proof_cases']==report['proof_cases']
                assert control['complete_normalized_row_pairs']==expected;controls+=1
            report['H']=H(mode);runs.append(report)
            print(json.dumps(dict(n=n,H=H(mode),complete_normalized_row_pairs=expected,status='pass')),flush=True)
    full=[v for v in runs if v['n']==13]
    assert [v['complete_normalized_row_pairs'] for v in full]==[55296000,276480000,276480000,55296000]
    assert sum(v['complete_normalized_row_pairs'] for v in full)==663552000 and controls==8
    names=[Path(__file__).name,source.name,'check_b1_e6_f7_g8_seventh.py',
        'b1_e6_f7_g8_seventh_audit.json','B1_E6_F7_G8_PAIRED_SEVENTH_EXCLUSIONS.md']
    result=dict(status='pass',parameter=[13,9,1],branch=dict(E=[6],F=[7],G=[8]),
        alphabet='binary only',build_flags=flags,compiler_diagnostics='',
        independent_row_generation='Inject outside-guard inputs, then assign guard to each target; no kernel templates.',
        smaller_complete_proof_case_histograms_matched=controls,runs=runs,
        complete_n13_normalized_row_pairs=663552000,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete coupled n13 normalized rows for four conditional paired H geometries only. Every protected assignment retained. Does not classify H9/H29, arbitrary alphabets, all n13 automata, or an exact F value.')
    (ROOT/'paired_seventh_cpp_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='pass',complete_n13_normalized_row_pairs=663552000,matched_histograms=controls)),flush=True)
if __name__=='__main__':main()
