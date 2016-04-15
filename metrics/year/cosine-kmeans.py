#!/usr/bin/env python

import sys
import networkx as nx
import createGraph
from numpy import array
from scipy.cluster.vq import kmeans, kmeans2, vq
from numpy.random import rand
from pylab import plot, show
import cPickle as pickle

from sklearn.cluster import KMeans

# Cluster into 10 groups
K = 15
DATA_DIR = 'data/'
OUTPUT_DIR = 'output/'
SIMILARITY_FILE = 'data/similarity_Year.txt'
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

def writeToFile(communities, weighted):
    with open(OUTPUT_DIR + weighted + "_communities_cosine_kmeans.txt", 'w+') as f:
        for node in communities:
            f.write(node + ',' + str(communities[node]) + '\n')


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

    papers = pickle.load(open(DATA_DIR + "papers_dict.p", "rb"))
    ids, similarityMatrix = getMatrix(SIMILARITY_FILE)
    simMatrixArray = array(similarityMatrix)

    # centroids, labels = kmeans2(simMatrixArray, K)

    print "Finding communities!"
    km = KMeans(n_clusters = K, init = "random")
    labels = km.fit_predict(similarityMatrix)

    dataArgs = []
    clusters = [[] for no in xrange(0, K)]

    for i in xrange(0, len(labels)):
        clusters[labels[i]].append(ids[i])

    print "Storing communities!"
    partition = {}
    cNo = 0
    for cluster in clusters:
        print "Cluster " + str(cNo)
        for node in cluster:
            partition[node] = cNo
        cNo += 1

    # No graph in this case
    writeToFile(partition, weighted='uw')

if __name__ == "__main__":
    run(SIMILARITY_FILE)
