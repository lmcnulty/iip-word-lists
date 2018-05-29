#!/usr/bin/env python3

import os
import sys
import traceback
import re
import glob
import argparse
import copy
import cltk

from collections import OrderedDict
from collections import defaultdict
from lxml import etree
from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
from nltk.corpus import stopwords

from repl import *
from wordlist_constants import *
from wordlist_output import *
from wordlist_strings import *
from wordlist_ngrams import *
from wordlist_classes import *
from wordlist_arguments import *
from wordlist_check_suspicious import *
from wordlist_commands import *

# Begin a new word as the supplied word. Will often be blank, such that
# future characters will be added.
def append_to_word_list(word_list, word):
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
def add_trailing_text(word_list, element, trailing_text, edition_type, 
                               lang, path, include_initial_line_break, 
                                                region, xml_context=""):
	# Make a list of tokens in the text following the tag
	for e in IGNORE:
		trailing_text.replace(e, " ")
	trailing_text_list = trailing_text.split() 
		
	# Add a new entry to the word list if it is empty or the previous 
	# word is complete
	if (len(word_list) == 0 or trailing_text[0] == ' ' 
	    or (trailing_text[0] == '\n' and include_initial_line_break)):
		if word_list[-1].text != "":
			append_to_word_list(word_list, iip_word_occurence( 
                                  edition_type, lang, "", path, region))
	# If the text in question is the inner text of the element, add it 
	# to the xml field of the generated word.
	if (trailing_text == element.text):
		try:
			word_list[-1].xml_context += \
			"<" + element.tag.replace(ns, "").replace(xmlNs, "") + ">"
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
			new_word = iip_word_occurence(edition_type, lang, 
			                     trailing_text_list[i], path, region)
			append_to_word_list(word_list, new_word)
	
	# If the last word is complete, add an empty word to the end of the
	# list.
	if (trailing_text[-1] == ' ' or trailing_text[-1] == '\n'):
		if word_list[-1].text != "":
			append_to_word_list(word_list, iip_word_occurence( 
			                    edition_type, lang, "", path, region))

def add_element_to_word_list(e, word_list, edition, mainLang, path, region):	
	# Get the language of the element
	editionLang = mainLang
	if (XML_NS + 'lang' in edition.keys()):
		editionLang = edition.attrib[XML_NS + 'lang']
	wordLang = editionLang
	
	# Get the subtype
	subtype = ""
	if "subtype" in edition.attrib:
		subtype = edition.attrib['subtype']

	# The last word in the list _at the time of calling the function_.
	prev_word = copy.copy(word_list[-1])
	
	if e.tag == TEI_NS + "gap":
		word_list[-1].contains_gap = True
	
	# Start a new word if the tag is a linebreak without break="no"
	if e.tag == TEI_NS + "lb" and not ('break' in e.attrib 
	                                   and e.attrib['break'] == "no"):
		append_to_word_list(word_list, iip_word_occurence(subtype, 
		                    editionLang, "", path, region))
	previous = e.getprevious()
	if (e.tag == TEI_NS + "expan" and previous != None 
	               and previous.tag == TEI_NS + "abbr"):
		if len(word_list[-1].text) < 1:
			del(word_list[-1])
		word_list[-1].text = ""
		word_list[-1].edition = edition

	# Add the text within the element not inside any child element
	if (e.text != None):	
		add_trailing_text(word_list, e, e.text, subtype, 
		                            wordLang, path, True, region)
	# Add each child element
	children = e.getchildren()
	for i in range(0, len(children)):
		# When adding children of a <choice> element, the preceding word
		# is added between children so that each possible version of the
		# word will appear in the final word list.
		if (e.tag == TEI_NS + "choice" and i > 0):
			append_to_word_list(word_list, prev_word)
		add_element_to_word_list(children[i], word_list, 
                                 edition, mainLang, path, region)
	try:
		word_list[-1].xml_context += \
		"</" + e.tag.replace(TEI_NS, "").replace(XML_NS, "") + ">"
	except:
		pass
		
	# Add the words following the element which are not in any sibling
	if (e.tail != None):
		add_trailing_text(word_list, e, e.tail, subtype, wordLang, 
		                  path, (e.tag in INCLUDE_TRAILING_LINEBREAK), 
		                                                        region)

def get_words_from_file(path, file_dict):
	root = etree.parse(path).getroot()
	words = []
	nsmap = {'tei': "http://www.tei-c.org/ns/1.0"}
	bodies = root.findall('.//' + TEI_NS + 'body')
	textLang = root.find('.//' + TEI_NS + 'textLang')
	textRegion = root.find('.//' + TEI_NS + 'region')
	if textRegion != None:
		file_dict[path] = iip_file(path, textRegion.text)	
	mainLang = ""
	if (textLang != None):
		mainLang = textLang.attrib['mainLang']
	for edition in root.findall(".//tei:div[@type='edition']", 
	                                          namespaces=nsmap):
		new_words = [iip_word_occurence(edition.attrib['subtype'], 
		                            mainLang, "", path, textRegion.text)]
		add_element_to_word_list(edition, new_words, edition, 
		                                     mainLang, path, textRegion.text)
		words += new_words
	for translation in root.findall(".//tei:div[@type='translation']", 
	                                                  namespaces=nsmap):
		if mainLang.strip == "":
			mainLang = "unk"
		mainLang += "-transl"
		new_words = [iip_word_occurence("translation", mainLang, 
		                                          "", path, textRegion.text)]
		add_element_to_word_list(translation, new_words, 
		                         translation, mainLang, path, textRegion.text)
		words += new_words
	null_words = []
	for word in words:
		word.text = str(word.text)
		for pattern in IGNORE:
			word.text = word.text.replace(pattern, "")
		if (word.text.strip() == ""):
			null_words.append(word)	
		if word.language.strip() == "":
			word.language = "unk"
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

