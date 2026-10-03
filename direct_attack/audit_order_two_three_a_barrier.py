"""Scoped post-release replay and actual command receipt, preserving the release."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from .submission_runtime import lean_compiler
from .weighted_class_reset_native import capture

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    git = ['git', '-c', 'safe.directory='+ROOT.as_posix()]
    tracked = subprocess.check_output(git+['ls-files'], cwd=ROOT, text=True, encoding='utf-8').splitlines()
    protected = {p: digest(ROOT/p) for p in tracked
                 if p.startswith('submission/') or p == 'OPENMATH_SUBMISSION.md'
                 or p.endswith('.lean') and not p.startswith('direct_attack/post_release/')}
    runs = [capture([sys.executable, '-m', module]) for module in (
        'direct_attack.order_two_three_a_barrier',
        'direct_attack.check_order_two_three_a_barrier',
        'direct_attack.order_two_three_a_lean')]
    lean = lean_compiler()
    runs.append(capture([lean, '--version']))
    runs.append(capture([lean, 'direct_attack/post_release/OrderTwoThreeABarrier.lean']))
    assert protected == {p: digest(ROOT/p) for p in protected}
    assert 'sorryAx' not in runs[-1]['stdout'] and 'error:' not in runs[-1]['stdout']
    hashes = {p: digest(ROOT/p) for p in (
        'direct_attack/order_two_three_a_barrier.py', 'direct_attack/check_order_two_three_a_barrier.py',
        'direct_attack/order_two_three_a_lean.py', 'direct_attack/post_release/OrderTwoThreeABarrier.lean',
        'direct_attack/data/order_two_three_a_barrier.json')}
    out = dict(scope='post-release literal n25 ordinary minimum 10, finite three-a controls; infinite family paper',
               base_release_head='ac948e7001bff5428c22d236f96974856452d34d', runs=runs,
               protected_release_and_old_lean_sha256=protected, source_and_data_sha256=hashes,
               historical_registry_modified=False, full_historical_rerun=False)
    (ROOT/'direct_attack/data/order_two_three_a_barrier_audit.json').write_text(
        json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(verified=True, scoped_commands=len(runs), protected_files=len(protected),
                          lean_minimum=10, general_Cerny='OPEN')))


if __name__ == '__main__':
    main()
