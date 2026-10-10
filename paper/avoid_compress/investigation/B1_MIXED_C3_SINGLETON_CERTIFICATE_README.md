# B1/C3 mixed singleton-third-entrance certificate

This auxiliary package contains B1_MIXED_C3_SINGLETON_EXCLUSION.md and
an independent audit. At (13,9,1), binary equality with B={4},C={0,1,5}
cannot have singleton third entrance D={6}. Initial-set reachability
is unnecessary for this negative. No unrestricted exclusion is asserted.

With Python 3.10+ and the standard library, run:

```sh
python check_b1_mixed_c3_singleton.py
```

The checker must report pass, 4,140 abstract R kernels, all 40,320 F
R permutations, and a complete literal normalized eight-state row control
with 7,776 assignments. It independently builds the set partitions and
uses forward pair BFS and ordinary strong-connectivity checks. The
symbolic graph arguments are additionally checked using all possible
unspecified thirteen-state output sets. These controls support the paper
proof; they are not a full thirteen-state transition-table search or a
new extremal bound extrapolated from small automata.

The established H cover, |P1|<=4 budget and earlier outside-kernel
obstruction are premises with proof notes included. Their larger previous
certificates remain separate prerequisites. Along with the four earlier
sole-new-point-2 exclusions, the intact inventory has 168 residual binary
typed third orbits and 927 letter-profile pairs. The joint cases stay
26 binary / 43 unrestricted; both extrema stay [11,12]. The package's
cumulative count uses those preceding exclusions but audits the new
singleton proof independently.

Remaining B1/C3 mixed D labels are {0,6},{2,6},{0,1,6},{0,2,6},{0,1,2,6}.
Here 6 is a D point; the kernel partner q in this singleton proof is
distinct and normalized to 7. The manuscript and its accepted 109-file
supplement are unchanged. CHECKSUMS.txt authenticates the original bytes,
and this standalone checker regenerates b1_mixed_c3_singleton_audit.json
byte for byte. No new F value, complete answer, solver negative or
numerical alphabet separation is claimed.
