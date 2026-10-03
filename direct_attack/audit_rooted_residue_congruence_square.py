"""Fresh scoped residue-congruence audit; no historical release replacement."""
from pathlib import Path
import json
import sys
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    protected=json.loads((ROOT/'direct_attack/data/rooted_period_rank_payment_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    modules=['rooted_residue_congruence_square','check_rooted_residue_congruence_square']
    runs=[capture([sys.executable,'-m','direct_attack.'+m]) for m in modules]
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths=['direct_attack/'+m+'.py' for m in modules]+['direct_attack/ROOTED_RESIDUE_CONGRUENCE_SQUARE.md',
        'direct_attack/data/rooted_residue_congruence_square.json','direct_attack/data/rooted_period_rank_payment.json']
    out=dict(scope='ALL-n order-two square paper theorem; independent compatible original resets and complete both-root-flag periodic targets',
        runs=runs,sha256={p:digest(ROOT/p) for p in paths},protected_release_and_lean_sha256=protected,
        formally_verified=False,model_square='PROVED paper',model_WEXT='PROVED paper',general_Cerny='OPEN',
        full_historical_rerun=False,historical_registry_modified=False)
    (ROOT/'direct_attack/data/rooted_residue_congruence_square_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,commands=len(runs),protected_files=len(protected),model_square='PROVED paper',general_Cerny='OPEN')))


if __name__=='__main__':main()
