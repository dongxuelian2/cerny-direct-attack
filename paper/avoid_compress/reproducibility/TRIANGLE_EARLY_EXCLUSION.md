# Triangle early-pair obstruction at codimension three

**Claim.** For n>=6, a strongly connected synchronizing automaton with an
(n-3)-subset of shortest compression length ten cannot have

    P1={01}, P2={01,02}, P3={01,02,12}.

The alphabet is arbitrary and finite; reachability of the subset is not
assumed. Throughout C={0,1,2}. A hole set covers P3 exactly when it is C
or is {i,j,x}, with {i,j} a core pair and x outside C. Every image reached
within six letters must have such holes, else a P3 word compresses the
original subset within nine letters.

The distinct images reached within i letters grow strictly at each step
until a compressed image is included. A plateau would be invariant under
every letter and contradict synchronization. Thus the assumptions imply
at least i+1 distinct images within i letters for 0<=i<=9.

## Letter structure

The credited short-pair refinement forces every letter to be a permutation
or a rank-(n-1) map with common kernel 01. Inverse pairs of 01 lie in P2;
inverse pairs of 02 lie in P3. A permutation therefore preserves C. A
singular letter has missing output 0 or 1. If it omits 1, inverse pairs
of 02 force it to map C onto {0,2}. If it omits 0, write its kernel
image c=f(0)=f(1) and its other core image t=f(2), with c!=t and c,t!=0.

Some permutation g satisfies g^{-1}(01)=02, since singular letters have
no two-point preimages of 01. In particular g(02)=01 and g preserves C
and its complement. Strong connectivity requires a singular letter that
does not preserve C: otherwise every letter preserves this proper set.
Such a letter omits 0. Its possibilities are:

* A: c in {1,2}, t outside C;
* B1: c outside C, t=1;
* B2: c outside C, t=2;
* C: c,t outside C.

## Case A: pure exclusion

TRIANGLE_MIXING_CASE_A.md proves this case impossible. Briefly, the domain
D_f of P3-covering holes whose f-images also cover P3 consists of C,
{0,2,v}, {1,2,v}, and all {0,1,x}, where v is the unique external
preimage of the other point in {1,2}. Its intersection with g^{-1}(D_f)
has at most four elements. All images reached within four letters must
be in that intersection, contradicting strict image growth.

## Case B1: pure exclusion

Let v be the unique external preimage of 2. Then

    D_f={C,{0,1,v}}
        union {{0,2,x},{1,2,x}: x outside C}.

Define D=D_f intersection g^{-1}(D_f) intersection f^{-1}(D_f).
All images reached within four letters lie in D: appending f, gf or ff
must still cover P3 within six letters.

The core pair 02 has at most one external choice in D, because g sends
02 to 01. For pair 12, membership in f^{-1}(D_f) forces x=v or f(x)=v,
so there are at most two external choices. The pair 01 has at most its
single choice v. The hole C belongs to f^{-1}(D_f) only if c=v. If c=v,
there is no external preimage of v (it is the kernel image), so the pair
12 has only its choice v. Thus |D|<=4 in both cases c=v and c!=v. Strict
image growth within four letters gives a contradiction.

This argument excludes B1 for every singular letter in any putative
tight triangle automaton. It is subsequently used as a necessary cut.

## Case B2: reduction to two four-image domains

Now f(2)=2. Let v=f^{-1}(1) outside C and let u=g^{-1}(v), also outside
C. Again D_f consists of C, {0,1,v}, and all {0,2,x},{1,2,x}. Put

    D=D_f intersection g^{-1}(D_f)
          intersection f^{-1}(D_f) intersection (fg)^{-1}(D_f).

The tests correspond to f,gf,ff,fgf, all of length at most three.
Every image reached within three letters therefore lies in D.

The following direct restrictions hold:

* C is in D only if c=u (test fgf);
* {0,1,v} is in D only if c=v (test ff);
* core pair 02 has at most external choice u (test gf); it further
  requires u=v or f(u)=u (test fgf);
* core pair 12 has at most external choices v and w=f^{-1}(u), where
  w is included only if it exists outside C (test fgf).

