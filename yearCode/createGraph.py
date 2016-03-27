#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx

# loads the matrix in 'similarityFileName' into 'similarityMatrix' and list of ids 'ids'
def getMatrix(similarityFileName):
    similarityFile = open(similarityFileName, 'r')

    ids = []
    similarityMatrix = []

    for line in similarityFile:
        line = line.split(',')

        # add the next id to 'ids' and similarityVector to 'similarityMatrix'
        ids.append(line[0])
        similarityMatrix.append(line[1:])

    return (ids, similarityMatrix)


# return average similarity between any two nodes
# to be used as a threshold fo adding an edge between any two nodes while forming the graph
def getAvgSimilarity(similarityMatrix):
    sumSimilarity = 0.0
    totalSimilarities = 0.0

    for i in range(len(similarityMatrix)):
        for j in range(i, len(similarityMatrix[i])):
            sumSimilarity += float(similarityMatrix[i][j])
            totalSimilarities += 1.0

    return (sumSimilarity/totalSimilarities)


# returns list of edges as [(node1, node2), ...]
def getEdges(ids, similarityMatrix, avgSimilarity):
    edges = []

    for i in range(len(similarityMatrix)):
        for j in range(i, len(similarityMatrix[i])):
            if float(similarityMatrix[i][j]) > avgSimilarity:
                edges.append((ids[i], ids[j]))

    return edges


def buildGraph(similarityFileName):
    ids, similarityMatrix = getMatrix(similarityFileName)
    avgSimilarity = getAvgSimilarity(similarityMatrix)

    edges = getEdges(ids, similarityMatrix, avgSimilarity)

    # creating the graph
    G = nx.Graph()
    
    G.add_nodes_from(ids)
    G.add_edges_from(edges)

    return G


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: " + sys.argv[0] + " <Similarity Vector File Name>")
        sys.exit(2)

    similarityFileName = sys.argv[1]

    G = buildGraph(similarityFileName)
    print "Number of Nodes in Community Graph (number of research papers considered): ", G.number_of_nodes()
    print "Number of Edges in Community Graph", G.number_of_edges()
