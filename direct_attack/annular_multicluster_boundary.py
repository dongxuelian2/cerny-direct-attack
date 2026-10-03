"""Integer annular vectors for two precise failed multicluster extensions."""
import argparse,json
from hashlib import sha256
from pathlib import Path


def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def push(v,f):
    out=[0]*len(v)
    for q,c in enumerate(v):out[f[q]]+=c
    return out
def seed(C,f):
    u=[0]*len(f)
    for q in C:u[f[q]]+=1;u[q]-=1
    return u
def omega(u,a,g,cyclic):
    # Sum h0 first, then apply g and the literal final a-powers.
    powers=[u]
    for _ in range(cyclic-1):powers.append(push(powers[-1],a))
    out=[0]*len(a)
    for h1 in range(cyclic):
        v=[sum(w[q] for w in powers[:cyclic-h1]) for q in range(len(a))]
        v=push(v,g)
        for _ in range(h1+1):v=push(v,a)
        out=[x+y for x,y in zip(out,v)]
    return out
def binary(n):
    a=list(range(n));a[-1]=0;b=list(range(1,n))+[0];C=list(range(n-1));u=seed(C,b);om=omega(u,a,b,n-1)
    assert om==[n-1,-(n-1)]+[0]*(n-2) and push(u,a)==[0]*n
    return dict(kind='binary_loops',n=n,rows_sha256=digest([a,b]),seed=u,omega=om,cyclic_states=C,
                previous_projected_space='zero',reset_length=(n-1)**2)
def equal(m):
    n=2*m+1;a=list(range(1,m))+[0]+list(range(m+1,2*m))+[m]+[0]
    b=list(range(n));b[0]=1;g=list(range(n));g[0],g[m]=m,0;g[1],g[-1]=n-1,1
    C=list(range(2*m));ub=seed(C,b);ug=seed(C,g);om=omega(ub,a,g,2*m)
    assert sum(om[m:2*m])==-2*(m-1)
    return dict(kind='equal_nontrivial_cycles',m=m,n=n,rows_sha256=digest([a,b,g]),seeds=[ub,ug],omega=om,
                second_cycle_mass=sum(om[m:2*m]),cyclic_states=C,previous_projected_space='supported on first cycle, total zero')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('direct_attack/data/annular_multicluster_boundary.json'));args=ap.parse_args()
    out=dict(binary=[binary(n) for n in list(range(3,41))+[64,100,128,256]],
             equal=[equal(m) for m in list(range(2,25))+[32,64,128]],
             boundary='REFUTED paper EVERY n>=3 binary Cerny and EVERY m>=2 equal-two-cycle ternary SC sync corank<=1: unmodified all-cyclic-states annular formula fails at order1. Does NOT refute original one-cluster lemma. Infinite claims paper only; priority and general Cerny OPEN, no formal claim.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(binary=len(out['binary']),equal=len(out['equal']),maximum_n=max(z['n'] for z in out['binary']+out['equal']),boundary=out['boundary'])),flush=True)
if __name__=='__main__':main()
