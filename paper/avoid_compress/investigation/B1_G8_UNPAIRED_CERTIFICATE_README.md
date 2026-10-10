# Complete binary E6/F7/G8 exclusion: the remaining H9/H29

This21-file auxiliary package treats only n=13, |S|=9,
ac(S,{3})=12, B0/C14/D5/E6/F7/G8. Its new contribution is a
complete exclusion of binary H9/H29, completing the seven conditional
H cases for this G8 geometry. It supplies no new extremal F value.

Use Python>=3.10, standard library only, assertions enabled, and a
C++17 compiler. Set CXX to the executable if clang++/g++ is not on PATH:

    python -B enumerate_b1_g8_unpaired_rows.py
    python -B check_b1_g8_unpaired.py

The two data files and one audit reproduce byte-identically.
CHECKSUMS.txt authenticates the other20 files. Compilation and full
temporary row lists are created in an adjacent _qa directory; these
large generated lists are omitted from the package. Both C++ programs
use explicit runtime checks, not removable assert. The canonical raw
and retained row lists have portable LF bytes and independently checked
SHA-256 hashes; per-field row counts and all initial-set masks agree.

The earlier seventh geometry/Boolean inventory, core-isolation theorem,
and four paired-H exclusions are included as explicit premises (notes
and audit reports). This package does not rerun all earlier source
classifications, the core lemma's exhaustive small-automaton controls,
or the prior663,552,000 paired-H scan. Those are supplied in the earlier
mandatory_core_seventh and b1_e6_f7_g8_seventh certificates. The present
package reproduces every new row domain and both new full coupled scans;
it does not silently replace the stated upstream proof premises.

Every128 field row and1094 original binary field pair is retained per
geometry. The Python generator injects outside-K inputs field by field
and assigns guards to every allowed output. C++ instead assigns each
named input in order and rejects exactly forbidden immediate equalities.
Both enumerate280,800 raw individual rows. Necessary single-letter
pair-isolation, cover and actual pure-power image checks retain39,672
rows for H9 and32,856 for H29. Every actual equality model survives
these cuts. No rank bound or ordinary representative permutation is fixed.

The raw field-pair products sum2,045,318,400. Each of two independently
implemented algorithms completely checks the remaining110,203,776
normalized pairs (91,664,640 H9;18,539,136 H29). The first uses forward/
reverse state reachability and reverse pair-preimage closure; the other
uses Boolean transitive closure and simultaneous forward pair-distance
relaxation to a fixed point. Cut order differs; both scans have zero
survivors. Positive and negative state/pair-algorithm controls are run
with branch-specific cuts disabled; every geometry scan enables all cuts.
No timeout, limited pair depth or failure to find a word certifies a negative.

With the earlier H2 and four paired-H exclusions, binary E6/F7/G8 is
excluded completely. Binary E6/F7 retains G28 (365 sixth field pairs),
and selected sixth admission is now7 geometries/35 labels/1278 pairs.
All122 original fifth pairs remain covered in that branch. Other
fifth/third/joint branches remain, and the unrestricted G8 geometry is
not excluded by a binary scan. Both F(13,9,1) maxima remain[11,12],
with no numerical alphabet separation. The article and its109-file
formal supplement/release are unchanged.
