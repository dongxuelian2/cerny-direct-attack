"""Independent complete finite controls and literal E6 field coverage."""
from pathlib import Path
from itertools import product,permutations,combinations
from collections import deque
import hashlib,json
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_text())
def reverse_dist(rows):
    n=len(rows[0]);pairs=list(combinations(range(n),2));back={p:[] for p in pairs};d={};todo=deque()
    for p in pairs:
        for row in rows:
            out=tuple(sorted({row[q] for q in p}))
            if len(out)==1:
                if p not in d:d[p]=1;todo.append(p)
            else:back[out].append(p)
    while todo:
        p=todo.popleft()
        for prev in back[p]:
            if prev not in d:d[prev]=d[p]+1;todo.append(prev)
    return d

def forward_merge(rows,pair):
    todo=deque([frozenset(pair)]);dist={frozenset(pair):0}
    while todo:
        S=todo.popleft()
        if len(S)==1:return dist[S]
        for row in rows:
            T=frozenset(row[q] for q in S)
            if T not in dist:dist[T]=dist[S]+1;todo.append(T)
    return None

def strong(rows):
    n=len(rows[0])
    for source in range(n):
        seen={source};todo=[source]
        for q in todo:
            for row in rows:
                if row[q] not in seen:seen.add(row[q]);todo.append(row[q])
        if len(seen)!=n:return False
    return True

def conditions(rows,D):
    n=len(rows[0]);kernel=all(row[x]!=row[y] or {x,y}<=D for row in rows for x,y in combinations(range(n),2))
    preimages=[{q for q in range(n) if row[q] in D} for row in rows]
    return kernel,all(R<=D or len(R)<=1 for R in preimages),bool(D) and len(D)<n

def main():
    records=[];total=direct=sc_count=0
    for n in range(5,8):
        D={0,1,2};c=3;e=4;outside=set(range(3,n));M=[];F=[]
        for into in D:
            for tail in permutations(sorted(outside-{c})):
                row=[c]*3+[-1]*(n-3);row[e]=into
                for q,t in zip(sorted(outside-{e}),tail):row[q]=t
                M.append(tuple(row))
        for inside in product(range(3),repeat=3):
            for outside_values in permutations(sorted(outside)):
                F.append(tuple([*inside,*outside_values]))
        checked=separate=connected=0
        for m,f in product(M,F):
            rows=[m,f];assert conditions(rows,D)==(True,True,True)
            dist=reverse_dist(rows);assert dist=={p:1 for p in combinations(range(3),2)}
            if checked<64:
                for pair in combinations(range(n),2):assert forward_merge(rows,pair)==dist.get(pair)
                separate+=1
            if strong(rows):connected+=1
            checked+=1
        assert checked==len(M)*len(F)
        records.append(dict(n=n,complete_M=len(M),complete_F=len(F),complete_pairs=checked,
            direct_forward_controls=separate,strongly_connected_nonsynchronizing=connected))
        total+=checked;direct+=separate;sc_count+=connected
    boundaries=[dict(rows=[[2,2,0],[1,2,0]],D=[0,1],expected=[True,False,True],reset='aba'),
        dict(rows=[[3,3,3,4,0],[3,3,3,3,3]],D=[0,1,2],expected=[False,True,True],reset='b'),
        dict(rows=[[0,0,0]],D=[0,1,2],expected=[True,True,False],reset='a')]
    for z in boundaries:
        rows=z['rows'];assert list(conditions(rows,set(z['D'])))==z['expected']
        S=set(range(len(rows[0])))
        for c in z['reset']:S={rows[ord(c)-97][q] for q in S}
        assert len(S)==1
    data=read('b1_c4_fourth_inventory.json')
    z=next(z for z in data['records'] if z['D']==[1,2,5] and z['E']==[6])
    assert z['allowed_preD_fibers']==[[0],[1,2,5],[4],[6]]
    pairs=[xy for p in z['pairs'] for xy in p['fourth_field_pairs']]
    assert len(pairs)==9
    fields=[]
    for x,y in pairs:
        l,r=z['rows'][x],z['rows'][y]
        m,f=(l,r) if l['preC']==[1,2,5] else (r,l)
        assert m['preC']==[1,2,5] and m['preD']==[6] and f['preD']==[1,2,5]
        assert f['preC']!=[1,2,5]
        fields.append(dict(fields=[x,y],moving_preC=m['preC'],moving_preD=m['preD'],fixed_preD=f['preD']))
    names=[Path(__file__).name,'PROOF.md#problem4-closed-merging-block','b1_c4_fourth_inventory.json','b1_c4_fourth_audit.json',
        'PROOF.md#problem4-b1-c4-fourth-space','PROOF.md#problem4-common-collapsing-block-trap','common_collapsing_block_audit.json']
    result=dict(status='pass',uniform_proof='PROOF.md#problem4-closed-merging-block',complete_M_F_pairs=total,
        direct_forward_controls=direct,strongly_connected_nonsync_controls=sc_count,finite_controls=records,
        omitted_hypothesis_controls=boundaries,exact_E6_field_pairs=fields,binary_C4_D125_E6_paper_excluded=True,
        source_sha256={n:sha(ROOT/n) for n in names},
        scope='Uniform conditional closed-merging-block criterion and independent binary C4/D125/E6 paper exclusion; no unrestricted E6 or global F value.')
    (ROOT/'closed_merging_block_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_sha256','finite_controls','omitted_hypothesis_controls','exact_E6_field_pairs')}),flush=True)
if __name__=='__main__':main()
