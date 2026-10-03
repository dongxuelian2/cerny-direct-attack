"""Replay only the new weighted streams and capture their exact child argv."""
import json
from direct_attack.weighted_class_reset_native import ROOT, capture, digest, ensure_build


def main():
    binary = ensure_build()
    scratch = ROOT/'direct_attack/native_build/weighted_replay'
    assert scratch.resolve().is_relative_to((ROOT/'direct_attack/native_build').resolve())
    scratch.mkdir(parents=True, exist_ok=True)
    children = []
    for mode, trials, seed, name in [
            ('search', 1000000, 20261021, 'weighted_class_reset_pressure'),
            ('tiny', 250000, 20261021, 'weighted_class_reset_tiny')]:
        output = scratch/(name+'.json')
        record = capture([binary, '--trials', trials, '--seed', seed,
                          '--mode', mode, '--out', output])
        saved = ROOT/'direct_attack/data'/(name+'.json')
        assert json.loads(output.read_text(encoding='utf-8')) == json.loads(saved.read_text(encoding='utf-8'))
        record['replayed_source'] = str(saved.relative_to(ROOT))
        record['saved_sha256'] = digest(saved)
        record['replay_sha256'] = digest(output)
        children.append(record)
    report = dict(verified=True, streams=len(children), source_sha256=digest(ROOT/'direct_attack/weighted_class_reset_pressure.cpp'),
                  binary_sha256=digest(binary), runs=children,
                  scope='exact deterministic replay of the new weighted million-proposal stream and tiny labeled cover; no historical stream rerun')
    (ROOT/'direct_attack/data/weighted_class_reset_replays.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(verified=True, streams=2, sampled_proposals=1000000, tiny_complete_inputs=5816)))


if __name__ == '__main__':
    main()
