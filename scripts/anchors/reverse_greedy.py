"""Test a canonical earliest-birth schedule in the reverse quotient."""
import heapq


def schedule(r, births):
    # Root singleton at0; first split at nonmerge time0.
    available=[]
    events=[0]
    heapq.heappush(available,r)
    heapq.heappush(available,r+1)
    while len(events)<births:
        ready=heapq.heappop(available)
        clock=max(ready,events[-1]+2)
        events.append(clock)
        heapq.heappush(available,clock+r)
        heapq.heappush(available,clock+r+1)
    return events,sorted(available)


def main():
    for r in range(2,41):
        events,leaves=schedule(r,r+1)
        h=(r-1).bit_length()
        A=(h+1)*r-(1<<h)+2
        # Last endpoint deadlines = A+1 (two hidden), A+2..A+r+1 (window).
        offsets=[1,1]+list(range(2,r+2))
        greedy=max(x-y for x,y in zip(leaves,offsets))
        print(r,'birth-time',events[-1],'leaf-bound',greedy,'expected',A,
              'matches',greedy==A)
    for r in range(2,41):
        events,_=schedule(r,r+1)
        j,x=0,1
        x|=2
        peak=0
        for t in range(1,events[-1]+1):
            u=int(t in events)
            assert u<=j,(r,t,j)
            out=x>>(r-1)
            j+=out-u
            x=((x<<1)&((1<<r)-1))|u
            if u:
                assert x&3==1
                x|=2
            peak=max(peak,j)
        print('realization',r,'peak-hidden',peak,'end',j,x.bit_count(),
              'full',x==(1<<r)-1)


if __name__=='__main__':
    main()
