# Conditional compulsory-letter splitting

The actual alphabet E is contained in the current literal pool L and
meets each required domain R_j. Pick a domain with two or more members.
Every actual E contains some a in R_j. Cover every such a by a branch
that adds the singleton requirement {a}. Overlapping branches are allowed:
E may contain several members and is then covered more than once.

In each branch, the singleton requirement justifies safe-image propagation
from the already justified actual prefix images, with their depth bounds.
The existing propagation proof applies without change. A branch closes
only when a required domain becomes empty or a complete obligatory-letter
product supplies explicitly checked unsafe words within the horizon.
If every branch closes, every possible actual alphabet is excluded under
the stated safety premises. Any unclosed branch makes the routine return
no cut. The independent checker reconstructs the entire split domain,
tests exact branch coverage and replays all image and word certificates.

The generator's caps (512 active letters, at most four split choices) only
skip cuts. They are not hypotheses of the conditional argument. No numerical
extremum, alphabet separation or complete geometry is asserted here.
