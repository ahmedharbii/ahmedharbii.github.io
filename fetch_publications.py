import yaml
from scholarly import scholarly
import os

def fetch_publications(scholar_id):
    print(f"Fetching publications for Scholar ID: {scholar_id}...")
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=['publications'])
    
    publications = []
    for pub in author['publications']:
        print(f"Processing: {pub['bib']['title']}")
        # Fill publication details
        pub_filled = scholarly.fill(pub)
        bib = pub_filled['bib']
        
        pub_data = {
            'title': bib.get('title'),
            'authors': bib.get('author'),
            'year': bib.get('pub_year'),
            'venue': bib.get('journal') or bib.get('conference') or bib.get('publisher', 'N/A'),
            'link': pub_filled.get('pub_url', ''),
            'citation': f"{bib.get('author', '')} ({bib.get('pub_year', '')}). {bib.get('title', '')}. {bib.get('journal', bib.get('conference', ''))}"
        }
        publications.append(pub_data)
    
    # Sort by year descending
    publications.sort(key=lambda x: str(x['year']), reverse=True)
    return publications

def save_to_yaml(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    print(f"Saved {len(data)} publications to {filepath}")

if __name__ == "__main__":
    SCHOLAR_ID = "JZ3FAx8AAAAJ"
    DATA_FILE = "_data/publications.yml"
    
    try:
        pubs = fetch_publications(SCHOLAR_ID)
        save_to_yaml(pubs, DATA_FILE)
    except Exception as e:
        print(f"Error: {e}")
