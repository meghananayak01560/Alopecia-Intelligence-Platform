#pull paper IDs from PubMed and fetch the paper details
import requests
import xml.etree.ElementTree
from database import insert_paper
import time

# linksss :)
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
# linksss :)

#can add more as we think of mor epopular search queries
SEARCH_QUERIES = [
    "alopecia young women",
    "female pattern hair loss",
    "androgenetic alopecia women",
    "teen girls hair loss treatment",
    "alopecia areata female",
    "telogen effluvium women stress"
]

def search_pubmed(query, retmax=10):
  parameters = {
    "db": "pubmed",
    "term": query,
    "retmax": retmax,
    "retmode": "json"
  }
  response = requests.get(PUBMED_SEARCH_URL, params=parameters)
  response.raise_for_status()
  data = response.json()
  return data["esearchresult"]["idlist"]

def fetch_pubmed_details(paper_id):
  if not paper_id:
    return []
  
  parameters = {
    "db": "pubmed",
    "id":",".join(paper_id),
    "retmode": "xml"
  }
  response = requests.get(PUBMED_FETCH_URL, params=parameters)
  response.raise_for_status()
  root = xml.etree.ElementTree.fromstring(response.content)
  papers = []
  for article in root.findall(".//PubmedArticle"):
    pubmed_id = article.findtext(".//PMID")

    title = article.findtext(".//ArticleTitle") or ""

    abstract_parts = article.findall(".//AbstractText")
    abstract = " ".join(part.text or "" for part in abstract_parts)

    journal = article.findtext(".//Journal/Title") or ""

    year_text = article.findtext(".//PubDate/Year")
    year = int(year_text) if year_text and year_text.isdigit() else None

    url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"

    papers.append({
            "pubmed_id": pubmed_id,
            "title": title,
            "abstract": abstract,
            "journal": journal,
            "year": year,
            "url": url
        })
    return papers


def ingest_papers():
    for query in SEARCH_QUERIES:
        print(f"Processing query, searching PubMed for: '{query}'")
        paper_ids = search_pubmed(query)
        papers = fetch_pubmed_details(paper_ids)
        for paper in papers:
            insert_paper(
                PubMed_id=paper["pubmed_id"],
                title=paper["title"],
                abstract=paper["abstract"],
                journal=paper["journal"],
                year=str(paper["year"]) if paper["year"] else None,
                url=paper["url"],
                search_query=query
            )
        print(f"Completed inserting {len(papers)} papers for query: '{query}'")
        time.sleep(1)  # needed to add this bc i didnt realize that im hitting api limit for too many requests
        #Sleep for 1 second to respect API rate limits