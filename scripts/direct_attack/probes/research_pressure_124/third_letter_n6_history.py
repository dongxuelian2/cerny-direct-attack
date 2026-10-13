"""Fresh arbitrary third-letter history attack; native cover remains exploratory."""
import json,time
from pathlib import Path
from hashlib import sha256
from direct_attack.probes.research_pressure_120.focused_full_history_pressure import analyse

def main():
    start=time.monotonic();data=json.loads(Path('scripts/direct_attack/native_build/third_letter_n6_history.json').read_text(encoding='utf-8'));records=[];counter=None;seen=set();duplicates=0;stream=sha256();nodes=0
    for z in data['records']:
        key=tuple(sorted(tuple(f) for f in z['rows']))
        if key in seen:duplicates+=1;continue
        seen.add(key);answer=analyse(z['rows'],start+180);assert answer.get('rt')==z['rt']
        record=dict(base=z['base'],rows=z['rows'],analysis=answer);records.append(record);nodes+=answer.get('nodes',0);stream.update(json.dumps(record,separators=(',',':')).encode()+b'\n')
        if 'counter' in answer:counter=answer['counter'];break
    out=dict(designated_retained=len(data['records']),distinct_retained_labeled_alphabets=len(records),duplicate_labeled_alphabets=duplicates,
             all_shortest_searches=sum(z['analysis'].get('all_optimal_paths_excluded',False) for z in records),capacity_exclusions=sum(z['analysis'].get('capacity_excluded',False) for z in records),
             dfs_nodes=nodes,records=records,counter=counter,semantic_sha256=stream.hexdigest(),seconds=time.monotonic()-start,
             boundary='EXPLORATORY only; ALL third-letter additions to fixed37 bases, not all ternary or arbitrary alphabets, not independently audited. Exact field rank applies at n6; general Cerny and ALL/SOME history cost/rank OPEN.')
    Path('scripts/direct_attack/native_build/third_letter_n6_history.analysis.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__=='__main__':main()
