#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from nltk import ngrams
from nltk import word_tokenize
from collections import Counter
import sys

def get_ngrams(n, corpora):
	bigrams = []
	for text in corpora:
		token = word_tokenize(text)
		new_bigrams = ngrams(token, n)
		bigrams += new_bigrams
	counter_bigrams = Counter(bigrams)
	return counter_bigrams.most_common()

if __name__ == '__main__':
	path = "."
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	corpus = []
	n = 2
	min_display = 1
	if len(sys.argv) > 1:
		n = int(sys.argv[1])
	if len(sys.argv) > 2:
		min_display = int(sys.argv[2]) - 1
	for e in onlyfiles:
		f = open(e)
		corpus.append(f.read())
	for e in get_ngrams(n, corpus):
		if (e[1] > min_display):
			sys.stdout.write(str(e[1]) + "\t")
			for f in e[0]:
				sys.stdout.write(f + " ")
			sys.stdout.write('\n')
