# Two-root unrestricted D12 conditional certificate

This auxiliary package excludes B0/C4/D12 and B4/C0/D12 at (13,9,1),
conditional on equality12 and the accepted entry/P5-cover premises.
It applies to arbitrary finite alphabets and hence binary alphabets.
It does not determine either F(13,9,1), exclude either whole B/C joint,
or prove alphabet separation. Both extrema remain [11,12].

Read C4_D12_UNRESTRICTED_EXCLUSION.md for both paper branch proofs and
SINGLETON_C_D12_UNRESTRICTED_EXCLUSION.md for complete composition.
All16 E5 and12 E15 fields are included; supplier overlap is retained.
E5 first forces full-image coverage of O, then uses a last entrance
and the closed-block lemma. E15 forces a guard barrier using either
a mandatory-pair contradiction or an outside-K pair contradiction.
Every one of the48 labelled E extensions across the two roots is
independently checked, including guard swaps and ordinary relabelings.
No Boolean companion or larger-alphabet letter is omitted.

Python >=3.10, standard library only. Do not disable assertions.

    python -B enumerate_b1_c4_fourth.py
    python -B check_b1_c4_fourth.py
    python -B enumerate_c4_d12_unrestricted.py
    python -B check_c4_d12_unrestricted.py
    python -B check_singleton_c_d12_unrestricted_composition.py

These regenerate three data files and three audits byte-identically.
Distinct generators reconstruct all7,328 individual rows at n6..9.
All135,616 ordered binary alphabets with both suppliers at n6..8
are checked, including one letter supplying both D and E. Another
48,000 seeded larger alphabets support the proof, without providing
a negative mathematical theorem. Every constructive short word is
evaluated directly and checked against reverse pair BFS; E5 closed
cases are independently checked as nonsynchronizing.

The actual n13 E5 initial family has70 literal sets and bit69 is
explicitly retained with Python integers. No uint64 family mask is
used. Structural SC/sync boundary controls have (J-pair,R-pair)
depths (3,3) for E5 and (7,3) for E15. The latter shows why mandatory
isolation through four alone is insufficient for that proof: the
outside-K pair condition must also be used. These controls are not
attaining F witnesses.

Earlier local/entry, mandatory-core, small-third, common-block and
closed-block sources are fixed premises. The historical common-block
report distinguishes five already excluded parent pairs in each root
from eighteen newly removed pairs. Its bound source bytes are included;
the commands do not rerun every historical audit. Two earlier checker
modules supply only generic graph/rank functions and are included.
CHECKSUMS.txt binds all bytes. The accepted article and release remain
unchanged; earlier notes listing these D12 types as unresolved are
historical and superseded by this proof.
