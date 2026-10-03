"""Independent paired-swap rows, all phase branches, bad-set invariant and forward DAGs."""
import argparse
from collections import deque
import copy
from hashlib import sha256
import json
from pathlib import Path


def determinant(matrix):
    a=[r[:] for r in matrix];previous=1;sign=1
    for j in range(len(a)-1):
        p=next((i for i in range(j,len(a)) if a[i][j]),None)
        if p is None:return 0
        if p!=j:a[j],a[p]=a[p],a[j];sign=-sign
        pivot=a[j][j]
        for x in range(j+1,len(a)):
            for y in range(j+1,len(a)):
                value=a[x][y]*pivot-a[x][j]*a[j][y]
                assert value%previous==0;a[x][y]=value//previous
            a[x][j]=0
        previous=pivot
    return sign*a[-1][-1]


def verify(z):
    assert [r['d'] for r in z['records']]==list(range(2,13))
    branch_controls=0;row_state_controls=0;bad_controls=0;literal_letters=0;finite=[]
    for r in z['records']:
        d=r['d'];n=2**d-1;Q=(1<<n)-1
        B=[set(range(2**i-1,2**(i+1)-1)) for i in range(d)]
        masks=[sum(1<<q for q in block) for block in B]
        selected=lambda k:sum(mask for i,mask in enumerate(masks) if k>>i&1)
        rows=[]
        for i in range(1,d):
            s=min(B[i]);unit=list(range(n));unit[0]=s;rows.append(unit)
            carry=list(range(n))
            for q in range(s):carry[q],carry[s+1+q]=carry[s+1+q],carry[q]
            carry[s]=0;rows.append(carry)
        assert r['n']==n and r['base_letter_count']==len(rows)==2*(d-1)
        assert r['augmented_letter_count']==len(rows)+n-1
        assert sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()==r['original_rows_sha256']
        assert r['explicit_original_rows']==(rows if d<=4 else None)
        indegree=[0]*n;blockimages=[]
        for row in rows:
            assert len(set(row))==n-1
            for q,t in enumerate(row):indegree[t]+=1;row_state_controls+=1
            blockimages.append([sum(1<<q for q in {row[t] for t in block}) for block in B])
        assert indegree==[len(rows)]*n
        # SC, using actual original rows, independently of added swaps.
        for direction in (False,True):
            edges=[[] for _ in range(n)]
            for row in rows:
                for q,t in enumerate(row):edges[t if direction else q].append(q if direction else t)
            reached={0};queue=deque([0])
            while queue:
                q=queue.popleft()
                for t in edges[q]:
                    if t not in reached:reached.add(t);queue.append(t)
            assert len(reached)==n
        def bad(S):
            return any(S&mask and not(S>>min(block)&1) and S&~mask
                       for block,mask in zip(B[1:],masks[1:]))
        choices=[];word=[];number=1
        for k in range(n,1,-1):
            S=selected(k);valid=[]
            for a,images in enumerate(blockimages):
                T=0
                for i in range(d):
                    if k>>i&1:T|=images[i]
                branch_controls+=1
                if T.bit_count()!=k-1:continue
                if T==selected(k-1):valid.append(a)
                else:assert bad(T)
            assert valid
            choices.append(valid);word.append(valid[0]);number*=len(valid)
        assert choices==r['all_optimal_forward_label_choices']
        assert word==r['canonical_original_reset_indices'] and len(word)==n-1
        assert number==r['shortest_labeled_word_count']
        assert r['rt']==r['P']==n-1 and r['unique_reset_endpoint']==0
        assert r['optimal_endpoint_chain_count']==1 and r['proper_stages']==n-2
        digest=sha256();size=(n+7)//8
        for k in range(2,n):digest.update(selected(k).to_bytes(size,'little'))
        assert digest.hexdigest()==r['canonical_proper_mask_sha256']
        assert r['raw_proper_plus_Q_rank']==r['full_inverse_raw_rank']==d
        assert r['normalized_proper_rank']==d-1
        # Explicit cell basis and exact integer centered minor for EVERY d.
        assert selected(3)&~selected(2)==masks[0]
        matrix=[[n*int(selected(2**i)>>min(B[j])&1)-2**i for j in range(1,d)] for i in range(1,d)]
        assert determinant(matrix)==n**(d-2)
        if d<=8:
            current=set(range(n))
            for a in word:current={rows[a][q] for q in current};literal_letters+=1
            assert current=={0}
        if d<=4:
            # ALL subsets and EVERY decreasing edge: independently attack
            # the bad-block invariant, not just prescribed counter states.
            tables=[];pop=[S.bit_count() for S in range(Q+1)]
            for row in rows:
                table=[0]*(Q+1)
                for S in range(1,Q+1):
                    b=S&-S;table[S]=table[S^b]|(1<<row[b.bit_length()-1])
                tables.append(table)
            for S in range(1,Q+1):
                if not bad(S):continue
                for table in tables:
                    T=table[S]
                    if pop[T]==pop[S]-1:assert bad(T);bad_controls+=1
            finish=[False]*(Q+1);count=[0]*(Q+1)
            for q in range(n):finish[1<<q]=True;count[1<<q]=1
            for S in sorted(range(1,Q+1),key=int.bit_count):
                if pop[S]==1:continue
                for table in tables:
                    T=table[S]
                    if pop[T]==pop[S]-1 and finish[T]:finish[S]=True;count[S]+=count[T]
            assert finish[Q] and count[Q]==number
            optimal={Q};queue=deque([Q])
            while queue:
                S=queue.popleft()
                for table in tables:
                    T=table[S]
                    if pop[T]==pop[S]-1 and finish[T] and T not in optimal:optimal.add(T);queue.append(T)
            assert optimal=={selected(k) for k in range(1,n+1)}
            added=[]
            for q in range(n-1):
                perm=list(range(n));perm[q],perm[q+1]=perm[q+1],perm[q];added.append(perm)
            all_tables=tables[:]
            for row in added:
                table=[0]*(Q+1)
                for S in range(1,Q+1):
                    b=S&-S;table[S]=table[S^b]|(1<<row[b.bit_length()-1])
                    assert pop[table[S]]==pop[S]
                all_tables.append(table)
            actual={Q};queue=deque([Q])
            while queue:
                S=queue.popleft()
                for table in all_tables:
                    T=table[S]
                    if T not in actual:actual.add(T);queue.append(T)
            assert len(actual)==r['augmented_actual_image_count']==Q
            finite.append(dict(d=d,n=n,all_subset_vertices=Q,optimal_vertices=len(optimal),
                               all_shortest_labeled_words=number,augmented_actual_images=len(actual)))
        else:assert r['augmented_actual_image_count'] is None
    return dict(verified=True,parameters=11,maximum_n=4095,original_row_state_controls=row_state_controls,
                all_counter_phase_label_controls=branch_controls,all_subset_bad_invariant_edges=bad_controls,
                literal_whole_reset_letters=literal_letters,finite_all_subset_scopes=finite,
                boundary='all-d theorem is PAPER; parameter controls through n4095 and exhaustive all-subset scopes n3/7/15 are computational, not a formal kernel')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',default='direct_attack/data/optimal_counter_history.json')
    ap.add_argument('--out',default='direct_attack/data/optimal_counter_history_checks.json')
    args=ap.parse_args();z=json.loads(Path(args.root).read_text());result=verify(z);rejected=[]
    for name,change in (
        ('dimension',lambda x:x['records'][-1].update(normalized_proper_rank=12)),
        ('word_count',lambda x:x['records'][2].update(shortest_labeled_word_count=23)),
        ('wrong_carry',lambda x:x['records'][2]['all_optimal_forward_label_choices'][0].append(1)),
        ('reset_letter',lambda x:x['records'][2]['canonical_original_reset_indices'].__setitem__(0,1)),
        ('row_hash',lambda x:x['records'][1].update(original_rows_sha256='0'*64)),
        ('actual_count',lambda x:x['records'][2].update(augmented_actual_image_count=32766)),
    ):
        bad=copy.deepcopy(z);change(bad)
        try:verify(bad)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('accepted corruption: '+name)
    result.update(status='COMPUTATIONALLY VERIFIED independent bounded controls; all-d proof paper, not formal',rejected_corruptions=rejected)
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
