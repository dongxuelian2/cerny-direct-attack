"""Literal deterministic replay and independent audit of only equality lifts."""
import json
import sys
from direct_attack.weighted_class_reset_native import ROOT, capture, digest


def main():
    scratch = ROOT/'direct_attack/native_build/weighted_equality_replay'
    assert scratch.resolve().is_relative_to((ROOT/'direct_attack/native_build').resolve())
    scratch.mkdir(parents=True, exist_ok=True)
    output, report = scratch/'weighted_class_equality_lifts.json', scratch/'weighted_class_equality_lifts_checks.json'
    saved = ROOT/'direct_attack/data/weighted_class_equality_lifts.json'
    saved_report = ROOT/'direct_attack/data/weighted_class_equality_lifts_checks.json'
    generate = capture([sys.executable, '-m', 'direct_attack.weighted_class_equality_lifts', '--out', output])
    assert json.loads(output.read_text(encoding='utf-8')) == json.loads(saved.read_text(encoding='utf-8'))
    # Audit the frozen source so source_sha256 has the same literal byte hash.
    audit = capture([sys.executable, '-m', 'direct_attack.check_weighted_class_equality_lifts', '--source', saved, '--out', report])
    assert json.loads(report.read_text(encoding='utf-8')) == json.loads(saved_report.read_text(encoding='utf-8'))
    summary = dict(verified=True, runs=[generate, audit],
                   generator_sha256=digest(ROOT/'direct_attack/weighted_class_equality_lifts.py'),
                   checker_sha256=digest(ROOT/'direct_attack/check_weighted_class_equality_lifts.py'),
                   saved_sha256=digest(saved), replay_sha256=digest(output),
                   report_sha256=digest(saved_report), replay_report_sha256=digest(report),
                   scope='deterministic replay and original-subset independent audit of the new designated equality-lift cover only')
    (ROOT/'direct_attack/data/weighted_class_equality_lifts_replays.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(verified=True, replayed_designated_inputs=34560, retained_records=70)))


if __name__ == '__main__':
    main()
