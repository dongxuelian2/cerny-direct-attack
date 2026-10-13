"""Independent ordinary-set check of a finite selector-cover contradiction."""
def check(rows,S,required,clauses,tree):
    assert rows and len(S)==9 and 3 in S and set(S)<=set(range(13))
    assert all(len(row)==13 and set(row)<=set(range(13)) for row in rows)
    N=len(rows);universum=set(range(N));groups=list(map(set,required));negative=[]
    assert groups and all(g and g<=universum for g in groups)
    for c in clauses:
        word=c['word'];assert 1<=len(word)<= (6 if c['kind']=='short_rank_word' else 11)
        assert set(word)<=universum
        T=set(range(13)) if c['kind']=='short_rank_word' else set(S)
        for i in word:T={rows[i][q] for q in T}
        if c['kind']=='short_rank_word':assert len(T)<=9
        else:assert c['kind']=='unsafe_word' and (len(T)<9 or 3 not in T)
        negative.append(set(word))
    counts={'nodes':0,'leaves':0,'unit_steps':0}
    def visit(F,D,node):
        counts['nodes']+=1;assert F.isdisjoint(D)
        for step in node['units']:
            i=step['letter'];assert i in universum-F-D
            if step['kind']=='force':
                R=groups[step['group']];assert not R&F and R-D=={i};F.add(i)
            else:
                assert step['kind']=='delete';R=negative[step['clause']]
                assert not R&D and R-F=={i};D.add(i)
            counts['unit_steps']+=1
        if node['reason']=='missing_group':
            R=groups[node['group']];assert not R&F and R<=D;counts['leaves']+=1;return
        if node['reason']=='forbidden_alphabet':
            assert negative[node['clause']]<=F;counts['leaves']+=1;return
        assert node['reason']=='all_first_suppliers_rejected'
        R=groups[node['group']];assert not R&F
        choices=sorted(R-D);assert choices and [z['letter'] for z in node['children']]==choices
        prior=set()
        for i,child in zip(choices,node['children']):
            visit(F|{i},D|prior,child['node']);prior.add(i)
    visit(set(),set(),tree)
    return counts
