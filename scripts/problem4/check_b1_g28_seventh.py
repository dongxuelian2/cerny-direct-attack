"""Independent G28 seventh space, crossed cuts, and binary H19 words."""
from itertools import combinations,product,permutations
from fractions import Fraction
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
Q=set(range(13));A={3};B={0};C={1,4};D={5};E={6};F={7};G={2,8};K={1,2}
KNOWN=(B,C,D,E,F,G);KEYS=('preA','preB','preC','preD','preE','preF')
FULL=8191;OUT=FULL^(1<<3);P={0,3,5,6,7}

def mask(X):return sum(1<<q for q in X)
def points(x):return [q for q in range(13) if x>>q&1]
def inc(x,y):return bool(x&~y) and bool(y&~x)

def rank(cols):
    work=[[int(bool(x>>q&1)) for x in cols] for q in points(OUT)];r=0
    for j in range(len(cols)):
        i=next((i for i in range(r,len(work)) if work[i][j]),None)
        if i is None:continue
        work[r],work[i]=work[i],work[r];v=pow(work[r][j],-1,100003)
        work[r]=[x*v%100003 for x in work[r]]
        for i in range(r+1,len(work)):
            v=work[i][j]
            if v:work[i]=[(x-v*y)%100003 for x,y in zip(work[i],work[r])]
        r+=1
    return r

def extension(H,allowed,parent,protected):
    caps=[1,1,2,1,1,1,2,4];rows=[];records=[]
    for i,old in enumerate(parent['rows']):
        for R in [A]+allowed:
            groups=[set(old[key]) for key in KEYS]+[R]
            if sum(map(len,groups))!=len(set().union(*groups)):continue
            groups.append(Q-set().union(*groups))
            forced={p for X,cap in zip(groups,caps) if cap==1 for p in combinations(sorted(X),2)}
            if len(forced)>4 or any(not set(p)&K or set(p)&protected for p in forced):continue
            rows.append(dict(parent_row=i,**{key:old[key] for key in KEYS},preG=sorted(R),
                forced_pairs=[list(p) for p in sorted(forced)],capacity=[min(len(X),cap) for X,cap in zip(groups,caps)]))
    for previous in parent['pairs']:
        for x,y in previous['sixth_field_pairs']:
            pairs=[]
            for i,left in enumerate(rows):
                for j,right in enumerate(rows):
                    if (left['parent_row'],right['parent_row'])!=(x,y) or (x==y and i>j):continue
                    if left['preG']!=sorted(H) and right['preG']!=sorted(H):continue
                    if any(left['capacity'][h]+right['capacity'][h]<caps[h] for h in range(8)):continue
                    if len({tuple(p) for row in (left,right) for p in row['forced_pairs']})>4:continue
                    pairs.append([i,j])
            records.append(dict(original_third_rows=previous['original_third_rows'],original_fourth_rows=previous['original_fourth_rows'],
                original_fifth_rows=previous['original_fifth_rows'],original_sixth_rows=[x,y],seventh_field_pairs=pairs))
    return rows,records

def crossed(H):
    choices=([A,B],[A,B,C],[A,B,C,D],[A,B,C,D,E],[A,B,C,D,E,F],[A,B,C,D,E,F,G])
    tested=disjoint=0
    for fields in product(*choices):
        tested+=1;used=set(H);good=True
        for X in fields:
            if X&used:good=False;break
            used|=X
        disjoint+=good
    assert tested==5040 and disjoint==0
    return dict(H=sorted(H),individual_field_tuples=tested,disjoint_tuples=disjoint)

def left_rows():
    R=(9,10,11,12)
    for outputs,preA in product(permutations(R),(0,3)):
        for u in sorted({0,3,5}-{preA}):
            for preD,preE,v in permutations(sorted(P-{preA,u})):
                for delta in (1,4):
                    for placement in ('preF','preG'):
                        for values in product((2,8),repeat=1 if placement=='preF' else 2):
                            L=[-1]*13;L[1]=L[4]=0;L[preA]=3;L[u]=delta;L[preD]=5;L[preE]=6
                            if placement=='preF':L[2]=L[8]=7;L[v]=values[0]
                            else:L[2],L[8]=values;L[v]=7
                            for q,t in zip(R,outputs):L[q]=t
                            assert all(t>=0 for t in L);yield L,u

def right_rows():
    for out,swap,gamma,values in product(permutations((9,10,11,12)),(False,True),(1,4),product((2,8),repeat=2)):
        X=[-1]*13;X[0]=3 if swap else 0;X[3]=0 if swap else 3
        X[5]=gamma;X[6]=5;X[7]=6;X[2]=X[8]=7;X[1],X[9]=values
        for q,t in zip((4,10,11,12),out):X[q]=t
        assert all(t>=0 for t in X);yield X

