import pandas as pd
import re
from pathlib import Path

# ---------------------------------------------------------
#  Paths to csvs to combine and where to write to working 
# ---------------------------------------------------------
input_csv = Path(r"data\eFlora_of_Thailand\Vol_1_to_8\working\descriptions_combined.csv")
output_root = Path(r"data\eFlora_of_Thailand\Vol_1_to_8\output")
# ---------------------------------------------------------

df = pd.read_csv(input_csv)

# ---------------------------------------------------------
# Extract Volume and Part from bibliographicCitation. I hope this works.
# ---------------------------------------------------------

vol_part_regex = re.compile(
    r"Vol\.?\s*(\d+)"          # Volume number
    r"(?:\s*[\.,]?\s*Part\s*(\d+))?",  # Part number
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
# Split and write outputs It might mess with the Github three folder scheme.
# ---------------------------------------------------------

for (vol, part, dtype), group in df.groupby(["Volume", "Part", "type"]):
    if pd.isna(vol) or pd.isna(part):
        continue  # skip rows with no volume/part match

    outdir = output_root / f"Vol_{int(vol)}" / f"Part_{int(part)}"
    outdir.mkdir(parents=True, exist_ok=True)

    outfile = outdir / f"{dtype}.csv"
    group.to_csv(outfile, index=False)

print("Done. Output written to:", output_root)
