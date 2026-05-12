import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# Paths to csvs to combine and where to write to working 
# ---------------------------------------------------------
csv1_path = Path(r"data\eFlora_of_Thailand\Vol_1_to_16\raw\distribution.txt")      # main table (take entirely)
csv2_path = Path(r"data\eFlora_of_Thailand\Vol_1_to_16\raw\references.txt")        # table with citation + URI
output_path = Path(r"data\eFlora_of_Thailand\Vol_1_to_16\working\distribution_combined.csv")
# ---------------------------------------------------------

# Load CSVs (tab-delimited)
csv1 = pd.read_csv(csv1_path, sep="\t")
csv2 = pd.read_csv(csv2_path, sep="\t")

# Join fields
key_csv1 = "WFOID"
key_csv2_original = "WFOID"
key_csv2_renamed = "WFOID_ref"   # safe renamed join key

# ---------------------------------------------------------
# Rename join key in CSV2 to avoid collisions
# ---------------------------------------------------------
csv2 = csv2.rename(columns={key_csv2_original: key_csv2_renamed})

# Check required columns
required_csv2 = {key_csv2_renamed, "bibliographicCitation", "URI"}
missing = required_csv2 - set(csv2.columns)
if missing:
    raise ValueError(f"CSV2 missing required columns: {missing}")

if key_csv1 not in csv1.columns:
    raise ValueError(f"CSV1 missing key column: {key_csv1}")

# Reduce CSV2 to only the fields we want to add
csv2_small = csv2[[key_csv2_renamed, "bibliographicCitation", "URI"]]

# ---------------------------------------------------------
# Merge (left join)
# ---------------------------------------------------------
merged = csv1.merge(
    csv2_small,
    left_on=key_csv1,
    right_on=key_csv2_renamed,
    how="left"
)

# ---------------------------------------------------------
# Drop the renamed join key (NOT the real WFOID)
# ---------------------------------------------------------
merged = merged.drop(columns=[key_csv2_renamed])

# ---------------------------------------------------------
# Write output
# ---------------------------------------------------------
merged.to_csv(output_path, index=False)
print(f"Done. Combined CSV written to: {output_path}")
