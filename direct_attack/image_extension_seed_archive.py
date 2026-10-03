"""Archive the immutable seed inputs used by the first two adversarial runs."""
import json
from pathlib import Path


def main():
    for n in [8,10]:
        seeds=[]
        for root in sorted(Path('direct_attack/data').glob('image_extension_*')):
            if 'adversarial' in root.name:continue
            for path in sorted(root.glob(f'n{n}_cost*.json')):
                seeds.append(json.loads(path.read_text())['rows'])
        path=Path(f'direct_attack/data/image_extension_adversarial_n{n}/input_seeds.json')
        path.write_text(json.dumps(seeds,separators=(',',':'))+'\n',encoding='utf-8')
        print(json.dumps(dict(n=n,seeds=len(seeds),note='Reconstructed from the unchanged source directories used at dispatch.')))


if __name__=='__main__':main()
