"""Cofinal extension of the manuscript's larger-gap construction.

Rows and symbolic original-letter certificates only. The independent audit
in check_cofinal.py verifies the finite controls; the uniform proof is separate.
"""
def construct(r,g,M):
    assert r>=1 and g>=2 and M>=2*g+1
    h=1+(M-1)%g
    assert 1<=h<=g and M>=2*g+h
    p=r+1;n=p+M;s=p+g
    a=list(range(n));b=list(range(n))
    b[0]=p+h-1
    for q in range(1,p):b[q]=q-1
    for j in range(1,M+1):
        q=p+j-1
        a[q]=p+j if j<M else p+h
        if (j-h+1)%g==0:b[q]=r
        elif h>=2 and j==g:b[q]=p
        elif j==M:b[q]=p+h+g-1
        else:b[q]=p+j
    return dict(r=r,g=g,M=M,h=h,n=n,s=s,rows=[a,b],S=list(range(s)),A=list(range(r)),
                reaching=[['b',g+1]],attaining=[['a',M-g],['b',g+1]],
                unit=[['a',M-h],['b',s]],
                reset_prefix=[['b',g+1]],reset_program='c (b c)^(s-2)',
                reset_length=g+1+(s-1)*(M-h+s)+(s-2))

def expand(program):return ''.join(letter*count for letter,count in program)

def reset_word(z):
    c=expand(z['unit'])
    return expand(z['reset_prefix'])+c+('b'+c)*(z['s']-2)

def boundary(r,g):
    assert r>=1 and g>=2
    M=2*g;p=r+1;n=p+M;s=p+g
    a=list(range(n));b=list(range(n));b[0]=p+g-1
    for q in range(1,p):b[q]=q-1
    for j in range(1,M+1):
        q=p+j-1;a[q]=p+j%M
        b[q]=r if j%g==g-1 else (p+j if j<M else q)
    reaching='b'*(g+1)+'a'*(g-1)+'b'*s+'a'*g
    d='a'*(g-1)+'b'*s;e=d*g
    reset='b'*(g+1)+e+('b'+e)*(s-1)
    return dict(r=r,g=g,M=M,n=n,s=s,rows=[a,b],S=list(range(s)),A=list(range(r)),
                reaching_word=reaching,attaining_word='a'*g+'b'*(g+1),
                root_unit=e,reset_word=reset)
