"""Independent finite cut/Bellman audit plus pinned Lean kernel compilation."""
from copy import deepcopy
from hashlib import sha256
import json,re,shutil,subprocess,time
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def step(rows,S,i):
    T=0
    for q in range(6):
        if (S//(2**rows[i][q]))%2:T+=2**q
    return T

def history(rows,q,w):
    S=1<<q;out=[S]
    for i in reversed(w):assert i in (0,1);S=step(rows,S,i);out.append(S)
    return out

def check(data):
    rows=data['rows'];assert rows==[[4,4,2,3,1,5],[1,5,3,4,2,0]]
    old=[[0,1,2,4,3,3],[1,3,5,0,2,4]];relabel=[5,4,0,1,3,2]
    assert all(relabel[rows[i][q]]==old[i][relabel[q]] for i in range(2) for q in range(6))
    R=set(data['cut']);assert len(R)==35 and sorted(R)==data['cut'] and 63 not in R
    assert all(1<<q in R for q in range(6));edges=allowed=letters=0
    for S in R:
        assert 0<S<64
        for i in range(2):
            T=step(rows,S,i);edges+=1
            if T.bit_count()>=S.bit_count():assert T in R;allowed+=1
    seen=set()
    for z in data['reach_witnesses']:
        assert z['S'] in R and z['S'] not in seen and 0<=z['q']<6;seen.add(z['S'])
        trace=history(rows,z['q'],z['word']);assert trace[-1]==z['S']
        assert all(y.bit_count()>=x.bit_count() for x,y in zip(trace,trace[1:]));letters+=6*len(z['word'])
    assert seen==R
    d=data['lex_distances'];assert len(d)==64 and d[63]==[0,0];lexedges=0
    for S,value in enumerate(d):
        assert value is None or len(value)==2 and all(type(x) is int and x>=0 for x in value)
        if S==63:continue
        values=[]
        for i in range(2):
            T=step(rows,S,i);lexedges+=1
            if d[T] is not None:values.append((d[T][0]+int(T.bit_count()<S.bit_count()),d[T][1]+1))
        assert (tuple(value) if value is not None else None)==(min(values) if values else None)
    assert all(d[1<<q][0]==1 for q in range(6)) and d[16]==[1,25]
    q=data['target'];w=data['word'];assert q==4 and len(w)==25;trace=history(rows,q,w)
    assert trace[-1]==63 and sum(y.bit_count()<x.bit_count() for x,y in zip(trace,trace[1:]))==1
    assert all(y.bit_count()-x.bit_count() in (-1,0,1) for x,y in zip(trace,trace[1:]));letters+=6*len(w)
    ordinary=data['original_distances'];assert len(ordinary)==64;ordinaryedges=0
    for S,value in enumerate(ordinary):
        assert type(value) is int and value>=0
        if S.bit_count()<=1:assert value==0;continue
        values=[]
        for f in rows:
            T=0
            for r in range(6):
                if S>>r&1:T|=1<<f[r]
            ordinaryedges+=1;values.append(1+ordinary[T])
        assert value==min(values)
    assert ordinary[-1]==25
    for start in range(6):
        p=start
        for i in w:p=rows[i][p]
        assert p==q
    lean=(ROOT/'direct_attack/KariInverseShrink.lean').read_text(encoding='utf-8')
    cut=re.search(r'def cut : List Nat :=\s*(\[[^\]]+\])',lean).group(1)
    witness=re.search(r'def inverseWitness : List \(Fin 2\) :=\s*(\[[^\]]+\])',lean).group(1)
    assert json.loads(cut)==data['cut'] and json.loads(witness)==list(reversed(w))
    return dict(verified=True,closed_cut_states=len(R),cut_edges=edges,nondecreasing_cut_edges=allowed,
                max_monotone_inverse_size=max(S.bit_count() for S in R),lex_bellman_edges=lexedges,
                original_bellman_edges=ordinaryedges,literal_particle_letter_controls=letters,
                singleton_lex=[d[1<<q] for q in range(6)],optimal_cost=25,minimum_shrink_count=1,
                inverse_cardinalities=[S.bit_count() for S in trace],
                boundary='Independent exact finite original Kari rows: closed all-singleton cut forbids monotone inverse resets at ANY length; reach witnesses certify exact35 reachable masks. ALL64 lexicographic shrink/length and original-cost Bellman controls, one-shrink optimal cost25 reset. Separate Lean all-word cut plus literal witness are formally verified; ordinary threshold lower bound remains computational, not formal. General Cerny OPEN.')

def compile_lean():
    from direct_attack.submission_runtime import lean_compiler
    lean=str(lean_compiler())
    source=ROOT/'direct_attack/KariInverseShrink.lean';code=source.read_text(encoding='utf-8')
    code=re.sub(r'--[^\n]*','',code);assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|implemented_by|extern)\b',code)
    assert re.findall(r'^import\s+(.+)$',code,flags=re.M)==['Std']
    version=subprocess.run([lean,'--version'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',check=True,timeout=60)
    assert re.search(r'\bversion 4\.19\.0(?:,|\s)',version.stdout)
    argv=[lean,str(source)];started=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
    result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=60)
    assert result.returncode==0 and not result.stderr and 'warning:' not in result.stdout and 'error:' not in result.stdout,result.stdout+result.stderr
    expected=['no_monotone_inverse_reset','literal_preimage_correct','reset_needs_shrink','witness_resets','witness_one_shrink','witness_cost'];printed={}
    for name in expected:
        full='KariInverseShrink.'+name
        match=re.search("'"+re.escape(full)+"' depends on axioms: \\[([^\\]]*)\\]",result.stdout)
        if match:printed[full]=match.group(1).split(', ') if match.group(1) else []
        else:assert "'"+full+"' does not depend on any axioms" in result.stdout;printed[full]=[]
        assert set(printed[full])<= {'propext','Quot.sound'}
    return dict(verified=True,status='FORMALLY VERIFIED',compiler_version=version.stdout.strip(),compiler_path=lean,
                compiler_sha256=sha256(Path(lean).read_bytes()).hexdigest(),source='direct_attack/KariInverseShrink.lean',
                source_sha256=sha256(source.read_bytes()).hexdigest(),start_utc=started,seconds=time.monotonic()-tick,
                argv=argv,cwd=str(ROOT),returncode=result.returncode,stdout=result.stdout,stderr=result.stderr,printed_axioms=printed,
                boundary='Lean4.19 kernel, Std only, decide (not native_decide), no sorry/admit or custom axioms. Verifies the literal n6 preimage-mask cut for ALL word lengths and cost25/one-shrink witness. It does not formally verify the optimal-cost lower bound, any arbitrary-n class proof or general Cerny.')

def main():
    data=json.loads((ROOT/'direct_attack/data/kari_inverse_shrink.json').read_text());out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data)
        if mode==0:bad['rows'][0][0]=0
        if mode==1:bad['cut'].append(63)
        if mode==2:bad['cut'].remove(3)
        if mode==3:bad['reach_witnesses'][0]['q']=1
        if mode==4:bad['lex_distances'][16]=[0,25]
        if mode==5:bad['word'].pop()
        if mode==6:bad['original_distances'][-1]=24
        if mode==7:bad['reach_witnesses'].pop()
        try:check(bad)
        except (AssertionError,KeyError,ValueError,TypeError):rejected.append(mode)
        else:raise AssertionError('accepted corruption')
    out['corruptions_rejected']=rejected;formal=compile_lean()
    (ROOT/'direct_attack/data/kari_inverse_shrink_lean_checks.json').write_text(json.dumps(formal,indent=2)+'\n',encoding='utf-8')
    out['formal_source_sha256']=formal['source_sha256']
    (ROOT/'direct_attack/data/kari_inverse_shrink_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True);print(json.dumps({k:formal[k] for k in ('verified','status','source','printed_axioms','boundary')}),flush=True)

if __name__=='__main__':main()
