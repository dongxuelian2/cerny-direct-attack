"""Independent product enumeration of normalized integer arrays."""
from itertools import product
from check_language_stabilization import schedules


def main():
    for L in (2,3):
        p=1<<L
        free=[i for i in range(1,p) if i&(i-1)]
        bounds={i:2*(i-(1<<(i.bit_length()-1)))*((1<<(L-i.bit_length()+1))-1)
                for i in free}
        vectors=[]
        for values in product(*(range(bounds[i]+1) for i in free)):
            z=[0]*(2*p)
            for i,value in zip(free,values):
                z[i]=value
            if any(z[i]>z[i+1] for i in range(1,p-1) if (i+1)&i):
                continue
            if any(z[i]>z[2*i]+2*(i-(1<<(i.bit_length()-1))) for i in range(1,p)):
                continue
            vectors.append(z)
        count=len(vectors)
        assert count==(3 if L==2 else 279)
        for r in (2*p-2,2*p-1,2*p):
            mapped=set()
            for z in vectors:
                s=[]
                for i in range(1,r+2):
                    d=i.bit_length()-1
                    s.append(d*r+2*(i-(1<<d))+z[i] if i<p else L*r+2*(i-p))
                mapped.add(tuple(s))
            expected={tuple(s) for s in schedules(r)}
            assert mapped==expected
        print('C_'+str(L),count,'independent normalized arrays; three bijections checked')


if __name__=='__main__':
    main()
