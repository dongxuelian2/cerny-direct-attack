"""Authenticate seven open-region controls without an omitted-case claim."""
from pathlib import Path
import json
import sys
from .weighted_class_reset_native import ROOT,capture,digest
from .check_short_tail_unpaired_weighted_pressure import NAMES


def main():
    protected=json.loads((ROOT/'direct_attack/data/short_tail_opposite_weighted_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    source=ROOT/'direct_attack/short_tail_unpaired_weighted_pressure.cpp';binary=ROOT/'direct_attack/native_build/short_tail_unpaired_weighted_pressure.exe'
    build=json.loads((ROOT/'direct_attack/data/short_tail_unpaired_weighted_build.json').read_text())
    assert build['source_sha256']==digest(source) and build['binary_sha256']==digest(binary)
    native=[];paths=[]
    for name in NAMES:
        output=ROOT/'direct_attack/data'/ (name+'.json');receipt=output.with_name(name+'_capture.json');run=json.loads(receipt.read_text())
        assert run['source_sha256']==digest(source) and run['binary_sha256']==digest(binary) and run['output_sha256']==digest(output)
        assert run['returncode']==0 and run['argv'][0]==str(binary) and run['argv'][2]==str(output)
        native.append(run);paths.extend([str(output.relative_to(ROOT)),str(receipt.relative_to(ROOT))])
    check=capture([sys.executable,'-m','direct_attack.check_short_tail_unpaired_weighted_pressure'])
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths.extend(['direct_attack/short_tail_unpaired_weighted_pressure.cpp','direct_attack/short_tail_unpaired_weighted_native.py',
        'direct_attack/check_short_tail_unpaired_weighted_pressure.py','direct_attack/check_short_tail_opposite_weighted_pressure.py',
        'direct_attack/UNPAIRED_SHORT_TAIL_PRESSURE.md','direct_attack/data/short_tail_unpaired_weighted_build.json'])
    out=dict(scope='Only retained OPEN-region cuts, excluding solved paired forms; no omitted-proposal coverage',native_captures=native,
        independent_check=check,sha256={p:digest(ROOT/p) for p in paths},protected_release_and_lean_sha256=protected,
        full_historical_rerun=False,historical_registry_modified=False,formally_verified=False,general_Cerny='OPEN',proposal_counts='EXPLORATORY')
    (ROOT/'direct_attack/data/short_tail_unpaired_weighted_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,retained_cuts=len(native),protected_files=len(protected),proposal_counts='EXPLORATORY')))


if __name__=='__main__':main()
