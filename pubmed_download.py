r"""
Python script to download PubMed document abstracts for specified period
  Example to run this conversion script:
    python download_pubmed.py --start  "2023/01/01" --end "2023/12/31"
"""

from argparse import ArgumentParser
from Bio import Entrez
import json
import time

Entrez.email = "vying@scu.edu"

def fetch_idlist(start: str = "2023/01/01", end: str = "2023/12/31", max_docs: int = 10000):

    # Format date range in YYYY/MM/DD format
    date_prefix = f"({start}[Date - Publication] : {end}[Date - Publication])"

    # Search for background
    background_suffix = " AND (Letter[pt] OR Review[pt] OR Conference Abstract[pt])"
    search_query = date_prefix + background_suffix
    handle = Entrez.esearch(db='pubmed', term=search_query, sort='relevance', 
                            retmax=max_docs, retmode='xml')
    background_ids = Entrez.read(handle)['IdList']
    handle.close()

    # Search for reference
    reference_suffix = " AND (Journal Article[pt] OR Clinical Trial[pt])"
    search_query = date_prefix + reference_suffix
    handle = Entrez.esearch(db='pubmed', term=search_query, sort='relevance', 
                            retmax=max_docs, retmode='xml')
    reference_ids = Entrez.read(handle)['IdList']
    handle.close()

    return (background_ids, reference_ids) 


def fetch_details(id_list):
    # Fetch metadata of PubMed documents based on ID
    ids = ','.join(id_list)
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=ids)
    results = Entrez.read(handle)
    handle.close()
    return results

def retrieve_abstracts(id_list):
    papers = fetch_details(id_list)
    results = {}

    if papers:
        for i, paper in enumerate(papers['PubmedArticle']):
            abstract = paper['MedlineCitation']['Article'].get('Abstract')
            date = paper['MedlineCitation']['Article']['ArticleDate']

            # Keep only documents where date and abstract information is available
            if abstract and date:
                results[i] = {
                    "article_title": paper['MedlineCitation']['Article']['ArticleTitle'],
                    "article_abstract": abstract['AbstractText'][0],
                    "pub_date": {
                            "year": paper['MedlineCitation']['Article']['ArticleDate'][0]['Year'],
                            "month": paper['MedlineCitation']['Article']['ArticleDate'][0]['Month'],
                            "day": paper['MedlineCitation']['Article']['ArticleDate'][0]['Day'],
                    }
                }
            else:
                pass
    return results

def write_abstracts(results, directory, filename):
    filepath = directory + filename
    with open(filepath, 'w') as f:
        f.write(json.dumps(list(results.values())))
        

def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--output_directory",
        type=str,
        default="./",
        help="Path to downloaded directory",
    )
    parser.add_argument(
        "--start",
        type=str,
        required=True,
        help="Start date for PubMed search",
    )
    parser.add_argument(
        "--end",
        type=str,
        required=True,
        help="End date for PubMed search",
    )
    parser.add_argument(
        "--num_docs",
        type=int,
        default=10000,
        help="Max numer of documents to retrieve with PubMed search query",
    )
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    background_ids, reference_ids = fetch_idlist(start=args.start, end=args.end, max_docs=args.num_docs)
    if background_ids:
        abstracts = retrieve_abstracts(background_ids)
        print(f"{len(abstracts)} background documents downloaded")
        write_abstracts(abstracts, args.output_directory, "pubmed_background.json")

    if reference_ids:
        abstracts = retrieve_abstracts(reference_ids)
        print(f"{len(abstracts)} reference documents downloaded")
        write_abstracts(abstracts, args.output_directory, "pubmed_reference.json")
