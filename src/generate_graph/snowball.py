import requests
from bs4 import BeautifulSoup

from generate_graph.build_nodes_edges import extract_nodes_edges
from generate_graph.utils import expand_graph


def snowball_abstracts(author_url,
                       url_addon="https://dl.acm.org"):
      all_nodes = list()
      all_edges = list()

      author_publications = author_url + "/publications"

      r = requests.get(author_publications)
      soup = BeautifulSoup(r.text, 'html.parser')

      papers_list = soup.find_all("li", {"class": "search__item issue-item-container"})

      for paper in papers_list:
          nodes, edges = extract_nodes_edges(paper, url_addon, different_style=2)
          all_nodes += nodes
          all_edges += edges

      return all_nodes, all_edges


def snowball_cheap(author_url,
                   base_url_addon="https://dl.acm.org"):

    all_nodes = list()
    all_edges = list()

    r = requests.get(author_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    papers_div = soup.find("div", class_="multi-search multi-search--latest-issues")
    papers_li = papers_div.find_all("li", {"class": "grid-item"})


    for listing in papers_li:
        nodes, edges = extract_nodes_edges(listing, base_url_addon, different_style=1)
        all_nodes += nodes
        all_edges += edges

    return all_nodes, all_edges


def snowball_expensive(graph,
                       author_url,
                       base_url_addon="https://dl.acm.org"):

    all_nodes = list()
    all_edges = list()

    author_colleagues = author_url + "/colleagues"

    r = requests.get(author_colleagues)
    soup = BeautifulSoup(r.text, 'html.parser')

    colleages_ul = soup.find("ul", class_="rlist results-list")

    if colleages_ul == None:
      print("Scraping Blocked")
      return False

    colleages_li_list = colleages_ul.find_all("li")

    for colleague in colleages_li_list:
        col_info = colleague.find("div", class_="list__img")
        col_name = col_info.find("span").text

        col_profile_extension = col_info.find("a")["href"]
        col_url = base_url_addon + col_profile_extension

        shared_papers_url_div = colleague.find("div", class_="list__count hidden-xs")
        shared_papers_url = shared_papers_url_div.find("a")["href"]
        shared_papers_url = base_url_addon + shared_papers_url

        if int(shared_papers_url_div.find("a").text) >= 4:

            r = requests.get(shared_papers_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            papers_list = soup.find_all("li", {"class": "search__item issue-item-container"})
            for paper in papers_list:
                nodes, edges = extract_nodes_edges(paper, base_url_addon, shared_papers_url)
                all_nodes += nodes
                all_edges += edges

        else:
          print("Less than 1 Paper Published!")

    expand_graph(graph, all_nodes, all_edges)

    return True