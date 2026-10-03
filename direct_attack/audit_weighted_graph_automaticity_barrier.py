"""Scope-specific counter/prefix audit; old formal/release hashes protected."""
from pathlib import Path
import json
import sys
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    protected=json.loads((ROOT/'direct_attack/data/order_two_weighted_graph_native_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    runs=[capture([sys.executable,'-m','direct_attack.'+m]) for m in
          ('weighted_graph_automaticity_barrier','check_weighted_graph_automaticity_barrier')]
    checker=ROOT/'direct_attack/native_build/check_order_two_weighted_graph_native.exe'
    checker_meta=json.loads((ROOT/'direct_attack/data/order_two_weighted_graph_check_build.json').read_text())
    assert checker_meta['binary_sha256']==digest(checker)
    generations=[]
    for M in (16,18,24,32,48,64,128):
        path=ROOT/('direct_attack/data/weighted_late_block_M'+str(M)+'_sample1000000_seed2026100331.tsv')
        record=json.loads(path.with_suffix('.capture.json').read_text())
        assert record['data_sha256']==digest(path) and record['counter_sha256']==digest(path.with_suffix('.counter.json'))
        assert record['source_sha256']==digest(ROOT/'direct_attack/order_two_weighted_late_block_pressure.cpp')
        assert record['dependency_sha256']==digest(ROOT/'direct_attack/order_two_weighted_graph_pressure.cpp')
        # For M24 this verifies only the successful retained prefix; the failure
        # itself is independently certified by the preceding barrier checker.
        runs.append(capture([checker,path]));generations.append(record)
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths=['direct_attack/'+p for p in ('WEIGHTED_GRAPH_AUTOMATICITY_BARRIER.md',
        'weighted_graph_automaticity_barrier.py','check_weighted_graph_automaticity_barrier.py',
        'order_two_weighted_late_block_pressure.cpp','order_two_weighted_late_block_native.py',
        'data/weighted_graph_automaticity_barrier.json')]
    out=dict(scope='literal graph automaticity refutation and retained pressure PASS prefixes only',runs=runs,
        pressure_generation_captures=generations,sha256={p:digest(ROOT/p) for p in paths},
        protected_release_and_lean_sha256=protected,formally_verified=False,full_historical_rerun=False,
        historical_registry_modified=False,automatic_original_graph='REFUTED',weighted_M_extension='OPEN',general_Cerny='OPEN')
    (ROOT/'direct_attack/data/weighted_graph_automaticity_barrier_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,commands=len(runs),protected_files=len(protected),automatic_graph='REFUTED',general_Cerny='OPEN')))


if __name__=='__main__':main()
