import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# Paths to csvs to combine and where to write to working 
# ---------------------------------------------------------
csv1_path = Path(r"data\eFlora_of_Thailand\Vol_1_to_8\raw\vernacular.txt")      # main table (take entirely)
csv2_path = Path(r"data\eFlora_of_Thailand\Vol_1_to_8\raw\references.txt")      # table with citation + URI
output_path = Path(r"data\eFlora_of_Thailand\Vol_1_to_8\working\vernacular_combined.csv")  # output file
# ---------------------------------------------------------

# Load CSVs citation file is messy so needs escape.
csv1 = pd.read_csv(csv1_path, sep="\t")
csv2 = pd.read_csv(csv2_path, sep="\t")


# Join fields
key_csv1 = "source"
key_csv2 = "identifier"

# Check required columns
required_csv2 = {key_csv2, "bibliographicCitation", "URI"}
missing = required_csv2 - set(csv2.columns)
if missing:
    raise ValueError(f"CSV2 missing required columns: {missing}")

if key_csv1 not in csv1.columns:
    raise ValueError(f"CSV1 missing key column: {key_csv1}")

# Reduce CSV2 to only the fields we want to add
csv2_small = csv2[[key_csv2, "bibliographicCitation", "URI"]]

# Merge (left join)
merged = csv1.merge(
    csv2_small,
    left_on=key_csv1,
    right_on=key_csv2,
    how="left"
)

# Drop the duplicate join key from CSV2
merged = merged.drop(columns=[key_csv2])

# Write output
merged.to_csv(output_path, index=False)
print(f"Done. Combined CSV written to: {output_path}")
