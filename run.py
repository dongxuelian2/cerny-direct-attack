"""Small research launcher. All generated files live under build/."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / 'build'
SOURCES = ('.py', '.cpp', '.hpp', '.h', '.in')


def compiler():
    name = os.environ.get('CXX', 'g++')
    path = shutil.which(name)
    if not path:
        raise RuntimeError('Install a C++17 compiler or set CXX to its executable.')
    return path


def compile_cpp(source):
    source = Path(source).resolve()
    if not source.is_relative_to(ROOT):
        raise ValueError('The C++ source must be inside this repository.')
    out = BUILD / 'bin' / source.relative_to(ROOT).with_suffix('')
    out.parent.mkdir(parents=True, exist_ok=True)
    includes = set()
    def dependencies(path):
        for name in re.findall(r'^\s*#include\s+"([^"]+)"', path.read_text(), re.M):
            dependency = (path.parent/name).resolve()
            if dependency not in includes:
                includes.add(dependency)
                dependencies(dependency)
    dependencies(source)
    if not out.exists() or any(p.stat().st_mtime > out.stat().st_mtime for p in [source, *includes, Path(__file__)]):
        subprocess.run([compiler(), '-std=c++17', '-O3', '-pthread', str(source), '-o', str(out)], check=True)
    return out


def workspace(task):
    dest = BUILD / 'work' / task
    if dest.exists() and task != 'manual':
        shutil.rmtree(dest)
    elif dest.exists():
        # Keep producer outputs, while removing Python modules deleted from source.
        for old in dest.rglob('*.py'):
            if not (ROOT/old.relative_to(dest)).is_file():
                old.unlink()
    for folder in ('scripts',):
        for source in (ROOT / folder).rglob('*'):
            if source.is_file() and source.suffix in SOURCES:
                target = dest / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
    (dest / 'scripts/direct_attack/data').mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env['PYTHONPATH'] = os.pathsep.join([str(dest), str(dest/'scripts'), str(dest/'scripts/problem4'), str(dest/'scripts/anchors')])
    env['CXX'] = compiler()
    return dest, env


def invoke(argv, cwd, env=None, **kwargs):
    tick = time.perf_counter()
    subprocess.run(list(map(str, argv)), cwd=cwd, env=env, check=True, **kwargs)
    print(f'Completed in {time.perf_counter()-tick:.3f}s', flush=True)


def cerny(n):
    if not 2 <= n <= 24:
        raise ValueError('The dense subset search supports 2 <= n <= 24.')
    return [[(q+1) % n for q in range(n)], list(range(n-1))+[0]]


def reset(args):
    rows = cerny(args.cerny)
    record = f'reset {args.cerny} 2 ' + ' '.join(str(q) for row in rows for q in row) + '\n'
    exe = compile_cpp(ROOT/'scripts/native/subset_search.cpp')
    tick = time.perf_counter()
    result = subprocess.run([str(exe)], input=record, text=True, capture_output=True, check=True)
    values = list(map(int, result.stdout.split()))
    word = ''.join('ab'[i] for i in values[2:])
    print(f'C{args.cerny}: shortest reset length {values[0]}, visited {values[1]} subsets')
    print('word:', word)
    print(f'Search time: {time.perf_counter()-tick:.3f}s (including process startup)')


def open_point(args):
    work, env = workspace('open-point')
    sys.path.insert(0, str(work/'scripts/problem4'))
    from two_block_family import construct
    z = construct(6, 3, 1)
    def mask(values): return sum(1 << q for q in values)
    record = f'avoid {z["n"]} 2 {mask(z["S"])} {mask(z["A"])} ' + ' '.join(str(q) for row in z['rows'] for q in row) + '\n'
    result = subprocess.run([str(compile_cpp(ROOT/'scripts/native/subset_search.cpp'))], input=record, text=True, capture_output=True, check=True)
    length, visited, *letters = map(int, result.stdout.split())
    word = ''.join('ab'[a] for a in letters)
    # Independently apply the construction's reaching/reset words and the C++ witness.
    from verify_certificates import apply, strong
    assert strong(z['rows']) and apply(range(13), z['reaching'], z['rows']) == set(z['S'])
    assert len(apply(range(13), z['reset'], z['rows'])) == 1
    end = apply(z['S'], word, z['rows'])
    assert length == 11 and (len(end) < 9 or not set(z['A']) <= end)
    print(f'(13,9,1): binary construction attains {length}; visited {visited} subsets; word={word}')
    print('This verifies the lower bound 11. The matching computational upper bound is in PROOF.md#problem4-full-fiber-flag.')


def c7(args):
    work, env = workspace('c7')
    project = work/'scripts/problem4/upper_bound'
    profiles = compile_cpp(ROOT/'scripts/problem4/upper_bound/problem4_c7_profiles.cpp')
    distances = compile_cpp(ROOT/'scripts/problem4/upper_bound/problem4_c7_distances.cpp')
    def generate(name, flags):
        with (project/name).open('wb') as out:
            subprocess.run([str(profiles), *flags], stdout=out, check=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(generate, 'c7-partition.txt', []), pool.submit(generate, 'c7-literal.txt', ['--literal'])]
        for future in futures: future.result()
    if (project/'c7-partition.txt').read_bytes() != (project/'c7-literal.txt').read_bytes():
        raise RuntimeError('The independent action generators disagree.')
    with (project/'c7-literal.txt').open('rb') as source:
        invoke([distances, '--threads', args.threads], project, env, stdin=source)
    if args.independent:
        invoke([sys.executable, '-B', 'problem4_c7_audit.py', 'c7-literal.txt'], project, env)


def families(args):
    work, env = workspace('families')
    project = work/'scripts/problem4'
    for name in ('generator.py', 'checker.py', 'check_cofinal.py', 'check_boundary.py',
                 'check_defect_two.py', 'check_codimension_three.py', 'two_block_family.py', 'check_two_block.py'):
        invoke([sys.executable, '-B', name], project, env)


def tau4(args):
    work, env = workspace('tau4')
    source = ROOT/'scripts/problem4'
    classify = compile_cpp(source/'upper_bound/problem4_tau4_core.cpp')
    primary = compile_cpp(source/'upper_bound/problem4_core_distances.cpp')
    independent = compile_cpp(source/'upper_bound/problem4_core_profiles_check.cpp')
    invoke([classify, '--threads', args.threads], work, env)
    # Fresh in-memory comparisons: no stored inventories or report files.
    def compare(core):
        commands = ([str(exe), '--profiles', str(core)] for exe in (primary, independent))
        a, b = (subprocess.check_output(cmd, cwd=work, env=env) for cmd in commands)
        if a != b:
            raise RuntimeError(f'Core {core}: independent action/arrow generators disagree.')
        return core, len(a.splitlines())
    with ThreadPoolExecutor(max_workers=min(args.threads, 9)) as pool:
        for core, signatures in pool.map(compare, range(9)):
            print(f'Core {core}: all {signatures} signatures and arrow unions agree', flush=True)
    invoke([primary, '--threads', args.threads, '--pair-cap', getattr(args, 'pair_cap', 6)], work, env)


def upper(args):
    work, env = workspace('upper')
    project = work/'scripts/problem4'
    invoke([sys.executable, '-B', 'check_codimension_three_upper.py', '--rerun', '--compiler', compiler(),
            '--build-dir', BUILD/'bin/codimension-three'], project, env)


def script(args):
    source = (ROOT / args.source).resolve()
    if not source.is_relative_to(ROOT/'scripts') or not source.is_file():
        raise ValueError('Select an existing scripts/*.py or scripts/*.cpp source.')
    work, env = workspace('manual')
    target = work / source.relative_to(ROOT)
    if source.suffix == '.py':
        if source.is_relative_to(ROOT/'scripts/direct_attack'):
            module = '.'.join(source.relative_to(ROOT/'scripts').with_suffix('').parts)
            invoke([sys.executable, '-B', '-m', module, *args.arguments], work, env)
        else:
            invoke([sys.executable, '-B', target.name, *args.arguments], target.parent, env)
    elif source.suffix == '.cpp':
        invoke([compile_cpp(source), *args.arguments], target.parent, env)
    else:
        raise ValueError('The selected file must be Python or C++.')



def eleven(args):
    """Reconstruct the complete fixed-parameter proof from source."""
    open_point(args)
    work, env = workspace('eleven')
    upper_sources = ROOT/'scripts/problem4/upper_bound'
    upper_copy = work/'scripts/problem4/upper_bound'
    invoke([sys.executable, '-B', work/'scripts/problem4/check_eleven_lower.py'], work, env)
    for name in ('problem4_peeling_controls.py', 'problem4_p3_shapes.py'):
        invoke([sys.executable, '-B', upper_copy/name], upper_copy, env)
    tau4(args)
    flags = compile_cpp(upper_sources/'full_fiber_flags.cpp')
    for options in ([], ['--tau3']):
        invoke([flags, '--all-entrances', '--quotient', '--threads', args.threads, *options],
               upper_copy, env)
    print('Complete (13,9,1) lower witness and all-entrance upper domains passed.', flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('reset', help='Exact C++ reset search on a Cerny automaton')
    q.add_argument('--cerny', type=int, default=10); q.set_defaults(action=reset)
    q = sub.add_parser('open-point', help='Reconstruct the (13,9,1) lower witness, then recompute its value')
    q.set_defaults(action=open_point)
    q = sub.add_parser('eleven', help='Recompute the complete (13,9,1) mathematical reduction and finite rejection')
    q.add_argument('--threads', type=int, default=min(16, os.cpu_count() or 1))
    q.set_defaults(action=eleven)
    q = sub.add_parser('c7', help='Generate both action domains and run the multi-threaded C7 exclusion')
    q.add_argument('--threads', type=int, default=min(16, os.cpu_count() or 1))
    q.add_argument('--independent', action='store_true', help='Also run the small independent Python check')
    q.set_defaults(action=c7)
    q = sub.add_parser('tau4', help='Reconstruct the nine cover-four cores and check a short-pair layer')
    q.add_argument('--threads', type=int, default=min(16, os.cpu_count() or 1))
    q.add_argument('--pair-cap', type=int, choices=range(6, 10), default=6)
    q.set_defaults(action=tau4)
    q = sub.add_parser('families', help='Generate and check the finite lower-construction scopes')
    q.set_defaults(action=families)
    q = sub.add_parser('upper', help='Rebuild all components of the codimension-three computer-assisted proof')
    q.set_defaults(action=upper)
    q = sub.add_parser('script', help='Run another research source in the generated workspace')
    q.add_argument('source'); q.add_argument('arguments', nargs=argparse.REMAINDER); q.set_defaults(action=script)
    args = p.parse_args()
    if getattr(args, 'threads', 1) < 1 or getattr(args, 'threads', 1) > 64:
        p.error('--threads must be 1..64')
    if args.command == 'eleven' and args.threads > 32:
        p.error('eleven --threads must be 1..32')
    try: args.action(args)
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as e:
        p.exit(1, str(e)+'\n')


if __name__ == '__main__':
    main()
