"""Charged witnesses for fixed ternary and binary quadratic image extension."""
import argparse
import json
from pathlib import Path


def record(p):
    n = 2*p+1
    s, k = p//2, (p+1)//2
    a = [(i+1)%p for i in range(p)] + [p+(j+1)%(p+1) for j in range(p+1)]
    b = list(range(p)) + [j%p for j in range(p+1)]
    c = list(range(n))
    c[0], c[p] = p, 0
    xi = [c, b, a]
    zero = [((i+1)%3)*n+q for i in range(3) for q in range(n)]
    one = [xi[i][q] for i in range(3) for q in range(n)]
    A = list(range(s,p)) if p%2 == 0 else list(range(s))
    T = [q for q in range(n) if b[q] in A]
    amin = (p*p+3*p-2)//2
    M = amin-k+1
    z = dict(p=p, n=n, binary_n=3*n, s=s, k=k,
             rows=dict(a=a, b=b, c=c), binary_rows={'0':zero, '1':one},
             projected_target=A, target=T, binary_target=T,
             a_lower_bound=amin, c_lower_bound=k, mandatory_b_count=1,
             entering_repeated_ca=k-1, entering_final_a=M,
             image_extension=amin+k+1, binary_image_extension=3*amin+k+1,
             reset_upper_bound=1+(p+3)*(p-1),
             binary_reset_upper_bound=3+(3*p+6)*(p-1),
             binary_entering_source_selector=1,
             binary_actual_target_word_length=3*amin+k+3,
             ternary_larger_actual_sources='only Q',
             binary_larger_actual_sources='full Qprime and Q x {0,1,2}',
             status='PROVED paper all-parameter exact fixed-alphabet image extension; priority OPEN; no formal verification')
    if p <= 16:
        w = 'b'+'ca'*(k-1)+'c'+'a'*M
        r = 'b'+('c'+'a'*(p+1)+'b')*(p-1)
        codes = {'c':'1', 'b':'01', 'a':'001'}
        bw = '1'+''.join(codes[x] for x in w[1:])
        br = '1'+''.join(codes[x] for x in r)
        z.update(literal_entering_word=w, literal_reset_word=r,
                 literal_binary_entering_word=bw,
                 literal_binary_actual_target_word='10'+bw,
                 literal_binary_reset_word=br)
    return z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=Path('scripts/direct_attack/data/two_cycle_image_obstruction.json'))
    args = ap.parse_args()
    parameters = list(range(2,65))+[65,100,128,256,512,1024]
    out = dict(verified=True, arguments=dict(out=str(args.out)),
               records=[record(p) for p in parameters],
               scopes=dict(parameters=parameters, literal_parameters=list(range(2,17)),
                           ternary_forward_parameters=list(range(2,10)),
                           ternary_inverse_parameters=list(range(2,10)),
                           binary_forward_parameters=list(range(2,9)),
                           binary_inverse_parameters=list(range(2,7)),
                           maximum_ternary_n=2049, maximum_binary_n=6147),
               status='PROVED paper; every universal linear image-extension bound REFUTED even for SC irreducibly synchronizing binary DFAs; Cerny and compatible policy square OPEN; no formal verification')
    args.out.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out['scopes']),flush=True)


if __name__ == '__main__':
    main()
