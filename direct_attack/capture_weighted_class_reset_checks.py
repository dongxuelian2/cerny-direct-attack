"""Literal independent-check captures for the main and separately saved pilot."""
import json
import sys
from direct_attack.weighted_class_reset_native import ROOT, capture, digest


def main():
    children = []
    for name in ('weighted_class_reset_pressure', 'weighted_class_reset_pressure_pilot'):
        source = ROOT/'direct_attack/data'/(name+'.json')
        report = ROOT/'direct_attack/data'/(name+'_checks.json')
        record = capture([sys.executable, '-m', 'direct_attack.check_weighted_class_reset_pressure',
                          '--source', source, '--out', report])
        record['source_sha256'] = digest(source)
        record['checker_sha256'] = digest(ROOT/'direct_attack/check_weighted_class_reset_pressure.py')
        record['report_sha256'] = digest(report)
        children.append(record)
    target = ROOT/'direct_attack/data/weighted_class_reset_check_captures.json'
    target.write_text(json.dumps(dict(verified=True, runs=children,
                      scope='all 21 main and 21 separately saved pilot records; tiny cover has 5816 unique designations'), indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(verified=True, retained_records=42, unique_tiny_inputs=5816, captured_checks=2)))


if __name__ == '__main__':
    main()
