# Two-cover obstruction for a one-count immediate kernel

Use P_h for distinct pairs merged within h letters. For a letter f,
write f^*(G) for pairs with distinct f-images forming an edge of G.
Thus P_(h+1)=P1 union all f^*(P_h). Immediate collisions are included
in P1, not in f^*(G). This distinction is retained below.

## No matching in P2

In a synchronizing automaton on n>=4 states, let a two-state K cover
P5. The credited unique-immediate-pair consequence gives P1={e}, and
every letter is a permutation or a rank-n-1 map with sole kernel e.
The established P3 classification admits triangle, path4 or matching2.

Suppose P2 contains an edge d disjoint from e. P3 then is the matching
G={e,d} plus at most one crossing edge. If P2 contained that crossing,
its three-edge path would have three independent (n-2)-sets. The
finite-independent-image trap at h=2,N=3 and the P5 cover would
contradict synchronization. Hence P2=G.

For a permutation f, f^*({e}) is an edge of P2, and f^*({d}) is disjoint
from it. The only disjoint partner in P3 is the other matching edge;
a crossing edge intersects both matching edges. Thus f^*(G)=G.
For a singular f, put t=f(e). A G edge incident to t with its other
endpoint available would lift to two edges joining the two e endpoints
to the same third input. P3 has at most one crossing edge, so this
is impossible. Such an edge has no lift. Every other lifted G edge
has inputs outside e; the only possible such P3 edge is d. Therefore
f^*(G) is contained in G for every letter. P3=P2=G stabilizes forever,
contradicting synchronization. No P2 edge can be disjoint from e.
In particular P3 cannot be matching2: P2=e alone would already be a
plateau. P3 is a triangle or a four-vertex path. This argument needs
neither strong connectivity nor initial-image reachability.

## Obstruction with a one-count kernel

Let a strongly connected synchronizing automaton have a subset S of
size s>=2, put m=n-s, and suppose:

1. a two-state K covers P5;
2. c(S)>=m+8, where c(S) is its shortest compression length;
3. a two-state E satisfies |Sw intersection E|=1 for all |w|<=m+1;
4. some letter T sends both E states to the same state outside E.

These four conditions are inconsistent. The alphabet is arbitrary
finite; no reachability assumption on S is needed.

Condition4 and unique P1 give E=e. For every letter f, every Sw with
|w|<=m meets the vertex fiber f^(-1)(e) once: the appended image has
one e point and no collision, since m+1<c(S). If this fiber is a
singleton {p}, then p belongs to every image through m. The proved
mandatory-core lemma makes p isolated in P7, because
c(S)-m-1>=7. Only this conservative threshold is asserted here.

For T, the sole double output t is outside e. If both e endpoints
were available outputs, their two distinct preimages would form a P2
edge disjoint from e, impossible by the first part. T therefore omits
one endpoint x of e. The other endpoint y has a single preimage p,
which is P7-isolated. Every output except x is available. An edge
{y,q} in P6 with q!=x would lift under T to a P7 pair incident to p,
impossible. Thus y has no P6 neighbor except x.

Consequently P3 is a path y--x--z--v, with e={x,y} its end edge;
the triangle would give y two neighbors. P2 cannot equal e alone,
and cannot contain the disjoint edge {z,v}. Hence
P2={{x,y},{x,z}} exactly. Both K states are among these four active
vertices: one active point cannot cover the path.

No singular letter can generate the third edge {z,v} from P2.
To see this let f(e)=t. If t is an e endpoint and the other e endpoint
is available, lifting e produces an edge joining y to an input outside
e, which is not in P2. Hence the other endpoint must be omitted.
If t=x (so y is omitted), lifting {x,z} similarly gives a forbidden
P3 neighbor of y. If t=y and x is omitted, both P2 edges have an
omitted endpoint, so their lifts are empty.
If t is outside e, both e endpoints available would give a disjoint
P2 edge. Thus one endpoint is omitted and the other's preimage is
a mandatory singleton p, isolated in P7. Omitting x kills both P2
lifts. Omitting y leaves x,z available, so lifting {x,z} creates a
P3 pair incident to p, again impossible. This exhausts singular f.

Since P3 contains {z,v}, some permutation f must generate it. Its
e lift belongs to P2; a lift of {x,z} equal to {z,v} forces
f(z)=x, f(x)=y, f(v)=z. Put w=f^(-1)(v); it differs from x,z,v.
The edge {v,w}=f^*({z,v}) belongs to P4. If w=y, it violates y's
P6 isolation from every point except x. Otherwise w is outside the
four active vertices, hence outside K. P4 coverage gives v in K.
Put u=f^(-1)(w). The edge {w,u} belongs to P5, so u is in K.
But x,z,v map to active vertices and w is outside, so u is none of
x,z,v. Since K is active, u=y. The P5 edge {w,y} again violates
the sole-neighbor property of y. This contradiction proves the claim.

## Current application and limits

For(13,9,1), equality12 implies c(S)>=12=m+8 with m=4. First,
second and third entrance pair fibers are one-count through depths
10,9,8, respectively, and fourth pair fibers through7. When the
preceding target is a singleton outside that pair, its supplier
satisfies condition4. The explicit two-state P5 cover is required;
three-cover branches never inherit this obstruction automatically.

The graph checker exhausts every permutation and every rank-n-1 map
with a fixed kernel on n4..6. It independently checks matching
stabilization, singular path lifts and permutation path growth, with
an omitted mandatory-singleton boundary retained. These are exact
graph controls supporting the uniform written proof, not a search
over all thirteen-state automata or a new numerical F maximum.
