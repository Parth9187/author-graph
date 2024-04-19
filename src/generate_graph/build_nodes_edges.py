def extract_nodes_edges(listing, base_url_addon,
                        shared_papers_url=None,
                        proceedings_url=None,
                        different_style=0):

      assert not ( shared_papers_url and proceedings_url ), "Can't provide both shared_papers_url or proceedings_url"

      proceedings_nodes = list()
      proceedings_edges = list()

      try:
        if different_style in [0, 2]:
          paper_name = listing.find("h5", class_="issue-item__title").text
          paper_doi = listing.find("h5", class_="issue-item__title").find(href=True)['href']
          paper_doi = paper_doi.split("/")[-2] + '/' + paper_doi.split("/")[-1]

          paper_access = "CLOSED"

          open = listing.find_all("div", {"title": "This content is available through an open access license"})
          if open:
            paper_access = "OPEN"

          public = listing.find_all("div", {"title": "This content is available through a public access license"})
          if public:
            paper_access = "PUBLIC"

          free = listing.find_all("div", {"title": "This content is available for free"})
          if free:
            paper_access = "FREE"
          

        else:
          paper_name = listing.find("h3", class_="issue-item__title").text
          paper_doi = listing.find("h3", class_="issue-item__title").find(href=True)['href']
          paper_doi = paper_doi.split("/")[-2] + '/' + paper_doi.split("/")[-1]

          paper_access = "CLOSED"

      except Exception as e:
        return False, False

      paper_link = "https://doi.org/" + paper_doi
      paper_list = [paper_name, paper_doi, paper_link]

      paper_abstract = "NoAbstract"
      if different_style in [2]:
        abstract_div = listing.find("div", class_="issue-item__abstract")
        if abstract_div:
          paper_abstract = abstract_div.find("p").text

      if shared_papers_url:
        pass
      

      if proceedings_url:
          paper_info = [paper_doi, paper_name, paper_link, proceedings_url, paper_abstract, paper_access]

      if not proceedings_url:
          paper_info = [paper_doi, paper_name, paper_link, "NoURL", paper_abstract, paper_access]

      paper_authors_info = list()

      if different_style in [0]:
        authors_ul = listing.find_all("ul", {"aria-label": "authors"})
        authors_li_list = [li.find_all("a") for li in authors_ul][0]

      else:
        authors_ul = listing.find_all("ul", {"title": "list of authors"})
        authors_li_list = [li.find_all("a") for li in authors_ul][0]

      for author in authors_li_list:
        author_name = author.find("span").text
        author_url = base_url_addon + author['href']
        author_info = [author_url, author_name]

        paper_authors_info.append(author_info)

      for a_one in range(len(paper_authors_info)):
        for a_two in range(a_one + 1, len(paper_authors_info)):

          author_one_url = paper_authors_info[a_one][0]
          author_two_url = paper_authors_info[a_two][0]

          author_urls = (author_one_url, author_two_url)

          edge = [author_urls, paper_info]
          proceedings_edges.append(edge)

      for author in paper_authors_info:
        if author not in proceedings_nodes:
          proceedings_nodes.append(author)

      return proceedings_nodes, proceedings_edges
