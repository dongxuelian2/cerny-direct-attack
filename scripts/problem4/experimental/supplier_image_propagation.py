"""Safe-image propagation from nonempty obligatory supplier groups."""
def propagate_images(images,active,required,seeds,horizon):
    known=dict(seeds);steps=[]
    assert all(isinstance(m,int) and 0<=d<=horizon for m,d in known.items())
    while True:
        changed=False
        if any(not(g&active) for g in required):break
        for _,m in sorted((d,m) for m,d in known.items()):
            depth=known[m]
            if depth>=horizon:continue
            outputs=images(m);allowed=0
            for domain in outputs.values():allowed|=domain
            removed=active&~allowed
            if removed:
                steps.append(dict(kind='delete',source=m,source_depth=depth,removed_hex=hex(removed)))
                active&=allowed;changed=True
            if any(not(g&active) for g in required):return active,steps,known
            for j,g in enumerate(required):
                domain=g&active
                unanimous=next((Y for Y,bits in sorted(outputs.items()) if domain&bits==domain),None)
                if unanimous is None:continue
                d=depth+1
                if unanimous not in known or d<known[unanimous]:
                    steps.append(dict(kind='force',source=m,source_depth=depth,group=j,target=unanimous,target_depth=d))
                    known[unanimous]=d;changed=True
        if not changed:break
    return active,steps,known
