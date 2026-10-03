"""Separate integer recurrence, literal words, support flows and parameter audit."""
from copy import deepcopy
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json,re,subprocess,time

ROOT=Path(__file__).resolve().parents[1]

def action(F,w):
    assert isinstance(w,list) and all(type(i) is int and i in (0,1) for i in w)
    states=list(range(len(F[0])))
    for i in w:states=[F[i][q] for q in states]
    return states

def integer_cut(layers):
    assert len(layers)==9 and layers[0]==[[]];controls=0
    for k in range(8):
        current={tuple(H) for H in layers[k]};new=set();assert len(current)==len(layers[k])
        for H in current:
            assert list(H)==sorted(set(H)) and all(-k<=h<=k for h in H)
            assert not(0 in H and 1 in H)
            A=tuple(sorted({1}|{1-h for h in H if h!=0 and h!=1}));B=tuple(h+1 for h in H)
            new|={A,B};controls+=2
        assert new=={tuple(H) for H in layers[k+1]} and len(new)==len(layers[k+1])
    assert all(-8<=h<=8 for H in layers[8] for h in H)
    return controls

def check(data):
    integer_edges=integer_cut(data['abstract_hole_layers']);parameters=list(range(3,81))+[127,256,512,1024,2048]
    assert [z['M'] for z in data['records']]==parameters
    particles=small_words=stationary_words=0
    for z in data['records']:
        M=z['M'];F=z['rows'];a,b=F;assert a==[M,M]+[M+1-q for q in range(2,M)]+[0] and b==list(range(1,M))+[0,M]
        c=action(F,[0,0]);assert c==[0,0]+list(range(2,M+1))
        R=action(F,[0,1,0,1]);assert R==[1,1,M]+list(range(3,M+1))
        f=action(F,[0,1,0,1,1]);assert f==[2,2,M]+list(range(4,M))+[0,M] if M>=4 else f==[2,2,M,M]
        word=z['reset_word'];assert word==[0,1,0,1,1]*(M-2)+[0,1,0,1] and len(word)==5*M-6
        assert action(F,word)==[M]*(M+1)
        heights=[]
        for q in range(M+1):
            seen=set();p=q;h=0
            while p!=M:assert p not in seen;seen.add(p);p=f[p];h+=1
            heights.append(h)
        assert max(heights)==M-1
        v=z['three_a_word'];assert v==[0]+[1]*(M-2)+[0]+[1]*(M-1)+[0] and v.count(0)==3 and len(v)==2*M
        states=action(F,v);assert set(states)==set(range(M))-{1}
        coeff=z['three_a_support_coefficients'];assert coeff==[0]+[2]+[1]*(M-2)
        da=[a.count(q)-1 for q in range(M+1)];row=[da[q]+states.count(q)-1 for q in range(M+1)]
        for j,w in enumerate(coeff):row[j]+=w;row[(j+1)%M]-=w
        assert row==[0]*(M+1) and max([len(v)]+[j+2 for j,w in enumerate(coeff) if w])==2*M
        stationary_words+=2+sum(w>0 for w in coeff)
        if M>=5:
            v=z['short_avoid_word'];assert v==[0,1,0,0,1,0,1,1,0] and len(v)==9 and v.count(0)==5
            states=action(F,v);assert set(states)==set(range(M))-{1,M-2}
            coeff=z['short_support_coefficients'];assert coeff==[0]+[3 if j==M-2 else 2 for j in range(1,M)]
            row=[da[q]+states.count(q)-1 for q in range(M+1)]
            for j,w in enumerate(coeff):row[j]+=w;row[(j+1)%M]-=w
            assert row==[0]*(M+1) and max([9]+[j+2 for j,w in enumerate(coeff) if w])==max(9,M+1)<2*M
            stationary_words+=2+sum(w>0 for w in coeff)
        else:assert z['short_avoid_word'] is None and z['short_support_coefficients'] is None
        if 5<=M<=16:
            layer=[list(range(M+1))]
            for length in range(9):
                assert all(M in S for S in layer);small_words+=len(layer)
                if length<8:layer=[[F[i][q] for q in S] for S in layer for i in (0,1)]
        particles+=(M+1)*(len(word)+len(z['three_a_word'])+(9 if M>=5 else 0)+11)
    assert small_words==12*511
    source=(ROOT/'direct_attack/ReflectionCoreCut.lean').read_text(encoding='utf-8')
    assert json.loads(re.search(r'^def layers : .* := (\[.*\])$',source,re.M).group(1))==data['abstract_hole_layers']
    return dict(verified=True,inputs=len(parameters),maximum_n=2049,abstract_integer_hole_edges=integer_edges,
                complete_small_words=small_words,literal_particle_controls=particles,stationary_word_flow_controls=stationary_words,
                status='PROVED paper parameter transfer from exact integer depth8 cut and complete small-word cover: root avoidance9 for all M>=5, three-a avoidance and optimal-singular-count stationary cost2M, cheaper unrestricted stationary cost<=max(9,n), paid original reset5M-6 for all M>=3. Finite literal/flow controls COMPUTATIONALLY VERIFIED; full all-n theorem not FORMALLY VERIFIED. General Cerny OPEN, no priority claim.')

