# Known compression bound and protected-cover stripping

This auxiliary certificate excludes joint b1_in_c2, B={0},C={1},
at(13,9,1) for every finite alphabet. It also excludes eight further
third-profile orbits beyond that joint. It invokes the existing
Frankl--Pin bound, independently checked in Szykula2018, Theorem1;
neither that bound nor its cover-floor corollary is claimed novel.

With Python3.10+ and the standard library, run:

```sh
python check_compression_cover_floor.py
```

The checker independently covers all43 original joint orbits and
4,806 labelled ordered pairs. Six labelled pairs give the newly
excluded whole joint. It separately computes actual-image family
intersections by bit masks for all235 B1/B2 third orbits, all1,482
labelled D choices, and177,512 literal nine-set intersection tests.
Eleven third orbits are excluded: three within the whole joint and
eight additional. Thirty labelled D choices within their canonical
B,C profiles are excluded. This third inventory does not include B3.

Complete small controls are all ordered binary rows at n=2,3,4
(16,729,65,536 assignments), and ternary rows at n=3(19,683).
Independent actual-subset BFS checks compression against shortest
pair distances on the first64 qualified models per domain. All290
verified frontier examples (147 distinct row models) satisfy the cut
and the protected-pair bound. Another300 seeded larger-alphabet
controls propose n=4..9,alphabet2..4;152 are strongly connected and
synchronizing. None of these finite controls replaces the symbolic
proof or is a complete13-state transition-table scan.

The D one-count condition holds through eight, so its forced points
are isolated in P4. They are stripped from the P4 cover, not silently
from P5. Additional Boolean fibers may further restrict image forms
and never weaken their mandatory intersection. Auxiliary sets need
not be reachable: the cited compression theorem covers all subsets.

Composition leaves23 binary /42 unrestricted joint cases and152
binary typed third orbits /784 earlier pairs. Both F extrema remain
[11,12]; no numerical alphabet separation or complete answer follows.
The article and109-file release are unchanged. A primary-source title
typo in the existing bibliography is recorded for the next rebuild.

CHECKSUMS.txt authenticates all bytes. The standalone generator and
checker regenerate their JSON outputs byte for byte. Prerequisite
equality/cover proof notes are included; complete earlier certificates
remain separate.
