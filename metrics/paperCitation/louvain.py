#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import networkx as nx
import cPickle as pickle
import community
import matplotlib.pyplot as plt
from createGraph import *

OUTPUT_DIR = 'output/'

# Load graph and get communities
def getCommunities(weighted):
    G = loadGraph(weighted)
    return (G, community.best_partition(G))


def writeToFile(communities):
    out = open(OUTPUT_DIR + weighted + "_communities_louvain.txt", 'w+')

    for node in communities:
        out.write(node + ',' + str(communities[node]) + '\n')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: " + sys.argv[0] + " <weighted(w) / unweighted(uw)>\n")
        sys.exit(2)

    weighted = sys.argv[1]

    G, communities = getCommunities(weighted)
    print "Communitites formed!"

    writeToFile(communities)
