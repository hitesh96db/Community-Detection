#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parseData import *
from scipy import spatial

# returns list of unique 'years'
def getUniqueYears(parsedData):
    years = []

    for i in parsedData:
        if i[3] not in years:
            
            years.append(i[3])

    return years


# build number_of_papers * number_of_unique_tokens incidence matrix
def buildVectors(years, parsedData):
    idVectors = [[0 for y in range(len(years))] for x in range(len(parsedData))]

    for i in range(len(parsedData)):
        for j in range(len(years)):
            idVectors[i][j] = parsedData[i][3].count(years[j])

    return idVectors


# build a number_of_papers * number_of_papers size matrix conatining similarity measure (cosine-similarity) between any two papers
def buildSimilarityMatrix(parsedData):
    years = getUniqueYears(parsedData)
    idVectors = buildVectors(years, parsedData)

    similarityMatrix = [[0 for y in range(len(parsedData))] for x in range(len(parsedData))]

    for i in range(len(parsedData)):
        for j in range(i, len(parsedData)):
            print i, j
            similarityMatrix[i][j] = similarityMatrix[j][i] = \
                1 - spatial.distance.cosine(idVectors[i], idVectors[j])

    return similarityMatrix


# write the matrix into a file
def writeMatrix(similarityMatrix, parsedData):
    out = open('similarity_Year.txt', 'w+')

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
