"""New proper-history query on the retained binary six-state near-criticals."""
import json,time
from pathlib import Path
from collections import Counter
from direct_attack.data.research_pressure_120.focused_full_history_pressure import analyse
from direct_attack.core import canonical

def main():
    start=time.monotonic();source=json.loads(Path('direct_attack/native_build/nearcritical_n6_history.json').read_text(encoding='utf-8'))
    grouped={};lengths=Counter()
    for z in source['records']:
        key=canonical(z['rows']);lengths[z['rt']]+=1
        grouped.setdefault(key,z)
    records=[]
    for key,z in sorted(grouped.items()):
        rs=[list(f) for f in key];answer=analyse(rs,start+180)
        assert answer.get('rt')==z['rt'];records.append(dict(rows=rs,analysis=answer))
        print(json.dumps(dict(rt=z['rt'],analysis=answer)),flush=True)
    out=dict(new_query='ALL shortest full inverse histories of the binary SC n6 near-criticals, excluding d<=5; original reset/greedy cover is not recounted as new evidence',
             covering_records=len(source['records']),covering_histogram=dict(lengths),isomorphism_classes=len(grouped),records=records,seconds=time.monotonic()-start,
             boundary='EXPLORATORY only: both native complete prefilter and this class reduction/search need independent audit. This is a proper-rank query, not an arbitrary-alphabet theorem or a new Cerny census.')
    Path('direct_attack/native_build/nearcritical_n6_history.analysis.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(records=len(records),counters=sum('counter' in z['analysis'] for z in records),seconds=out['seconds'])),flush=True)

if __name__=='__main__':main()
