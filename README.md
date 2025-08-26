# author-graph
Author information derived from public information about research.

## Overview
## Key Components

### Scraping Conference Proceedings

``` python
from generate_graph.proceedings_base import crawl_proceedings

# Build nodes and edges for CHIWORK 2023 proceedings
nodes, edges, doi_url = crawl_proceedings(
    "https://dl.acm.org/doi/proceedings/10.1145/3596671",
    base_url_addon="https://dl.acm.org",
    open_access=False
)
```

### Building the Base Graph

``` python
import networkx as nx
from generate_graph.utils import expand_graph

# start with an empty graph
g = nx.Graph()

# add nodes and edges obtained from crawl_proceedings
expand_graph(g, nodes, edges)

# write to disk for later use
nx.write_gml(g, "data/chiwork_base.gml")
```

### Extracting Nodes and Edges from Papers
**Collecting Metadata (Emails)**
``` python
import re, requests, io, PyPDF2

def get_emails(pdf_url):
    response = requests.get(pdf_url, stream=True)
    if response.content[:len(b"%PDF-")] != b"%PDF-":
        return []
    reader = PyPDF2.PdfReader(io.BytesIO(response.content))
    text = reader.pages[0].extract_text()
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+", text)
```

### Snowball Expansion
``` python
from generate_graph.snowball import snowball_generator

for author_id in list(g.nodes):
    success = snowball_generator(g, author_id)
    if not success:
        break  # handle IP blocks by resuming later
```

### Visualizing the Graph
``` python
import matplotlib.pyplot as plt
import networkx as nx

def graph_vis(graph, image_path):
    pos = nx.kamada_kawai_layout(graph)
    plt.figure(figsize=(15, 10))
    nx.draw(graph, pos, node_size=15, alpha=0.4, width=0.3)
    plt.savefig(image_path)
```
**Initial Plot of CHIWork '22 and '23**
![plot](./figures/chiwork.png)

**Expanded Abstracts Graph After 1 Snowball Cycle**
![plot](./figures/chiwork_showball_abstract.png)

### Analyzing Author Similarity

