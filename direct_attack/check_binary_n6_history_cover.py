"""Independent orbit coverage + full inverse replay + exact retained-history audit."""
import argparse,json,subprocess,time
from datetime import datetime,timezone
from hashlib import sha256
from itertools import permutations
from pathlib import Path
from direct_attack.check_nearcritical_n6_history import audit_case,canonical_key
from direct_attack.weighted_class_reset_native import ROOT,COMPILER,capture,digest

def orbit_code(f,p):
    renamed=[0]*6
    for q in range(6):renamed[p[q]]=p[f[q]]
    code=0
    for x in renamed:code=6*code+x
    return code

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/binary_n6_history_cover_checks.json'));args=ap.parse_args()
    prefilter=ROOT/'direct_attack/data/research_pressure_121/nearcritical_n6_history.json';old=json.loads(prefilter.read_text(encoding='utf-8'))
    reps=old['first_map_representatives'];assert len(reps)==130 and len({tuple(f) for f in reps})==130
    pp=list(permutations(range(6)));union=set();orbit_controls=0
    for f in reps:
        assert len(f)==6 and all(0<=x<6 for x in f)
        orbit={orbit_code(f,p) for p in pp};assert not union&orbit,'first-map orbits overlap'
        union.update(orbit);orbit_controls+=len(pp)
    assert union==set(range(46656)),'first-map conjugation cover is incomplete'
    cases=json.loads((ROOT/'direct_attack/data/research_pressure_121/nearcritical_n6_history.analysis.json').read_text(encoding='utf-8'))['records']
    assert len(cases)==37;audited={canonical_key(z['rows']):audit_case(z) for z in cases};assert len(audited)==37
    retained=old['records'];assert len(retained)==423;class_controls=0
    for z in retained:
        key=canonical_key(z['rows']);assert key in audited and audited[key]['rt']==z['rt'];class_controls+=1
    source=ROOT/'direct_attack/binary_n6_history_cover_verify.cpp';binary=ROOT/'direct_attack/native_build/binary_n6_history_cover_verify.exe'
    buildfile=ROOT/'direct_attack/data/binary_n6_history_cover_native_build.json'
    if binary.exists() and buildfile.exists():
        build=json.loads(buildfile.read_text());valid=build['source_sha256']==digest(source) and build['binary_sha256']==digest(binary)
    else:valid=False
    if not valid:
        version=capture([COMPILER,'--version']);compiled=capture([COMPILER,'-O3','-std=c++11','-static-libgcc','-static-libstdc++',source,'-o',binary])
        buildfile.write_text(json.dumps(dict(source_sha256=digest(source),binary_sha256=digest(binary),compile=compiled,compiler_version=version),indent=2)+'\n',encoding='utf-8')
    # Explicit marshal of every expected high input; the verifier checks no additional high input exists.
    text='130\n'+'\n'.join(' '.join(map(str,f)) for f in reps)+'\n423\n'
    text+='\n'.join(' '.join(map(str,z['rows'][0]+z['rows'][1]+[z['rt']])) for z in retained)+'\n'
    inputfile=ROOT/'direct_attack/native_build/binary_n6_history_cover_verify.in';inputfile.write_text(text,encoding='utf-8')
    replay=capture([binary,inputfile]);result=json.loads(replay['stdout']);assert result['verified_complete_inverse_replay']
    assert result['covering_pairs']==6065150 and result['high_length_records']==423 and result['maximum_rt']==25
    negative_captures=[]
    prefixes='130\n'+'\n'.join(' '.join(map(str,f)) for f in reps)+'\n423\n'
    for name in ('wrong_retained_length','replaced_high_input','duplicate_high_input','wrong_orbit_count'):
        altered=json.loads(json.dumps(retained))
        if name=='wrong_retained_length':altered[0]['rt']-=1
        elif name=='replaced_high_input':altered[0]['rows'][1]=[0]*6
        elif name=='duplicate_high_input':altered[0]=altered[1]
        badtext=prefixes+'\n'.join(' '.join(map(str,z['rows'][0]+z['rows'][1]+[z['rt']])) for z in altered)+'\n'
        if name=='wrong_orbit_count':badtext='129\n'+badtext.split('\n',1)[1]
        badfile=ROOT/'direct_attack/native_build/binary_n6_history_cover_corruption.in';badfile.write_text(badtext,encoding='utf-8')
        start=datetime.now(timezone.utc).isoformat();clock=time.monotonic();child=subprocess.run([str(binary),str(badfile)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        expected={'wrong_retained_length':{6},'replaced_high_input':{6,7},'duplicate_high_input':{5},'wrong_orbit_count':{3}}[name]
        assert child.returncode in expected,(name,child.returncode,child.stdout)
        negative_captures.append(dict(name=name,argv=[str(binary),str(badfile)],cwd=str(ROOT),start_utc=start,seconds=time.monotonic()-clock,
                                     returncode=child.returncode,stdout=child.stdout,stderr=child.stderr,input_sha256=sha256(badtext.encode()).hexdigest(),expected_rejection=True))
    out=dict(verified=True,first_map_orbits=130,all_labeled_first_maps_covered=len(union),literal_conjugation_controls=orbit_controls,
             retained_isomorphism_classes=37,retained_conjugacy_controls=class_controls,complete_inverse_replay=result,replay_capture=replay,
             checker_sha256=digest(Path(__file__)),native_source_sha256=digest(source),native_binary_sha256=digest(binary),input_sha256=sha256(text.encode()).hexdigest(),
             exact_minor_certificates=sum(len(z['full_rank_branch_certificates']) for z in audited.values()),
             corruptions_rejected=negative_captures,
             boundary='COMPUTATIONALLY VERIFIED: ALL synchronizing6-state DFAs with at most2 letters satisfy L<=(n-1)(d-1) for ANY globally shortest FULL inverse history. Distinct rows: complete first-map conjugation cover and independent inverse replay, plus exact ALL-prefix integer-minor audits of ALL37 high-length classes. Duplicate rows are one-letter DFAs with L<=5; prior paper d<=4 bound and the trivial d>=5 target cover them. For all L<=20, prior paper d<=4 bound plus d>=5 target applies. All423 L>20 records have d6 and L<=25. Covering counts overlap. This is finite/computational, not an arbitrary-alphabet, all-n, or formal proof; general Cerny and universal ALL/SOME cost/rank OPEN.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='replay_capture'}),flush=True)

if __name__=='__main__':main()
