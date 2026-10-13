"""Explicit seed preparation; no theorem or upper-bound inference."""
import json
from pathlib import Path
from cofinal_family import construct, boundary

ROOT = Path(__file__).resolve().parent

def main():
    for n in (11,12):
        pairs = []
        for name in (f"reuse_n{n}.json", f"structured_n{n}.json",
                     f"active_n{n}_h4.json", f"active_n{n}_h5.json",
                     f"active_n{n}_h6.json", "subdivide_probe.json",
                     "binary_obstruction_witness.json",
                     f"mutate_n{n}_s7_r1_k2.json",
                     f"mutate_n{n}_s8_r1_k2.json"):
            path = ROOT/name
            if not path.exists():
                continue
            data = json.loads(path.read_text())
            records = data.get("results",data.get("certificates",[data]))
            for z in records:
                rows = z.get("rows",[])
                if len(rows)==2 and all(len(row)==n for row in rows):
                    pairs.append(rows)
        for r in range(1,n-4):
            M=n-r-1
            for g in range(2,M//2+1):
                z=boundary(r,g) if M==2*g else construct(r,g,M)
                pairs.append(z["rows"])
        # Single-edge extensions of all checked previous-size automata.
        previous=json.loads((ROOT/"formula_certificates.json").read_text())["certificates"]
        if n==11:
            previous=[z for z in previous if z["n"]==n-1]
        else:
            previous=[dict(n=11,rows=rows) for rows in pairs if len(rows[0])==11]
            previous.append(json.loads((ROOT/"binary_obstruction_witness.json").read_text()))
            newly=ROOT/"mutate_n11_s7_r1_k2.json"
            if newly.exists():
                previous.append(json.loads(newly.read_text()))
        for z in previous:
            for letter in range(2):
                for source in range(n-1):
                    rows=[row+[n-1] for row in z["rows"]]
                    rows[letter][n-1]=rows[letter][source]
                    rows[letter][source]=n-1
                    pairs.append(rows)
        pairs=list({tuple(tuple(row) for row in rows): rows for rows in pairs}.values())
        for k in (2,3):
            rows_list = pairs if k==2 else [
                rows+[third] for rows in pairs
                for third in (list(range(n)),rows[0],rows[1])]
            path=ROOT/f"mutation_seeds_n{n}_k{k}.txt"
            path.write_text(str(len(rows_list))+"\n"+
                            "\n".join(" ".join(map(str,[q for row in rows for q in row]))
                                      for rows in rows_list)+"\n")
            print(json.dumps(dict(n=n,alphabet_size=k,seeds=len(rows_list))))

if __name__=="__main__":
    main()
