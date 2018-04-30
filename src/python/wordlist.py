#!/usr/bin/env python3

import os
import sys
from collections import OrderedDict
from lxml import etree
from copy import copy
import glob
import argparse
import copy
from wordlist_constants import *
from wordlist_output import *
from wordlist_strings import *
import cltk
from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer

class iip_word:
	equivilence = ["edition_type", "language", "text", "file_name"]
	def __init__(self, edition_type, language,  text, file_name, contains_gap=False):
		# eg: diplomatic
		self.edition_type = edition_type
		# eg: grc
		if (language == "he"):
			self.language = "heb"
		elif (language == "lat"):
			self.language = "la"
		else:
			self.language = language
		# eg: Πἁποϲ
		self.text = text
		# eg: jeru00001.xml
		self.file_name = file_name
		# eg: happ<unclear>i</unclear>n<supplied>ess</supplied>
		self.xml_context = text
		self.lemmatization = "";
		
	def __hash__(self):
		new_hash = 0
		for e in iip_word.equivilence:
			new_hash += hash(getattr(self, e))
		return new_hash
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return hash(self) == hash(other)
		else:
			return False
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def append_string(self, string):
		self.text += string
		self.xml_context += string
	
	def print(self):
		print(self.text + " | " + self.lemmatization + " | " + self.language + " | " + self.edition_type + " | " + self.file_name + "|" + self.xml_context)

# Begin a new word as the supplied word. Will often be blank, such that
# future characters will be added.
def append_to_word_list(word_list, word):
	#for existing_word in word_list:
	#	if existing_word.text == word.text:
	#		existing_word.file_name += " " + word.file_name
	#		print(word.text + " == " + existing_word.text)
	#		return
	word_list.append(word)


# Add a string to the end of the last word in the word list.
def append_string_to_word_list_end(word_list, addition):
	word_copy = copy.deepcopy(word_list[-1])
	word_copy.append_string(addition)
	del word_list[-1]
	append_to_word_list(word_list, word_copy)
	

# Add to the supplied word list text that is either within a tag and 
# preceding all child elements or following a tag but before any sibling
# elements. In lxml terms, element.text() and element.tail()
def add_trailing_text(word_list, element, trailing_text, edition_type, lang, path, include_initial_line_break, xml_context=""):
	
	# Make a list of tokens in the text following the tag
	trailing_text_list = trailing_text.split() 
	
		
	# Add a new entry to the word list if it is empty or the previous 
	# word is complete
	if len(word_list) == 0 or trailing_text[0] == ' ' or (trailing_text[0] == '\n' and include_initial_line_break):
		if word_list[-1].text != "":
			append_to_word_list(word_list, iip_word(edition_type, lang, "", path))
	
	# If the text in question is the inner text of the element, add it 
	# to the xml field of the generated word.
	if (trailing_text == element.text):
		try:
			word_list[-1].xml_context += "<" + element.tag.replace(ns, "").replace(xmlNs, "") + ">"
		except:
			pass
			
	# If there is no trailing text, return.
	if len(trailing_text_list) < 1:
		return
	
	# Append first token of the trailing text to the last word in the 
	# list.
	append_string_to_word_list_end(word_list, trailing_text_list[0])
	
	# For all following words, add a new element to the words list.
	if len(word_list) > 1:
		for i in range(1, len(trailing_text_list)):
			new_word = iip_word(edition_type, lang, trailing_text_list[i], path)
			append_to_word_list(word_list, new_word)
	
	# If the last word is complete, add an empty word to the end of the
	# list.
	if (trailing_text[-1] == ' ' or trailing_text[-1] == '\n'):
		if word_list[-1].text != "":
			append_to_word_list(word_list, iip_word(edition_type, lang, "", path))


def add_element_to_word_list(e, word_list, edition, mainLang, path):	
	# Get the language of the element
	editionLang = mainLang
	if (XML_NS + 'lang' in edition.keys()):
		editionLang = edition.attrib[XML_NS + 'lang']
	wordLang = editionLang
	
	# The last word in the list _at the time of calling the function_.
	prev_word = copy.copy(word_list[-1])
	
	if e.tag == TEI_NS + "gap":
		word_list[-1].contains_gap = True
	
	# Start a new word if the tag is a linebreak without break="no"
	if e.tag == TEI_NS + "lb" and not ('break' in e.attrib and e.attrib['break'] == "no"):
		append_to_word_list(word_list, iip_word(edition.attrib['subtype'], editionLang, "", path))
	
	# Add the text within the element not inside any child element
	if (e.text != None):
		add_trailing_text(word_list, e, e.text, edition.attrib['subtype'], wordLang, path, True)
	
	# Add each child element
	children = e.getchildren()
	for i in range(0, len(children)):
		# When adding children of a <choice> element, the preceding word
		# is added between children so that each possible version of the
		# word will appear in the final word list.
		if (e.tag == TEI_NS + "choice" and i > 0):
			append_to_word_list(word_list, prev_word)
		add_element_to_word_list(children[i], word_list, edition, mainLang, path)
	
	try:
		word_list[-1].xml_context += "</" + e.tag.replace(TEI_NS, "").replace(XML_NS, "") + ">"
	except:
		pass
		
	# Add the words following the element which are not in any sibling
	if (e.tail != None):
		add_trailing_text(word_list, e, e.tail, edition.attrib['subtype'], wordLang, path, (e.tag in INCLUDE_TRAILING_LINEBREAK))

