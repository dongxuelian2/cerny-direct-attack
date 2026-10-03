"""Preserve the 75-check run and capture the documented four-check continuation.

The unchanged 75 checks are not rerun. The extended return checker is
refreshed, then four newly registered checks are appended with literal
child captures. Reinvocation after success only reseals hashes.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from direct_attack.reproduce import ROOT, reproduction_commands, seal_manifest


def main():
    data = ROOT/'direct_attack/data'
    audit_path = data/'audit_run.json'
    provenance = data/'return_lift_provenance'
    original_path = provenance/'completed_75_audit_run.json'
    continuation_path = provenance/'audit_continuation.json'
    current = json.loads(audit_path.read_text(encoding='utf-8'))
    if original_path.exists() and len(current['runs']) == 79:
        assert current['all_passed'] and all(r['returncode'] == 0 for r in current['runs'])
        print(json.dumps(dict(already_complete=True, checks=79, **seal_manifest())))
        return
    assert len(current['runs']) == 75 and current['all_passed']
    assert all(r['returncode'] == 0 for r in current['runs'])
    original_bytes = audit_path.read_bytes()
    provenance.mkdir(exist_ok=True)
    if original_path.exists():
        assert original_path.read_bytes() == original_bytes
    else:
        original_path.write_bytes(original_bytes)
    captures = []

    def capture(argv):
        started = datetime.now(timezone.utc).isoformat()
        t = time.monotonic()
        run = subprocess.run([sys.executable]+argv, cwd=ROOT, capture_output=True,
                             text=True, encoding='utf-8', errors='replace')
        record = dict(argv=[sys.executable]+argv, cwd=str(ROOT), start_utc=started,
                      seconds=time.monotonic()-t, returncode=run.returncode,
                      stdout=run.stdout, stderr=run.stderr)
        captures.append(record)
        print(json.dumps(dict(module=argv[1], returncode=run.returncode,
                              seconds=record['seconds'])), flush=True)
        if run.returncode:
            continuation_path.write_text(json.dumps(dict(completed=False,runs=captures),indent=2)+'\n',encoding='utf-8')
            raise SystemExit(run.returncode)
        return record

    refreshed = capture(['-m','direct_attack.check_return_word_lift'])
    indices = [i for i,r in enumerate(current['runs'])
               if r['argv'][1:] == ['-m','direct_attack.check_return_word_lift']]
    assert len(indices) == 1
    current['runs'][indices[0]] = refreshed
    appended = [['-m','direct_attack.check_class_compression_pressure'],
                ['-m','direct_attack.check_mixed_rank_extension','--root',
                 'direct_attack/data/mixed_rank_extension_n16'],
                ['-m','direct_attack.check_mixed_rank_extension','--root',
                 'direct_attack/data/mixed_rank_extension_n24_fixed'],
                ['-m','direct_attack.replay_return_and_mixed']]
    for argv in appended:
        current['runs'].append(capture(argv))
    tree = ast.parse((ROOT/'direct_attack/reproduce.py').read_text(encoding='utf-8'))
    entry = next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name == 'main')
    registered = next(node.value for node in entry.body if isinstance(node,ast.Assign)
                      and any(isinstance(t,ast.Name) and t.id == 'checks' for t in node.targets)
                      and isinstance(node.value,ast.List))
    assert len(registered.elts) == len(current['runs']) == 79
    commands = reproduction_commands()
    assert len(commands) == 173
    (data/'reproduction_commands.json').write_text(json.dumps(commands,indent=2)+'\n',encoding='utf-8')
    boundary = ('Completed 75-check default run, one extended return-checker refresh, '
                'and four new checks appended. This is not a second full 79-check run.')
    continuation = dict(completed=True, original_checks=75, final_registered_checks=79,
                        base_audit=str(original_path.relative_to(ROOT)).replace('\\','/'),
                        base_audit_sha256=hashlib.sha256(original_bytes).hexdigest(),
                        refreshed_modules=['direct_attack.check_return_word_lift'],
                        appended_checks=len(appended), runs=captures, boundary=boundary)
    continuation_path.write_text(json.dumps(continuation,indent=2)+'\n',encoding='utf-8')
    current['continuation'] = dict(provenance=str(continuation_path.relative_to(ROOT)).replace('\\','/'),
                                   boundary=boundary, original_checks=75, appended_checks=4,
                                   refreshed_checks=1)
    current['all_passed'] = all(r['returncode'] == 0 for r in current['runs'])
    assert current['all_passed']
    audit_path.write_text(json.dumps(current,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(checks=len(current['runs']), regeneration_commands=len(commands),
                          all_passed=True, **seal_manifest())), flush=True)


if __name__ == '__main__':
    main()
