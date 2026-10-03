"""Fresh NEW tail-order controls; protected release/Lean files unchanged."""
from pathlib import Path
import json
import sys
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    protected=json.loads((ROOT/'direct_attack/data/short_tail_unpaired_weighted_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    modules=['permuted_shadow_square','check_permuted_shadow_square']
    runs=[capture([sys.executable,'-m','direct_attack.'+m]) for m in modules]
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths=['direct_attack/'+m+'.py' for m in modules]+['direct_attack/PERMUTED_SHADOW_SQUARE.md',
        'direct_attack/data/permuted_shadow_square.json','direct_attack/paired_root_cycle_square.py']
    out=dict(scope='Opposite root/tail SET with arbitrary tail order and MIXED remaining A; complete NEW small inputs and original controls',
        runs=runs,sha256={p:digest(ROOT/p) for p in paths},protected_release_and_lean_sha256=protected,
        full_historical_rerun=False,historical_registry_modified=False,formally_verified=False,general_Cerny='OPEN')
    (ROOT/'direct_attack/data/permuted_shadow_square_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,commands=len(runs),protected_files=len(protected),general_Cerny='OPEN')))


if __name__=='__main__':main()