def get_words_from_file(path):
	root = etree.parse(path).getroot()
	words = []
	nsmap = {'tei': "http://www.tei-c.org/ns/1.0"}
	bodies = root.findall('.//' + TEI_NS + 'body')
	textLang = root.find('.//' + TEI_NS + 'textLang')
	mainLang = ""
	if (textLang != None):
		mainLang = textLang.attrib['mainLang']
	for edition in root.findall(".//tei:div[@type='edition']", namespaces=nsmap): 	
		new_words = [iip_word(edition.attrib['subtype'], mainLang, "", path)]
		add_element_to_word_list(edition, new_words, edition, mainLang, path)
		words += new_words	
	null_words = []
	for word in words:
		word.text = str(word.text)
		for pattern in IGNORE:
			word.text = word.text.replace(pattern, "")
		if (len(word.text) < 1 or word.text == "" or word.text == '\n' or word.text == '\t' or word.text.isspace()):
			null_words.append(word)	
	words = [x for x in words if x not in null_words]
	return words

def print_usage():
	print("wordlist.py [file1] [file2] ... \n"
		   + "\t Create a list of words from the specified files")

def print_debug(string):
	if (DEBUG):
		print(string)

def flatten_list(word_list):
	flat_list = []
	for word in word_list:
		flat_list.append(word.text)
	return flat_list

def remove_duplicates(items):
	return list(OrderedDict.fromkeys(items))

def remove_digits(some_string):
	return ''.join([i for i in some_string if not i.isdigit()])

def lemmatize(word_list):
	la_corpus_importer = CorpusImporter('latin')
	la_corpus_importer.import_corpus('latin_text_latin_library')
	la_corpus_importer.import_corpus('latin_models_cltk')
	la_lemmatizer = LemmaReplacer('latin')
	grc_corpus_importer = CorpusImporter('greek')
	grc_corpus_importer.import_corpus('greek_models_cltk')
	grc_lemmatizer = LemmaReplacer('greek')
	for word in word_list:
		if word.language in LATIN_CODES:
			word.lemmatization = remove_digits(la_lemmatizer.lemmatize(word.text)[0])
		elif word.language in GREEK_CODES:
			word.lemmatization = remove_digits(grc_lemmatizer.lemmatize(word.text)[0])
		else:
			word.lemmatization = word.text

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Produce word list from files.')
	parser.add_argument('files', type=str, nargs='+', help='The epidoc xml files to process')
	parser.add_argument("--html", help="Output list as html file(s)", action="store_true")
	parser.add_argument("--csv", help="Output list as csv file", action="store_true")
	parser.add_argument("--plaintext", help="Create flat text document for each parsed file", action="store_true")
	parser.add_argument("--silent", help="Don't print the word list to the console", action="store_true")
	parser.add_argument("--duplicates", help="Include each instance of every word in the word list", action="store_true")
	parser.add_argument("--nodiplomatic", help="Do not include words extracted from diplomatic editions in word list", action="store_true")
	parser.add_argument("--fileexception", help="Print exceptions for files which could not be read", action="store_true")
	parser.add_argument("--langfiles", help="Write a seperate file for each language", action="store_true")
	parser.add_argument("-s", "--sort", type=str, help="Sort the list by the specified fields")
	parser.add_argument("-n", "--name", type=str, help="The name of the output file without the extension")
	parser.add_argument("-f", "--flat", type=str, help="Specify the location to store plain text files.")
	parser.add_argument("--nolemma", help="Don't lemmatize words before writing to plain text files", action="store_true")
	args = parser.parse_args()

	# Extract words from each file
	words = []
	plaintextdir = "flat"
	plaintext_lemmatize = True
	if args.nolemma != None:
		plaintext_lemmatize = not args.nolemma
	if args.flat != None:
		plaintextdir = args.flat
	for file in args.files:
		if args.fileexception:
			new_words = get_words_from_file(file)
			lemmatize(new_words)
			if args.plaintext:
				word_list_to_plain_text(new_words, plaintextdir + "/" + file.replace(".xml", ""))
			words += new_words
		else:
			try:
				new_words = get_words_from_file(file)
				if args.plaintext:
					word_list_to_plain_text(new_words, plaintextdir + "/" + file.replace(".xml", ""), plaintext_lemmatize)
				words += new_words
			except:
				sys.stderr.write("Cannot read " + file + "\n")

	if not args.duplicates:
		words = remove_duplicates(words)

	# If this is too slow, it should be changed to be a parameter for 
	# get_words_from_file so as to avoid iterating over the entire list.
	if args.nodiplomatic:
		filtered_words = []
		for word in words:
			if word.edition_type != "diplomatic":
				filtered_words.append(word)
		words = filtered_words

	

	# Sort according to the given arguments before writing to file
	sort_order = []
	if args.sort != None:
		for e in args.sort:
			if e == 'l':
				sort_order.append("language")
			elif e == 't' or e == 'a':
				sort_order.append("text")
			elif e == 'f':
				sort_order.append("file_name")
			elif e == "e":
				sort_order.append("edition_type")
			else:
				print("Invalid sort criterion: '" + e + "'")
	sort_order.reverse()
	for field in sort_order:
		words = sorted(words, key=lambda word: word.__dict__[field])

	# Print each extracted word on a new line
	if not args.silent:
		for word in words:		
			word.print()

	# Output words to files
	output_name = DEFAULT_OUTPUT_NAME;
	if args.name != None:
		output_name = args.name
	if args.html:
		word_list_to_html(words, output_name=output_name, langfiles=args.langfiles)
	if args.csv:
		word_list_to_csv(words, output_name=output_name, langfiles=args.langfiles)
	sys.exit(0)
