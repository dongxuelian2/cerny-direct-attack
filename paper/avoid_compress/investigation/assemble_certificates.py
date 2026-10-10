"""Assemble fully audited small witnesses without altering the manuscript."""
from pathlib import Path
import json
from audit_small import bfs, strong
from verify_certificates import verify

ROOT=Path(__file__).resolve().parent

def main():
    pool=[]
    for z in json.loads((ROOT/'small_case_audit.json').read_text())['certificates']:
        pool.append(dict(z,value=z['ac'],source='exhaustive binary cover, n<=7'))
    extension=json.loads((ROOT/'extension_audit.json').read_text())
    for z in extension['structured_certificates']+extension['active_certificates']:
        v=z['verification'];pool.append(dict(z,reaching=v['reaching'],reset=v['reset'],attaining=v['attaining']))
    for file in sorted(ROOT.glob('reuse_n*.json')):
        for z in json.loads(file.read_text())['results']:pool.append(dict(z,source=file.name))
    for name in ('cofinal_audit.json','boundary_audit.json','defect_two_audit.json','defect_one_audit.json'):
        for z in json.loads((ROOT/name).read_text())['records']:
            pool.append(dict(z,value=z.get('ac',z.get('value')),source=name,
                             reaching=z.get('reaching',z.get('reaching_word')),
                             attaining=z.get('attaining',z.get('attaining_word')),
                             reset=z.get('reset',z.get('reset_word'))))
    for name in ('subdivide_probe.json',):
        if (ROOT/name).exists():pool.extend(json.loads((ROOT/name).read_text())['certificates'])
    for file in ROOT.glob('boolean_*.json'):
        report=json.loads(file.read_text())
        if report.get('status')=='witness_verified':
            pool.append(dict(report['witness'],n=report['n'],s=report['s'],r=report['r'],source=file.name))
    best={}
    for z in pool:
        key=z['n'],z['s'],z['r']
        if key not in best or z['value']>best[key]['value']:best[key]=z
    records=[]
    for n in range(2,11):
        for s in range(2,n+1):
            for r in range(1,s):
                z=best[n,s,r]
                assert z['value']==min(n-r,(n-s+2)*(n-s+1)//2)
                records.append({key:z[key] for key in ['n','s','r','value','rows','S','A','reaching','attaining','reset','source']})
    report=dict(status='The all-parameter conjecture remains unproved and unrefuted.',
                exhaustive_automaton_scope='binary, strongly connected and synchronizing, n=2..7',
                constructive_certification_scope='all triples n=2..10, with actual reachable images',
                certificates=records)
    path=ROOT/'formula_certificates.json';path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    verify(path)
    intervals=[]
    for (n,s,r),z in sorted(best.items()):
        if n>=10 and z['value']<min(n-r,(n-s+2)*(n-s+1)//2):
            intervals.append(dict(n=n,s=s,r=r,verified_lower=z['value'],known_upper=min(n-r,(n-s+2)*(n-s+1)//2)))
    (ROOT/'unresolved_intervals.json').write_text(json.dumps(dict(scope='Only bounds supplied by these finite probes; not exact maxima.',intervals=intervals),indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
