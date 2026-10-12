# Combining a compulsory supplier with a connectivity escape

This is an auxiliary conditional pruning rule, not an extremal theorem.

Let L contain the actual alphabet E. Assume E meets every nonempty
supplier domain R_j in L and every actual word of length at most H
is safe for (S,A). A singleton R_j forces its unique literal letter;
let F collect all such forced letters.

First consider two obligatory domains R_j,R_k. If every pair b in R_j,
e in R_k has an unsafe literal word over F union {b,e} of length at
most H, the branch is impossible. The actual alphabet contains some
actual choices b,e, and the corresponding word is an actual unsafe word.
This part needs neither connectivity nor synchronization.
The identical argument applies to a product of three obligatory domains.
The implementation tests such a product only when one domain has at
most two members; this is a conservative heuristic, not a proof premise.

Alternatively suppose every letter in F fixes
state q. Strong connectivity requires some e in E with qe!=q.
Choose any other obligatory domain R_j. The actual alphabet contains
some b in R_j and some e in L escaping from {q}.

If for EVERY such pair (b,e) a literal word over F union {b,e} of
length at most H is unsafe, the branch is impossible. The word may
depend on the pair. It is an actual word of E for the actual choices,
contradicting safety. This proves the rule for every finite alphabet.

The implementation skips large products and returns no cut when a
pair has no found word. These are conservative search choices. A cut
stores every pair and its explicit word. The independent checker
reconstructs both domains, checks nonempty premises and the entire
Cartesian product, and simulates each word on ordinary sets. No
incomplete product, merely nonsynchronizing model, or solver timeout
supplies a cut. No word beyond H is used.
