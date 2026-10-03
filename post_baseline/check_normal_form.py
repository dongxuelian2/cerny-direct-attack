"""Adversarial optimal-path and independent finite scheduling checks."""
import random
from anchor_quotient import solve, edges
from uniform_construction import clocks


def greatest(r,K):
    A=2*K+max(d*r-(1<<(d+1)) for d in range(K.bit_length()))
    direct=[A-2*K+min((1<<(d+1))*i-d*r
                     for d in range(K.bit_length()) if (1<<d)*i<=K)
            for i in range(1,K+1)]
    backward=[0]*(K+1)
    backward[K]=A
    for i in range(K-1,0,-1):
        candidates=[backward[i+1]-2]
        if 2*i<=K:
            candidates.append(backward[2*i]-r)
        if 2*i+1<=K:
            candidates.append(backward[2*i+1]-r-1)
        backward[i]=min(candidates)
    assert direct==backward[1:]
    assert direct[0]==0
    return direct


def main():
    for r in range(1,71):
        for K in range(1,71):
            greatest(r,K)
    rng=random.Random(2026092802)
    count=ineffective=0
    for n in range(4,12):
        for r in range(2,n-1):
            d=solve(n,r)
            K=n-1
            L=(r-1).bit_length()-1
            C=L*r-(1<<(L+1))
            latest=greatest(r,K)
            assert latest[:r+1]==clocks(r)
            for trial in range(50):
                state=(n-r,(1<<r)-1)
                clock=0
                events=[]
                word=[]
                while d[state]:
                    label,target=rng.choice([(a,t) for a,t in edges(n,r,state) if d[t]==d[state]-1])
                    word.append(label)
                    before=state[0]+state[1].bit_count()
                    after=target[0]+target[1].bit_count()
                    if before>after:
                        assert label=='b' and before==after+1
                        events.append(clock)
                    else:
                        clock+=1
                        ineffective+=label=='b'
                    state=target
                reverse=[clock-t for t in reversed(events)]
                assert len(reverse)==K and clock==2*K+C
                assert all(a<=b for a,b in zip(reverse,latest))
                assert all(reverse[(1<<dd)-1]==dd*r for dd in range(L+1))
                assert all(reverse[i-1]==C+2*i for i in range(1<<L,K+1))
                assert ''.join(word).startswith('baa'*(K-(1<<L))+'b')
                count+=1
    print('Greatest relaxed schedules:',70*70,'parameter points')
    print('Optimal-path rigidity:',count,'paths;',ineffective,'ineffective b letters')
    assert ineffective==0
    # Explore every distance-decreasing reachable state/edge, not just samples.
    models=vertices=checked_edges=0
    for n in range(4,15):
        for r in range(2,n-1):
            d=solve(n,r)
            start=(n-r,(1<<r)-1)
            L=(r-1).bit_length()-1
            prefix='baa'*(n-1-(1<<L))+'b'
            prescribed = ('baa'*(n-2)+'b' if r==2 else
                          'baa'*(n-3)+'b'+'a'*r+'b' if r in (3,4) else None)
            seen={start}
            pending=[start]
            while pending:
                state=pending.pop()
                for letter,target in edges(n,r,state):
                    if d[target]!=d[state]-1:
                        continue
                    checked_edges+=1
                    position=d[start]-d[state]
                    if position<len(prefix):
                        assert letter==prefix[position]
                    if prescribed is not None:
                        assert letter==prescribed[position]
                    if letter=='b':
                        assert target[0]+target[1].bit_count()==state[0]+state[1].bit_count()-1
                    if target not in seen:
                        seen.add(target)
                        pending.append(target)
            vertices+=len(seen)
            models+=1
    print('No-wasted-b: ALL optimal-path edges in',models,'models,',vertices,'vertices,',checked_edges,'edges')


if __name__=='__main__':
    main()