def H19_words(profile):
    fields=profile['rows'];role_pairs=0
    for old in profile['pairs']:
        for a,b in old['seventh_field_pairs']:
            pair=[fields[a],fields[b]]
            X=[r for r in pair if r['preG']==[1,9]];L=[r for r in pair if r['preB']==[1,4]]
            assert len(X)==len(L)==1 and X[0]!=L[0];X=X[0];L=L[0]
            assert sorted([X['preA'],X['preB']])==[[0],[3]]
            assert [X[k] for k in ('preC','preD','preE','preF')]==[[5],[6],[7],[2,8]]
            assert L['preA'] in ([0],[3]) and L['preC'] in ([0],[3],[5])
            fixed=[L[k] for k in ('preA','preC','preD','preE')]
            assert all(len(s)==1 for s in fixed) and len(set().union(*map(set,fixed)))==4
            v=next(iter(P-set().union(*map(set,fixed))))
            assert (L['preF'],L['preG']) in (([2,8],[v]),([v],[2,8]));role_pairs+=1
    left=list(left_rows());right=list(right_rows());hist={};controls={}
    assert len(left)==6912 and len(right)==384
    for (L,u),X in product(left,right):
        gamma=X[5];delta=L[u]
        if gamma==delta:
            assert 5-gamma not in set(L)|set(X);reason='missing_C_target'
        else:
            if gamma==1:pair=(5,next(q for q in (4,10,11,12) if X[q]==9));word=(X,X,X);reason='protected_XXX'
            else:
                assert gamma==4 and delta==1;pair=(u,next(q for q in (9,10,11,12) if L[q]==9));word=(L,X,X);reason='protected_LXX'
            assert pair[0]!=pair[1] and set(pair)&P
            current=set(pair)
            for row in word:current={row[q] for q in current}
            assert current=={7}
            if reason not in controls:controls[reason]=dict(pair=list(pair),word='XXX' if gamma==1 else 'LXX',L=L,X=X)
        hist[reason]=hist.get(reason,0)+1
    assert role_pairs==48 and hist==dict(missing_C_target=1327104,protected_XXX=663552,protected_LXX=663552)
    return dict(original_field_pairs_checked=role_pairs,complete_normalized_L_rows=len(left),complete_normalized_X_rows=len(right),
        complete_n13_normalized_row_pairs=len(left)*len(right),proof_cases=hist,literal_word_examples=controls)

