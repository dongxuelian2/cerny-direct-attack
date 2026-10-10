# Sharpness at codimension two in the compression range

**Proposition.** For n>=7 and 1<=r<=n-6 there is a binary, strongly connected, synchronizing n-state automaton with a reachable (n-2)-element image S and an r-element A subset S such that ac(S,A)=6. This equals min(n-r,binom(n-|S|+2,2)).

Set L=n-3>=4. Use states T={x_0,...,x_(L-2),z} and three additional states w,v,u. Let b cycle T in the displayed order and cycle w,v,u. Let a fix T\{z} and w, interchange z and u, and send v to z. Its only non-singleton fiber is {u,v}. The a-edges between the two b-cycles prove strong connectivity.

Put S=T union {v} and choose any r-element subset A of {x_2,...,x_(L-2)}. This set has L-3=n-6 elements, including when L=4. Until compression, describe an image by its two holes. Starting with H_0={w,u}, the following is the complete transition table needed before depth six:

| Holes | Earliest depth | Under a | Under b |
| --- | ---: | --- | --- |
| H_0={w,u} | 0 | H_1 | H_1 |
| H_1={w,v} | 1 | H_1 | H_2 |
| H_2={u,v} | 2 | H_3 | H_0 |
| H_3={z,v} | 3 | H_2 | H_4 |
| H_4={x_0,u} | 4 | H_5 | H_6 |
| H_5={x_0,v} | 5 | not needed | not needed |
| H_6={x_1,w} | 5 | compression | not needed |

Each displayed transition preserves image cardinality n-2. Induction on word length shows that every word of length at most five has one of these seven hole sets. None intersects A. Hence every word shorter than six is safe. The word ababb reaches H_6, where both u and v are present; its final a compresses. Therefore ac(S,A)=6.

Here are explicit original-letter words certifying reachability and synchronization. Let N=lcm(L,3), so b^N is the identity. The word e=a^2 is the unit v -> u, fixing all other states. The conjugate f=b^(N-1)e b is the unit u -> w. Thus k=ef collapses {w,v,u} to w and fixes T, and Qkb=T union {v}=S.

Let c=k a f a k. It sends each state in {w,v,u,z} to w and fixes T\{z}: the initial k sends the three extra states to w; z follows z -> u -> w -> w -> w through a,f,a,k. The word c(bc)^(L-1) resets Q to w. After the initial c, only states of the b-cycle T other than z remain besides w. Each bc sends the predecessor of z to z and then to w; the cyclic order ensures that all L states of T have disappeared after L-1 repetitions. Meanwhile w follows b to v and c back to w. This proves synchronization without adjoining any letter.

`defect_two.py` generates these words and transitions. `check_defect_two.py` independently verifies the transition table, complete actions of e,f,k,c, exact ac by ordinary subset BFS, strong connectivity, actual reachability and the full reset. The saved audit covers 300 parameter choices, all 7<=n<=30 and all admissible r. These are implementation checks; the proof above applies to every stated parameter.

## Codimension one

For completeness the other compression face also has a direct construction. For n>=4 let b cycle u,v,z,x_0,...,x_(n-4), and let a interchange z,u, send v to z, and fix the other states. Put S=Q\{u}. For 1<=r<=n-3 choose A inside the n-3 states {x_0,...,x_(n-4)}. The successive possible holes through depth two are u, v and z: the initial hole u goes to v under either letter; from hole v, a preserves that hole and b takes it to z. Hence all words shorter than three are safe. The word bba compresses, because after bb the hole is z and both u,v are present. Thus ac=3.

Letter b alone proves strong connectivity. The word e=a^2 is the unit v -> u. Therefore e(be)^(n-2) resets Q by the same cyclic-interval argument as in `COFINAL_PROOF.md`. Moreover Qa=Q\{v}, so Qab^(n-1)=Q\{u}=S. This proves binary sharpness 3 whenever n-r>=3. The existing first face covers r=n-2 with value 2. Together with the full-image boundary and the codimension-two proposition, every triple with n-s<=2 is determined.
