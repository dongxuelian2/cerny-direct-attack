"""New ALL-shortest-history pressure after the fixed-row complete prefilter."""
import json,time
from pathlib import Path
from hashlib import sha256
from direct_attack.data.research_pressure_120.focused_full_history_pressure import analyse

def main():
    start=time.monotonic();data=json.loads(Path('direct_attack/native_build/rooted_cycle_full_history.json').read_text(encoding='utf-8'));scopes=[];counter=None
    for scope in data['scopes']:
        results=[];stream=sha256();counts=dict(retained=len(scope['records']),all_shortest_searches=0,capacity_exclusions=0,dfs_nodes=0)
        for entry in scope['records']:
            answer=analyse(entry['rows'],start+120);assert answer.get('rt')==entry['rt']
            counts['all_shortest_searches']+=answer.get('all_optimal_paths_excluded',False);counts['capacity_exclusions']+=answer.get('capacity_excluded',False);counts['dfs_nodes']+=answer.get('nodes',0)
            result=dict(rows=entry['rows'],analysis=answer);results.append(result);stream.update(json.dumps(result,separators=(',',':')).encode()+b'\n')
            if 'counter' in answer:counter=answer['counter'];break
        scopes.append(dict(n=scope['n'],minimum_rt=scope['minimum_rt'],counts=counts,semantic_sha256=stream.hexdigest(),results=results))
        print(json.dumps(dict(n=scope['n'],counts=counts,counter=counter,seconds=time.monotonic()-start)),flush=True)
        if counter:break
    out=dict(scopes=scopes,counter=counter,seconds=time.monotonic()-start,
             boundary='EXPLORATORY ALL-shortest-history query over the retained fixed-rooted-cycle SC inputs only; native prefilter/search have not been independently audited. Capacity exclusions are already proved consequences, not new negative evidence. General Cerny and universal ALL/SOME full-history cost/rank remain OPEN.')
    Path('direct_attack/native_build/rooted_cycle_full_history.analysis.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
