"""Regenerate all literal rows and independently replay the bounded probe."""
from pathlib import Path
from itertools import combinations,permutations
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent
def partitions(n,maximum):
    if not n:yield [];return
    for first in range(min(n,maximum),0,-1):
        for rest in partitions(n-first,first):yield [first,*rest]
def main():
    saved=json.loads((ROOT/'codimension_four_cycle5_probe.json').read_text())
    assert saved['status']=='complete_bounded_11_cycle_partitions' and saved['total_row_pairs']==1164240
    expected_parts=list(partitions(6,6));assert len(expected_parts)==11
    assert [r['partition'] for r in saved['reports']]==expected_parts
    build=ROOT.parent/'_qa'/'active7_independent';build.mkdir(parents=True,exist_ok=True)
    raw=build/'rank6_rows.txt';digest=hashlib.sha256();seen=set();tested=0
    with raw.open('wb') as output:
        for omit in range(7):
            for x,y in combinations(range(7),2):
                for target in permutations([q for q in range(7) if q!=omit]):
                    # Independently build the partition into six source blocks.
                    blocks=[[6+q] for q in range(7) if q!=y];blocks[x].append(6+y)
                    row=list(range(13))
                    for block,t in zip(blocks,target):
                        for q in block:row[q]=6+t
                    key=tuple(row);assert key not in seen;seen.add(key);tested+=1
                    data=(' '.join(map(str,row))+'\n').encode();digest.update(data);output.write(data)
    assert tested==len(seen)==105840
    for report in saved['reports']:assert report['raw_rows_sha256']==digest.hexdigest()
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    if compiler is None:raise RuntimeError('C++17 compiler required; set CXX')
    flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic'];executables=[]
    for name in ('probe_codimension_four_cycle5','check_codimension_four_active7'):
        exe=build/(name+('.exe' if os.name=='nt' else ''))
        run=subprocess.run([compiler,*flags,str(ROOT/(name+'.cpp')),'-o',str(exe)],capture_output=True,text=True)
        assert run.returncode==0 and not run.stderr,(run.stdout,run.stderr);executables.append(exe)
    records=[];rebuilt=[]
    for old in saved['reports']:
        part=','.join(map(str,old['partition']));primary_raw=build/'primary_rows.txt'
        first=subprocess.run([str(executables[0]),str(primary_raw),part],capture_output=True,text=True)
        assert first.returncode==0 and not first.stderr,(first.stdout,first.stderr)
        actual=[json.loads(line) for line in first.stdout.splitlines()];assert actual==old['outputs']
        assert hashlib.sha256(primary_raw.read_bytes()).hexdigest()==digest.hexdigest()
        rebuilt.append(dict(partition=old['partition'],outputs=actual,raw_rows_sha256=digest.hexdigest()))
        second=subprocess.run([str(executables[1]),str(raw),part],capture_output=True,text=True)
        assert second.returncode==0 and not second.stderr,(second.stdout,second.stderr)
        audit=json.loads(second.stdout);original=actual[-1]
        assert original['status']=='complete_bounded_probe' and audit['status']=='complete_independent'
        for key in ('tested','strong','synchronizing','compression_admitted_rows'):assert original[key]==audit[key],key
        assert not original['found_value12'] and original['compression_admitted_rows']==0
        assert original['local_initial_tests']==original['reachable_admitted_rows']==0 and audit['algorithm_controls']==5
        records.append(dict(partition=old['partition'],primary=original,independent=audit))
    regenerated=dict(status='complete_bounded_11_cycle_partitions',reports=rebuilt,total_row_pairs=1164240,
        scope='n13, binary; b a seven-cycle through0..6 and arbitrary permutation-cycle partition of7..12; a fixes0..5 and has rank6 on6..12. No unrestricted-table upper bound.')
    assert regenerated==saved
    (ROOT/'codimension_four_cycle5_probe.json').write_bytes((json.dumps(regenerated,indent=2)+'\n').encode())
    names=[Path(__file__).name,'probe_codimension_four_cycle5.cpp','check_codimension_four_active7.cpp',
        'codimension_four_cycle5_probe.json','ACTIVE_SEVEN_CYCLE_PROBE.md']
    result=dict(status='pass',parameter=[13,9,1],complete_bounded_cycle_partitions=11,
        literal_rows_per_partition=105840,complete_bounded_row_pairs=1164240,records=records,
        canonical_raw_rows_sha256=digest.hexdigest(),no_nine_subset_compression12_in_domain=True,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Two complete independent algorithms agree on a restricted active-seven/rank-six a and seven-cycle-plus-arbitrary-permutation b domain. No global F bound or binary/unrestricted separation.')
    (ROOT/'codimension_four_cycle5_probe_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(dict(status='pass',cycle_partitions=11,row_pairs=1164240,independent_compression_admission=0)))
if __name__=='__main__':main()
