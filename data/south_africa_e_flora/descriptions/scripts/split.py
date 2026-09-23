import pandas as pd
import csv
from pathlib import Path

# === Load main descriptions CSV ===
df = pd.read_csv(
    r"data\south_africa_e_flora\descriptions\raw\dwca-flora_descriptions-v1.42\description.txt",
    sep="\t",
    encoding="utf-8",
    dtype=str,
    low_memory=False
)

df.columns = df.columns.str.strip()

# === Load reference file ===
ref = pd.read_csv(
    r"data\south_africa_e_flora\descriptions\raw\dwca-flora_descriptions-v1.42\reference.txt",
    sep="\t",
    encoding="utf-8",
    dtype=str
)

ref.columns = ref.columns.str.strip()

# === Deduplicate ===
ref = ref.drop_duplicates(subset="identifier")

# === Merge bibliographicCitation into main dataframe ===
df = df.merge(
    ref[["identifier", "bibliographicCitation"]],
    left_on="source",
    right_on="identifier",
    how="left"
)


# === Output folder ===
out_dir = Path(r"data\south_africa_e_flora\descriptions\out")
out_dir.mkdir(exist_ok=True)

print("\n=== Splitting CSV by type and language ===")

# === Get all unique (type, language) combinations ===
pairs = df[["type", "language"]].dropna().drop_duplicates()

for _, row in pairs.iterrows():
    t = row["type"]
    lang = row["language"]

    subset = df[(df["type"] == t) & (df["language"] == lang)]

    outfile = out_dir / f"e_flora_SA_v1.42_{t}_{lang}.csv"

    subset.to_csv(
        outfile,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL
    )

    print(f"Saved: {outfile}")

print("\n=== Done ===")
