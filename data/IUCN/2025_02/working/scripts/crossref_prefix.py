import csv
import requests
import time


def to_apa(item):
    """Robust APA 7 citation generator for Crossref items."""

    # --- Authors ---
    authors = item.get("author", [])
    author_strs = []

    for a in authors:
        family = a.get("family", "").strip()
        given = a.get("given", "").strip()
        if family:
            initials = "".join([part[0] + "." for part in given.split()]) if given else ""
            author_strs.append(f"{family}, {initials}")

    if len(author_strs) > 1:
        authors_formatted = ", ".join(author_strs[:-1]) + ", & " + author_strs[-1]
    elif author_strs:
        authors_formatted = author_strs[0]
    else:
        authors_formatted = ""   # APA allows no authors

    # --- Year ---
    year = None
    issued = item.get("issued", {})
    if "date-parts" in issued and issued["date-parts"][0]:
        year = issued["date-parts"][0][0]

    year_str = f"({year})." if year else "(n.d.)."

    # --- Title ---
    title = item.get("title", [""])[0].strip()

    # Remove trailing periods (APA adds its own)
    if title.endswith("."):
        title = title[:-1]

    # --- Journal ---
    journal = item.get("container-title", [""])[0].strip()

    # --- Volume, issue, pages ---
    volume = item.get("volume", "")
    issue = item.get("issue", "")
    pages = item.get("page", "")

    vol_issue = ""
    if volume:
        vol_issue += volume
    if issue:
        vol_issue += f"({issue})"
    if vol_issue:
        vol_issue += ","

    pages_str = f" {pages}" if pages else ""

    # --- DOI ---
    doi = item.get("DOI", "")
    doi_url = f"https://doi.org/{doi}" if doi else ""

    # --- Build citation ---
    parts = [
        authors_formatted,
        year_str,
        f"{title}.",
    ]

    if journal:
        parts.append(f"*{journal}*,")
    if vol_issue:
        parts.append(vol_issue)
    if pages:
        parts.append(pages_str)

    if doi_url:
        parts.append(doi_url)

    # Join and clean spacing
    apa = " ".join(p.strip() for p in parts if p.strip())
    apa = apa.replace(" ,", ",").replace("..", ".").strip()

    return apa

def harvest_all(prefix, mailto="your_email@example.com", csv_path="crossref_full_harvest.csv", rows=1000):
    """
    Harvest ALL Crossref works for a DOI prefix using cursor-based pagination.
    Writes each record to CSV as it is fetched.
    """

    url = "https://api.crossref.org/works"
    cursor = "*"
    total = 0

    # Open CSV once
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "doi", "title", "authors", "year", "journal",
            "volume", "issue", "pages", "doi_url", "apa_citation"
        ])

        while True:
            params = {
                "filter": f"prefix:{prefix}",
                "cursor": cursor,
                "rows": rows,
                "mailto": mailto
            }

            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            message = response.json()["message"]

            items = message.get("items", [])
            if not items:
                print("No more records — harvest complete.")
                break

            for item in items:
                doi = item.get("DOI", "")
                title = item.get("title", [""])[0]

                authors = item.get("author", [])
                authors_str = "; ".join(
                    f"{a.get('family','')}, {a.get('given','')}"
                    for a in authors
                )

                year = None
                issued = item.get("issued", {})
                if "date-parts" in issued:
                    year = issued["date-parts"][0][0]

                journal = item.get("container-title", [""])[0]
                volume = item.get("volume", "")
                issue = item.get("issue", "")
                pages = item.get("page", "")
                doi_url = f"https://doi.org/{doi}" if doi else ""

                apa = to_apa(item)

                writer.writerow([
                    doi, title, authors_str, year, journal,
                    volume, issue, pages, doi_url, apa
                ])

                total += 1

            print(f"Fetched {len(items)} records — total so far: {total}")

            # Move to next cursor
            cursor = message.get("next-cursor")

            # Be polite to Crossref
            time.sleep(1)

    print(f"Finished! Total records harvested: {total}")
    print(f"CSV written to: {csv_path}")


if __name__ == "__main__":
    harvest_all("10.2305")
