import re
import pandas as pd

# --- 1. Parse JSTOR citation list ---
def parse_jstor_file(path):
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        block = []
        for line in f:
            if line.startswith("@article"):
                block = [line]
            elif block:
                block.append(line)
                if line.strip() == "}":
                    text = "".join(block)

                    # Extract fields
                    url = re.search(r"URL\s*=\s*{([^}]+)}", text)
                    vol = re.search(r"volume\s*=\s*{([^}]+)}", text)

                    if url and vol:
                        entries.append({
                            "volume": vol.group(1),
                            "stable_url": url.group(1)
                        })
    return pd.DataFrame(entries)

# --- 2. Extract monograph number from your citations ---
def extract_monograph_number(citation):
    m = re.search(r"Monogr\.\s*([0-9]+[A-Za-z]?)", citation)
    return m.group(1) if m else None

# --- 3. Load your datasets ---
jstor_df = parse_jstor_file(r"data\New_York_Botanic_Garden\Flora Neotropica\work\citations (5).txt")
refs_df = pd.read_csv(r"data\New_York_Botanic_Garden\Flora Neotropica\work\neotropica_refs.csv")

# --- 4. Add monograph number to your refs ---
refs_df["Monograph"] = refs_df["bibliographicCitation"].apply(extract_monograph_number)

# --- 5. Merge on monograph number = volume ---
merged = refs_df.merge(jstor_df, left_on="Monograph", right_on="volume", how="left")

# --- 6. Save output ---
merged.to_csv(r"data\New_York_Botanic_Garden\Flora Neotropica\work\neotropica_with_jstor_urls.csv", index=False)

print("Done.")
