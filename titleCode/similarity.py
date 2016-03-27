#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parseData import *
from scipy import spatial

# returns list of unique tokens in 'titles'
def getUniqueTokens(parsedData):
    tokens = []

    for i in parsedData:
        for token in i[2]:
            if token not in tokens:
                tokens.append(token)

    return tokens


# build number_of_papers * number_of_unique_tokens incidence matrix
def buildVectors(tokens, parsedData):
    idVectors = [[0 for y in range(len(tokens))] for x in range(len(parsedData))]

    for i in range(len(parsedData)):
        for j in range(len(tokens)):
            idVectors[i][j] = parsedData[i][2].count(tokens[j])

    return idVectors


# build a number_of_papers * number_of_papers size matrix conatining similarity measure (cosine-similarity) between any two papers
def buildSimilarityMatrix(parsedData):
    tokens = getUniqueTokens(parsedData)
    idVectors = buildVectors(tokens, parsedData)

    similarityMatrix = [[0 for y in range(len(parsedData))] for x in range(len(parsedData))]

    for i in range(len(parsedData)):
        for j in range(i, len(parsedData)):
            print i, j
            similarityMatrix[i][j] = similarityMatrix[j][i] = \
                1 - spatial.distance.cosine(idVectors[i], idVectors[j])

    return similarityMatrix


# write the matrix into a file
def writeMatrix(similarityMatrix, parsedData):
    out = open('similarity_Title.txt', 'w+')

    for i in range(len(similarityMatrix)):
        out.write(parsedData[i][0])

        for j in range(len(similarityMatrix[i])):
            out.write(',' + str(similarityMatrix[i][j]))

        out.write('\n')


if __name__ == "__main__":
    dataFile = "../aan/release/2013/acl-metadata.txt"

    parsedData = parse(dataFile)
    similarityMatrix = buildSimilarityMatrix(parsedData)
    writeMatrix(similarityMatrix, parsedData)
