#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from tokenizer import *
from stemmer import *
import cPickle as pickle

paperIdRe = re.compile(ur"id = \{(.*?)\}", flags = re.U)
titleRe = re.compile(ur"title = \{(.*?)\}", flags = re.U)
yearRe = re.compile(ur"year = \{(.*?)[\n]*\}", flags = re.U)


def processTitles(titles):
    for ind, title in enumerate(titles):
        title = tokenize(title)
        titles[ind] = stemList(title)

    return titles


def parse(dataFile):
    data = open(dataFile).read()

    # finds all the paper ids, titles, years and loads them into a list
    ids = paperIdRe.findall(data)
    raw_titles = titleRe.findall(data)
    years = yearRe.findall(data)
    
    # tokenize, case-fold, remove stop-words, stem titles
    titles = processTitles(raw_titles[:])
    
    # returns the data for first 10,000 papers as [(id, raw_title, title(after pre-processing, year)), ...]
    return map(lambda w, x, y, z: (w, x, y, z), ids, raw_titles, titles, years)[:10000]


if __name__ == "__main__":
    dataFile = "../aan/release/2013/acl-metadata.txt"
    parsedData = parse(dataFile)

    # Create dict dump of papers
    papers = {}
    for data in parsedData:
        papers[data[0]] = {"id": data[0],
                           "raw_title": data[1],
                           "title": " ".join(data[2]),
                           "year": data[3]}
    pickle.dump(papers, open("papers_dict.p", "wb"))
