import csv
from pathlib import Path
from lxml import etree

XML_FILE = r"data/Flora Guiana/raw/FotG_A11_final.xml"
OUT_DIR = Path(r"C:\Users\alane\OneDrive - Royal Botanic Garden Edinburgh\wfo-text-content\wfo-text-content\data\Flora Guiana\work\dwca_out\a11")
OUT_DIR.mkdir(exist_ok=True)

tree = etree.parse(XML_FILE)
root = tree.getroot()

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def text(el):
    return el.text.strip() if el is not None and el.text else ""

NAME_CLASSES = {
    "kingdom", "phylum", "class", "order",
    "family", "subfamily", "tribe", "subtribe",
    "genus", "species", "infraspecificEpithet"
}

def build_scientific_name(nom):
    parts = []
    for n in nom.findall("./name"):
        cls = n.get("class", "").lower()
        val = text(n)
        if cls in NAME_CLASSES and val:
            parts.append(val)
    return " ".join(parts)

def get_rank(nom):
    for rank in ["species", "genus", "subtribe", "tribe", "subfamily", "family"]:
        if nom.find(f"./name[@class='{rank}']") is not None:
            return rank
    return ""

def get_authorship(nom):
    auth = nom.find("./name[@class='author']")
    return text(auth)

def get_name_published_in(nom):
    cit = nom.find("./citation")
    if cit is None:
        return ""
    parts = [text(p) for p in cit.findall("./refPart") if text(p)]
    return " ".join(parts)

def make_taxon_id(nom):
    num = text(nom.find("./num"))
    sci = build_scientific_name(nom)
    base = f"{num}-{sci}" if num else sci
    return "taxon-" + base.replace(" ", "_").replace(".", "").replace(",", "")

def extract_description(feature):
    if feature is None:
        return ""
    raw = " ".join(t.strip() for t in feature.itertext() if t.strip())
    return " ".join(raw.split())

def extract_distribution(feature):
    if feature is None:
        return None
    full_text = " ".join(t.strip() for t in feature.itertext() if t.strip())
    localities = []
    for loc in feature.findall(".//distributionLocality"):
        localities.append({
            "class": loc.get("class", ""),
            "value": text(loc)
        })
    return full_text, localities

def extract_vernacular(feature):
    """
    Extract vernacular names including:
    - region headings (<subHeading>)
    - multiple vernacular names inside one <vernacularName>
    - multiple localLanguage entries
    - doubtful languages
    - ignores wrapper headings and punctuation
    """
    names = []
    if feature is None:
        return names

    current_region = ""

    for el in feature.iter():

        # REGION HEADINGS
        if el.tag == "subHeading":
            region_text = text(el).strip().rstrip(":")
            # ignore top-level headings
            if region_text.lower() not in {
                "vernacular names",
                "vernacular (and commercial) names",
                "vernacular name",
                "vernacular"
            }:
                current_region = region_text

        # VERNACULAR NAME BLOCKS
        if el.tag == "vernacularName":

            # extract ALL vernacular names inside this block
            vern_names = el.findall(".//name[@class='vernacular']")
            langs = el.findall(".//localLanguage")

            # pair names and languages best-effort
            for i, vn in enumerate(vern_names):
                vern_text = text(vn)

                # language pairing
                if i < len(langs):
                    lang_text = text(langs[i])
                    doubtful = langs[i].get("doubtful", "")
                else:
                    lang_text = ""
                    doubtful = ""

                names.append({
                    "name": vern_text,
                    "region": current_region,
                    "language": lang_text,
                    "doubtful": doubtful
                })

    return names

def extract_habitat(feature):
    if feature is None:
        return ""
    raw = " ".join(t.strip() for t in feature.itertext() if t.strip())
    return " ".join(raw.split())

def extract_uses(feature):
    if feature is None:
        return ""
    raw = " ".join(t.strip() for t in feature.itertext() if t.strip())
    return " ".join(raw.split())

# ---------------------------------------------------------
# Output containers
# ---------------------------------------------------------

taxon_rows = []
synonym_rows = []
description_rows = []
occurrence_rows = []
reference_rows = []
multimedia_rows = []
distribution_rows = []
vernacular_rows = []
habitat_rows = []
uses_rows = []

# ---------------------------------------------------------
# Global references
# ---------------------------------------------------------

for ref in root.findall(".//references/reference"):
    parts = [text(p) for p in ref.findall("./refPart") if text(p)]
    citation = " ".join(parts)
    reference_rows.append({
        "referenceID": f"ref-{hash(citation)}",
        "bibliographicCitation": citation
    })

# ---------------------------------------------------------
# Process each taxon block
# ---------------------------------------------------------

