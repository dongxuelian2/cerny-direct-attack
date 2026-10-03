"""Authenticate complete M12 graph/reset check and new larger sampled scopes."""
from pathlib import Path
import subprocess
import sys
import json
from .weighted_class_reset_native import capture,digest

ROOT=Path(__file__).resolve().parents[1]


def main():
    protected=json.loads((ROOT/'direct_attack/data/order_two_weighted_graph_audit.json').read_text())['protected_release_and_lean_sha256']
    assert protected=={p:digest(ROOT/p) for p in protected}
    full=ROOT/'direct_attack/data/order_two_weighted_graph_M12_complete.tsv'
    completed=json.loads(full.with_suffix('.check.json').read_text())
    assert completed['returncode']==0 and completed['data_sha256']==digest(full)
    assert completed['source_sha256']==digest(ROOT/'direct_attack/check_order_two_weighted_graph_native.cpp')
    claims=json.loads(completed['stdout']);assert claims['complete_scope'] and claims['inputs_checked']==3628800 and claims['sync']==3624960
    checker=ROOT/'direct_attack/native_build/check_order_two_weighted_graph_native.exe'
    assert completed['binary_sha256']==digest(checker)
    labels=['M8_complete']+['M'+str(M)+'_sample100000' for M in (16,20,24,32,48,64,96,128)]
    runs=[]
    for label in labels:
        runs.append(capture([sys.executable,'-m','direct_attack.check_order_two_weighted_graph_native',
            'direct_attack/data/order_two_weighted_graph_'+label+'.tsv']))
    for M in (18,20):
        runs.append(capture([sys.executable,'-m','direct_attack.check_order_two_weighted_pressure',
            'direct_attack/data/order_two_weighted_pressure_M'+str(M)+'.json']))
    small=(ROOT/'direct_attack/data/order_two_weighted_graph_M8_complete.tsv').read_text().splitlines()
    negative=[]
    for mode in range(8):
        lines=small[:]
        if mode==0:lines.pop(1)
        elif mode==1:lines[2]=lines[1]
        elif mode in (6,7):
            v=list(map(int,small[1].split()));v[0]=0
            lines=['8 1',' '.join(map(str,v)), 'not_an_integer' if mode==6 else '7']
        else:
            v=list(map(int,lines[1].split()))
            if mode==2:v[1]=4
            if mode==3:v[2]=0
            if mode==4:v.pop()
            if mode==5:v[9],v[10]=v[10],v[9]
            lines[1]=' '.join(map(str,v))
        scratch=ROOT/('direct_attack/native_build/graph_corruption_'+str(mode)+'.tsv')
        scratch.write_text('\n'.join(lines)+'\n',encoding='utf-8')
        result=subprocess.run([str(checker),str(scratch)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        scratch.unlink();assert result.returncode!=0,('accepted corruption',mode)
        negative.append(dict(mode=mode,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr))
    generations=[]
    for label in ['M12_complete']+labels:
        data=ROOT/('direct_attack/data/order_two_weighted_graph_'+label+'.tsv')
        record=json.loads(data.with_suffix('.capture.json').read_text())
        assert record['residual_tsv_sha256']==digest(data) and record['source_sha256']==digest(ROOT/'direct_attack/order_two_weighted_graph_pressure.cpp')
        generations.append(record)
    larger=[]
    for M in (18,20):
        data=ROOT/('direct_attack/data/order_two_weighted_pressure_M'+str(M)+'.json')
        record=json.loads(data.with_name(data.stem+'_capture.json').read_text())
        assert record['output_sha256']==digest(data)
        assert record['original_source_sha256']==digest(ROOT/'direct_attack/order_two_weighted_pressure.cpp')
        assert record['generated_source_sha256']==digest(ROOT/'direct_attack/native_build/order_two_weighted_large_pressure.cpp')
        larger.append(record)
    assert protected=={p:digest(ROOT/p) for p in protected}
    out=dict(scope='COMPLETE M12 criteria and ALL chronological resets; larger retained cases only, proposal counts exploratory',
             authenticated_complete_M12_checker=completed,runs=runs,negative_controls=negative,
             graph_generation_captures=generations,larger_weighted_pressure_captures=larger,
             protected_release_and_lean_sha256=protected,formally_verified=False,full_historical_rerun=False,
             historical_registry_modified=False,general_Cerny='OPEN',automatic_graph_connectivity='CONJECTURED/OPEN')
    (ROOT/'direct_attack/data/order_two_weighted_graph_native_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(verified=True,complete_M12=claims,scoped_commands=len(runs),corruptions_rejected=len(negative),protected_files=len(protected))))


if __name__=='__main__':main()
