"""Literal proof-step checker; does not import the propagation algorithm."""
def literal_image(row,mask):
    reached=set()
    for q in range(len(row)):
        if mask&(1<<q):reached.add(row[q])
    return sum(1<<q for q in reached)

def replay_images(rows,active,required,seeds,horizon,size,protected,steps):
    known=dict(seeds)
    assert all(m.bit_count()==size and m&protected==protected and 0<=d<=horizon for m,d in known.items())
    for record in steps:
        m=record['source'];depth=record['source_depth']
        assert m in known and known[m]==depth and depth<horizon
        if record['kind']=='delete':
            expected=0
            for i,row in enumerate(rows):
                if not(active&(1<<i)):continue
                image=literal_image(row,m)
                if image.bit_count()!=size or image&protected!=protected:expected|=1<<i
            assert expected and int(record['removed_hex'],16)==expected
            active&=~expected
        else:
            assert record['kind']=='force'
            index=record['group'];assert 0<=index<len(required)
            domain=required[index]&active;assert domain
            target=record['target'];d=record['target_depth'];assert d==depth+1 and d<=horizon
            assert target.bit_count()==size and target&protected==protected
            for i,row in enumerate(rows):
                if domain&(1<<i):assert literal_image(row,m)==target
            assert target not in known or d<known[target]
            known[target]=d
    return active,known