for taxon in root.findall(".//treatment/taxon"):

    accepted_noms = taxon.findall(".//homotypes/nom[@class='accepted']")
    if not accepted_noms:
        continue

    for nom in accepted_noms:
        taxon_id = make_taxon_id(nom)
        sci_name = build_scientific_name(nom)
        authorship = get_authorship(nom)
        rank = get_rank(nom)
        name_pub = get_name_published_in(nom)

        family = text(nom.find("./name[@class='family']"))
        subfamily = text(nom.find("./name[@class='subfamily']"))
        genus = text(nom.find("./name[@class='genus']"))

        taxon_rows.append({
            "taxonID": taxon_id,
            "scientificName": sci_name,
            "scientificNameAuthorship": authorship,
            "taxonRank": rank,
            "family": family,
            "subfamily": subfamily,
            "genus": genus,
            "namePublishedIn": name_pub,
            "taxonomicStatus": "accepted"
        })

        # synonyms
        for syn in taxon.findall(".//homotypes/nom[@class='synonym']"):
            syn_name = build_scientific_name(syn)
            syn_pub = get_name_published_in(syn)
            synonym_rows.append({
                "taxonID": taxon_id,
                "scientificName": syn_name,
                "namePublishedIn": syn_pub,
                "taxonomicStatus": "synonym"
            })

        # descriptions
        desc_feature = taxon.find(".//feature[@class='description']")
        desc_text = extract_description(desc_feature)
        if desc_text:
            description_rows.append({
                "taxonID": taxon_id,
                "description": desc_text
            })

        # distribution
        dist_feature = taxon.find(".//feature[@class='distribution']")
        dist = extract_distribution(dist_feature)
        if dist:
            full_text, localities = dist
            if localities:
                for loc in localities:
                    distribution_rows.append({
                        "taxonID": taxon_id,
                        "locality": loc["value"],
                        "localityType": loc["class"],
                        "distributionText": full_text
                    })
            else:
                distribution_rows.append({
                    "taxonID": taxon_id,
                    "locality": "",
                    "localityType": "",
                    "distributionText": full_text
                })

        # vernacular names
        vern_feature = taxon.find(".//feature[@class='vernacular']")
        vernaculars = extract_vernacular(vern_feature)
        for vn in vernaculars:
            vernacular_rows.append({
                "taxonID": taxon_id,
                "vernacularName": vn["name"],
                "language": vn["language"],
                "region": vn["region"],
                "doubtful": vn["doubtful"]
            })

        # habitat
        hab_feature = taxon.find(".//feature[@class='habitat']")
        hab_text = extract_habitat(hab_feature)
        if hab_text:
            habitat_rows.append({
                "taxonID": taxon_id,
                "habitat": hab_text
            })

        # uses
        use_feature = taxon.find(".//feature[@class='uses']")
        use_text = extract_uses(use_feature)
        if use_text:
            uses_rows.append({
                "taxonID": taxon_id,
                "use": use_text
            })

        # specimens → occurrence
        spec_feature = taxon.find(".//feature[@class='specimens']")
        if spec_feature is not None:
            for ggroup in spec_feature.findall(".//gatheringGroup"):
                country = ggroup.get("geoscope", "")
                for g in ggroup.findall("./gathering"):
                    collector = text(g.find("./collector"))
                    fieldnum = text(g.find("./fieldNum"))
                    occ_id = f"occ-{hash((collector, fieldnum, sci_name))}"
                    occurrence_rows.append({
                        "occurrenceID": occ_id,
                        "taxonID": taxon_id,
                        "scientificName": sci_name,
                        "recordedBy": collector,
                        "recordNumber": fieldnum,
                        "country": country
                    })

        # figures → multimedia
        for fig in taxon.findall(".//figure"):
            fig_id = fig.get("id", "")
            url = fig.get("url", "")
            legend = text(fig.find("./figureLegend"))
            num = text(fig.find("./num"))
            media_id = f"media-{fig_id or hash(url)}"
            multimedia_rows.append({
                "multimediaID": media_id,
                "taxonID": taxon_id,
                "identifier": url,
                "title": f"Fig. {num}" if num else "",
                "description": legend
            })

# ---------------------------------------------------------
# Write CSVs
# ---------------------------------------------------------

def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
            quoting=csv.QUOTE_ALL,
            quotechar='"',
            escapechar='\\'
        )
        w.writeheader()
        for r in rows:
            w.writerow(r)


write_csv(
    OUT_DIR / "taxon.txt",
    ["taxonID", "scientificName", "scientificNameAuthorship",
     "taxonRank", "family", "subfamily", "genus",
     "namePublishedIn", "taxonomicStatus"],
    taxon_rows
)

write_csv(
    OUT_DIR / "synonym.txt",
    ["taxonID", "scientificName", "namePublishedIn", "taxonomicStatus"],
    synonym_rows
)

write_csv(
    OUT_DIR / "description.txt",
    ["taxonID", "description"],
    description_rows
)

write_csv(
    OUT_DIR / "occurrence.txt",
    ["occurrenceID", "taxonID", "scientificName",
     "recordedBy", "recordNumber", "country"],
    occurrence_rows
)

write_csv(
    OUT_DIR / "reference.txt",
    ["referenceID", "bibliographicCitation"],
    reference_rows
)

write_csv(
    OUT_DIR / "multimedia.txt",
    ["multimediaID", "taxonID", "identifier", "title", "description"],
    multimedia_rows
)

write_csv(
    OUT_DIR / "distribution.txt",
    ["taxonID", "locality", "localityType", "distributionText"],
    distribution_rows
)

write_csv(
    OUT_DIR / "vernacularname.txt",
    ["taxonID", "vernacularName", "language", "region", "doubtful"],
    vernacular_rows
)

write_csv(
    OUT_DIR / "habitat.txt",
    ["taxonID", "habitat"],
    habitat_rows
)

write_csv(
    OUT_DIR / "uses.txt",
    ["taxonID", "use"],
    uses_rows
)

print("DwC-A extraction complete.")
