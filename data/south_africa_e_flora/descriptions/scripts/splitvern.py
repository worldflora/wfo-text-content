import pandas as pd
import csv
from pathlib import Path
import re

# === Load vernacularname.txt ===
df = pd.read_csv(
    r"data\south_africa_e_flora\descriptions\raw\dwca-flora_descriptions-v1.42\vernacularname.txt",
    sep="\t",
    encoding="utf-8",
    dtype=str,
    low_memory=False
)

df.columns = df.columns.str.strip()
df["type"] = "vernacular"

# === Load reference data ===
ref = pd.read_csv(
    r"data\south_africa_e_flora\descriptions\raw\dwca-flora_descriptions-v1.42\reference.txt",
    sep="\t",
    encoding="utf-8",
    dtype=str
)
ref.columns = ref.columns.str.strip()
ref = ref.drop_duplicates(subset="identifier")

df = df.merge(
    ref[["identifier", "bibliographicCitation"]],
    left_on="source",
    right_on="identifier",
    how="left"
)
# drop this field not needed.
df = df.drop(columns=["identifier"])
# === URL extraction ===
def extract_urls(citation):
    if pd.isna(citation):
        return ""
    brackets = re.findall(r"\[(.*?)\]", citation)
    urls = [b for b in brackets if re.match(r"https?://|doi:", b)]
    return "; ".join(urls)

if "bibliographicCitation" in df.columns:
    df["url"] = df["bibliographicCitation"].apply(extract_urls)

# === Output folder ===
out_dir = Path(r"data/south_africa_e_flora/descriptions/work/vernacular_split")
out_dir.mkdir(exist_ok=True)

print("\n=== Strict ISO Mode: Splitting vernacular.txt by ISO language code ===")

# === ISO 639-1 mapping ===
ISO_MAP = {
    "afrikaans": "af",
    "english": "en",
    "zulu": "zu",
    "xhosa": "xh",
    "sepedi": "nso",
    "northern sotho": "nso",
    "southern sotho": "st",
    "sotho": "st",
    "tswana": "tn",
    "swati": "ss",
    "siswati": "ss",
    "venda": "ve",
    "tsonga": "ts",

    # alternates
    "isizulu": "zu",
    "isixhosa": "xh",
    "sesotho": "st",
    "setswana": "tn",
    "xitsonga": "ts",
    "tshivenda": "ve",

    # flora languages
    "latin": "la",
    "german": "de",
    "french": "fr",
    "portuguese": "pt",
    "spanish": "es",
}

# === Normalisation ===
def normalize_lang(text):
    if pd.isna(text):
        return None
    text = text.lower().strip()
    text = re.sub(r"[^a-z]+", " ", text)
    return text.strip() or None

# === Strict ISO lookup ===
def iso_code_strict(lang):
    if lang is None:
        return None
    if lang in ISO_MAP:
        return ISO_MAP[lang]
    for part in lang.split():
        if part in ISO_MAP:
            return ISO_MAP[part]
    return None  # STRICT MODE: no fallback

# === Process languages ===
languages = df["language"].dropna().unique()

unmapped = []
merged = {}

for lang in languages:
    norm = normalize_lang(lang)
    code = iso_code_strict(norm)

    if code is None:
        unmapped.append(lang)
        continue

    # Merge rows for languages mapping to same ISO code
    if code not in merged:
        merged[code] = df[df["language"] == lang].copy()
    else:
        merged[code] = pd.concat([merged[code], df[df["language"] == lang]], ignore_index=True)

# === Write merged ISO files ===
for code, subset in merged.items():
    outfile = out_dir / f"e_flora_SA_v1.42_vernacular_{code}.csv"
    subset.to_csv(
        outfile,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL
    )
    print(f"Saved: {outfile}")

# === Report unmapped languages ===
print("\n=== Unmapped languages (strict ISO mode) ===")
for u in unmapped:
    print(" -", u)

print("\n=== Done ===")
