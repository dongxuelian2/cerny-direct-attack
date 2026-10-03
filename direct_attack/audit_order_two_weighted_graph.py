"""Separate post-release graph/endpoint audit; prior snapshots protected."""
from pathlib import Path
import subprocess
import sys
import json
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    git=['git','-c','safe.directory='+ROOT.as_posix()]
    names=subprocess.check_output(git+['ls-files'],cwd=ROOT,text=True,encoding='utf-8').splitlines()
    protected={p:digest(ROOT/p) for p in names if p.startswith('submission/') or p=='OPENMATH_SUBMISSION.md' or p.endswith('.lean')}
    modules=['order_two_weighted_endpoints','check_order_two_weighted_endpoints',
             'order_two_weighted_graph_criterion','check_order_two_weighted_graph_criterion']
    runs=[capture([sys.executable,'-m','direct_attack.'+m]) for m in modules]
    assert protected=={p:digest(ROOT/p) for p in protected}
    paths=['direct_attack/'+m+'.py' for m in modules]+[
        'direct_attack/WEIGHTED_GRAPH_SQUARE.md','direct_attack/data/order_two_weighted_endpoints.json',
        'direct_attack/data/order_two_weighted_graph_criterion.json']
    out=dict(scope='endpoint words, graph criterion and finite square resets only; automatic connectivity OPEN',
             runs=runs,sha256={p:digest(ROOT/p) for p in paths},protected_release_and_lean_sha256=protected,
             full_historical_rerun=False,historical_registry_modified=False,formally_verified=False,general_Cerny='OPEN')
    (ROOT/'direct_attack/data/order_two_weighted_graph_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,scoped_commands=len(runs),protected_files=len(protected),general_Cerny='OPEN')))


if __name__=='__main__':main()
