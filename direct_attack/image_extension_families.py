"""Probe parameter families suggested by the five-state image-extension obstruction."""
import json
from pathlib import Path
from direct_attack.image_extension import profile


def main():
    out=Path('direct_attack/data/image_extension_families');out.mkdir(parents=True,exist_ok=True)
    records=[]
    for n in range(5,16):
        for mode in ['two_pairs','alternating','half_block','long_fiber']:
            a=list(range(n));b=[(q+1)%n for q in range(n)]
            if mode=='two_pairs':a[1]=0;a[3]=2
            elif mode=='alternating':
                for q in range(1,n,2):a[q]=q-1
            elif mode=='half_block':
                for q in range(1,(n+1)//2):a[q]=0
            else:
                for q in range(1,n-1):a[q]=0
            p=profile([a,b])
            if p is None:records.append(dict(n=n,family=mode,synchronizing=False));continue
            p['source']=mode;name=f'n{n}_cost{p["max_cost"]}_{mode}.json'
            (out/name).write_text(json.dumps(p,separators=(',',':'))+'\n',encoding='utf-8')
            w=p['witness'];S=w['start'];T=w['larger_image']
            records.append(dict(n=n,family=mode,max_cost=p['max_cost'],
                                start=[q for q in range(n) if S>>q&1],
                                larger=[q for q in range(n) if T>>q&1],
                                rank=len(set(a)),word=w['word']))
            print(json.dumps({k:v for k,v in records[-1].items() if k!='word'}),flush=True)
    (out/'summary.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
