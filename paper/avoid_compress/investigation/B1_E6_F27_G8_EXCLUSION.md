# Complete binary E6/F27/G8 exclusion

Conditional at n=13, |S|=9, ac(S,{3})=12, B0/C14/D5/E6/F27/G8.
The seventh inventory gives H9,H12,H17,H19,H24,H29,H129.
B1_F27_G8_SEVENTH_ENTRANCE.md excludes the four crossed types for
all alphabets and H19 for binary alphabets. H9,H29 need full row scans.
Both independent implementations report zero survivors on the complete
normalized domains described below. Hence every binary target in this
conditional sixth geometry is excluded. No unrestricted-alphabet
exclusion of this whole geometry follows.

Targets A,B,C,D,E,F,G,remainder are3,0,14,5,6,27,8,9-12, with
capacities1,1,2,1,1,2,1,4. Mandatory cores are0,3,5,6,8,9 for H9 and
0,3,5,6,8 for H29. F27 has one-count but its points2,7 are not
individually protected. Both literal families contain12 nine-sets.

Every row maps each preimage input to the designated target field.
Outside-K inputs in each field are injected: any collision of two
such inputs would violate K covering P5. Guard inputs1,2 may choose
any output not already used by a mandatory input; neither may collide
with a mandatory input. These are exactly the immediate-cover and
mandatory-isolation constraints. Independent Python target-field
injections and C++ named-input recursion enumerate the same sorted
raw domain. Every valid full automaton row is represented.

Single-letter cuts reject protected pairs merging by powers through7,
pairs with both points outside K merging by powers through5, and rows
having no literal initial nine-set whose powers are safe through11 and
stay in the literal family through4. These are necessary constraints.
The literal image-family intersection, together with strong connectivity
and the mandatory-core lemma, justifies protected P7 even though some
extra powers are evaluated beyond the family depth.

Two independent coupled algorithms check every retained manifest pair.
The first uses forward/reverse reachability from0 for strong connectivity
and reverse preimage BFS in the78-state pair graph. The second uses
Boolean transitive closure and scalar forward pair-distance relaxation.
They use different cut orders but identical complete candidate domains.
All-pair mergeability is equivalent to synchronization: merging any
pair in a non-singleton current image reduces that image, and repeating
this operation gives a reset word. Conversely, a reset word merges
every pair.
Control rows cycle/identity, cycle/constant, identity/constant separately
check nonsynchronizing, synchronizing and non-strongly-connected cases.
Controls disable conditional short-pair cuts, which are enabled only
for the classified actual domains.

Actual models would additionally need a common safe S and Q-to-S
reachability. A negative at the earlier necessary-pair stage suffices;
uninvoked reaching/prefix algorithms do not establish a model.
No finite-time timeout or necessary field admission proves a negative.
Unrestricted alphabets are not covered by a two-row search.


## Complete domains and independent negative counts

| H | field rows | parent field pairs | raw rows | retained rows | raw pair product | checked pairs per implementation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 9 |128|1094|25920|11376|31647744|5859072|
| 29 |80|162|11712|5376|1935360|241920|

Both generators agree on every sorted raw row via a canonical SHA-256
hash. The independent scalar checker also agrees on every retained
row and its initial-image mask. The208 field rows and1256 parent
field pairs are copied and reconstructed separately from the inventory.
The entire raw pair domain has33,583,104 pairs. Necessary single-letter
cuts reduce it to6,100,992; both coupled implementations exhaust that
retained domain. Their separate histograms cover every checked pair.
No pair survives to the additional prefix/reachability checks.

Fresh points9-12 form one symmetry cell; each of the four choices of
fresh point in H9/H19/H29/H129 is obtained by a permutation fixing
A,B,C,D,E,F,G,K. All field restrictions, actual family conditions,
short-pair bounds and state graph tests commute with this permutation.
Thus scanning each canonical H representative covers all its labels.
The independent rank checker separately tests all19 literal labels.
When parent letter fields coincide, unordered field-pair symmetry is
valid by interchanging the binary letters; each same-field product is
fully retained, including equal transformations.

The four crossed H cases and binary H19 were proved separately. Their
union with H9/H29 is exactly all seven admitted geometries. Consequently
binary E6/F27/G8 is excluded, including all365 original sixth field pairs.
The other four crossed G types in E6/F27 were already excluded for all
alphabets in B1_SIXTH_ENTRANCE.md. Residual binary E6/F27 therefore has
G18/G28 only:two geometries/ten labels/105 sixth field pairs, covering
93 of122 original fifth field pairs. The other29 fifth pairs cannot
extend in any sixth geometry and are eliminated under this same binary
conditional branch. All14 third and41 fourth parent pairs remain covered.
No whole F27, E6, third or joint geometry is removed.

Unrestricted E6/F27/G8 still retains H9/H19/H29,three geometries/twelve
labels. H19's two-letter argument explicitly needs binary role coverage;
a third letter could supply additional incoming C edges. The two-letter
negative scans likewise do not cover larger alphabets. Both F(13,9,1)
intervals remain[11,12], with no numerical alphabet separation established.

Run enumerate_b1_f27_g8_seventh.py, check_b1_f27_g8_seventh.py,
enumerate_b1_f27_g8_rows.py and check_b1_f27_g8_rows.py in that order,
with Python>=3.10, assertions enabled and a C++17 compiler. This is an
auxiliary conditional proof; the accepted article and109-file supplement
remain unchanged. The minimal package reruns these new reductions and
scans, while its explicitly named upstream classification/core premises
are separately certified and are not all rerun by this package.
