#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import cPickle as pickle

DATA_DIR = 'data/'

# loads the matrix in 'similarityFileName' into 'similarityMatrix' and list of ids 'ids'
def getMatrix(similarityFileName):
    similarityFile = open(DATA_DIR + similarityFileName, 'r')

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
def getEdges(ids, similarityMatrix, weighted, avgSimilarity = None,):
    edges = []

    if weighted == 'w':
        for i in range(len(similarityMatrix)):
            for j in range(i, len(similarityMatrix[i])):
                edges.append((ids[i], ids[j], float(similarityMatrix[i][j])))

    else:            
        for i in range(len(similarityMatrix)):
            for j in range(i, len(similarityMatrix[i])):
                if float(similarityMatrix[i][j]) > avgSimilarity:
                    edges.append((ids[i], ids[j]))

    return edges


def buildGraph(similarityFileName, weighted):
    ids, similarityMatrix = getMatrix(similarityFileName)

    if weighted == 'w':
        edges = getEdges(ids, similarityMatrix, weighted = weighted)
    else:
        avgSimilarity = getAvgSimilarity(similarityMatrix)
        edges = getEdges(ids, similarityMatrix, weighted, avgSimilarity)

    pseudo_Graph = {
        "ids_list": ids,
        "edges_list": edges
    }
    pickle.dump(pseudo_Graph, open(DATA_DIR + weighted + "_graph_dict.p", "wb"))


def loadGraph(weighted):
    pg = pickle.load(open(DATA_DIR + weighted + "_graph_dict.p", "rb"))

    G = nx.Graph()
    G.add_nodes_from(pg["ids_list"])

    if weighted == 'w':
        G.add_weighted_edges_from(pg["edges_list"])
    else:
        G.add_edges_from(pg["edges_list"])
        
    return G


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: " + sys.argv[0] + " <Similarity Vector File Name> <weighted(w) / unweighted(uw)>")
        sys.exit(2)

    similarityFileName = sys.argv[1]
    weighted = sys.argv[2]

    buildGraph(similarityFileName, weighted)
