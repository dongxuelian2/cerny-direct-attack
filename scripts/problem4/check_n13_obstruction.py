"""Independent saved-report and ordinary-BFS audit of the n=13 obstruction.

The negative mathematical step requires the complete C++ runs. This script
compares their full mathematical counts and checks all three lower witnesses.
"""
import hashlib
import json
from pathlib import Path
from verify_certificates import ac,apply,strong

ROOT=Path(__file__).resolve().parent


def main():
    names=('inverse_zero_n13.json','inverse_zero_n13_fibers.json')
    reports=[json.loads((ROOT/name).read_text()) for name in names]
    fields=('n','s','target','completed','compression_witness_found','first_classes',
            'visited_classes','assignments','discarded','leaves','candidate_strong_sync',
            'rows','S','orbit_export_mode')
    assert all(reports[0][key]==reports[1][key] for key in fields)
    for z in reports:
        assert (z['n'],z['s'],z['target'])==(13,10,10)
        assert z['completed'] and not z['compression_witness_found']
        assert z['first_classes']==z['visited_classes']==431
        assert z['assignments']==19839983511 and z['discarded']==185849863
        assert z['leaves']==6761103983 and z['candidate_strong_sync']==0
        assert not z['orbit_export_mode'] and z['rows']==[[],[]] and z['S']==[]
    data=json.loads((ROOT/'frontier_certificates.json').read_text())
    lowers=[]
    for r in (1,2,3):
        z=next(z for z in data['certificates'] if (z['n'],z['s'],z['r'])==(13,10,r))
        rows=z['rows'];S=set(z['S']);A=set(z['A'])
        assert len(rows)==2 and len(S)==10 and len(A)==r and A<S
        assert strong(rows) and apply(range(13),z['reaching'],rows)==S
        assert len(apply(range(13),z['reset'],rows))==1
        assert ac(rows,S,A)==z['value']==len(z['attaining'])==9
        attaining=apply(S,z['attaining'],rows)
        assert len(attaining)<10 or not A<=attaining
        assert z['binary_upper']==9 and z['unrestricted_upper']==10
        assert z['exact_binary'] and not z['exact_unrestricted']
        lowers.append(dict(n=13,s=10,r=r,value=9))
    width=json.loads((ROOT/'extended_width_audit.json').read_text())
    numeric=json.loads((ROOT/'inverse_fibers_audit.json').read_text())
    assert width['verified'] and width['cases']==1000 and 13 in width['checked_n']
    assert numeric['status']=='pass' and numeric['random_cases']==1000
    assert numeric['sizes']==[5,8,12,13,16] and numeric['positive_control_compression']==10
    for name,digest in numeric['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    result=dict(verified=True,parameter_triples=lowers,exact_binary_value=9,
                unrestricted_interval=[9,10],first_forms=431,
                assignments=19839983511,prunes=185849863,complete_maps=6761103983,
                eligible_maps=0,implementations=2,all_mathematical_counts_match=True,
                numeric_random_cases=1000,numeric_positive_control_compression=10,
                scope='Computer-assisted binary upper with complete original C++ runs; this checker does not rerun the full negative covers.')
    (ROOT/'n13_obstruction_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