If c=u, w does not exist outside C, since u is then the kernel image.
If c!=u, C is absent. These restrictions give |D|<=4. Strict growth
forces equality and all four domain images to be reached within three
letters. Equality has only two possibilities:

1. c=u=v. Then D is {012,01v,02v,12v}.
2. c=v!=u and f(u)=u. Then D is {01v,02u,12v,12u}.

Every letter must send every image in D to a P3-covering image: each
was reached within three letters. In particular the letter assumptions
A and B1 are excluded by the pure arguments above.

Complete projection of every remaining compatible letter onto the first
domain gives 11 actions. Every domain image must eventually exit under
synchronization. Four finite exit distances are at most four, and a first
distance four requires a permutation of 1,2,3,4. All 24 vectors are checked:
none permits every vertex to exit. Thus the first exit distance is at
most three. Leaving D fails one of the defining tests of length at most
three; a further P3 word of length at most three compresses within nine.

For the second domain, the complete projection gives 38 actions. Of the
24 distance vectors, exactly three permit every vertex to exit:

    (2,3,4,1), (3,4,1,2), (4,3,1,2).

For each of these vectors every compatible letter satisfying its exit
inequalities maps the five-state set C union {v,u} into itself. This
is verified for every literal core-row template, not only for a selected
representative of each projected action. Every actual alphabet having
first exit distance four is included among those compatible actions.
Consequently C union {v,u} is invariant, contrary to strong connectivity
when n>=6. Otherwise first exit is at most three, again compressing within
nine. This is why the claim's state range is n>=6; the invariant set has
five states. No tight-compression-ten claim at n=5 is made here.

## Case C: a six-image domain

Let v_1,v_2 be the distinct external preimages of 1,2. The domain D_f is
exactly the six holes formed by one core pair and one of v_1,v_2; C itself
is not in D_f. Every image reached within five letters lies in D_f, because
its f-image reached within six letters must cover P3. Strict growth gives
all six domain images by depth five. Every letter sends every domain
image to a P3-covering image.

The complete compatible projection gives 61 actions. Synchronization
requires finite exit distances for all six domain images; each is at most
six. A first distance six requires a permutation of 1,...,6. All 720
vectors are checked, and none permits every vertex to exit. The first
exit thus has length at most five. Appending f leaves the P3-covering
family and a word of length at most three then compresses. Total length
is at most 5+1+3=9, a contradiction.

## Complete finite projections and independent checks

For any hole domain above, only the letter's images of the distinguished
states, and its missing output, matter. Permutations preserve C and are
bijections on the outside. Singular maps omitting 1 preserve C. Singular
maps omitting 0 with both core images inside C are also included. After
excluding A and B1, mixing possibilities B2 and C remain. The requirement
that every domain image still cover P3 forces every necessary external
preimage of 1 or 2 to be among the distinguished outside points. The code
enumerates its choice explicitly. All other represented external images
are distinct outside values; at most two fresh outside labels are needed.

triangle_reduced_actions.py enumerates these inverse/structural cases and
computes the projected holes. It scans all distance permutations, adds ALL
actions satisfying d(v)<=1+d(f(v)), d(EXIT)=0, and checks reverse exit
closure. Adding these actions cannot shorten the asserted lower distances.
For the three surviving B2 vectors it checks closure of the five-state
set for every underlying partial row.

audit_triangle_actions.cpp independently enumerates every forward partial
row on four or five represented states with five or seven output labels.
It tests all early inverse pairs literally, the separately proved A/B1
cuts, and the P3-covering image requirement. It checks exit by a forward
search from each vertex. All profiles, every profile's row-closure flag,
all distance vectors and all candidates coincide with the Python output.
The reports are triangle_reduced_actions.json,
triangle_actions_independent.json and codimension_three_upper_audit.json.

There is also an actual reachable, strongly connected synchronizing
five-state positive control with rows

    f=(3,3,2,1,4), g=(0,2,1,4,3), h=(1,0,2,3,4).

For S={2,4}, its first exit from the second four-image domain is four.
Ordinary forward BFS checks this and gives actual compression length NINE.
It is a positive control of the projected distance-four check, not a
compression-ten witness or a new exact maximum. This control prevents
mistaking projected exit distances for compression lengths.

## Scope