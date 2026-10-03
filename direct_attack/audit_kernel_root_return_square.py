"""Separate higher-tail audit preserving release snapshots and all Lean files."""
from pathlib import Path
import json
import subprocess
import sys
from .audit_order_two_three_a_barrier import digest
from .weighted_class_reset_native import capture

ROOT = Path(__file__).resolve().parents[1]


def main():
    git = ['git', '-c', 'safe.directory='+ROOT.as_posix()]
    tracked = subprocess.check_output(git+['ls-files'], cwd=ROOT, text=True, encoding='utf-8').splitlines()
    protected = {p: digest(ROOT/p) for p in tracked
                 if p.startswith('submission/') or p == 'OPENMATH_SUBMISSION.md' or p.endswith('.lean')}
    runs = [capture([sys.executable, '-m', module]) for module in
            ('direct_attack.kernel_root_return_square', 'direct_attack.check_kernel_root_return_square')]
    assert protected == {p: digest(ROOT/p) for p in protected}
    hashes = {p: digest(ROOT/p) for p in (
        'direct_attack/kernel_root_return_square.py', 'direct_attack/check_kernel_root_return_square.py',
        'direct_attack/KERNEL_ROOT_RETURN_SQUARE.md', 'direct_attack/data/kernel_root_return_square.json')}
    out = dict(scope='arbitrary-tail admissible kernel-return square, complete NEW higher-tail finite inputs',
               theorem_formally_verified=False, runs=runs, source_and_data_sha256=hashes,
               protected_release_and_all_lean_sha256=protected,
               historical_registry_modified=False, full_historical_rerun=False)
    (ROOT/'direct_attack/data/kernel_root_return_square_audit.json').write_text(
        json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(verified=True, scoped_commands=len(runs), protected_files=len(protected),
                          arbitrary_tail_criterion='PROVED paper', general_Cerny='OPEN')))


if __name__ == '__main__':
    main()
