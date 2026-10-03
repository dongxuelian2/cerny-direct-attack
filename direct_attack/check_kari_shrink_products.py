"""Solver-independent literal base/Bellman/product and Lean audit."""
from copy import deepcopy
from datetime import datetime,timezone
from hashlib import sha256
from math import prod
from pathlib import Path
import json,re,subprocess,time

ROOT=Path(__file__).resolve().parents[1]

def pre(rows,S,i):
    return sum(2**q for q in range(6) if (S//(2**rows[i][q]))%2)

def walk(rows,S,word):
    trace=[S]
    for i in word:
        assert i in (0,1);S=pre(rows,S,i);trace.append(S)
    return trace

def check(data):
    rows=data['rows'];assert rows==[[4,4,2,3,1,5],[1,5,3,4,2,0]] and data['seed']==4
    parameters=list(range(1,17))+[32,63,127,257]
    assert len(data['records'])==20 and [z['d'] for z in data['records']]==parameters
    for start in range(6):
        seen={start};todo=[start]
        for q in todo:
            for f in rows:
                if f[q] not in seen:seen.add(f[q]);todo.append(f[q])
        assert len(seen)==6
    R=set(data['forward_cut']);C=set(data['co_cut']);assert len(R)==35 and len(C)==13 and 63 not in R and 63 in C
    assert all(1<<q in R for q in range(6));edges=0;bridges=[]
    for S in range(64):
        for i in range(2):
            T=pre(rows,S,i);edges+=1
            if T.bit_count()>=S.bit_count():
                if S in R:assert T in R
                if T in C:assert S in C
            elif T in C:bridges.append(dict(S=S,T=T,letter=i))
    assert bridges==data['last_negative_bridges']==[dict(S=45,T=44,letter=0),dict(S=47,T=60,letter=0)]
    assert [b for b in bridges if b['S'] in R]==[dict(S=47,T=60,letter=0)]
    assert min(S.bit_count() for S in C)==3
    bellman=0
    for key,target,mono in [('inverse_full_distances',63,False),('to45_distances',45,False),('monotone_full_distances',63,True)]:
        d=data[key];assert len(d)==64 and d[target]==0
        assert all(v is None or type(v) is int and v>=0 for v in d)
        for S,value in enumerate(d):
            if S==target:continue
            values=[]
            for i in range(2):
                T=pre(rows,S,i)
                if mono and T.bit_count()<S.bit_count():continue
                bellman+=1
                if d[T] is not None:values.append(1+d[T])
            assert value==(min(values) if values else None)
        if mono:assert C=={S for S in range(64) if d[S] is not None}
    assert min(data['inverse_full_distances'][1<<q] for q in range(6))==25
    assert min(data['to45_distances'][1<<q] for q in range(6))==16
    assert data['monotone_full_distances'][44]==10
    rectangle_edges=0
    rect=data['rectangle_d2'];assert set(rect)=={'ordinary','cap2','cap3','cap4','cap3_lex'}
    for key,values in rect.items():
        assert len(values)==4096 and values[4095]==([0,0] if key.endswith('lex') else 0)
        cap=None if key=='ordinary' else 3 if key.endswith('lex') else int(key[-1])
        islex=key.endswith('lex')
        for S,value in enumerate(values):
            assert value is None or (len(value)==2 and all(type(v) is int and v>=0 for v in value) if islex else type(value) is int and value>=0)
            if S==4095:continue
            x,y=S%64,S//64;card=x.bit_count()*y.bit_count();candidates=[]
            for c in range(2):
                for i in range(2):
                    T=pre(rows,x,i)+64*y if c==0 else x+64*pre(rows,y,i)
                    loss=max(0,card-(T%64).bit_count()*(T//64).bit_count());rectangle_edges+=1
                    if cap is not None and loss>cap:continue
                    v=values[T]
                    if v is not None:candidates.append((v[0]+int(loss>0),v[1]+1) if islex else v+1)
            actual=tuple(value) if islex and value is not None else value
            assert actual==(min(candidates) if candidates else None)
    seeds=[2**q+64*2**r for q in range(6) for r in range(6)]
    assert min(rect['ordinary'][S] for S in seeds)==50 and all(rect['cap2'][S] is None for S in seeds)
    assert min(rect['cap3'][S] for S in seeds if rect['cap3'][S] is not None)==52
    assert min(rect['cap4'][S] for S in seeds if rect['cap4'][S] is not None)==50
    assert min(tuple(rect['cap3_lex'][S]) for S in seeds if rect['cap3_lex'][S] is not None)==(3,52)
    seen=set();base_letters=0
    for z in data['mono_suffixes']:
        S=z['S'];assert S in C and S not in seen;seen.add(S)
        trace=walk(rows,S,z['word']);assert trace[-1]==63 and len(z['word'])==data['monotone_full_distances'][S]
        assert all(y.bit_count()>=x.bit_count() for x,y in zip(trace,trace[1:]));base_letters+=6*len(z['word'])
    assert seen==C
    phases=data['phases'];assert set(phases)=={'one_pre','one_post','two_pre','two_post'}
    for kind,end,leadcost,postcost,shrinks in [('one',60,20,5,1),('two',44,17,10,2)]:
        lead,post=phases[kind+'_pre'],phases[kind+'_post'];assert len(lead)==leadcost and len(post)==postcost
        trace=walk(rows,16,lead);assert trace[-1]==end and trace[-2]==(47 if kind=='one' else 45)
        assert sum(y.bit_count()<x.bit_count() for x,y in zip(trace,trace[1:]))==shrinks
        assert all(abs(y.bit_count()-x.bit_count())<=1 for x,y in zip(trace,trace[1:]))
        tail=walk(rows,end,post);assert tail[-1]==63 and all(y.bit_count()>=x.bit_count() for x,y in zip(tail,tail[1:]));base_letters+=6*(len(lead)+len(post))
    lean=(ROOT/'direct_attack/KariShrinkProducts.lean').read_text(encoding='utf-8')
    for key,name in [('inverse_full_distances','fullPotential'),('to45_distances','prefixPotential'),('monotone_full_distances','monoPotential')]:
        values=json.loads(re.search(r'def '+name+r'[^\n]*\n\s*\((\[[^\]]+\])',lean).group(1))
        assert values==[1000 if x is None else x for x in data[key]]
    assert json.loads(re.search(r'def coCut : List Nat := (\[[^\]]+\])',lean).group(1))==data['co_cut']
    for key,name in [('one_pre','onePrefix'),('one_post','oneSuffix'),('two_pre','twoPrefix'),('two_post','twoSuffix')]:
        assert json.loads(re.search(r'def '+name+r' : List \(Fin 2\) := (\[[^\]]+\])',lean).group(1))==phases[key]
    symbolic=literal=0;literal_parameters=[]
    for z in data['records']:
        d=z['d'];n=6**d;assert z['n']==n and z['alphabet']==2*d and z['literal_all_states']==(d<=4)
        schedules={
            'shortest':[[c,'one_pre'] for c in range(d)]+[[c,'one_post'] for c in range(d)],
            'minimax':[[c,'two_pre'] for c in range(d-1)]+[[d-1,'one_pre']]+[[c,'two_post'] for c in range(d-1)]+[[d-1,'one_post']]}
        for mode,blocks in schedules.items():
            assert z[mode+'_blocks']==blocks
            letters=[2*c+i for c,phase in blocks for i in phases[phase]]
            assert sha256(json.dumps(letters,separators=(',',':')).encode()).hexdigest()==z[mode]['inverse_word_sha256']
            factors=[{4} for _ in range(d)];trace=[1];shrinks=maxloss=0
            for letter in letters:
                c,i=divmod(letter,2);assert 0<=c<d
                factors[c]={q for q in range(6) if rows[i][q] in factors[c]};assert factors[c]
                size=prod(len(S) for S in factors);maxloss=max(maxloss,trace[-1]-size);shrinks+=size<trace[-1];trace.append(size);symbolic+=6
            assert all(S==set(range(6)) for S in factors)
            expected=(25*d,d,4**(d-1)) if mode=='shortest' else (27*d-2,2*d-1,3**(d-1))
            assert (len(letters),shrinks,maxloss)==expected
            assert z[mode]['cost']==expected[0] and z[mode]['shrinks']==expected[1] and z[mode]['maxloss']==expected[2] and z[mode]['final_card']==n
            if d<=4:
                places=[6**c for c in range(d)]
                def apply(q,letter):
                    c,i=divmod(letter,2);v=(q//places[c])%6
                    return q+(rows[i][v]-v)*places[c]
                target=sum(4*p for p in places);S={target}
                for j,letter in enumerate(letters):
                    S={q for q in range(n) if apply(q,letter) in S};assert len(S)==trace[j+1];literal+=n
                assert S==set(range(n))
                for q in range(n):
                    for letter in reversed(letters):q=apply(q,letter);literal+=1
                    assert q==target
        if d<=4:literal_parameters.append(d)
    return dict(verified=True,parameters=20,literal_all_state_parameters=literal_parameters,base_cut_edges=edges,
                base_bellman_edges=bellman,base_particle_letters=base_letters,symbolic_particle_letters=symbolic,
                literal_product_particle_letters=literal,last_negative_bridges=bridges,
                rectangle_d2_states=4096,rectangle_d2_bellman_edges=rectangle_edges,
                boundary='Independent all64 base positive-cost Bellman/cut/phase controls and20 parameter schedules; ALL Cartesian states d1..4 literally reset in both directions, larger d only exact rectangle arithmetic. ALL-d minimum-shrink/cost/max-loss tradeoff is PROVED paper from coordinate projections and formally verified literal base facts, not a formal product theorem or computational all-n cover. General Cerny OPEN.')

def compile_lean():
    from direct_attack.submission_runtime import lean_compiler
    compiler=lean_compiler()
    source=ROOT/'direct_attack/KariShrinkProducts.lean';code=source.read_text(encoding='utf-8')
    stripped=re.sub(r'--[^\n]*','',code);assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|implemented_by|extern)\b',stripped)
    assert re.findall(r'^import\s+(.+)$',stripped,flags=re.M)==['Std']
    version=subprocess.run([str(compiler),'--version'],capture_output=True,text=True,encoding='utf-8',check=True,timeout=60)
    assert 'version 4.19.0,' in version.stdout
    argv=[str(compiler),str(source)];started=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
    r=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=60)
    assert r.returncode==0 and not r.stderr and 'warning:' not in r.stdout and 'error:' not in r.stdout,r.stdout+r.stderr
    names=['KariInverseShrink.literal_preimage_correct','KariInverseShrink.reset_needs_shrink']+['KariProductBase.'+x for x in ['reset_length_lower','to45_length_lower','mono44_length_lower','last44_length_lower','last_negative_word','single_negative_word','one_phase_witness','two_phase_witness']]
    axioms={}
    assert len(r.stdout.splitlines())==len(names)
    for name in names:
        m=re.search("'"+re.escape(name)+"' depends on axioms: \\[([^\\]]*)\\]",r.stdout)
        if m:axioms[name]=m[1].split(', ') if m[1] else []
        else:assert "'"+name+"' does not depend on any axioms" in r.stdout;axioms[name]=[]
        assert set(axioms[name])<= {'propext','Quot.sound'}
    return dict(verified=True,status='FORMALLY VERIFIED',compiler_path=str(compiler),compiler_version=version.stdout.strip(),
                compiler_sha256=sha256(compiler.read_bytes()).hexdigest(),source='direct_attack/KariShrinkProducts.lean',source_sha256=sha256(source.read_bytes()).hexdigest(),
                start_utc=started,seconds=time.monotonic()-tick,argv=argv,cwd=str(ROOT),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,printed_axioms=axioms,
                boundary='Lean4.19/Std/decide kernel: literal n6 ALL-word reset length>=25, any last inverse decrease is45->44 or47->60, a sole decrease is47->60, any reset last45->44 has length>=27 via16+1+10, phase witnesses25/27. Arbitrary-d Cartesian lifting is PAPER, not formal. No sorry/admit/native_decide/custom axioms.')

def main():
    data=json.loads((ROOT/'direct_attack/data/kari_shrink_products.json').read_text(encoding='utf-8'));out=check(data);rejected=[]
    for mode in range(10):
        bad=deepcopy(data)
        if mode==0:bad['rows'][0][0]=0
        if mode==1:bad['co_cut'].remove(22)
        if mode==2:bad['last_negative_bridges'][0]['T']=60
        if mode==3:bad['to45_distances'][16]=15
        if mode==4:bad['monotone_full_distances'][44]=9
        if mode==5:bad['phases']['two_pre'].pop()
        if mode==6:bad['records'][0]['minimax']['maxloss']=0
        if mode==7:bad['rectangle_d2']['cap2'][1040]=0
        if mode==8:bad['rectangle_d2']['cap3'][1040]=51
        if mode==9:bad['records'].pop()
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(mode)
        else:raise AssertionError('accepted corruption')
    out['corruptions_rejected']=rejected;formal=compile_lean();out['formal_source_sha256']=formal['source_sha256']
    (ROOT/'direct_attack/data/kari_shrink_products_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    (ROOT/'direct_attack/data/kari_shrink_products_lean_checks.json').write_text(json.dumps(formal,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out),flush=True);print(json.dumps({k:formal[k] for k in ('verified','status','source','printed_axioms','boundary')}),flush=True)

if __name__=='__main__':main()