def main():
    assert all(100003%d for d in range(2,317)) and 9**9<100003**2
    inv=json.loads((ROOT/'b1_g28_seventh_inventory.json').read_text(encoding='utf-8'))
    parent=next(z for z in json.loads((ROOT/'b1_sixth_inventory.json').read_text(encoding='utf-8'))['records']
        if z['E']==[6] and z['F']==[7] and z['G']==[2,8])
    assert parent['additional_Boolean_fibers']==[]
    known=list(map(mask,KNOWN));k=mask(K)
    allS=[s for s in range(FULL+1) if s&(1<<3) and s.bit_count()==9]
    candidates=[h for h in range(1,FULL+1) if not h&(1<<3) and (h&~k).bit_count()<=1]
    members={}
    for h in candidates:
        if any(not inc(h,x) for x in known):continue
        forms=[s for s in allS if all((s&x).bit_count()==1 for x in (*known,h))]
        if not forms or rank([OUT,*known,h])!=8:continue
        sig=tuple(sum(bool(h>>q&1) and tuple(int(bool(x>>q&1)) for x in (k,*known))==key for q in points(OUT))
            for key in product((0,1),repeat=7));members.setdefault(sig,[]).append(h)
    assert len(members)==7 and sum(map(len,members.values()))==19
    masks=ranktests=labelled=0;summary=[];cross_controls=[]
    for z in inv['records']:
        h=mask(z['H']);sig=tuple(z['cell_signature'])
        assert h in members[sig] and len(members[sig])==z['labelled_H']==z['orbit_size']
        for actual in members[sig]:
            cols=[OUT,*known,actual];forms=[s for s in allS if all((s&x).bit_count()==1 for x in cols[1:])]
            assert len(forms)==z['feasible_nine_sets'];common=FULL
            for s in forms:common&=s
            cells={}
            for q in points(OUT):
                key=tuple(int(bool(x>>q&1)) for x in cols[1:]);cells[key]=cells.get(key,0)|(1<<q)
            bools=[]
            for r in range(1,FULL+1):
                if r&(1<<3):continue
                masks+=1
                if any(r&cell not in (0,cell) for cell in cells.values()):continue
                ranktests+=1
                if rank(cols+[r])==8 and all((s&r).bit_count()==1 for s in forms):bools.append(r)
            allowed=[r for r in bools if (r&~k).bit_count()<=1 and all(r==x or inc(r,x) for x in cols[1:])]
            if actual!=h:
                mapping={}
                for key in product((0,1),repeat=7):
                    cell=[q for q in points(OUT) if tuple(int(bool(x>>q&1)) for x in (k,*known))==key]
                    source=[q for q in cell if h>>q&1]+[q for q in cell if not h>>q&1]
                    target=[q for q in cell if actual>>q&1]+[q for q in cell if not actual>>q&1];mapping.update(zip(source,target))
                assert set(bools)=={sum(1<<mapping[q] for q in v['R']) for v in z['all_Boolean_one_count_fibers']}
            else:
                assert set(bools)=={mask(v['R']) for v in z['all_Boolean_one_count_fibers']}
                for v in z['all_Boolean_one_count_fibers']:
                    co=list(map(Fraction,v['coefficients']));r=mask(v['R'])
                    assert all(sum(t*int(bool(x>>q&1)) for t,x in zip(co,cols))==int(bool(r>>q&1)) for q in points(OUT))
                    assert 8*co[0]+sum(co[1:])==1
                    assert v['covered_by_K']==((r&~k).bit_count()<=1)
                assert points(common)==z['mandatory_through_four'] and z['mandatory_core_isolation_depth']==7
                assert not common&mask(G) and common&mask(P)==mask(P)
                assert z['preG_target_capacity']==2 and z['remaining_target_capacity']==4
                assert {mask(R) for R in z['allowed_preG_fibers']}==set(allowed)
                rows,pairs=extension(set(z['H']),[set(points(r)) for r in sorted(allowed,key=points)],parent,set(points(common)))
                assert rows==z['rows'] and pairs==z['pairs']
            if actual&mask(C) and actual&mask(G):cross_controls.append(crossed(set(points(actual))))
            else:assert set(allowed)==set(cols[1:])
            labelled+=1
        summary.append(dict(H=z['H'],labels=z['labelled_H'],forms=z['feasible_nine_sets'],mandatory=z['mandatory_through_four'],
            additional_Boolean_fibers=z['additional_Boolean_fibers'],additional_covered_fibers=z['additional_covered_fibers'],
            binary_field_pairs=sum(len(p['seventh_field_pairs']) for p in z['pairs'])))
    assert labelled==19 and masks==77805 and len(cross_controls)==7
    assert [v['binary_field_pairs'] for v in summary]==[1094,0,0,48,0,243,0]
    assert [v['additional_Boolean_fibers'] for v in summary]==[[[10,11,12]],[[4,8]],[[2,4]],[],[[1,8]],[],[]]
    words=H19_words(next(z for z in inv['records'] if z['H']==[1,9]))
    kept=[z for z in inv['records'] if z['H'] in ([9],[2,9])]
    coverage={tuple(p['original_sixth_rows']) for z in kept for p in z['pairs'] if p['seventh_field_pairs']}
    original={tuple(xy) for p in parent['pairs'] for xy in p['sixth_field_pairs']}
    assert coverage==original and len(coverage)==365
    assert sum(len(p['seventh_field_pairs']) for z in kept for p in z['pairs'])==1337
    for name,digest in inv['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    names=[Path(__file__).name,'enumerate_b1_g28_seventh.py','b1_g28_seventh_inventory.json','PROOF.md#problem4-b1-g28-seventh-entrance',
        'b1_sixth_inventory.json','b1_sixth_audit.json','PROOF.md#problem4-b1-sixth-entrance','PROOF.md#problem4-mandatory-core-isolation',
        'mandatory_core_isolation_audit.json','PROOF.md#problem4-entry-fiber-flag','PROOF.md#problem4-local-equality-flag']
    result=dict(status='pass',parameter=[13,9,1],branch=dict(E=[6],F=[7],G=[2,8]),
        geometric_orbits=7,labelled_H=19,all_subset_masks_tested=masks,augmented_rank_tests=ranktests,records=summary,
        all_alphabet_crossed_exclusions=[[1,2],[1,8],[2,4],[1,2,9]],crossed_controls=cross_controls,
        binary_only_excluded_H=[1,9],binary_H19_controls=words,
        remaining_unrestricted_H=[[9],[1,9],[2,9]],remaining_unrestricted_geometries=3,remaining_unrestricted_labels=12,
        remaining_binary_H=[[9],[2,9]],remaining_binary_geometries=2,remaining_binary_labels=8,remaining_binary_field_pairs=1337,
        all_original_sixth_pairs_retained=365,
        source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names},
        scope='Complete capacity2 seventh space, all companions and four all-alphabet crossed exclusions, plus binary H19 three-letter proof. No whole G28/E6/F7 removal, exact F value, or numerical separation.')
    (ROOT/'b1_g28_seventh_audit.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(dict(status='pass',orbits=7,labels=19,masks=masks,ranktests=ranktests,
        crossed_labels=len(cross_controls),binary_H19_pairs=words['complete_n13_normalized_row_pairs'],
        remaining_binary_field_pairs=1337)),flush=True)
if __name__=='__main__':main()
