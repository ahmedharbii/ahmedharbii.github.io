#!/usr/bin/env python3
"""Fetch publications from Google Scholar and surface the ones not yet on the site.

The site renders the Publications page from ``_data/publications.yml`` (consumed
by ``publications.html`` via Liquid). This script never edits that file silently.
Instead it compares your Scholar profile against it and writes any *new* entries
to ``_data/publications.draft.yml`` for you to validate (fix author order, pick a
canonical DOI over the Scholar redirect, add a thumbnail) before promoting them.

Backends:
  * ``scholarly`` (default) -- free, but Google Scholar blocks scraping from
    cloud IPs, so this is most reliable when run locally (``make fetch``).
  * SerpAPI -- set ``SERPAPI_KEY`` to use the official Google Scholar Author API,
    which works reliably from CI. Free tier is ~100 searches/month.

Usage:
  python scripts/fetch_publications.py            # write new pubs to the draft file
  python scripts/fetch_publications.py --apply    # append new pubs straight into
                                                  # publications.yml (used by CI to
                                                  # open a PR you then review)
"""

import argparse
import os
import re
import sys

import yaml

SCHOLAR_ID = os.environ.get("SCHOLAR_ID", "JZ3FAx8AAAAJ")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "_data", "publications.yml")
DRAFT_FILE = os.path.join(ROOT, "_data", "publications.draft.yml")


def normalize_title(title):
    """Lowercase, strip punctuation/whitespace so titles compare reliably."""
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())


def split_authors(authors):
    """Scholar/SerpAPI give authors as a single ' and '/',' separated string."""
    if isinstance(authors, list):
        return [a.strip() for a in authors if a.strip()]
    if not authors:
        return []
    parts = re.split(r"\s+and\s+|,", authors)
    return [p.strip() for p in parts if p.strip()]


def fetch_via_serpapi(api_key):
    import requests

    print("Fetching publications via SerpAPI...")
    resp = requests.get(
        "https://serpapi.com/search",
        params={
            "engine": "google_scholar_author",
            "author_id": SCHOLAR_ID,
            "api_key": api_key,
            "num": 100,
        },
        timeout=60,
    )
    resp.raise_for_status()
    pubs = []
    for art in resp.json().get("articles", []):
        pubs.append(
            {
                "title": art.get("title"),
                "authors": split_authors(art.get("authors")),
                "year": art.get("year"),
                "venue": art.get("publication", ""),
                "url": art.get("link", ""),
            }
        )
    return pubs


def fetch_via_scholarly():
    from scholarly import scholarly

    print(f"Fetching publications via scholarly for Scholar ID {SCHOLAR_ID}...")
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["publications"])

    pubs = []
    for pub in author["publications"]:
        bib = pub.get("bib", {})
        title = bib.get("title")
        print(f"  - {title}")
        pubs.append(
            {
                "title": title,
                "authors": split_authors(bib.get("author")),
                "year": bib.get("pub_year"),
                "venue": bib.get("journal") or bib.get("conference") or bib.get("publisher", ""),
                "url": pub.get("pub_url", ""),
            }
        )
    return pubs


def fetch_publications():
    api_key = os.environ.get("SERPAPI_KEY")
    if api_key:
        return fetch_via_serpapi(api_key)
    return fetch_via_scholarly()


def load_existing_titles():
    if not os.path.exists(DATA_FILE):
        return set()
    with open(DATA_FILE) as f:
        existing = yaml.safe_load(f) or []
    return {normalize_title(p.get("title")) for p in existing}


def format_entry(pub):
    """Render one publication as a YAML block matching publications.yml style."""
    title = (pub.get("title") or "").replace('"', "'")
    lines = [f'- title: "{title}"', "  authors:"]
    for author in pub.get("authors", []):
        lines.append(f"    - {author}")
    lines.append(f"  year: {pub.get('year') or 'TODO'}")
    lines.append(f"  venue: {pub.get('venue') or 'TODO'}")
    lines.append(f"  url: {pub.get('url') or 'TODO'}")
    lines.append("  image: /assets/images/publications/REPLACE_ME.webp  # TODO: add thumbnail")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Append new entries directly into publications.yml (instead of the draft file).",
    )
    args = parser.parse_args()

    try:
        fetched = fetch_publications()
    except Exception as exc:  # noqa: BLE001 - report and exit cleanly for CI
        print(f"Error fetching publications: {exc}")
        print("Google Scholar often blocks automated access from cloud IPs.")
        print("Try running locally (`make fetch`) or set SERPAPI_KEY for a reliable backend.")
        sys.exit(1)

    existing = load_existing_titles()
    new_pubs = [p for p in fetched if p.get("title") and normalize_title(p["title"]) not in existing]
    # Newest first
    new_pubs.sort(key=lambda p: str(p.get("year") or ""), reverse=True)

    print(f"\nFetched {len(fetched)} publications; {len(new_pubs)} are new.")
    if not new_pubs:
        # Clear any stale draft so CI doesn't open an empty PR
        if os.path.exists(DRAFT_FILE):
            os.remove(DRAFT_FILE)
        print("Nothing new to add. The site is up to date.")
        return

    blocks = "\n\n".join(format_entry(p) for p in new_pubs)

    if args.apply:
        with open(DATA_FILE, "a") as f:
            f.write("\n" + blocks + "\n")
        print(f"Appended {len(new_pubs)} new publication(s) to {DATA_FILE}.")
        print("Review the diff: fix author order, set the canonical URL, and add thumbnails.")
    else:
        header = (
            "# New publications detected on Google Scholar that are NOT yet in\n"
            "# publications.yml. Validate each entry (author order, canonical URL,\n"
            "# year, venue), add a thumbnail under assets/images/publications/, then\n"
            "# move the entry into _data/publications.yml. Delete this file when done.\n\n"
        )
        with open(DRAFT_FILE, "w") as f:
            f.write(header + blocks + "\n")
        print(f"Wrote {len(new_pubs)} new publication(s) to {DRAFT_FILE} for review.")


if __name__ == "__main__":
    main()