def compile_lean():
    from direct_attack.submission_runtime import lean_compiler
    compiler=lean_compiler();source=ROOT/'direct_attack/ReflectionCoreCut.lean'
    code=re.sub(r'--[^\n]*','',source.read_text(encoding='utf-8'))
    assert re.findall(r'^import\s+(.+)$',code,re.M)==['Std']
    assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|implemented_by|extern)\b',code)
    version=subprocess.run([str(compiler),'--version'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=60,check=True)
    assert re.search(r'\bversion 4\.19\.0(?:,|\s)',version.stdout)
    argv=[str(compiler),str(source)];start=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
    result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=60)
    assert result.returncode==0 and not result.stderr and 'warning:' not in result.stdout and 'error:' not in result.stdout,result.stdout+result.stderr
    axioms={}
    for name in ['cut_closed','run_in_layers','no_avoid_first_eight','witness_prefix_holes','witness_final_unsafe']:
        full='ReflectionCoreCut.'+name;match=re.search("'"+re.escape(full)+"' depends on axioms: \\[([^\\]]*)\\]",result.stdout)
        if match:axioms[full]=match.group(1).split(', ') if match.group(1) else []
        else:assert "'"+full+"' does not depend on any axioms" in result.stdout;axioms[full]=[]
        assert set(axioms[full])<={'propext','Quot.sound'}
    return dict(verified=True,status='FORMALLY VERIFIED',compiler_version=version.stdout.strip(),compiler_path=str(compiler),
                compiler_sha256=sha256(compiler.read_bytes()).hexdigest(),source='direct_attack/ReflectionCoreCut.lean',source_sha256=sha256(source.read_bytes()).hexdigest(),
                argv=argv,cwd=str(ROOT),start_utc=start,seconds=time.monotonic()-tick,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr,printed_axioms=axioms,
                boundary='Lean4.19 Std/kernel decide, no native_decide/custom axioms/sorry/admit. Abstract integer-hole recurrence closed cut and induction quantify over ALL words of length<=8; ninth-letter abstract witness is unsafe. Parameter transfer to literal arbitrary-M automata, small-M enumeration, avoidance metric comparison and linear reset theorem are NOT formally verified by this source; they have separate paper/finite checks. General Cerny OPEN.')

def main():
    data=json.loads((ROOT/'direct_attack/data/reflection_core_tradeoff.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(8):
        bad=deepcopy(data)
        if mode==0:bad['abstract_hole_layers'][0]=[[1]]
        if mode==1:bad['abstract_hole_layers'][4].pop()
        if mode==2:bad['records'][2]['short_avoid_word'].pop()
        if mode==3:bad['records'][2]['three_a_word'].pop()
        if mode==4:bad['records'][2]['reset_word'].pop()
        if mode==5:bad['records'][2]['three_a_support_coefficients'][1]=1
        if mode==6:bad['records'][2]['short_support_coefficients'][1]=0
        if mode==7:bad['records'][2]['rows'][0][2]=2
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    out['corruptions_rejected']=rejected
    formal=compile_lean();out['lean_status']=formal['status'];out['formal_boundary']=formal['boundary']
    (ROOT/'direct_attack/data/reflection_core_tradeoff_lean_checks.json').write_text(json.dumps(formal,indent=2)+'\n',encoding='utf-8')
    (ROOT/'direct_attack/data/reflection_core_tradeoff_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
