import pandas as pd
import csv
from pathlib import Path

# === Load main descriptions CSV ===
df = pd.read_csv(
    "data/Royal_Botanic_Gardens_Kew/FTEA/work/descriptions.csv",
    sep=",",
    encoding="utf-8",
    dtype=str,
    low_memory=False
)

df.columns = df.columns.str.strip()

# === Load references CSV ===
refs = pd.read_csv(
    "data/Royal_Botanic_Gardens_Kew/FTEA/work/references.csv",
    sep=",",
    encoding="utf-8",
    dtype=str,
    low_memory=False
)

refs.columns = refs.columns.str.strip()

# === Print counts per type as a sense check ===
print("\n=== Description Type Counts ===")
type_counts = df["type"].value_counts(dropna=False)
for t, count in type_counts.items():
    print(f"{t}: {count}")
print("================================\n")

# === Output folder === Save to working until its finalized and moved to the final output folder
out_dir = Path("data/Royal_Botanic_Gardens_Kew/FTEA/out")
out_dir.mkdir(exist_ok=True)

# === Process each type ===
types = df["type"].dropna().unique()

for t in types:
    subset = df[df["type"] == t]

    # === Concatenate descriptions per WFO ID if necessary===
    grouped = (
        subset.groupby("wfo_id")["description"]
        .apply(lambda x: " ".join(x))
        .reset_index()
    )

    # Extract reference IDs per WFO ID
    refs_for_type = (
        subset.groupby("wfo_id")["source"]
        .apply(lambda x: x.dropna().unique())
        .reset_index()
    )

    # Check reference ID fields names across the files and ensure they are consistent. If there are multiple reference IDs, take the first one.
    refs_for_type["source"] = refs_for_type["source"].apply(
        lambda lst: lst[0] if len(lst) > 0 else None
    )

    # Merge reference IDs into grouped descriptions
    merged = grouped.merge(refs_for_type, on="wfo_id", how="left")

    # Merge with references.csv using source → identifier
    merged = merged.merge(
        refs[["identifier", "bibliographicCitation", "URL"]],
        left_on="source",
        right_on="identifier",
        how="left"
    )

    # Remove identifier from output
    merged = merged.drop(columns=["identifier"])

    # Save output
    outfile = out_dir / f"FTEA_{t}.csv"

    merged.to_csv(
        outfile,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL
    )

    print(f"Saved: {outfile}")
