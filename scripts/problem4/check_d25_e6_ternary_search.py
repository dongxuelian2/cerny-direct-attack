"""Independent literal checks of seeded ternary search decisions and positives."""
from pathlib import Path
from itertools import combinations,combinations_with_replacement
from collections import deque
import hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent
Q=set(range(13));B={0};C={1,4};D={2,5};E={6};CORE={0,3,6};K={1,2}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_text())
def im(S,row):return frozenset(row[q] for q in S)
def points(mask):return frozenset(q for q in Q if mask>>q&1)
def strong(rows):
    for q in Q:
        seen={q};todo=[q]
        for t in todo:
            for row in rows:
                if row[t] not in seen:seen.add(row[t]);todo.append(row[t])
        if seen!=Q:return False
    return True

def distances(rows):
    pairs=list(combinations(range(13),2));back={p:[] for p in pairs};todo=deque();dist={}
    for p in pairs:
        for row in rows:
            target=tuple(sorted({row[t] for t in p}))
            if len(target)==1:
                if p not in dist:dist[p]=1;todo.append(p)
            else:back[target].append(p)
    while todo:
        p=todo.popleft()
        for prev in back[p]:
            if prev not in dist:dist[prev]=dist[p]+1;todo.append(prev)
    return dist

def bfs(rows,start,kind,target=None):
    start=frozenset(start);todo=deque([start]);seen={start:''}
    while todo:
        S=todo.popleft();w=seen[S]
        good=(S==target if kind=='reach' else len(S)==1 if kind=='reset' else len(S)<9 or 3 not in S)
        if good:return w
        for i,row in enumerate(rows):
            T=im(S,row)
            if T not in seen:seen[T]=w+chr(97+i);todo.append(T)
    return None

def decision(rows,S):
    if not strong(rows):return 'not_strongly_connected'
    d=distances(rows)
    protected=min((v for p,v in d.items() if set(p)&CORE and v<=7),default=999)
    uncovered=min((v for p,v in d.items() if not set(p)&K and v<=5),default=999)
    if protected<=uncovered and protected<999:return 'protected_P7_depth'+str(protected)
    if uncovered<999:return 'uncovered_P5_depth'+str(uncovered)
    if len(d)!=78:return 'not_synchronizing'
    ac=bfs(rows,S,'ac');assert ac is not None and len(ac)<=12
    if len(ac)<12:return 'short_ac_'+str(len(ac))
    reaching=bfs(rows,Q,'reach',S)
    if reaching is None:return 'not_reachable_initial_image'
    assert bfs(rows,Q,'reset') is not None
    return 'verified_attaining_candidate'

