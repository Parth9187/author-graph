def extract_nodes_edges(listing, base_url_addon,
                        shared_papers_url=None,
                        proceedings_url=None,
                        different_style=False):

      assert not ( shared_papers_url and proceedings_url ), "Can't provide both shared_papers_url or proceedings_url"

      proceedings_nodes = list()
      proceedings_edges = list()
        
      if not different_style:
        paper_name = listing.find("h5", class_="issue-item__title").text
        paper_doi = listing.find("h5", class_="issue-item__title").find(href=True)['href']
        paper_doi = paper_doi.split("/")[-2] + '/' + paper_doi.split("/")[-1]

      else:
        paper_name = listing.find("h3", class_="issue-item__title").text
        paper_doi = listing.find("h3", class_="issue-item__title").find(href=True)['href']
        paper_doi = paper_doi.split("/")[-2] + '/' + paper_doi.split("/")[-1]

      paper_link = "https://doi.org/" + paper_doi
      paper_list = [paper_name, paper_doi, paper_link]

      if proceedings_url:
          paper_info = [paper_doi, paper_name, paper_link, proceedings_url]

      if not proceedings_url:
          paper_info = [paper_doi, paper_name, paper_link, "NoURL"]

      # Authors Information
      paper_authors_info = list()

      if not different_style:
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

      # Build Edges
      for a_one in range(len(paper_authors_info)):
        for a_two in range(a_one + 1, len(paper_authors_info)):

          author_one_url = paper_authors_info[a_one][0]
          author_two_url = paper_authors_info[a_two][0]

          # Tuple to link nodes for NetworkX
          author_urls = (author_one_url, author_two_url)

          # Combine tuple with Paper Details and add to Edges list()
          edge = [author_urls, paper_info]
          proceedings_edges.append(edge)

      # Build Nodes
      for author in paper_authors_info:
        if author not in proceedings_nodes:
          proceedings_nodes.append(author)

      return proceedings_nodes, proceedings_edges

