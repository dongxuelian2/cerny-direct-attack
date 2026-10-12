# Short images forced by a whole supplier group

Auxiliary pruning only. This does not establish an extremal value.

Let L be a finite overapproximation of the actual alphabet E, and let
R_1,...,R_t be supplier domains such that E meets each R_j. Suppose
every actual word of length at most H is safe for (S,A): its image has
size |S| and contains A. A known image X with depth bound d means that
there exists an actual word of length at most d sending S to X.

For every known X with d<H, any candidate letter taking X to an unsafe
image may be deleted: if it were actual, appending it to such a word
would contradict safety at depth at most d+1. This preserves E inside L.

If all remaining members of R_j have the same X-image Y, then E has a
member in R_j and hence Y is an actual image at depth at most d+1.
This is an existential statement about the image; no individual letter
is asserted to be forced. Add this depth bound and repeat the two rules.
If a supplier domain becomes empty, the conditional branch is impossible.
Finite domains and the finite collection of subset/depth pairs ensure
termination. Each deletion and each forced-image inference preserves
the actual alphabet and its actual short images, by induction.

In an equality-flag branch the supplied basis rows have actual depth
bounds 0,1,...,k, by the existing actual-image flag induction. These
are premises, not arbitrary Boolean vectors in the span. Every additional
image needs the explicit nonempty-group inference above. No safety at
depth H+1 is used; images at depth H are never used to delete letters.

The implementation uses cached masks of letters sending a source image
to each safe image. The independent checker simulates every literal
letter in each proof step. Supplied initial depth bounds must be justified
by the calling certificate. Controls do not replace this conditional proof.
