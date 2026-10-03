"""Scope-specific word/cut audit with finite negative controls, not a full release rerun."""
from pathlib import Path
import json
import subprocess
import sys
from .audit_order_two_three_a_barrier import digest
from .weighted_class_reset_native import capture
from .check_order_two_weighted_extension import check

ROOT = Path(__file__).resolve().parents[1]


def main():
    git = ['git', '-c', 'safe.directory='+ROOT.as_posix()]
    tracked = subprocess.check_output(git+['ls-files'], cwd=ROOT, text=True, encoding='utf-8').splitlines()
    protected = {p: digest(ROOT/p) for p in tracked
                 if p.startswith('submission/') or p == 'OPENMATH_SUBMISSION.md' or p.endswith('.lean')}
    runs = [capture([sys.executable, '-m', 'direct_attack.order_two_weighted_extension_native', '--M', 6])]
    labels = ['M6_complete', 'M10_complete', 'M12_sample10000', 'M14_sample5000', 'M16_sample2000']
    paths = [ROOT/('direct_attack/data/order_two_weighted_'+label+'.tsv') for label in labels]
    for path in paths:
        runs.append(capture([sys.executable, '-m', 'direct_attack.check_order_two_weighted_extension', path.relative_to(ROOT)]))
    for M in (12, 14, 16):
        runs.append(capture([sys.executable, '-m', 'direct_attack.check_order_two_weighted_pressure',
                             'direct_attack/data/order_two_weighted_pressure_M'+str(M)+'.json']))
    for module in ('weighted_extension_reflection_barrier', 'check_weighted_extension_reflection_barrier'):
        runs.append(capture([sys.executable, '-m', 'direct_attack.'+module]))
    lines = paths[0].read_text().splitlines()
    first_sync = next(i for i, line in enumerate(lines[1:], 1) if line.split()[1] == '1')
    rejected = []
    for mode in range(7):
        changed = lines[:]
        if mode == 0:
            changed.pop()
        elif mode == 1:
            v = list(map(int, changed[1].split()))
            v[0] = 1
            changed[2] = ' '.join(map(str, v))
        else:
            v = list(map(int, changed[first_sync].split()))
            if mode == 2:
                v.pop()
            if mode == 3:
                v[6] = 7
            if mode == 4:
                v[6:8] = [1, 0]
            if mode == 5:
                v = v[:6]
                v[1] = 0
            if mode == 6:
                v[2] = 0
            changed[first_sync] = ' '.join(map(str, v))
        scratch = ROOT/('direct_attack/native_build/weighted_corruption_'+str(mode)+'.tsv')
        scratch.write_text('\n'.join(changed)+'\n', encoding='utf-8')
        scratch.with_suffix('.counter.json').write_text('null\n', encoding='utf-8')
        try:
            check(scratch)
        except (AssertionError, KeyError, TypeError, ValueError, StopIteration):
            rejected.append(mode)
        else:
            raise AssertionError(('accepted corruption', mode))
        finally:
            scratch.unlink()
            scratch.with_suffix('.counter.json').unlink()
    assert protected == {p: digest(ROOT/p) for p in protected}
    generations = [json.loads(path.with_suffix('.capture.json').read_text()) for path in paths]
    for path, record in zip(paths, generations):
        assert record['witness_sha256'] == digest(path)
        assert record['source_sha256'] == digest(ROOT/'direct_attack/order_two_weighted_extension.cpp')
    hashes = {p: digest(ROOT/p) for p in (
        'direct_attack/order_two_weighted_extension.cpp', 'direct_attack/order_two_weighted_pressure.cpp',
        'direct_attack/check_order_two_weighted_extension.py', 'direct_attack/check_order_two_weighted_pressure.py',
        'direct_attack/weighted_extension_reflection_barrier.py', 'direct_attack/check_weighted_extension_reflection_barrier.py',
        'direct_attack/data/weighted_extension_reflection_barrier.json')}
    out = dict(scope='finite weighted extension words and retained pressure minima only; all-n target OPEN',
               runs=runs, native_generation_captures=generations, source_and_data_sha256=hashes,
               corruptions_rejected=rejected, protected_release_and_all_lean_sha256=protected,
               historical_registry_modified=False, full_historical_rerun=False, formally_verified=False)
    (ROOT/'direct_attack/data/order_two_weighted_extension_audit.json').write_text(
        json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(verified=True, scoped_commands=len(runs), rejected_corruptions=rejected,
                          protected_files=len(protected), weighted_order_two='CONJECTURED/OPEN', general_Cerny='OPEN')))


if __name__ == '__main__':
    main()
