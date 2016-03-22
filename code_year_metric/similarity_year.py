#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time;
from parseData import *
from scipy import spatial



def getUniqueTokens(parsedData):
    tokens = []

    for i in parsedData:
        if i[2] not in tokens:
            print i[2]
            tokens.append(i[2])

    return tokens


def buildVectors(tokens, parsedData):
    idVectors = [[0 for y in range(len(tokens))] for x in range(len(parsedData))]        #????

    for i in range(len(parsedData)):
        for j in range(len(tokens)):
            idVectors[i][j] = parsedData[i][2].count(tokens[j])

    return idVectors


def buildSimilarityMatrix(parsedData):
    tokens = getUniqueTokens(parsedData)
    #print tokens
    idVectors = buildVectors(tokens, parsedData)
    #print idVectors
    similarityMatrix = [[0 for y in range(len(parsedData))] for x in range(len(parsedData))]      #????

    for i in range(len(parsedData)):
        for j in range(i, len(parsedData)):
            #print "i=",i, "j=",j
            similarityMatrix[i][j] = 1 - spatial.distance.cosine(idVectors[i], idVectors[j])

    #print similarityMatrix[1]

    return similarityMatrix


def writeMatrix(similarityMatrix, parsedData):
    out = open('similarity_year.txt', 'w+')

    for i in range(len(similarityMatrix)):
        out.write(parsedData[i][0])

        for j in range(len(similarityMatrix[i])):
            out.write(',' + str(similarityMatrix[i][j]))

        out.write('\n')


if __name__ == "__main__":
    print "start"
    startticks = time.time()
    dataFile = "../aan/release/2013/acl-metadata.txt"
    parsedData = parse(dataFile)
    print parsedData
    endticks = time.time()
    print "parsing done time:",endticks-startticks
    similarityMatrix = buildSimilarityMatrix(parsedData)
    print "similarity done.. time:",endticks-startticks
    print "write to file.."
    writeMatrix(similarityMatrix, parsedData)
    endticks = time.time()
    print endticks-startticks
