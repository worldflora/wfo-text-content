import requests
import pandas as pd
import time
import csv

def lookup_doi(citation):
    url = "https://api.crossref.org/works"
    try:
        r = requests.get(url, params={"query.bibliographic": citation}, timeout=10)
        items = r.json().get("message", {}).get("items", [])
        if items:
            doi = items[0].get("DOI")
            return f"https://doi.org/{doi}" if doi else None
    except Exception as e:
        print(f"Error for citation: {citation}\n{e}")
    return None

# Load your file
df = pd.read_csv("data\\New_York_Botanic_Garden\\Memoirs_NYBG\\work\\uniqueRefs.csv", sep=",", encoding="utf-8")

# Clean column names
df.columns = df.columns.str.strip()

citation_col = "bibliographicCitation"

# Clean Identifier (remove .0)
df["Identifier"] = df["Identifier"].astype(str).str.replace(".0", "", regex=False)

# Open output file for streaming writes
with open("data\\New_York_Botanic_Garden\\Memoirs_NYBG\\work\\publications_with_doi2.tsv", "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out, delimiter="\t")

    # Write header
    writer.writerow(["Identifier", "bibliographicCitation", "DOI"])

    # Process rows one by one
    for i, row in df.iterrows():
        citation = row[citation_col]
        print(f"Looking up DOI for: {citation}")

        doi = lookup_doi(citation)

        writer.writerow([
            row["Identifier"],
            row[citation_col],
            doi
        ])

        out.flush()  # ensure data is written immediately
        time.sleep(0.2)  # polite rate limit

print("Done!")
