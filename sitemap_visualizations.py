import json
import networkx as nx
import matplotlib.pyplot as plt
import collections
from urllib.parse import urlparse
import os

def analyze_sitemap(file_path):
    with open(file_path, 'r') as file:
        sitemap_data = json.load(file)

    base_url = list(sitemap_data.keys())[0]
    G = nx.DiGraph()
    internal_links = 0
    external_links = 0
    inbound_links = collections.Counter()

    for page, links in sitemap_data.items():
        G.add_node(page)
        for link in links:
            G.add_edge(page, link)
            if base_url in link:
                internal_links += 1
            else:
                external_links += 1
            inbound_links[link] += 1

    save_directory = os.path.dirname(file_path)

    # Site Structure Visualization
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=False, node_size=10, font_size=8, node_color="blue", edge_color="gray", arrowsize=10)
    plt.title("Site Structure Visualization")
    plt.savefig(os.path.join(save_directory, 'site_structure.png'), bbox_inches='tight')
    plt.show()

    # Page Link Distribution Analysis
    plt.figure(figsize=(14, 10))
    out_degrees = [degree for node, degree in G.out_degree() if degree > 0]
    degree_count = collections.Counter(out_degrees)
    deg, cnt = zip(*degree_count.items())
    plt.bar(deg, cnt, color="blue")
    plt.title("Page Link Distribution Analysis")
    plt.xlabel("Number of Outbound Links")
    plt.ylabel("Number of Pages")
    plt.tight_layout()
    plt.savefig(os.path.join(save_directory, 'link_distribution.png'), bbox_inches='tight')
    plt.show()

    # Top 10 External Domains Linked From the Site
    plt.figure(figsize=(18, 10))
    external_domains = collections.Counter()
    for links in sitemap_data.values():
        for link in links:
            if base_url not in link:
                domain = urlparse(link).netloc
                external_domains[domain] += 1
    top_domains = external_domains.most_common(10)
    labels, values = zip(*top_domains)
    plt.bar(labels, values, color="blue")
    plt.title("Top 10 External Domains Linked From the Site")
    plt.xlabel("Domains")
    plt.ylabel("Number of Links")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.savefig(os.path.join(save_directory, 'external_domains.png'), bbox_inches='tight')
    plt.show()

    # Internal vs. External Links Distribution
    plt.pie([internal_links, external_links], labels=['Internal', 'External'], colors=['blue', 'orange'], autopct='%1.1f%%')
    plt.title('Internal vs External Links Distribution')
    plt.savefig(os.path.join(save_directory, 'internal_external_links.png'))
    plt.show()

    # Top 10 Most Linked Pages
    plt.figure(figsize=(20, 10))  # Increase the figure size
    top_linked_pages = inbound_links.most_common(10)
    pages, links_count = zip(*top_linked_pages)
    plt.bar(pages, links_count, color='blue')
    plt.title('Top 10 Most Linked Pages')
    plt.xlabel('Pages')
    plt.ylabel('Number of Inbound Links')
    plt.xticks(rotation=75)  # Rotate the labels by 75 degrees
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.35)  # Adjust the bottom margin
    plt.savefig(os.path.join(save_directory, 'most_linked_pages.png'), bbox_inches='tight')
    plt.show()

# Example call to the function
# analyze_sitemap('path/to/sitemap.json')
