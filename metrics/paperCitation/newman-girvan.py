#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import cPickle as pickle
import createGraph
import matplotlib.pyplot as plt

WEIGHTED = False
OUTPUT_DIR = 'output/'

def writeToFile(communities, weighted):
    with open(OUTPUT_DIR + weighted + "_communities_newman_girvan.txt", 'w+') as f:
        for node in communities:
            f.write(node + ',' + str(communities[node]) + '\n')

def girvan_newman(G, weight=None):
    """Find communities in graph using Girvan–Newman method.
    The Girvan–Newman algorithm detects communities by progressively removing
    edges from the original graph. Algorithm removes edge with the highest
    betweenness centrality at each step. As the graph breaks down into pieces,
    the tightly knit community structure is exposed and result can be depicted
    as a dendrogram.
    """
    # The copy of G here must include the edge weight data.
    g = G.copy().to_undirected()
    max_modularity = 0.0
    total_wt = g.number_of_edges()
    node_edges_wts = {}
    final_comm = None
    for node in g.nodes():
        node_edges_wts[node] = len(g.edges(node))

    while g.number_of_edges() > 0:
        print "Number of edges: ", g.number_of_edges()
        _remove_max_edge(g, weight)
        communities = tuple(
            list(H) for H in nx.connected_component_subgraphs(g))
        modularity = _modularityValue(communities, g, node_edges_wts, total_wt)
        print "Modularity : ", modularity
        if modularity >= max_modularity:
            max_modularity = modularity
            final_comm = communities

    print "Max Modularity: ", max_modularity
    return final_comm


def _modularityValue(communities, G, node_edge_wts, total_wt):
    value = 0.0
    for comm in communities:
        A, R = (0.0, 0.0)
        for node in comm:
            A += len(G.edges(node))
            R += node_edge_wts[node]
        value += (A - (float(R*R)/(2 * total_wt)))
    return (value/float(2 * total_wt))


def _remove_max_edge(G, weight=None):
    """
    Removes edge with the highest value on betweenness centrality.
    Repeat this step until more connected components than the connected
    components of the original graph are detected.
    """
    number_components = nx.number_connected_components(G)
    while nx.number_connected_components(G) <= number_components and G.number_of_edges():
        betweenness = nx.edge_betweenness_centrality(G, weight=weight)
        max_value = max(betweenness.values())
        # Use a list of edges because G is changed in the loop
        for edge in list(G.edges()):
            if betweenness[edge] == max_value:
                G.remove_edge(*edge)


def run():
    # Load the graph
    G = createGraph.loadGraph(weighted=('w' if WEIGHTED else 'uw'))
    # Run the algorithm
    communities = girvan_newman(G, weight=('weight' if WEIGHTED else None))

    partition = {}
    # Assign each node a community number
    community_id = 0
    for comm in communities:
        for node in comm:
            partition[node] = community_id
        community_id += 1

    writeToFile(partition, weighted=('w' if WEIGHTED else 'uw'))

if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.stderr.write("Usage: " + sys.argv[0] + " <weighted(w) / unweighted(uw)>\n")
        sys.exit(2)

    if sys.argv[1] == 'w':
        WEIGHTED = True

    run()
