import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
all_rows = []
for n in range(5, 13):
    path = BASE / f"landmarks_C{n}" / "landmarks.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        all_rows.extend(dict(row) for row in csv.DictReader(stream))

all_rows.sort(key=lambda row: (int(row["n"]), int(row["r"])))
with (BASE / "all_landmarks.csv").open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(all_rows[0]))
    writer.writeheader()
    writer.writerows(all_rows)

by_key = {(int(row["n"]), int(row["r"])): row for row in all_rows}
summary_fields = [
    "n", "reset_threshold", "B0", "B1", "B2", "B3", "B4",
    "B_n_minus_2", "B_n_minus_1", "B_n",
]
summary = []
for n in range(5, 13):
    optimum = (n - 1) ** 2
    entry = {"n": n, "reset_threshold": optimum}
    for r in range(5):
        entry[f"B{r}"] = int(by_key[n, r]["lower_bound"])
    for label, r in (
        ("B_n_minus_2", n - 2),
        ("B_n_minus_1", n - 1),
        ("B_n", n),
    ):
        entry[label] = int(by_key[n, r]["lower_bound"])
    summary.append(entry)

with (BASE / "summary.csv").open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=summary_fields)
    writer.writeheader()
    writer.writerows(summary)

print(",".join(summary_fields))
for row in summary:
    print(",".join(str(row[field]) for field in summary_fields))
print(f"ALL_ROWS={len(all_rows)} SUMMARY={BASE / 'summary.csv'}")
