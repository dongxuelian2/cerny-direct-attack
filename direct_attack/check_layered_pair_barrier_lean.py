"""Compile the abstract certificate with the pinned, already installed Lean kernel."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    from direct_attack.submission_runtime import lean_compiler
    parser.add_argument('--lean', default=str(lean_compiler()))
    parser.add_argument('--out', type=Path, default=ROOT / 'direct_attack/data/layered_pair_barrier_lean_checks.json')
    args = parser.parse_args()
    assert args.lean and Path(args.lean).is_file(), 'installed Lean 4.19.0 is required; this checker does not install it'
    source = ROOT / 'direct_attack/LayeredPairBarrier.lean'
    text = source.read_text(encoding='utf-8')
    code = re.sub(r'/\-.*?\-/', '', text, flags=re.S)
    code = re.sub(r'--[^\n]*', '', code)
    assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|implemented_by|extern)\b', code)
    assert re.findall(r'^import\s+(.+)$', code, flags=re.M) == ['Std']
    version = subprocess.run([args.lean, '--version'], cwd=ROOT, capture_output=True,
                             text=True, encoding='utf-8', check=True, timeout=60)
    assert re.search(r'\bversion 4\.19\.0(?:,|\s)', version.stdout), version.stdout
    argv = [args.lean, str(source)]
    started = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                            encoding='utf-8', timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not result.stderr and 'warning:' not in result.stdout and 'error:' not in result.stdout
    expected = ['Orion.DirectAttack.layered_invariants', 'Orion.DirectAttack.first_collapse_cost']
    ax = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", result.stdout)
    assert [name for name, _ in ax] == expected
    axioms = {name: value.split(', ') if value else [] for name, value in ax}
    assert all(value == ['propext', 'Classical.choice', 'Quot.sound'] for value in axioms.values())
    record = dict(verified=True, status='FORMALLY VERIFIED', compiler_version=version.stdout.strip(),
                  compiler_path=args.lean, compiler_sha256=digest(Path(args.lean)),
                  source='direct_attack/LayeredPairBarrier.lean', source_sha256=digest(source),
                  start_utc=started, seconds=time.monotonic() - tick, argv=argv, cwd=str(ROOT),
                  returncode=result.returncode, stdout=result.stdout, stderr=result.stderr,
                  printed_axioms=axioms, imported_modules=['Std'],
                  boundary='Lean kernel verifies only abstract layered graph-certificate soundness from explicit local entrance hypotheses. The concrete all-p family conditions remain PROVED paper plus finite computational controls; not a formal automaton instantiation, no unrestricted reset bound, priority and general Cerny OPEN.')
    args.out.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: record[key] for key in ('verified', 'status', 'compiler_version', 'source', 'source_sha256', 'printed_axioms', 'boundary')}), flush=True)


if __name__ == '__main__':
    main()
