"""Scoped long-tail theorem controls, preserving old formal/release inventory."""
from pathlib import Path
import json
import sys
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    protected=json.loads((ROOT/'direct_attack/data/rooted_residue_congruence_square_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    modules=['tail_cycle_weighted_square','check_tail_cycle_weighted_square']
    runs=[capture([sys.executable,'-m','direct_attack.'+m]) for m in modules]
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths=['direct_attack/'+m+'.py' for m in modules]+['direct_attack/TAIL_CYCLE_WEIGHTED_SQUARE.md',
        'direct_attack/data/tail_cycle_weighted_square.json']
    out=dict(scope='NEW excluded small kernels and original long-tail compatible reset/weighted-average controls',runs=runs,
        sha256={p:digest(ROOT/p) for p in paths},protected_release_and_lean_sha256=protected,
        full_historical_rerun=False,historical_registry_modified=False,formally_verified=False,
        long_tail_square='PROVED paper',general_Cerny='OPEN')
    (ROOT/'direct_attack/data/tail_cycle_weighted_square_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,commands=len(runs),protected_files=len(protected),general_Cerny='OPEN')))


if __name__=='__main__':main()
