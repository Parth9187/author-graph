def expand_graph(graph,
                 nodes,
                 edges):

    for url, name in nodes:
      if url not in graph.nodes:
        graph.add_node(url, authorname=name)

    for (url1, url2), info in edges:
      graph.add_edge(url1, url2, paperinfo=info)

    return True