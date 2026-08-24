import pandas as pd
import re
from pathlib import Path

PATTERN = re.compile(r"\.t(\d+)a(\d+)")

def extract_ids(doi):
    if not isinstance(doi, str):
        return None, None
    match = PATTERN.search(doi)
    if match:
        return match.group(1), match.group(2)
    return None, None

def main():
    # Hard‑coded paths
    input_path = Path(r"data/IUCN/2026_01/working/crossref_full_harvest2026_06.csv")
    output_path = Path(r"data/IUCN/2026_01/working/crossref_full_harvestIds.csv")

    df = pd.read_csv(input_path)

    # Auto-detect DOI column
    doi_col = None
    for col in df.columns:
        if col.lower() == "doi":
            doi_col = col
            break

    if doi_col is None:
        print("Could not find a DOI column. Columns are:")
        print(df.columns.tolist())
        return

    print(f"Using DOI column: {doi_col}")

    # Extract IDs
    extracted = df[doi_col].apply(lambda x: pd.Series(extract_ids(x)))
    extracted.columns = ["TaxonID", "AssessmentID"]

    df = pd.concat([df, extracted], axis=1)

    matched = extracted["TaxonID"].notna().sum()
    print(f"Extracted IDs for {matched} rows")

    df.to_csv(output_path, index=False)
    print(f"Updated CSV written to: {output_path}")

if __name__ == "__main__":
    main()
