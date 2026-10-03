"""Independent particle-prefix sums and original kernel-graph certificates."""
import argparse,copy,json
from collections import deque
from hashlib import sha256
from pathlib import Path


def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def seed(C,f):return [sum(f[q]==t for q in C)-int(t in C) for t in range(len(f))]
def projected(u,a):return [sum(c for q,c in enumerate(u) if a[q]==t) for t in range(len(a))]
def omega_particles(u,a,g,cyclic):
    out=[0]*len(a);current=u[:];controls=0
    # Sum h1 last: each initial signed particle follows original g,a edges.
    for h0 in range(cyclic):
        for q,c in enumerate(current):
            if not c:continue
            x=g[q];controls+=1
            for _ in range(cyclic-h0):x=a[x];out[x]+=c;controls+=1
        current=projected(current,a)
    return out,controls
def strongly_connected(rs):
    n=len(rs[0]);pred=[[] for _ in range(n)]
    for f in rs:
        for q,t in enumerate(f):pred[t].append(q)
    for backward in (False,True):
        seen={0};todo=[0]
        while todo:
            q=todo.pop()
            for t in pred[q] if backward else (f[q] for f in rs):
                if t not in seen:seen.add(t);todo.append(t)
        assert len(seen)==n
def verify_binary(z):
    n=z['n'];assert n>=3;a=[0 if q==n-1 else q for q in range(n)];b=[(q+1)%n for q in range(n)];C=list(range(n-1));u=seed(C,b)
    assert z['kind']=='binary_loops' and z['rows_sha256']==digest([a,b]) and z['cyclic_states']==C and z['seed']==u
    assert projected(u,a)==[0]*n and z['previous_projected_space']=='zero'
    om,controls=omega_particles(u,a,b,n-1)
    assert z['omega']==om==[n-1,-(n-1)]+[0]*(n-2) and any(om)
    strongly_connected([a,b]);root=[]
    for q in range(n):
        x=q
        for _ in range(n-1):x=b[x]
        root.append(a[x])
    assert root==[0]+list(range(n-1)) and z['reset_length']==(n-1)**2
    assert max(set(a))==n-2
    literal=0
    if n<=24:
        word=[0]+([1]*(n-1)+[0])*(n-2);current=list(range(n))
        for letter in word:current=[[a,b][letter][q] for q in current];literal+=n
        assert len(word)==z['reset_length'] and current==[0]*n
    return dict(n=n,annular_particle_letter_controls=controls,root_original_state_letter_controls=n*n,literal_reset_state_letter_controls=literal,
                total_annular_summands=(n-1)*n//2)
def equal_rows(m):
    n=2*m+1;a=list(range(n))
    for base in (0,m):
        for i in range(m):a[base+i]=base+(i+1)%m
    a[-1]=0;b=list(range(n));b[0]=1;g=list(range(n));g[0]=m;g[m]=0;g[1]=2*m;g[-1]=1
    return [a,b,g]
def verify_equal(z):
    m=z['m'];assert m>=2;n=2*m+1;a,b,g=equal_rows(m);C=list(range(2*m));us=[seed(C,f) for f in (b,g)]
    assert z['n']==n and z['kind']=='equal_nontrivial_cycles' and z['rows_sha256']==digest([a,b,g]) and z['cyclic_states']==C and z['seeds']==us
    for u in us:
        v=projected(u,a);assert sum(v[:m])==0 and v[m:]==[0]*(m+1)
    # Powers preserve first-cycle support, so second-cycle mass annihilates M0.
    om,controls=omega_particles(us[0],a,g,2*m);assert om==z['omega']
    assert z['second_cycle_mass']==sum(om[m:2*m])==-2*(m-1)!=0
    assert z['previous_projected_space']=='supported on first cycle, total zero'
    strongly_connected([a,b,g]);assert [len(set(f)) for f in (a,b,g)]==[n-1,n-1,n]
    edges=[];P=(0,1)
    for _ in range(m):edges.append(P);P=(a[P[0]],a[P[1]])
    edges.append((m-1,2*m));P=(g[0],g[1])
    for _ in range(m):edges.append(P);P=(a[P[0]],a[P[1]])
    seen={0};todo=[0]
    while todo:
        q=todo.pop()
        for x,y in edges:
            t=y if x==q else x if y==q else None
            if t is not None and t not in seen:seen.add(t);todo.append(t)
    assert len(seen)==n
    rt=None;verts=0
    if m<=6:
        Q=frozenset(range(n));ds={Q:0};todo=deque([Q])
        while todo:
            S=todo.popleft()
            if len(S)==1:rt=ds[S];break
            for f in (a,b,g):
                T=frozenset(f[q] for q in S)
                if T not in ds:ds[T]=ds[S]+1;todo.append(T)
        assert rt is not None;verts=len(ds)
    return dict(m=m,n=n,annular_particle_letter_controls=controls,total_annular_summands=m*(2*m+1),connected_original_kernel_image_edges=len(edges),small_rt=rt,small_subset_vertices=verts)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path('direct_attack/data/annular_multicluster_boundary.json'));ap.add_argument('--out',type=Path,default=Path('direct_attack/data/annular_multicluster_boundary_checks.json'));args=ap.parse_args();data=json.loads(args.source.read_text(encoding='utf-8'))
    assert [z['n'] for z in data['binary']]==list(range(3,41))+[64,100,128,256]
    assert [z['m'] for z in data['equal']]==list(range(2,25))+[32,64,128]
    binary=[verify_binary(z) for z in data['binary']];equal=[verify_equal(z) for z in data['equal']];bad=[]
    for key,val in [('rows_sha256','0'*64),('seed',[0]*3),('omega',[0]*3),('reset_length',3)]:
        z=copy.deepcopy(data['binary'][0]);z[key]=val;bad.append((verify_binary,z))
    for key,val in [('rows_sha256','0'*64),('second_cycle_mass',0),('omega',[0]*5),('seeds',[[0]*5,[0]*5])]:
        z=copy.deepcopy(data['equal'][0]);z[key]=val;bad.append((verify_equal,z))
    for checker,z in bad:
        try:checker(z)
        except AssertionError:pass
        else:raise AssertionError('corruption accepted')
    out=dict(verified=True,binary=binary,equal=equal,parameters=len(binary)+len(equal),maximum_n=max(z['n'] for z in binary+equal),
             annular_particle_letter_controls=sum(z['annular_particle_letter_controls'] for z in binary+equal),total_annular_summands=sum(z['total_annular_summands'] for z in binary+equal),
             root_original_state_letter_controls=sum(z['root_original_state_letter_controls'] for z in binary),literal_reset_state_letter_controls=sum(z['literal_reset_state_letter_controls'] for z in binary),
             connected_original_kernel_image_edges=sum(z['connected_original_kernel_image_edges'] for z in equal),small_ternary_subset_scopes=sum(z['small_rt'] is not None for z in equal),small_ternary_subset_vertices=sum(z['small_subset_vertices'] for z in equal),corruptions_rejected=len(bad),
             boundary='REFUTED paper unmodified all-cyclic-states annular extension, EVERY n>=3 binary and EVERY m>=2 equal-two-cycle ternary SC sync corank<=1. Finite scope only COMPUTATIONALLY VERIFIED. Original one-cluster lemma not refuted or independently proof-audited here; priority and general Cerny OPEN; no formal claim.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k not in ('binary','equal')}),flush=True)
if __name__=='__main__':main()
