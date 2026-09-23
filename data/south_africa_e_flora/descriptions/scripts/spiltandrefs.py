import pandas as pd
import csv
from pathlib import Path
import re

# === Load main descriptions CSV ===
df = pd.read_csv(
    r"data\south_africa_e_flora\descriptions\raw\dwca-flora_descriptions-v1.42\vernacularname.txt",
    sep="\t",
    encoding="utf-8",
    dtype=str,
    low_memory=False
)

df.columns = df.columns.str.strip()

# === Load reference file ===
ref = pd.read_csv(
    r"data\south_africa_e_flora\descriptions\raw\dwca-flora_descriptions-v1.42\reference.txt",
    sep="\t",        # adjust if needed
    encoding="utf-8",
    dtype=str
)

ref.columns = ref.columns.str.strip()

# === Deduplicate identifiers to prevent merge explosion ===
ref = ref.drop_duplicates(subset="identifier")

# === Merge bibliographicCitation into main dataframe ===
df = df.merge(
    ref[["identifier", "bibliographicCitation"]],
    left_on="source",
    right_on="identifier",
    how="left"
)

# === Extract URLs from bibliographicCitation ===
def extract_urls(citation):
    if pd.isna(citation):
        return ""
    # find all bracketed items
    brackets = re.findall(r"\[(.*?)\]", citation)
    # keep only URL-like items
    urls = [b for b in brackets if re.match(r"https?://|doi:", b)]
    return "; ".join(urls)

df["url"] = df["bibliographicCitation"].apply(extract_urls)

# === Output folder ===
out_dir = Path(r"data\Royal Botanic Garden Edinburgh\EJB\out")
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
