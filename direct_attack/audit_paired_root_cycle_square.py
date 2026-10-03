"""Separate paired-root-cycle theorem controls; preserve frozen release."""
from pathlib import Path
import json
import sys
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    protected=json.loads((ROOT/'direct_attack/data/tail_cycle_weighted_square_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    modules=['paired_root_cycle_square','check_paired_root_cycle_square']
    runs=[capture([sys.executable,'-m','direct_attack.'+m]) for m in modules]
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths=['direct_attack/'+m+'.py' for m in modules]+['direct_attack/PAIRED_ROOT_CYCLE_SQUARE.md',
        'direct_attack/data/paired_root_cycle_square.json','direct_attack/rooted_residue_congruence_square.py']
    out=dict(scope='ALL paired-root-cycle square paper theorem; complete NEW paired input coverage and complete small/named larger periodic controls',
        runs=runs,sha256={p:digest(ROOT/p) for p in paths},protected_release_and_lean_sha256=protected,
        full_historical_rerun=False,historical_registry_modified=False,formally_verified=False,
        paired_square='PROVED paper',paired_WEXT='PROVED paper',general_Cerny='OPEN')
    (ROOT/'direct_attack/data/paired_root_cycle_square_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,commands=len(runs),protected_files=len(protected),general_Cerny='OPEN')))


if __name__=='__main__':main()
