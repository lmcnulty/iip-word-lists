import nltk
import sys
from nltk.text import Text  
from nltk.corpus import PlaintextCorpusReader
import io

def concordance_string(files_list, word):
	text = "" 
	for e in files_list:
		print("Reading: " + e)
		f = open(e, "r")
		text += f.read()
		f.close()
	print("Completeing concordance...")
	sys.stdout = concordance = io.StringIO()
	nltk.Text(nltk.word_tokenize(text)).concordance(word)
	sys.stdout = sys.__stdout__
	return concordance.getvalue()
