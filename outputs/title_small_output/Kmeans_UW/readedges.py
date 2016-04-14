#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import cPickle as pickle


def loadGraph():
    pg = pickle.load(open("uw_graph_dict.p", "rb"))

    G = nx.Graph()
    G.add_nodes_from(pg["ids_list"])
    G.add_edges_from(pg["edges_list"])
    
    return G

def writeNodesToFile(nodes):
    with open("uw_nodes.txt", 'w+') as f:
        for node in nodes:
            print node
            f.write(node + '\n')

def writeEdgesToFile(edges):
    
    string_format = '%s,%s\n'
    
    with open("uw_edges.txt", 'w+') as f:
        for edge in edges:
            #print edge
            f.write(string_format % edge)


if __name__ == "__main__":
    
    G=loadGraph()
    nodesList=G.nodes()
    edgesList=G.edges()
    #writeNodesToFile(nodesList)
    writeEdgesToFile(edgesList)
    
   
