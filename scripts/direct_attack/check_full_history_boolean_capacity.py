"""Independent scaled-integer faces and opposite-order cube parametrizations."""
import argparse,copy,json,math
from hashlib import sha256
from itertools import product
from pathlib import Path

def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def check_faces(z):
    grid=sorted({12*p//q for p in range(-4,5) for q in range(1,5)});nonzero=[v for v in grid if v]
    def fraction(v):
        g=math.gcd(abs(v),12);return [v//g,12//g]
    assert z['grid']==[fraction(v) for v in grid] and z['nonzero_coefficients']==len(nonzero)
    stream=sha256();hist={};count=0
    for a,b,x in product(nonzero,nonzero,grid):
        values=[x+i*a+j*b for i,j in ((0,0),(1,0),(0,1),(1,1))]
        valid=sum(v in (0,12) for v in values);assert valid<=3
        stream.update(json.dumps([fraction(v) for v in (a,b,x)]+[valid],separators=(',',':')).encode()+b'\n')
        hist[valid]=hist.get(valid,0)+1;count+=1
    assert z['faces']==count and z['valid_count_histogram']=={str(k):v for k,v in hist.items()}
    assert z['maximum_valid']==max(hist)==3 and z['semantic_sha256']==stream.hexdigest()
    return count

def check_partition(z):
    n,d=z['n'],z['d'];blocks=z['blocks'];assert len(blocks)==d and sorted(q for C in blocks for q in C)==list(range(n))
    assert all(C for C in blocks) and blocks[0]==[0]
    masks=[sum(1<<q for q in C) for C in blocks]
    vertices=sorted(sum(M for M,bit in zip(masks,bits) if bit) for bits in product((0,1),repeat=d))
    assert len(set(vertices))==1<<d
    c=sum((1<<q) in vertices for q in range(n))
    assert z['c']==c==max(1,2*d-n) and z['cube_vertices']==len(vertices)
    assert z['vertices_sha256']==digest(vertices) and z['admissible_full_history_bound']==len(vertices)-c-1
    return len(vertices)

def check_nonpartition(z):
    d=z['d'];n=z['n'];assert n==d+1 and d>=4
    assert z['equation_coefficients']==[1,1,-1,-1]+[0]*(n-4)
    first=[]
    for a,b,c in product((0,1),repeat=3):
        last=a+b-c
        if last in (0,1):first.append(a+2*b+4*c+8*last)
    assert len(first)==6
    vertices=sorted(prefix+16*free for prefix in first for free in range(1<<(n-4)))
    # e0+e2, e1+e2, e3-e2 and the free standard vectors give an explicit n-1 basis.
    basis=[[int(q==j)+int(q==2) for q in range(n)] for j in (0,1)]
    basis.append([int(q==3)-int(q==2) for q in range(n)])
    basis.extend([[int(q==j) for q in range(n)] for j in range(4,n)])
    pivot_coordinates=[0,1,3]+list(range(4,n))
    assert len(basis)==d and all(row[p]==int(i==j) for i,row in enumerate(basis) for j,p in enumerate(pivot_coordinates))
    assert all(sum(a*b for a,b in zip(row,z['equation_coefficients']))==0 for row in basis)
    c=sum((1<<q) in vertices for q in range(n));assert c==z['c']==d-3
    assert z['cube_vertices']==len(vertices)==3*(1<<(d-2)) and z['vertices_sha256']==digest(vertices)
    assert z['admissible_full_history_bound']==len(vertices)-c-1
    return len(vertices)

def check_arithmetic(z):
    assert z['maximum_n']==4096 and z['regimes']==[[2,2],[3,3],[4,5]]
    h=sha256();count=0
    for d,start in z['regimes']:
        for n in range(start,4097):
            c=max(1,2*d-n);B=2**d-c-1
            if n>d:B=max(B,3*2**(d-2)-2)
            assert B<=(n-1)*(d-1);count+=1
            h.update(json.dumps([n,d,B,(n-1)*(d-1)],separators=(',',':')).encode()+b'\n')
    assert z['controls']==count and z['semantic_sha256']==h.hexdigest()
    return count

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,default=Path('scripts/direct_attack/data/full_history_boolean_capacity.json'));ap.add_argument('--out',type=Path,default=Path('scripts/direct_attack/data/full_history_boolean_capacity_checks.json'));args=ap.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'))
    assert [(z['n'],z['d']) for z in data['partition']]==[(n,d) for n in range(2,13) for d in range(2,n+1)]
    assert [z['d'] for z in data['nonpartition']]==list(range(4,15))
    counts=dict(rational_four_point_faces=check_faces(data['faces']),partition_scopes=len(data['partition']),
                partition_vertices=sum(check_partition(z) for z in data['partition']),nonpartition_scopes=len(data['nonpartition']),
                nonpartition_vertices=sum(check_nonpartition(z) for z in data['nonpartition']),arithmetic_controls=check_arithmetic(data['arithmetic']))
    corruptions=[]
    for name,section,field,value in [('partition_dimension','partition','d',3),('partition_singletons','partition','c',1),
                                    ('partition_vertices','partition','cube_vertices',5),('partition_bound','partition','admissible_full_history_bound',2),
                                    ('nonpartition_dimension','nonpartition','d',5),('nonpartition_singletons','nonpartition','c',2),
                                    ('nonpartition_vertices','nonpartition','cube_vertices',16),('nonpartition_bound','nonpartition','admissible_full_history_bound',12)]:
        z=copy.deepcopy(data[section][0]);z[field]=value
        try:(check_partition if section=='partition' else check_nonpartition)(z)
        except AssertionError:corruptions.append(name)
        else:raise AssertionError('accepted corruption '+name)
    for section,field,value,verify in [('faces','maximum_valid',4,check_faces),('arithmetic','controls',0,check_arithmetic)]:
        z=copy.deepcopy(data[section]);z[field]=value
        try:verify(z)
        except AssertionError:corruptions.append(section+'_'+field)
        else:raise AssertionError('accepted corruption '+field)
    assert all((h+1)**(h+1)<1000003**2*4**h for h in range(1,17))
    assert all(1000003%t for t in range(2,math.isqrt(1000003)+1))
    out=dict(verified=True,**counts,corruptions_rejected=corruptions,boolean_minor_dimensions_certified=16,
             modulus_prime_trial_divisors=math.isqrt(1000003)-1,
             boundary='finite exact real-space and arithmetic controls, not a universal DFA enumeration or formal proof. Infinite shortest-history capacity and low-dimension cost statements are paper proofs; general Cerny OPEN. Negative focused pressure records remain exploratory and are outside this checker.')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
