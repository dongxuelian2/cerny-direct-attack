"""Forward two-slot buffer: release particles in adjacent pairs."""


def construct(r,trace=False):
    j,x=2,(1<<r)-1
    half=False
    steps=rotations=merges=0
    events=[]
    while j+x.bit_count()>1:
        if x&3==3:
            x&=~2
            merges+=1
            events.append(rotations)
            label='b'
        else:
            t=int(half or j==2)
            assert t<=j<=1+t,(r,j,x,half)
            half=not half if t else False
            j+= (x&1)-t
            x=(x>>1)|(t<<(r-1))
            rotations+=1
            label='a'
        steps+=1
        if trace:
            print(steps,label,j,bin(x),half)
        if steps>20*r*(r.bit_length()+1):
            raise RuntimeError((r,j,x,half))
    return steps,rotations,events


def main():
    bad=[]
    for r in range(2,1001):
        value,A,events=construct(r)
        h=(r-1).bit_length()
        target=(h+2)*r-(1<<h)+3
        if value!=target:
            bad.append((r,value,target))
            if len(bad)<15:
                print('FAIL',bad[-1],events,flush=True)
    print('failures',len(bad),'first',bad[:5])


if __name__=='__main__':
    main()
