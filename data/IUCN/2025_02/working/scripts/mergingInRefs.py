import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# EDIT THESE THREE LINES ONLY
# ---------------------------------------------------------
crossref_path = Path("data/IUCN/2025_02/working/crossref_full_harvestIds.csv")
category_path = Path(r"data\IUCN\2025_02\working\RL_assessments_2025_02_VU.csv")
output_path   = Path("data/IUCN/2025_02/out/RL_assessments_2025_02_VU.csv")
# ---------------------------------------------------------

# Load both CSVs
crossref = pd.read_csv(crossref_path)
category = pd.read_csv(category_path)

# Ensure required columns exist
required_crossref = {"TaxonID", "AssessmentID"}
required_category = {"internalTaxonId", "assessmentId"}

if not required_crossref.issubset(crossref.columns):
    raise ValueError(f"Crossref CSV missing required columns: {required_crossref - set(crossref.columns)}")
if not required_category.issubset(category.columns):
    raise ValueError(f"Category CSV missing required columns: {required_category - set(category.columns)}")

# Rename RL_assessment columns to match Crossref
category = category.rename(columns={
    "internalTaxonId": "TaxonID",
    "assessmentId": "AssessmentID"
})

# Rename Crossref citation + URL fields
crossref = crossref.rename(columns={
    "apa_citation": "citation",
    "doi_url": "url"
})

# Select only the fields we want to merge in
fields_to_add = ["TaxonID", "AssessmentID", "url", "citation"]
fields_to_add = [f for f in fields_to_add if f in crossref.columns]

crossref_small = crossref[fields_to_add]

# Merge on both IDs
merged = category.merge(
    crossref_small,
    on=["TaxonID", "AssessmentID"],
    how="left"
)

# Write output
merged.to_csv(output_path, index=False)
print(f"Done. Enriched CSV written to: {output_path}")
