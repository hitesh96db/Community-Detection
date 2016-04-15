#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import cPickle as pickle

DATA_DIR = 'data/'
SIMILARITY_FILE = 'data/similarity_Year.txt'

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




# returns list of edges as [(node1, node2), ...]
def getEdges(ids, similarityMatrix):
    edges = []

    for i in range(len(similarityMatrix)):
        for j in range(i, len(similarityMatrix[i])):
            print i, j
            if float(similarityMatrix[i][j]) == 1:
                edges.append((ids[i], ids[j]))

    return edges


def buildGraph(similarityFileName):
    ids, similarityMatrix = getMatrix(similarityFileName)
    

    edges = getEdges(ids, similarityMatrix)

    pseudo_Graph = {
        "ids_list": ids,
        "edges_list": edges
    }
    pickle.dump(pseudo_Graph, open(DATA_DIR + "graph_dict.p", "wb"))

def loadGraph():
    pg = pickle.load(open(DATA_DIR + "graph_dict.p", "rb"))

    G = nx.Graph()
    G.add_nodes_from(pg["ids_list"])
    G.add_edges_from(pg["edges_list"])
    return G

if __name__ == "__main__":
    similarityFileName = SIMILARITY_FILE
    buildGraph(similarityFileName)
    #print "Number of Nodes in Community Graph (number of research papers considered): ", G.number_of_nodes()
    #print "Number of Edges in Community Graph", G.number_of_edges()
    
