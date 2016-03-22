#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from tokenizer import *
from stemmer import *

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

    ids = paperIdRe.findall(data)
    titles = titleRe.findall(data)
    years = yearRe.findall(data)
    #print ids, titles, years
    titles = processTitles(titles)
    # Is any proccesing for 'year' required?
    
    return map(lambda x, y, z: (x, y, z), ids, titles, years)[:1000]

if __name__ == "__main__":
    dataFile = "../aan/release/2013/acl-metadata.txt"

    parsedData = parse(dataFile)
    #print "hi"
    #print parsedData
