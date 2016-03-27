#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PorterStemmer import PorterStemmer

stemmer = PorterStemmer()

def stemList(tokens):
	tokens = [stemmer.stem(token, 0, len(token)-1) for token in tokens]
	return tokens