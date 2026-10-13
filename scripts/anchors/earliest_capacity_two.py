"""Explore earliest optimal clocks with forced unpaired inputs; not a proof."""


def earliest(r,K=None):
    K=K or r+1
    s=[0]*(K+1)
    for i in range(2,K+1):
        s[i]=max(s[i-1]+2,s[i//2]+r+i%2)
    return s[1:]


def check(r):
    s=earliest(r)
    events=set(s)
    full=(1<<r)-1
    j,x=0,1
    idle=[]
    for t in range(s[-1]+1):
        if t:
            u=int(t in events or j==2)
            if not u<=j<=1+u:
                return ('input',t,j,u),idle
            out=x>>(r-1)
            j=j-u+out
            x=((x<<1)&full)|u
            if u and t not in events:
                idle.append(t)
        if t in events:
            if x&3!=1:
                return ('split',t,j,x&3),idle
            x|=2
    if (j,x)!=(2,full):
        return ('endpoint',j,full^x),idle
    return None,idle


def main():
    successes=0
    for r in range(2,1001):
        fail,idle=check(r)
        if fail:
            print('FAILED r',r,fail,'idle inputs',idle[:20],flush=True)
            break
        successes+=1
    print('Successful earliest schedules:',successes)
    for r in [5,9,17,33,65,129,257]:
        print(r,check(r))


if __name__=='__main__':
    main()
