#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parseData import *
from scipy import spatial

def getUniqueTokens(parsedData):
    tokens = []

    for i in parsedData:
        for token in i[1]:
            if token not in tokens:
                tokens.append(token)

    return tokens


def buildVectors(tokens, parsedData):
    idVectors = [[0 for y in range(len(tokens))] for x in range(len(parsedData))]

    for i in range(len(parsedData)):
        for j in range(len(tokens)):
            idVectors[i][j] = parsedData[i][1].count(tokens[j])

    return idVectors


def buildSimilarityMatrix(parsedData):
    tokens = getUniqueTokens(parsedData)
    idVectors = buildVectors(tokens, parsedData)

    similarityMatrix = [[0 for y in range(len(parsedData))] for x in range(len(parsedData))]

    for i in range(len(parsedData)):
        for j in range(i, len(parsedData)):
            print i, j
            similarityMatrix[i][j] = 1 - spatial.distance.cosine(idVectors[i], idVectors[j])

    print similarityMatrix[1]

    return similarityMatrix


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