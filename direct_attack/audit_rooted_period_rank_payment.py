"""Separate rooted rank/payment audit; frozen submission and old Lean untouched."""
from pathlib import Path
import json
import sys
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    protected=json.loads((ROOT/'direct_attack/data/weighted_graph_automaticity_barrier_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    modules=['rooted_period_rank_payment','check_rooted_period_rank_payment','period_rank_extension_controls','check_period_rank_extension_controls']
    runs=[capture([sys.executable,'-m','direct_attack.'+m]) for m in modules]
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths=['direct_attack/'+m+'.py' for m in modules]+['direct_attack/period_rank_polynomials.py',
        'direct_attack/ROOTED_PERIOD_RANK_PAYMENT.md','direct_attack/data/rooted_period_rank_tables.json',
        'direct_attack/data/rooted_period_rank_payment.json','direct_attack/data/period_rank_extension_controls.json']
    out=dict(scope='rational Boolean rank coverage, compatible rooted payments, and separate periodic upper/saturation words',
             runs=runs,sha256={p:digest(ROOT/p) for p in paths},protected_release_and_lean_sha256=protected,
             full_historical_rerun=False,historical_registry_modified=False,formally_verified=False,general_Cerny='OPEN')
    (ROOT/'direct_attack/data/rooted_period_rank_payment_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,commands=len(runs),protected_files=len(protected),general_Cerny='OPEN')))


if __name__=='__main__':main()
