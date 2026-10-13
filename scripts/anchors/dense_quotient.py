"""Memory-efficient reverse BFS using analytic predecessors, not stored edges."""
from array import array


def solve_dense(r, m):
    N=1<<r
    d=array('i',[-1])*((m+1)*N)
    queue=array('I',[N]+[1<<i for i in range(r)])
    for s in queue:
        d[s]=0
    head=0
    lowmask=(N>>1)-1
    while head<len(queue):
        idx=queue[head]
        head+=1
        j,y=divmod(idx,N)
        newd=d[idx]+1
        t=y>>(r-1)
        low=(y&lowmask)<<1
        predecessors=[]
        if j<m:
            predecessors.append((j+t)*N+low)
        if j:
            predecessors.append((j-1+t)*N+low+1)
        if not y&2:
            if y&1:
                rest=y&~3
                predecessors.extend([j*N+rest+1,j*N+rest+2,j*N+rest+3])
            else:
                predecessors.append(idx)
        for s in predecessors:
            if s and d[s]<0:
                d[s]=newd
                queue.append(s)
    assert len(queue)==len(d)-1
    return d
