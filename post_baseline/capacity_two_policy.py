"""FAILED ROUTE: greedy policy; now explicitly rejects unrealizable inputs.

Earlier exploration checked only 0<=new_hidden<=2, which is insufficient.
The added precondition detects the error. No outputs of this policy support
the theorem; use uniform_construction.py for the proved construction.
"""


def construct(r):
    full=(1<<r)-1
    x,j=3,0
    births=1
    clock=0
    times=[0]
    while (x,j)!=(full,2):
        outgoing=x>>(r-1)
        want_birth=births<r+1 and not x&1
        u=int(j>0 and (want_birth or j+outgoing>2))
        assert u<=j<=1+u,('unrealizable reverse input',r,clock,j,u)
        j=j-u+outgoing
        assert 0<=j<=2
        x=((x<<1)&full)|u
        clock+=1
        if births<r+1 and x&3==1:
            births+=1
            x|=2
            times.append(clock)
        if clock>20*r*(r.bit_length()+1):
            raise RuntimeError((r,x,j,births))
    return clock,births,times


def main():
    bad=[]
    for r in range(2,2001):
        try:
            A,births,times=construct(r)
        except (AssertionError, RuntimeError) as error:
            print('REJECTED POLICY:',error,flush=True)
            return
        h=(r-1).bit_length()
        target=(h+1)*r-(1<<h)+2
        if A!=target:
            bad.append((r,A,target,times))
            if len(bad)<=10:
                print('FAIL',bad[-1],flush=True)
    print('failures',len(bad),'first',bad[:2])


if __name__=='__main__':
    main()
