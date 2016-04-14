#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import cPickle as pickle

MAX_NODES = 20
DATA_DIR = 'data/'
DATASET_FILE = '../../aan/release/2013/author_citation_network.txt' 

# Return the list of nodes and edges from the file
def getNodesEdges(citationNetworkFileName, weighted):

    global MAX_NODES

    citationNetworkFile = open(citationNetworkFileName, 'r')

    # list of nodes, edges as (node1, node2)
    nodes = []
    edges = []

    num_nodes = 0

    for citation in citationNetworkFile:
        citation = citation.split()

        if citation[0] not in nodes:
            num_nodes += 1
        if citation[2] not in nodes:
            num_nodes += 1

        nodes.append(citation[0])
        nodes.append(citation[2])        
        edges.append([citation[0], citation[2]])

        if num_nodes >= MAX_NODES:
            break

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
    
def writeNodesToFile(nodes):
    with open(DATA_DIR + "nodes.txt", 'w+') as f:
        for node in nodes:
            f.write(node + '\n')

def writeEdgesToFile(edges, weighted):
    if weighted == 'w':
        # Source, Target, Weight
        string_format = '%s,%s,%s\n'
    else:
        # Source, Target
        string_format = '%s,%s\n'

    with open(DATA_DIR + weighted + "_edges.txt", 'w+') as f:
        for edge in edges:
            f.write(string_format % edge)

# Gets the list of nodes and edges and Stores them.
def buildGraph(citationNetworkFileName, weighted):
    print "Reading file"
    print "Finding nodes and edges"
    nodes, edges = getNodesEdges(citationNetworkFileName, weighted)
    print "Writing nodes and edges to file"
    writeNodesToFile(nodes)
    writeEdgesToFile(edges, weighted)

    # Store 'nodes', 'edges'
    pseudo_Graph = {
        "nodes_list": nodes,
        "edges_list": edges
    }
    pickle.dump(pseudo_Graph, open(DATA_DIR + weighted + "_graph_dict.p", "wb"))
    print "Completed"

# Create networkx graph from 'nodes', 'edges'
def loadGraph(weighted):
    pg = pickle.load(open(DATA_DIR + weighted + "_graph_dict.p", "rb"))

    G = nx.Graph()
    G.add_nodes_from(pg["nodes_list"])

    if weighted == 'w':
        G.add_weighted_edges_from(pg["edges_list"])
    else:
        G.add_edges_from(pg["edges_list"])
    
    return G


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: " + sys.argv[0] + " <weighted(w) / unweighted(uw)>\n")
        sys.exit(2)

    citationNetworkFileName = DATASET_FILE

    weighted = sys.argv[1]

    buildGraph(citationNetworkFileName, weighted)

    G = loadGraph(weighted)

    print "Number of Nodes in Community Graph (number of research papers considered): ", G.number_of_nodes()
    print "Number of Edges in Community Graph", G.number_of_edges()
