import pandas as pd
import re
from pathlib import Path

# ---------------------------------------------------------
#  Paths to csvs to combine and where to write to working 
# ---------------------------------------------------------
input_csv = Path(r"data\eFlora_of_Thailand\Vol_1_to_16\working\vernacular_combined.csv")
output_root = Path(r"data\eFlora_of_Thailand\Vol_1_to_16\out")
# ---------------------------------------------------------

df = pd.read_csv(input_csv)

# ---------------------------------------------------------
# Extract Volume and Part from bibliographicCitation
# ---------------------------------------------------------

vol_part_regex = re.compile(
    r"Vol\.?\s*(\d+)"                 # Volume number
    r"(?:\s*[\.,]?\s*Part\s*(\d+))?", # Optional Part number
    flags=re.IGNORECASE
)

def extract_vol_part(text):
    if not isinstance(text, str):
        return None, None
    m = vol_part_regex.search(text)
    if not m:
        return None, None
    vol = int(m.group(1))
    part = int(m.group(2)) if m.group(2) else 1
    return vol, part

df["Volume"], df["Part"] = zip(*df["bibliographicCitation"].apply(extract_vol_part))

# ---------------------------------------------------------
# Desired output column order
# ---------------------------------------------------------

desired_order = [
    "WFOID",  "vernacularName", "identifier", "isPreferredName", "source", "language", "countryCode", "uri",  "bibliographicCitation", "rights", "license"
    # add/remove fields as needed
]

# ---------------------------------------------------------
# Split and write outputs
# ---------------------------------------------------------

for (vol, part), group in df.groupby(["Volume", "Part"]):
    if pd.isna(vol) or pd.isna(part):
        continue

    outdir = output_root / f"Vol_{int(vol)}" / f"Part_{int(part)}"
    outdir.mkdir(parents=True, exist_ok=True)

    # Reorder columns (ignore missing ones safely)
    group = group.reindex(columns=[c for c in desired_order if c in group.columns])

    outfile = outdir / "vernacular.csv"
    group.to_csv(outfile, index=False)

print("Done. Output written to:", output_root)
