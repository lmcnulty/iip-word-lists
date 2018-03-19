#!/usr/bin/env python3

import os
import sys
from lxml import etree
import glob

DEBUG = True 
ns = "{http://www.tei-c.org/ns/1.0}"
xmlNs = "{http://www.w3.org/XML/1998/namespace}"

ignore = ['(?)', ',', ';', '.', ':', '"', "'"]

class iip_word:
	def __init__(self, edition_type, language,  text):
		# eg: diplomatic
		self.edition_type = edition_type
		# eg: grc
		self.language = language
		# eg: Πἁποϲ
		self.text = text
	def print(self):
		print(self.text + " | " + self.language + " | " + self.edition_type)
def whitespace_to_space(text):
	if text == None or len(text) < 1:
		return ""
	return " ".join(text.split())

def add_trailing_text(word_list, trailing_text_list, edition_type, lang):
	if (len(word_list) == 0):
		word_list += iip_word(edition_type, "", lang)
	if (len(trailing_text_list) < 1):
		return
	word_list[-1].text += trailing_text_list[0]
	for i in range(1, len(trailing_text_list)):
		print_debug(trailing_text_list[i])
		try:
			word_list += iip_word(edition_type, trailing_text_list[i], lang)
		except:
			continue

def get_words_from_file(path):
	root = etree.parse(path).getroot()
	words = []
	nsmap = {'tei': "http://www.tei-c.org/ns/1.0"}
	bodies = root.findall('.//' + ns + 'body')
	textLang = root.find('.//' + ns + 'textLang')
	mainLang = ""
	if (textLang != None):
		mainLang = textLang.attrib['mainLang']
	for edition in root.findall(".//tei:div[@type='edition']", namespaces=nsmap): 
		editionLang = mainLang
		if (xmlNs+'lang' in edition.keys()):
			editionLang = edition.attrib[xmlNs+'lang']
		new_words = [iip_word(edition.attrib['subtype'], mainLang, "")]
		for e in edition.iter():	
			wordLang = editionLang
			if e.tag == ns + "lb" and not ('break' in e.attrib and e.attrib['break'] == "yes"):
				new_words.append(iip_word(edition.attrib['subtype'], editionLang, ""))
			if (xmlNs+'lang' in e.keys()):
				wordLang = e.attrib[xmlNs+'lang']
			if (e.text != None):
				add_trailing_text(new_words, e.text.split(), edition.attrib['subtype'], wordLang)
			if (e.tail != None):
				add_trailing_text(new_words, e.tail.split(), edition.attrib['subtype'], wordLang)
		words += new_words
	for word in words:
		word.text = str(word.text)
		for pattern in ignore:
			word.text = word.text.replace(pattern, "")
		print_debug(word.text)
	return words

def print_usage():
	print("wordlist.py [file1] [file2] ... \n"
	       + "\t Create a list of words from the specified files")

def print_debug(string):
	if (DEBUG):
		print(string)

if __name__ == '__main__':
	# Check for correct usage
	if (len(sys.argv) < 2):
		print_usage()
		sys.exit(1)
	
	words = []

	# Extract words from each file 
	for file in sys.argv[1:len(sys.argv)]:
		print_debug(file)
		words += get_words_from_file(file)
	
	# Print each extracted word on a new line
	for word in words:
		word.print()
	
	sys.exit(0)


