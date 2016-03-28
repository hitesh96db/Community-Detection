#!/usr/bin/env python

import sys
import networkx as nx
import createGraph
from numpy import array
from scipy.cluster.vq import kmeans, kmeans2, vq
from numpy.random import rand
from pylab import plot, show
import cPickle as pickle

# Cluster into 5 groups
K = 10
colors = [
    'or', # Red
    'og', # Green
    'ob', # Blue
    'oy', # Yellow
    'ok', # Black
    'om', # Magenta
    'oc', # Cyan
    'ow', # White
    ]

def getMatrix(similarityFileName):
    similarityFile = open(similarityFileName, 'r')

    ids = []
    similarityMatrix = []

    for line in similarityFile:
        line = line.strip('\n').split(',')

        ids.append(line[0])
        rest = map(lambda x: float(x), line[1:])
        similarityMatrix.append(rest)

    return (ids, similarityMatrix)

def run(fileName):

    global K, colors

    papers = pickle.load(open("papers_dict.p", "rb"))
#    G = createGraph.buildGraph(fileName)
#    k = nx.all_neighbors(G, G.nodes()[0])
    ids, similarityMatrix = getMatrix(similarityFileName)
    simMatrixArray = array(similarityMatrix)

    centroids, labels = kmeans2(simMatrixArray, K)

    dataArgs = []
    clusters = [[] for no in xrange(0, K)]

    for i in xrange(0, len(labels)):
        clusters[labels[i]].append(ids[i])
    
    for cNo in xrange(0, K):
        print "##########################"
        print "Cluster " + str(cNo + 1)
        for node in clusters[cNo][:10]:
            print node, papers[node]["raw_title"]
        print "##########################"
        print
        print

    for clusterNo in xrange(0, K):
        for dim in xrange(0, len(ids)):
            dataArgs.append(simMatrixArray[labels == clusterNo, dim])
        dataArgs.append(colors[clusterNo])

    plot(*dataArgs)
    show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: " + sys.argv[0] + " <Similarity Vector File Name>\n")
        sys.exit(2)

    similarityFileName = sys.argv[1]
    run(similarityFileName)
