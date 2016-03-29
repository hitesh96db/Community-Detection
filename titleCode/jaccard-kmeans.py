#!/usr/bin/env python

import sys
import networkx as nx
import createGraph
from numpy import array
from scipy.cluster.vq import kmeans, kmeans2, vq
from numpy.random import rand
from pylab import plot, show
import cPickle as pickle
import random

# Cluster into 10 groups
K = 10
MAX_ITERATIONS = 5
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

def run():

    global K, colors

    papers = pickle.load(open("papers_dict.p", "rb"))
    print "Constructing graph..."
    G = createGraph.loadGraph()
    print "Completed"
    nodes_list = G.nodes()

    # Pick any K random nodes as the centroids
    centroids = random.sample(nodes_list, K)

    iteration_no = 0

    print "Running K-means..."

    while True:

        # Termination condition
        if iteration_no == MAX_ITERATIONS:
            break
        
        # One cluster for every centroid
        clusters = [[] for no in xrange(0, K)]

        for node in nodes_list:
            idx = 0
            # Cluster index
            c_idx = 0
            max_jacc = 0.0

            # Find closest centroid            
            for c in centroids:
                # Neighbours of node
                n_node = nx.all_neighbors(G, node)
                # Neighbours of centroid
                n_c = nx.all_neighbors(G, c)
                val1 = len(set(n_node).intersection(n_c))
                val2 = len(set(n_node).union(n_c))
                # Calculate Jaccard similarity
                # Include the node and centroid in the union
                jacc = float(val1)/(val2 + 2.0)
                """
                try:
                    jacc = float(val1)/val2
                except ZeroDivisionError:
                    # ?
                    jacc = 0.0
                """
                if jacc >= max_jacc:
                    c_idx = idx
                    max_jacc = jacc
                idx += 1
    
            # Append node to the cluster
            clusters[c_idx].append(node)
       
        # Add centroids to respective clusters
        for no in xrange(0, len(centroids)):
            if centroids[no] not in clusters[no]:
                clusters[no].append(centroids[no])
 
        centroids = []

        # Formed our cluster, find new set of centroid points
        for cluster in clusters:
            # Choose the node with most neighbours as new centroid ?
            max_edges = 0
            new_centroid = None
            for node in cluster:
                no_of_edges = len(list(nx.all_neighbors(G, node)))
                if no_of_edges >= max_edges:
                    new_centroid = node
                    max_edges = no_of_edges

            if new_centroid == None:
                # Do this ?
                # Should never happen
                sys.stderr.write("One of the clusters was empty. Please restart\n")
                sys.exit(2)
            else:
                centroids.append(new_centroid)

        iteration_no += 1
        print "Completed Iteration " + str(iteration_no)

    print "K-Means completed."
    # Done with k-means
    # Output result
    cNo = 1
    for cluster in clusters:
        print "##########################"
        print "Cluster " + str(cNo)
        for node in cluster[:15]:
            print node, papers[node]["raw_title"]
        print "##########################"
        print
        print
        cNo += 1


if __name__ == "__main__":
    run()
