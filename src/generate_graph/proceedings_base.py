import requests
from bs4 import BeautifulSoup

from generate_graph.build_nodes_edges import extract_nodes_edges

def crawl_proceedings(conference_proceedings_url_crawl,
                      base_url_addon,
                      open_access=False):

    proceedings_nodes = list()
    proceedings_edges = list()
 
    # Setup Proceedings URL - Used for Edge + Node Formation
    proceedings_doi_url = "https://doi.org/" + "/".join(conference_proceedings_url_crawl.split("/")[-2:])

    print(proceedings_doi_url, flush=True)

    # Give Soup Access to Page
    r = requests.get(conference_proceedings_url_crawl)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find All Papers
    items_listing = soup.find_all("div", {"class": "issue-item-container"})

    # Filter Open Access
    if open_access:
      open_access_listings = [listing for listing in items_listing if listing.find("div", class_="access-icon open-access")]
      free_listings = [listing for listing in items_listing if listing.find("div", class_="access-icon free-access")]
      listings = open_access_listings + free_listings
    else:
      listings = items_listing

    # Draw Data for Each Paper
    for listing in listings:

      nodes, edges = extract_nodes_edges(listing, base_url_addon, proceedings_url=proceedings_doi_url)

      if nodes and edges:
        proceedings_nodes += nodes
        proceedings_edges += edges

    # Return Nodes, and Edges
    return proceedings_nodes, proceedings_edges, proceedings_doi_url