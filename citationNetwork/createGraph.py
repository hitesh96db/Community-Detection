#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import cPickle as pickle


# Return the list of nodes and edges from the file
def getNodesEdges(citationNetworkFileName, weighted):
    citationNetworkFile = open(citationNetworkFileName, 'r')

    # list of nodes, edges as (node1, node2)
    nodes = []
    edges = []

    for citation in citationNetworkFile:
        citation = citation.split()

        nodes.append(citation[0])
        nodes.append(citation[2])

        edges.append([citation[0], citation[2]])

    nodes = list(set(nodes))

    if weighted == 'w':
        weightedEdges = []

        cnt = 0

        for edge in edges:
            weightedEdges.append((edge[0], edge[1], edges.count(edge) + edges.count((edge[1], edge[0]))))
            cnt += 1

        weightedEdges = list(set(weightedEdges))

        return ((nodes, weightedEdges))

    else:
        for i in range(len(edges)):
            edges[i] = tuple(edges[i])

        return ((nodes, edges))
    

# Gets the list of nodes and edges and Stores them.
def buildGraph(citationNetworkFileName, weighted):
    nodes, edges = getNodesEdges(citationNetworkFileName, weighted)

    # Store 'nodes', 'edges'
    pseudo_Graph = {
        "nodes_list": nodes,
        "edges_list": edges
    }
    pickle.dump(pseudo_Graph, open(weighted + "_graph_dict.p", "wb"))


# Create networkx graph from 'nodes', 'edges'
def loadGraph(weighted):
    pg = pickle.load(open(weighted + "_graph_dict.p", "rb"))

    G = nx.Graph()
    G.add_nodes_from(pg["nodes_list"])

    if weighted == 'w':
        G.add_weighted_edges_from(pg["edges_list"])
    else:
        G.add_edges_from(pg["edges_list"])
    
    return G


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: " + sys.argv[0] + " <citation_network_fileName> <weighted(w) / unweighted(uw)>\n")
        sys.exit(2)

    citationNetworkFileName = sys.argv[1]

    weighted = sys.argv[2]

    buildGraph(citationNetworkFileName, weighted)

    G = loadGraph(weighted)

    print "Number of Nodes in Community Graph (number of research papers considered): ", G.number_of_nodes()
    print "Number of Edges in Community Graph", G.number_of_edges()
    