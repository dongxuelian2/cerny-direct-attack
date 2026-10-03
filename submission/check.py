"""Submission checks; standard library only, no new searches or downloads.

Reports and scratch copies go to ignored results/openmath/.
The direct suite runs the existing 146-check audit without --full.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, cwd, env, log):
    start = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic()
    result = subprocess.run(list(map(str, argv)), cwd=cwd, env=env,
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
    log.append(dict(argv=list(map(str, argv)), cwd=str(cwd), start_utc=start,
                    seconds=time.monotonic()-tick, returncode=result.returncode,
                    stdout=result.stdout, stderr=result.stderr))
    print(('PASS ' if result.returncode == 0 else 'FAIL ') + str(argv), flush=True)
    if result.returncode:
        print(result.stdout + result.stderr, flush=True)
        raise RuntimeError('Check failed; see report for exact output')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=['direct', 'formal', 'baseline', 'post', 'native', 'integrity', 'all'], default='all')
    parser.add_argument('--lean', help='Installed Lean 4.19.0 executable')
    parser.add_argument('--cxx', help='g++ executable for native replay checks')
    args = parser.parse_args()
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    count = int(env.get('GIT_CONFIG_COUNT', '0'))
    env['GIT_CONFIG_KEY_' + str(count)] = 'safe.directory'
    env['GIT_CONFIG_VALUE_' + str(count)] = ROOT.as_posix()
    env['GIT_CONFIG_COUNT'] = str(count + 1)
    if args.lean:
        env['ORION_LEAN'] = str(Path(args.lean).resolve())
    if args.cxx:
        compiler = Path(args.cxx).resolve()
        assert compiler.is_file()
        env['CXX'] = str(compiler)
        env['PATH'] = str(compiler.parent) + os.pathsep + env.get('PATH', '')
    output = ROOT / 'results/openmath'
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    report = dict(suite=args.suite, python=sys.version, platform=platform.platform(), runs=rows, all_passed=False)
    try:
        if args.suite in ('direct', 'all'):
            scratch = Path(tempfile.mkdtemp(prefix='direct-', dir=output))
            paths = subprocess.check_output(['git', 'ls-files', '-z', '-c', '-o', '--exclude-standard'],
                                            cwd=ROOT, env=env).decode('utf-8').split('\0')
            inputs = {}
            for rel in filter(None, paths):
                source = ROOT / rel
                if source.is_file():
                    target = scratch / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, target)
                    inputs[rel] = digest(source)
            report['scratch'] = str(scratch)
            report['input_sha256'] = inputs
            with (output/'direct-progress.log').open('w', encoding='utf-8') as progress:
                start = datetime.now(timezone.utc).isoformat()
                tick = time.monotonic()
                result = subprocess.run([sys.executable, '-m', 'direct_attack.reproduce'],
                                        cwd=scratch, env=env, stdout=progress, stderr=subprocess.STDOUT)
            rows.append(dict(argv=[sys.executable, '-m', 'direct_attack.reproduce'], cwd=str(scratch),
                             start_utc=start, seconds=time.monotonic()-tick, returncode=result.returncode,
                             stdout=(output/'direct-progress.log').read_text(encoding='utf-8'), stderr=''))
            capture = scratch / 'direct_attack/data/audit_run.json'
            if capture.is_file():
                report['direct_audit'] = json.loads(capture.read_text(encoding='utf-8'))
            assert result.returncode == 0, 'Direct audit failed; see results/openmath/direct-progress.log'
            assert report['direct_audit']['all_passed'] and len(report['direct_audit']['runs']) == 146
            # Documentation may be edited during the audit; its mathematical input
            # identity is recorded above, while proof/data hashes are checked below.
            scientific = {p:h for p,h in inputs.items() if p.startswith('direct_attack/') and p.endswith(('.py','.cpp','.lean','.json'))}
            report['scientific_inputs_unchanged'] = all(digest(ROOT/p) == h for p,h in scientific.items())
            assert report['scientific_inputs_unchanged'], 'Scientific inputs changed during replay'
        if args.suite in ('formal', 'baseline', 'post', 'native', 'integrity', 'all'):
            from audit import check_suite
            check_suite(args.suite, args.lean, env, rows, output, run)
        report['all_passed'] = True
    finally:
        path = output / (args.suite + '.json')
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
        print('Report: ' + str(path), flush=True)


if __name__ == '__main__':
    main()
