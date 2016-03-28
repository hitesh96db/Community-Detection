#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs

remPunctSpace = re.compile(ur"[\{\}\|\:\;\"\'\/\?\[\]\+\=\\`\~\!\$\#\^\*\(\)\_\-\<\>\@\%\&]", flags = re.U)
remPunctNoSpace = re.compile(ur"[\,\.]", flags = re.U)
punct = re.compile(ur"&quot;|&gt;|&lt;|&nbsp;", flags = re.U)

def getStopWords():
	sw = open("english_stopwords.txt", 'r')
	sw = sw.readlines()
	sw = map(lambda x: x.split()[0].lower(), sw)

	return sw

def tokenize(tokenString, stopWords = "Rem"):
	tokenString = re.sub(punct, " ", tokenString)
	tokenString = re.sub(remPunctSpace, " ", tokenString)
	tokenString = re.sub(remPunctNoSpace, "", tokenString)

	tokenString = tokenString.split()

	tokenString = map(lambda x: x.split()[0].lower(), tokenString)

	if (stopWords == "NoRem"):
		return tokenString

	else:
		stopWords = getStopWords()

		tokenString = filter(lambda x: x not in stopWords, tokenString)

		return tokenString