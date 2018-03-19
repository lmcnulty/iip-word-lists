#!/usr/bin/env python3

import os
import sys
from lxml import etree
import glob

DEBUG = True 
ns = "{http://www.tei-c.org/ns/1.0}"
xmlNs = "{http://www.w3.org/XML/1998/namespace}"

ignore = ['(?)', ',', ';', '.', ':', '"', "'", "<", ">"]

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

def word_list_to_str_list(word_list):
	str_list = ""
	for e in word_list:
		str_list += e.text + " "
	return str_list

def add_trailing_text(word_list, trailing_text, edition_type, lang):
	trailing_text_list = trailing_text.split() 
	if len(word_list) == 0 or trailing_text[0] == ' ' or trailing_text[0] == '\n':
		word_list.append(iip_word(edition_type, lang, ""))
	if len(trailing_text_list) < 1:
		return
	word_list[-1].text += trailing_text_list[0]
	if len(word_list) > 1:
		for i in range(1, len(trailing_text_list)):
			new_word = iip_word(edition_type, lang, trailing_text_list[i])
			word_list.append(new_word)
	if (trailing_text[-1] == ' ' or trailing_text[-1] == '\n'):
		word_list.append(iip_word(edition_type, lang, ""))
				

def add_element_to_word_list(e, new_words, edition, mainLang):
	editionLang = mainLang
	if (xmlNs+'lang' in edition.keys()):
		editionLang = edition.attrib[xmlNs+'lang']
	wordLang = editionLang
	if e.tag == ns + "lb" and not ('break' in e.attrib and e.attrib['break'] == "yes"):
		new_words.append(iip_word(edition.attrib['subtype'], editionLang, ""))
	if (e.text != None):
		print_debug(str(e) + " text: " + e.text)
		add_trailing_text(new_words, e.text, edition.attrib['subtype'], wordLang)
	for child in e.getchildren():
		add_element_to_word_list(child, new_words, edition, mainLang)
	if (e.tail != None):
		print_debug(str(e) + " tail: " + e.tail)
		add_trailing_text(new_words, e.tail, edition.attrib['subtype'], wordLang)
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
		
		new_words = [iip_word(edition.attrib['subtype'], mainLang, "")]
		add_element_to_word_list(edition, new_words, edition, mainLang)
		#for e in edition.getiterator():	
			#print_debug(e)
			#wordLang = editionLang
			#if e.tag == ns + "lb" and not ('break' in e.attrib and e.attrib['break'] == "yes"):
				#new_words.append(iip_word(edition.attrib['subtype'], editionLang, ""))
			#if (xmlNs+'lang' in e.keys()):
				#wordLang = e.attrib[xmlNs+'lang']
			#if (e.text != None):
				#print_debug(str(e) + " text: " + e.text)
				#add_trailing_text(new_words, e.text, edition.attrib['subtype'], wordLang)
			#if (e.tail != None):
				#print_debug(str(e) + " tail: " + e.tail)
				#add_trailing_text(new_words, e.tail, edition.attrib['subtype'], wordLang)
		
		words += new_words
	for word in words:
		word.text = str(word.text)
		for pattern in ignore:
			word.text = word.text.replace(pattern, "")
		if (len(word.text) < 1 or word.text == ""):
			word.text = "NULL"
			words.remove(word)
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


