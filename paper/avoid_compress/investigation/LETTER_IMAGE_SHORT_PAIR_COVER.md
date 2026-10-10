# Passing a short-pair cover through a letter

Let P_h be the graph of distinct pairs merged by words of length at
most h; P_0 is empty. For any complete deterministic automaton, any
letter f, and any vertex cover K of P_(h+1), h>=0,

    f(K) union (Q minus Qf) covers P_h.                    (1)

Indeed, if a P_h edge {x,y} avoids both displayed sets, choose
preimages p,q of its endpoints under f. They are distinct, outside K,
and their pair merges by f followed by a word of length at most h.
This contradicts the cover of P_(h+1). No injectivity, synchronization,
strong connectivity, image reachability or alphabet restriction is
needed for (1). Omitted output states must be retained.

Now assume n>=4, synchronization, and a two-state K covering P5.
TWO_COVER_UNIQUE_IMMEDIATE_PAIR.md, a credited application of the
known compression refinement, implies every letter has rank at least
n-1. Also P3 has no cover of size at most one: this follows from the
proved TWO_COVER_P3_CLASSIFICATION.md (or the one-cover compression
floor). Consequently no letter sends both K states to isolated
vertices of P3. Otherwise use (1) at h=3 and remove the isolated
vertices in f(K). Q minus Qf, of size at most one, covers P3, a
contradiction. The two K states may have the same image; (1) does not
count images with multiplicity.

This is an auxiliary cover observation and a necessary restriction,
not an extremal F formula or a new compression-bound claim. The
checker independently tests (1) on all labelled four-state maps and
graphs and on literal short-pair graphs in complete small binary and
ternary domains. It also checks the forbidden-image consequence and
retains an example showing why omitted outputs cannot be dropped.