def main():
    audit=read('d15_d25_fourth_rows_audit.json')
    assert audit['status']=='pass'
    for n,h in audit['source_sha256'].items():assert sha(ROOT/n)==h,n
    pool=ROOT/'experimental'/'d15_d25_fourth_audit'/'kept_forward.txt'
    assert pool.exists() and sha(pool)==audit['canonical_kept_rows_sha256']
    parent=read('b1_c14_nonsingleton_fourth_inventory.json')
    z=next(z for z in parent['records'] if z['D']==[2,5] and z['E']==[6])
    row_audit=next(x for x in audit['complete_pair_scans'] if x['D']==[2,5] and x['E']==[6])
    assert row_audit['kept_rows']==936000
    pool_record=next(r for r in read('d15_d25_fourth_rows_inventory.json')['records'] if r['D']==[2,5] and r['E']==[6])
    assert set(range(len(z['rows'])))==set(pool_record['active_original_fields'])
    flags=read('d25_e6_ternary_supply.json')['field_flags']
    expected=[sum(1<<j for j,(k,v) in enumerate((('preA',[0]),('preB',[1,4]),('preC',[2,5]),('preD',[6]))) if f[k]==v) for f in z['rows']]
    assert flags==expected and sorted(flags)==list(range(16))
    forms={frozenset(S) for S in combinations(range(13),9) if 3 in S and all(len(set(S)&X)==1 for X in (B,C,D,E))}
    assert len(forms)==60
    tuples=[t for t in combinations_with_replacement(range(16),3) if flags[t[0]]|flags[t[1]]|flags[t[2]]==15]
    compiler=os.environ.get('CXX') or shutil.which('clang++') or shutil.which('g++')
    assert compiler,'C++17 compiler required; set CXX'
    dest=ROOT/'experimental'/'d25_e6_ternary_search';dest.mkdir(exist_ok=True)
    exe=dest/('search.exe' if os.name=='nt' else 'search')
    compile_flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic']
    c=subprocess.run([compiler,*compile_flags,str(ROOT/'search_d25_e6_ternary.cpp'),'-o',str(exe)],capture_output=True,text=True)
    assert c.returncode==0 and not c.stderr,(c.stdout,c.stderr)
    seed=20261010
    run=subprocess.run([str(exe),str(pool),str(seed)],capture_output=True,text=True)
    assert run.returncode==0 and not run.stderr,(run.stdout,run.stderr)
    (dest/'output.jsonl').write_text(run.stdout)
    records=[json.loads(line) for line in run.stdout.splitlines()]
    summary=records[-1];assert summary['type']=='summary' and summary['seed']==seed
    assert summary['field_triples']==len(tuples) and summary['attempts']==len(tuples)*60*20
    assert sum(summary['decisions'].values())==summary['attempts']
    samples=[r for r in records if r['type']=='sample'];candidates=[r for r in records if r['type']=='candidate']
    assert len(samples)==summary['sampled_decisions'] and len(candidates)==summary['candidate_count']
    for i,r in enumerate(samples):
        rows=r['rows'];S=points(r['S_mask']);assert len({tuple(row) for row in rows})==3 and S in forms
        assert tuple(r['fields']) in tuples
        for row,field in zip(rows,r['fields']):
            f=z['rows'][field]
            assert len(row)==13 and all(q in Q for q in row)
            for key,target in (('preA',{3}),('preB',B),('preC',C),('preD',D)):
                assert {q for q in Q if row[q] in target}==set(f[key])
            assert len({row[q] for q in Q-K})==11
            T=S
            for h in range(1,12):
                T=im(T,row);assert len(T)==9 and 3 in T
                if h<=7:assert T in forms
        assert decision(rows,S)==r['decision'],r
        if i%50==0:print('Checked sampled decisions '+str(i+1),flush=True)
    for r in candidates:
        rows=r['rows'];S=points(r['S_mask'])
        assert decision(rows,S)=='verified_attaining_candidate'
        assert len(bfs(rows,S,'ac'))==r['value']==12
        for start,word,expected_kind in ((Q,r['reaching'],'reach'),(Q,r['reset'],'reset'),(S,r['attaining'],'ac')):
            T=frozenset(start)
            for c in word:T=im(T,rows[ord(c)-97])
            assert (T==S if expected_kind=='reach' else len(T)==1 if expected_kind=='reset' else len(T)<9 or 3 not in T)
    (ROOT/'d25_e6_ternary_sampled_decisions.json').write_bytes((json.dumps(dict(seed=seed,samples=samples,scope='Literal independently checked seeded samples only; no exhaustive negative.'),indent=2)+'\n').encode())
    names=[Path(__file__).name,'d25_e6_ternary_sampled_decisions.json','search_d25_e6_ternary.cpp','PROOF.md#problem4-d25-e6-ternary-search','d25_e6_ternary_supply.json',
        'd15_d25_fourth_rows_audit.json','d15_d25_fourth_rows_inventory.json','b1_c14_nonsingleton_fourth_inventory.json',
        'PROOF.md#problem4-d15-d25-row-cover','PROOF.md#problem4-mandatory-core-isolation','PROOF.md#problem4-local-equality-flag','PROOF.md#problem4-entry-fiber-flag']
    result=dict(status='pass',parameter=[13,9,1],alphabet='ternary',seed=seed,positive_only=True,
        loaded_individual_rows=936000,all_individual_fields=16,field_triples=len(tuples),initial_forms=60,
        summary=summary,independently_checked_sampled_decisions=len(samples),independently_verified_candidates=candidates,
        kept_rows_sha256=sha(pool),build_flags=compile_flags,source_sha256={n:sha(ROOT/n) for n in names},
        scope='Seeded positive-only search in one full individually admissible fourth row pool; negative samples prove no geometric exclusion, exact F value, alphabet separation or global upper.')
    (ROOT/'d25_e6_ternary_search_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','independently_verified_candidates')}),flush=True)
if __name__=='__main__':main()
