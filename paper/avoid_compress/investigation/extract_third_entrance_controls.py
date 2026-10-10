"""Select only the existing equality witnesses used by the new lemma audit."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def main():
 names=['frontier_certificates.json','boolean_local_prefix_control_n11.json','boolean_local_prefix_control_n8.json']
 candidates=json.loads((ROOT/names[0]).read_text(encoding='utf-8'))['certificates']
 candidates += [json.loads((ROOT/name).read_text(encoding='utf-8'))['witness'] for name in names[1:]]
 selected=[];seen=set()
 for z in candidates:
  key=(z['n'],z['s'],tuple(map(tuple,z['rows'])),tuple(z['S']),tuple(z['A']))
  if z['r']!=1 or z['s']<5 or z['value']!=z['n']-1 or key in seen:continue
  seen.add(key);selected.append(z)
 assert len(selected)==17
 result=dict(status='selected_existing_controls',witnesses=selected,
  historical_source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
  scope='Existing equality controls only; not a new extremum or exhaustive automaton cover.')
 (ROOT/'third_entrance_control_witnesses.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(controls=len(selected))))

if __name__=='__main__':main()
