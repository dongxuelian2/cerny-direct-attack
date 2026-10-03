"""Replay three NEW streams; retain exact literal child captures.

Historical searches are not rerun. Replay outputs remain under ignored
native_build/fiber_replay; no recursive deletion is performed.
"""
import json
from pathlib import Path
import sys
from direct_attack.class_reset_native import ROOT, capture, ensure_build


def main():
    binary = ensure_build()
    scratch = ROOT/'direct_attack/native_build/fiber_replay'
    assert scratch.resolve().is_relative_to((ROOT/'direct_attack/native_build').resolve())
    scratch.mkdir(parents=True, exist_ok=True)
    records = []
    out = scratch/'bijective_fiber_returns.json'
    record = capture([sys.executable,'-m','direct_attack.bijective_fiber_returns',
                      '--trials','3000','--seed','20261015','--out',out])
    assert json.loads(out.read_text()) == json.loads((ROOT/'direct_attack/data/bijective_fiber_returns.json').read_text())
    record['replayed_source'] = 'direct_attack/data/bijective_fiber_returns.json'
    records.append(record)
    for trials, seed, limit, mode, name in [
        (120000,20261016,30000,'small','class_reset_pressure'),
        (1000000,20261017,150000,'large','class_reset_pressure_large')]:
        out = scratch/(name+'.json')
        record = capture([binary,'--trials',trials,'--seed',seed,'--limit',limit,
                          '--profile-mode',mode,'--out',out])
        assert json.loads(out.read_text()) == json.loads((ROOT/'direct_attack/data'/out.name).read_text())
        record['replayed_source'] = 'direct_attack/data/'+out.name
        record['note'] = 'explicit small/large protocol reconstructs the source shape list; not a claim that the original argv contained --profile-mode'
        records.append(record)
    report = dict(verified=True, streams=len(records), native_proposals=1120000,
                  bijective_alphabets=3000, runs=records,
                  scope='literal deterministic replays of the three new streams only; no universal claim')
    (ROOT/'direct_attack/data/fiber_continuation_replays.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True, streams=3, native_proposals=1120000,bijective_alphabets=3000)))


if __name__ == '__main__':
    main()
