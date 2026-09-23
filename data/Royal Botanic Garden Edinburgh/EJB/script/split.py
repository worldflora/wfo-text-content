import pandas as pd
import csv
from pathlib import Path

# === Load main descriptions CSV ===
df = pd.read_csv(
    "data\\Royal Botanic Garden Edinburgh\\EJB\\work\\argent_Misc_vaccin.csv",
    sep=",",
    encoding="utf-8",
    dtype=str,
    low_memory=False
)

df.columns = df.columns.str.strip()

# === Output folder ===
out_dir = Path("data\\Royal Botanic Garden Edinburgh\\EJB\\out")
out_dir.mkdir(exist_ok=True)

# === Get all unique types ===
types = df["type"].dropna().unique()

print("\n=== Splitting CSV by type ===")

for t in types:
    subset = df[df["type"] == t]

    outfile = out_dir / f"EJB_{t}.csv"

    subset.to_csv(
        outfile,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL
    )

    print(f"Saved: {outfile}")

print("\n=== Done ===")
