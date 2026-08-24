import pandas as pd
import re
from pathlib import Path

# ---------------------------------------------------------
#  Paths to csvs to combine and where to write to working 
# ---------------------------------------------------------
input_csv = Path(r"data\eFlora_of_Thailand\Vol_1_to_16\working\descriptions_combined.csv")
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
# Desired output column order (edit as needed)
# ---------------------------------------------------------

desired_order = [
    "WFOID",
    "description",
    "type",
    "language",
    "contributor",
    "audience",
    "rightsHolder",
    "created",
    "creator",
    "source",
    "Volume",
    "Part",
    "bibliographicCitation",
    "URI"
    "rights",
    "license"
]

# ---------------------------------------------------------
# Split and write outputs
# ---------------------------------------------------------

for (vol, part, dtype), group in df.groupby(["Volume", "Part", "type"]):
    if pd.isna(vol) or pd.isna(part):
        continue

    outdir = output_root / f"Vol_{int(vol)}" / f"Part_{int(part)}"
    outdir.mkdir(parents=True, exist_ok=True)

    # Reorder columns safely (ignore missing ones)
    cols = [c for c in desired_order if c in group.columns]
    group = group.reindex(columns=cols + [c for c in group.columns if c not in cols])

    outfile = outdir / f"{dtype}.csv"
    group.to_csv(outfile, index=False)

print("Done. Output written to:", output_root)