def remove_digits(some_string):
	return ''.join([i for i in some_string if not i.isdigit()])

la_corpus_importer = CorpusImporter('latin')
la_corpus_importer.import_corpus('latin_text_latin_library')
la_corpus_importer.import_corpus('latin_models_cltk')
la_lemmatizer = LemmaReplacer('latin')
grc_corpus_importer = CorpusImporter('greek')
grc_corpus_importer.import_corpus('greek_models_cltk')
grc_lemmatizer = LemmaReplacer('greek')
def lemmatize(word_list, copy):
	for word in word_list:
		if copy:
			word.lemmatization = word.text
			return
		if word.language in LATIN_CODES:
			word.lemmatization = \
			    remove_digits(la_lemmatizer.lemmatize(word.text)[0])
		elif word.language in GREEK_CODES:
			word.lemmatization = \
			    remove_digits(grc_lemmatizer.lemmatize(word.text)[0])
		else:
			word.lemmatization = word.text

def print_word_info(word_string, word_dict):
	print("")
	language_dict = word_dict[word_string]
	for language in language_dict:
		word = language_dict[language]
		occurences = language_dict[language].occurences
		print("___" + language + "___")
		print("Occurances: " + str(len(occurences)))
		print("Variations: ")
		for variation in word.variations:
			print("    " + variation)
		print("Files: ")
		for file_name in word.files:
			print("    " + file_name)
		print("Regions")
		for region in word.regions:
			print("    " + region)
		print("")



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="""Produce word list 
	                                                from files.""")
	args = add_arguments(parser).parse_args()

	# Extract words from each file
	occurences = []  # Contains the iip_word_occurence objects 
	# Contains the iip_word objects
	word_dict = defaultdict(lambda: defaultdict(lambda: iip_word()))
	file_dict = {} # Maps file names to iip_file objects
	languages = set()
	
	plaintextdir = "flat"
	plaintext_lemmatize = True
	if args.nolemma != None:
		plaintext_lemmatize = not args.nolemma
	if args.flat != None:
		plaintextdir = args.flat
	for file in args.files:
		try:
			new_words = get_words_from_file(file, file_dict)
			lemmatize(new_words, args.nolemma)
			if args.plaintext:
				occurence_list_to_plain_text(new_words, plaintextdir +"/"
				                        + file.replace(".xml", ""))
			occurences += new_words
		except Exception as exception:
			if args.fileexception:
				raise exception
			else:
				sys.stderr.write("Cannot read " + file + "\n")

	# If this is too slow, it should be changed to be parameters for 
	# get_words_from_file so as to avoid iterating over the entire 
	# list.		
	filtered_words = []
	stop_words = set(stopwords.words('english'))
	for word in occurences:
		languages.add(word.language)
		# Filter the word ocurances if necessary
		add = True
		if args.nodiplomatic:
			if word.edition_type == "diplomatic":
				add = False
		if args.engstops:
			if (word.text in stop_words and 
			          "transl" in word.language):
				add = False
		if add:
			filtered_words.append(word)
		# Add occurences to dictionary
		word_dict[word.lemmatization.lower()][word.language].occurences.append(word)
		word_dict[word.lemmatization.lower()][word.language].variations.add(word.text)
		word_dict[word.lemmatization.lower()][word.language].files.add(word.file_name)
		word_dict[word.lemmatization.lower()][word.language].language = word.language
		word_dict[word.lemmatization.lower()][word.language].lemma = word.lemmatization
		word_dict[word.lemmatization.lower()][word.language].regions.add(file_dict[word.file_name].region)
		check_suspicious(word_dict[word.lemmatization.lower()][word.language])
		
	if args.nodiplomatic or args.engstops:
		occurences = filtered_words

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
		occurences = sorted(occurences, key=lambda word: 
			                        word.__dict__[field])
	# Print each extracted word on a new line
	if not args.silent:
		for word in occurences:		
			word.print()

	# Output words to files
	output_name = DEFAULT_OUTPUT_NAME;
	if args.name != None:
		output_name = args.name
	if args.html:
		occurence_list_to_html(occurences, langfiles=args.langfiles)
	if args.csv:
		occurence_list_to_csv(occurences, langfiles=args.langfiles)
	if args.html_general:
		word_list_to_html(word_dict, languages, output_name=".")
	if args.repl:
		main_repl = repl_instance()
		main_repl.add_repl_command(word_info_command(word_dict))
		main_repl.run_repl()
	sys.exit(0)
