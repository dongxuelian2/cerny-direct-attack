"""Editorial replacement of the finite-base section by its uniform proof."""
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
path=ROOT/"main.tex";tex=path.read_text(encoding="utf-8")
section=(ROOT/"investigation/TWO_BLOCK_SECTION.tex").read_text(encoding="utf-8")
section=section.replace("$D$","$\\Phi$").replace("D(E","\\Phi(E")
start=tex.index("\\section{Two exact codimension-four bands}")
end=tex.index("\\paragraph{Reproducibility and scope.}",start)
tex=tex[:start]+section+"\n"+tex[end:]
tex=tex.replace("A protected-state extension determines two infinite codimension-four bands.",
                "A uniform two-block construction determines every parameter with $m=n-|S|\\ge3$ and $2m+2\\le n-|A|\\le3m-1$.")
tex=tex.replace("$180$ codimension-three instances through $n=24$, and $39$ protected extensions\nthrough $n=31$, with $210$ further choices of protected subsets and the complete\n$62$-vertex base certificate.",
                "$180$ codimension-three instances through $n=24$, and $221$ two-block instances\nthrough $n=65$. The latter use ordinary subset breadth-first search in $216$ cases\nand checked pair-potential and cell-delay certificates in the five larger cases.")
# The printed extra point is now an immediate special case of the theorem;
# keep its finite literal certificate in the frontier regression data.
start=tex.index("An additional checked binary witness gives")
end=tex.index("The binary obstruction rules out",start)
tex=tex[:start]+"In particular Theorem~\\ref{thm:two-block} gives $\\Max_{\\rm bin}(13,8,1)=\\Max(13,8,1)=12$.\n"+tex[end:]
path.write_text(tex,encoding="utf-8")
print("uniform proof embedded")
