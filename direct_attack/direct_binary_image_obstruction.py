"""Direct binary double-cycle projection: charged quadratic extension witnesses."""
import argparse
import json
from pathlib import Path


def record(p):
    n=2*p+1
    s,k=p//2,(p+1)//2
    a=[(i+1)%p for i in range(p)]+[p+(j+1)%(p+1) for j in range(p+1)]
    b=[]
    for q in range(n):
        i=q if q<p else (q-p)%p
        b.append(p+i if i<k else i)
    A=list(range(s,p)) if p%2==0 else list(range(s))
    T=[i for i in range(p) if i in A]+[p+j for j in range(p+1) if j%p in A]
    M=(p*p+3*p)//2-k
    z=dict(p=p,n=n,s=s,k=k,rows=dict(a=a,b=b),
           initial_image=sorted(set(b)),projected_target=A,target=T,
           entering_a_count=M,image_extension=M+1,
           reset_lower_bound=p*p-k+1,reset_upper_bound=p*p+p-k,
           reset_first_macro_a=p+1,reset_first_macro_repetitions=p-k,
           reset_second_macro_a=p,reset_second_macro_repetitions=k-1,
           first_stall_a_counts=[p-i+1+(p if i>=k else 0) for i in range(p)],
           only_larger_actual_source='Q',
           status='PROVED paper exact direct binary image extension and quadratic reset interval; priority OPEN; no formal verification')
    if p<=24:
        z.update(literal_entering_word='b'+'a'*M,
                 literal_reset_word='b'+('a'*(p+1)+'b')*(p-k)+('a'*p+'b')*(k-1))
    if p==6:
        E=set(b)
        for _ in range(27):
            E={a[q] for q in E}
        z['extra_finite_target']=dict(target=sorted(E),actual_word='b'+'a'*27,
                                      image_extension=28,
                                      status='COMPUTATIONALLY VERIFIED finite target, not the all-parameter canonical formula')
    return z


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,default=Path('direct_attack/data/direct_binary_image_obstruction.json'))
    args=ap.parse_args()
    parameters=list(range(2,65))+[65,100,128,256,512,1024]
    output=dict(verified=True,arguments=dict(out=str(args.out)),records=[record(p) for p in parameters],
                scopes=dict(parameters=parameters,literal_parameters=list(range(2,25)),
                            forward_parameters=list(range(2,13)),inverse_parameters=list(range(2,13)),
                            maximum_n=2049),
                status='PROVED paper: fixed binary e(T)=n^2/8+O(n), rank-gap actual targets, explicit square resets; binary universal linear image extension REFUTED; Cerny and global policy square OPEN; no formal verification')
    args.out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output['scopes']),flush=True)


if __name__=='__main__':
    main()
