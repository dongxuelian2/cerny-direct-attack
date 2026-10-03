"""Authenticate actual native captures; independently certify retained cuts."""
from pathlib import Path
import json
import sys
from .weighted_class_reset_native import ROOT,capture,digest


def main():
    protected=json.loads((ROOT/'direct_attack/data/paired_root_cycle_square_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    source=ROOT/'direct_attack/short_tail_opposite_weighted_pressure.cpp'
    binary=ROOT/'direct_attack/native_build/short_tail_opposite_weighted_pressure.exe'
    build=json.loads((ROOT/'direct_attack/data/short_tail_opposite_weighted_build.json').read_text())
    assert build['source_sha256']==digest(source) and build['binary_sha256']==digest(binary)
    names=['short_tail_opposite_weighted_M6','short_tail_opposite_weighted_M8','short_tail_opposite_weighted_M10',
        'short_tail_opposite_weighted_M12_sample2000','short_tail_opposite_weighted_M14_sample1000',
        'short_tail_opposite_weighted_M16_sample500','short_tail_opposite_weighted_M18_sample250','short_tail_opposite_weighted_M20_sample100']
    native=[];paths=[]
    for name in names:
        output=ROOT/'direct_attack/data'/ (name+'.json');receipt=output.with_name(name+'_capture.json');run=json.loads(receipt.read_text())
        assert run['source_sha256']==digest(source) and run['binary_sha256']==digest(binary) and run['output_sha256']==digest(output)
        assert run['returncode']==0 and str(binary)==run['argv'][0] and str(output)==run['argv'][2]
        native.append(run);paths.extend([str(output.relative_to(ROOT)),str(receipt.relative_to(ROOT))])
    check=capture([sys.executable,'-m','direct_attack.check_short_tail_opposite_weighted_pressure'])
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths.extend(['direct_attack/short_tail_opposite_weighted_pressure.cpp','direct_attack/short_tail_opposite_weighted_native.py',
        'direct_attack/check_short_tail_opposite_weighted_pressure.py','direct_attack/SHORT_TAIL_WEIGHTED_CONTROLS.md',
        'direct_attack/data/short_tail_opposite_weighted_build.json'])
    out=dict(scope='Eight retained exact weighted cuts and actual resets; NO native omitted-proposal coverage claim',
        native_captures=native,independent_check=check,sha256={p:digest(ROOT/p) for p in paths},
        protected_release_and_lean_sha256=protected,full_historical_rerun=False,historical_registry_modified=False,
        formally_verified=False,general_Cerny='OPEN',proposal_counts='EXPLORATORY')
    (ROOT/'direct_attack/data/short_tail_opposite_weighted_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,retained_cuts=8,native_captures=8,protected_files=len(protected),proposal_counts='EXPLORATORY')))


if __name__=='__main__':main()
