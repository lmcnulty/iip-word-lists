#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
import nltk
from nltk import ngrams
from collections import Counter

if __name__ == '__main__':
	path = "."
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	corpus = []
	counter = 0
	for e in onlyfiles:
		f = open(e)
		corpus.append(f.read())
		counter += 1
		if counter > 10000:
			break
	bigrams = []
	for text in corpus:
		token = nltk.word_tokenize(text)
		new_bigrams = ngrams(token, 2)
		bigrams += new_bigrams
	print(Counter(bigrams))
