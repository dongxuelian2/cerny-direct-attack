"""Complete all-first-pair domains and negative actual-image flag trees."""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import Counter,deque
import json,hashlib
import enumerate_b3_staircase_first as first
from enumerate_b3_staircase import rref,contains
ROOT=Path(__file__).resolve().parent
from c1_word_staircase_letter_generator import pool
def image(mask,row):
    result=0
    for q in range(13):
        if mask>>q&1:result|=1<<row[q]
    return result
def short_word(rows,chosen,S,cap=11):
    seen={S:(None,None)};work=deque([(S,0)])
    while work:
        m,d=work.popleft()
        if d==cap:continue
        for ix in chosen:
            out=image(m,rows[ix])
            if out in seen:continue
            seen[out]=(m,ix)
            if out.bit_count()<9 or not(out>>3&1):
                word=[];cur=out
                while seen[cur][0] is not None:
                    prev,i=seen[cur];word.append(i);cur=prev
                return list(reversed(word)),len(seen)
            work.append((out,d+1))
    return None,len(seen)

def propagate_words(literals,S,active,required,stats):
    n=len(literals);rounds=[]
    def digest(domain):return hashlib.sha256(domain.to_bytes((n+7)//8,'little')).hexdigest()
    while True:
        domains=[g&active for g in required]
        if any(not g for g in domains):return active,rounds,False
        premises=[[j,g.bit_length()-1] for j,g in enumerate(domains) if g.bit_count()==1]
        forced=sorted({i for j,i in premises})
        if not forced:return active,rounds,False
        record=dict(before_size=active.bit_count(),before_sha256=digest(active),singleton_premises=premises,deletions=[])
        bad,visited=short_word(literals,forced,S)
        if bad is not None:
            record.update(forced_bad_word=bad,after_size=active.bit_count(),after_sha256=digest(active));rounds.append(record);stats['word_rounds']+=1
            return active,rounds,True
        deleted=0;bits=active
        while bits:
            bit=bits&-bits;bits-=bit;i=bit.bit_length()-1
            if i in forced:continue
            bad,visited=short_word(literals,sorted(set(forced)|{i}),S)
            if bad is not None:deleted|=bit;record['deletions'].append(dict(letter=i,word=bad))
        active&=~deleted;record.update(after_size=active.bit_count(),after_sha256=digest(active));rounds.append(record);stats['word_rounds']+=1;stats['word_deletions']+=deleted.bit_count()
        if not deleted:return active,rounds,False

def tree(rows,basis0,B,C,D,G):
    n=len(rows);literals=[r for r,f in rows];allletters=(1<<n)-1;inputs={};spans={};stats=Counter()
    masks9=[sum(1<<q for q in S) for S in combinations(range(13),9) if 3 in S];sets={m:{q for q in range(13) if m>>q&1} for m in masks9}
    groups=[sum(1<<i for i,(r,f) in enumerate(rows) if f>>flag&1) for flag in range(4)]
    edges=[[sum(1<<i for i,(r,f) in enumerate(rows) if r[p]==q) for q in range(13)] for p in range(13)]
    def images(m):
        if m not in inputs:
            incoming=[q for q in range(13) if m>>q&1];answer={}
            for i,(r,f) in enumerate(rows):
                out=0
                for q in incoming:out|=1<<r[q]
                if out.bit_count()==9 and out>>3&1:answer[out]=answer.get(out,0)|(1<<i)
            inputs[m]=answer
        return inputs[m]
    def span(basis):
        key=rref(basis)
        if key not in spans:spans[key]=frozenset(m for m in masks9 if contains(key,m))
        return key,spans[key]
    def safe(m,d):
        S=sets[m]
        return (d>10 or len(S&B)==1) and (d>9 or len(S&C)==1) and (d>8 or len(S&D)==1) and (d>8 or not any(set(e)<=S for e in G))
    def visit(basis,active,required):
        k=len(basis)-1;assert k<11,'A depth-11 flag is a candidate, not an exclusion';rank,current=span(basis);assert len(rank)==len(basis)
        stats['nodes']+=1;stats['depth_'+str(k)]+=1
        mapping=images(basis[-1]);valid={m:g&active for m,g in mapping.items() if g&active and safe(m,k+1)};safeletters=0
        for g in valid.values():safeletters|=g
        active&=safeletters
        rounds=[];forced_bad=False
        if k>=3 and active.bit_count()<=10000:
            active,rounds,forced_bad=propagate_words(literals,basis0[0],active,required,stats)
            valid={m:g&active for m,g in valid.items() if g&active}
        node=dict(basis=basis,depth=k,word_propagation=rounds,domain_size=active.bit_count(),domain_sha256=hashlib.sha256(active.to_bytes((n+7)//8,'little')).hexdigest(),required_group_sizes=[(active&g).bit_count() for g in required])
        if forced_bad:node.update(reason='forced_short_word');stats['forced_short_word']+=1;return node
        missing=next((i for i,g in enumerate(required) if not(g&active)),None)
        if missing is not None:node.update(reason='missing_required_group',missing_group=missing);stats['missing_required_group']+=1;return node
        adj=[sum(1<<q for q in range(13) if edges[p][q]&active) for p in range(13)];closed=first.closure(adj)
        if closed is not None:node.update(reason='maximal_graph_not_SC',closed_set=[q for q in range(13) if closed>>q&1]);stats['maximal_graph_not_SC']+=1;return node
        assert k<11,'A surviving complete flag is not an exclusion'
        choices=sorted((m,g) for m,g in valid.items() if m not in current)
        if not choices:node.update(reason='no_growth');stats['no_growth']+=1;return node
        children=[]
        for m,group in choices:
            _,allowed=span(basis+[m]);following=0
            for out,g in valid.items():
                if out in allowed:following|=g
            children.append(dict(next_image=m,node=visit(basis+[m],active&following,required+[group])))
        node.update(reason='all_children_rejected',children=children);stats['internal_nodes']+=1;return node
    result=visit(basis0,allletters,groups)
    return result,dict(stats)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_text())
def canonical(basis,extra,controls):
    cells={}
    for q in range(13):cells.setdefault(tuple(q in X for X in controls),[]).append(q)
    perm={};E=set(extra or [])
    for cell in cells.values():perm.update(zip(sorted(cell,key=lambda q:(q not in E,tuple(q in S for S in basis),q)),sorted(cell)))
    return tuple(sorted(perm[q] for q in E)),tuple(sum(1<<perm[q] for q in S) for S in basis),[perm[q] for q in range(13)]
def main():
    baseline=read('c1_word_staircase_baseline_state.json');checkpoint=read('AUXILIARY_AUDIT_20261010_22.json');assert sha(ROOT/'c1_word_staircase_baseline_state.json')==checkpoint['source_sha256']['active_research.json']
    name='b3_mixed_c1_third2';parent=next(z for z in read('b3_inverse_clique_inventory.json')['records'] if z['id']==name);z=next(z for z in read('b3_third_cover_inventory.json')['records'] if z['id']==name)
    B,C,D=map(set,[z['B'],z['C'],z['D']]);controls=[{0,1,2},{3},B,C,D];orbits=Counter();classes=[];transports=[]
    for c in parent['global_classes']:
        if c['reason']!='retained_overapproximation':continue
        G=set(map(tuple,parent['required_P3_edges']))|({tuple(c['extra_pair'])} if c['extra_pair'] else set())
        frames=[set(X) for X in combinations(range(13),9) if 3 in X and all(len(set(X)&Y)==1 for Y in [B,C,D]) and not any(set(e)<=set(X) for e in G)]
        classes.append(dict(extra_pair=c['extra_pair'],frames=[sorted(S) for S in frames]))
        for si,S in enumerate(frames):
            for ti,T in enumerate(frames):
                if si==ti:continue
                em,bm,perm=canonical([S,T],c['extra_pair'],controls);orbits[(em,bm)]+=1
                transports.append(dict(extra_pair=c['extra_pair'],indices=[si,ti],canonical_extra=list(em),basis=list(bm),permutation=perm))
    assert len(classes)==22 and len(transports)==44082 and len(orbits)==317
    entries=[];total=Counter()
    for oi,((em,basis),multiplicity) in enumerate(sorted(orbits.items())):
        c=next(c for c in parent['global_classes'] if tuple(c['extra_pair'] or [])==em);S,T=[{q for q in range(13) if m>>q&1} for m in basis]
        rows,G=pool(parent,c,S,T,B,C,D);proof,stats=tree(rows,list(basis),B,C,D,G)
        entries.append(dict(extra_pair=list(em),basis=list(basis),multiplicity=multiplicity,letter_count=len(rows),rows_sha256=hashlib.sha256(json.dumps([list(r) for r,f in rows],separators=(',',':')).encode()).hexdigest(),flags_sha256=hashlib.sha256(json.dumps([f for r,f in rows],separators=(',',':')).encode()).hexdigest(),tree=proof,tree_stats=stats))
        total.update(stats);total['orbits']+=1;total['literal_letters']+=len(rows)
        if (oi+1)%10==0:print('orbits',oi+1,'/',len(orbits),flush=True)
    total['prefix_transports']=len(transports)
    names=[Path(__file__).name,'c1_word_staircase_letter_generator.py','enumerate_b3_staircase.py','b3_staircase_letter_generator.py','enumerate_b3_staircase_first.py','C1_WORD_STAIRCASE_EXCLUSION.md','B3_STAIRCASE_FLAG_EXCLUSION.md','c1_word_staircase_scope.json','c1_word_staircase_baseline_state.json','AUXILIARY_AUDIT_20261010_22.json','b3_inverse_clique_inventory.json','b3_third_cover_inventory.json']
    result=dict(status='complete_necessary_exclusion_inventory',parameter=[13,9,1],id=name,classes=classes,transports=transports,orbits=entries,stats=dict(total),new_excluded_third_ids=[name],source_sha256={n:sha(ROOT/n) for n in names},scope='Complete all-first-pair arbitrary-alphabet staircase exclusion of the last B3 geometry. No numerical F value or alphabet separation.')
    (ROOT/'c1_word_staircase_inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['classes','transports','orbits','source_sha256']}),flush=True)
if __name__=='__main__':main()
