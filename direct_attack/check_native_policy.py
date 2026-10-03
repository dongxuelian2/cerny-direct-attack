"""Cross-check the native integer scorer against stored independent certificates."""
import json
from pathlib import Path
from direct_attack.native_policy import profile


def main():
    records=[]
    paths=[p for root in sorted(Path('direct_attack/data').glob('image_extension_policy*'))
           for p in sorted(root.glob('witness_*.json'))]
    transport=Path('direct_attack/data/singleton_transport/witness.json')
    if transport.exists():paths.append(transport)
    for path in paths:
        saved=json.loads(path.read_text());actual=profile(saved['rows'],details=True)
        assert actual is not None
        for key in ['n','best_policy','worst_policy','rt']:assert actual[key]==saved[key],(path,key)
        for key in ['extension','best','worst']:
            assert actual[key]=={int(s):v for s,v in saved[key].items()},(path,key)
        records.append(dict(file=str(path),n=saved['n'],verified=True))
    out=dict(checked=len(records),records=records)
    Path('direct_attack/data/native_policy_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(checked=len(records),verified=True)))


if __name__=='__main__':main()
