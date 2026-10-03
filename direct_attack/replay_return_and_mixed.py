"""Replay the new deterministic streams and preserve literal child captures."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    base = Path('direct_attack/native_build').resolve()
    base.mkdir(exist_ok=True)
    reports = []
    specs = [('return', Path('direct_attack/data/return_word_lift_search.json')),
             ('profile', Path('direct_attack/data/class_compression_pressure.json'))]
    specs += [('mixed', p) for p in (Path('direct_attack/data/mixed_rank_extension_n16'),
                                     Path('direct_attack/data/mixed_rank_extension_n24_fixed'))]
    for kind, source in specs:
        frozen = json.loads((source if kind != 'mixed' else source/'summary.json').read_text(encoding='utf-8'))
        arguments = frozen['arguments']
        with tempfile.TemporaryDirectory(prefix='return_mixed_replay_',dir=base) as folder:
            temporary = Path(folder).resolve()
            assert temporary.parent == base
            module = {'return':'return_word_lift', 'profile':'class_compression_pressure',
                      'mixed':'mixed_rank_extension_attack'}[kind]
            output = temporary/'replayed.json' if kind != 'mixed' else temporary
            argv = [sys.executable,'-m','direct_attack.'+module]
            for key,value in arguments.items():
                if value is not None:
                    argv += ['--'+key.replace('_','-'),str(value)]
            argv += ['--out',str(output)]
            run = subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',errors='replace')
            assert run.returncode == 0,run.stderr
            replayed = json.loads((output if kind != 'mixed' else output/'summary.json').read_text(encoding='utf-8'))
            for key in ('counts','records'):
                assert replayed[key] == frozen[key], (source,key)
            if kind == 'mixed':
                assert replayed['best'] == frozen['best']
                assert json.loads((output/'input_seeds.json').read_text()) == json.loads((source/'input_seeds.json').read_text())
                for name in frozen['records']:
                    assert json.loads((output/name).read_text()) == json.loads((source/name).read_text()), name
            else:
                assert replayed == frozen
            reports.append(dict(source=str(source).replace('\\','/'),argv=argv,
                                returncode=run.returncode,stdout=run.stdout,stderr=run.stderr,
                                verified=True,records=len(frozen['records'])))
    result = dict(verified=True,streams=reports,
                  boundary='Deterministic generation replay; independent mathematical array checks are separate.')
    Path('direct_attack/data/return_mixed_replay_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,streams=len(reports),
                          retained=sum(x['records'] for x in reports))))


if __name__ == '__main__':
    main()
