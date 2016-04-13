#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import cPickle as pickle
import createGraph
import matplotlib.pyplot as plt

WEIGHTED = False
OUTPUT_DIR = 'output/'

def add_edge_wts(G):
    # For each node, it adds the weights of all the edges incident on the node
    node_wts = {}
    nodes = G.nodes()
    # Find the adjacency matrix
    adj = nx.adj_matrix(G)
    summation = adj.sum(axis=1)
    N = G.number_of_nodes()
    for x in xrange(0, N):
        node_wts[nodes[x]] = summation[x, 0]
    return node_wts

def total_weight(G):
    adj = nx.adj_matrix(G)
    N = G.number_of_nodes()
    total = 0.0
    for i in xrange(0, N):
        for j in xrange(i, N):
            total += adj[i, j]
    return total

def splitGraph(G):
    # Graph partitioning step
    # Graph is split into clusters/connected components
    print "Splitting graph into components..."
    initial_comp = nx.number_connected_components(G)
    new_comp = initial_comp
    while G.number_of_edges() and new_comp <= initial_comp:
        print G.number_of_edges()
        # Get the edge betweenness for all edges in graph 
        edge_bw = nx.edge_betweenness_centrality(G, weight=('weight' if WEIGHTED else None))
        # Find the largest edge betweenness value
        max_bw = max(edge_bw.iteritems(), key=lambda x: x[1])[1]
        # Remove all those edges from the graph that have the max bw
        for edge in edge_bw:
            if edge_bw[edge] == max_bw:
                # Delete edge
                G.remove_edge(edge[0], edge[1])
        # Find the number of new connected components
        new_comp = nx.number_connected_components(G)

def modularityValue(G, node_edges_wts, total_wt):
    # Calculate the modularity value 
    communities = nx.connected_components(G)
    new_node_edges_wts = add_edge_wts(G)
    value = 0.0
    for comm in communities:
        # Edges within communities, Random edges
        A, R = (0.0, 0.0)
        for node in comm:
            A += new_node_edges_wts[node]
            R += node_edges_wts[node]
        value += (A - (float(R*R)/(2 * total_wt)))
    return (value/float(2 * total_wt))

def runAlgo(G, node_edges_wts, total_wt):
    
    max_modularity = 0.0
    communities = None
    # Stop when no edges are left
    while G.number_of_edges():
        print "Iterating..."
        splitGraph(G)
        m = modularityValue(G, node_edges_wts, total_wt)
        print "Modularity - %s" % m
        if m >= max_modularity:
            max_modularity = m
            communities = nx.connected_components(G)

    return (max_modularity, communities)

def writeToFile(communities, weighted):
    with open(OUTPUT_DIR + weighted + "_communities.txt", 'w+') as f:
        for node in communities:
            f.write(node + ',' + str(communities[node]) + '\n')

def run():
    # Load the graph
    G = createGraph.loadGraph(weighted=('w' if WEIGHTED else 'uw'))
    if WEIGHTED:
        # Find the summation of all the edge weights in the graph
        total_wt = total_weight(G)
    else:
        total_wt = G.number_of_edges()

    # Sum the edge wts around each node
    node_edges_wts = add_edge_wts(G)
    #for node in G:
    #node_edges_wts[node] = len(G.edges(node))

    # Run the algorithm
    _, communities = runAlgo(G, node_edges_wts, total_wt)

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
