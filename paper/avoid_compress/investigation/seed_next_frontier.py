"""Local stochastic seeds from audited n=12 automata; not proof data."""
import json
from pathlib import Path
from protected_padding import construct

ROOT=Path(__file__).resolve().parent
rows=[];seen=set()
for z in json.loads((ROOT/"frontier_certificates.json").read_text())["certificates"]:
    if z["n"]!=12:continue
    key=tuple(tuple(row) for row in z["rows"])
    if key not in seen:seen.add(key);rows.append(z["rows"])
seeds=[];seen=set()
for old in rows:
    for letter in range(2):
        for q in range(12):
            out=[row+[12] for row in old]
            target=out[letter][q];out[letter][q]=12;out[letter][12]=target
            key=tuple(tuple(row) for row in out)
            if key not in seen:seen.add(key);seeds.append(out)
seeds.append(construct(11,2)["rows"])
for k in (2,3):
    candidates=seeds if k==2 else [rows+[list(range(13))] for rows in seeds]
    path=ROOT/f"mutation_seeds_n13_k{k}.txt"
    path.write_text(str(len(candidates))+"\n"+"\n".join(
        " ".join(str(q) for row in rows for q in row) for rows in candidates)+"\n")
    print(path.name,len(candidates))
