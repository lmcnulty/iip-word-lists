#!/usr/bin/env python3

import os
import sys
from lxml import etree
import glob

DEBUG = True 
ns = "{http://www.tei-c.org/ns/1.0}"

ignore = ['(?)']

class iip_word:
	def __init__(self, edition_type, language,  text):
		# eg: diplomatic
		self.edition_type = edition_type
		# eg: grc
		self.language = language
		# eg: Πἁποϲ
		self.text = text

def whitespace_to_space(text):
	return " ".join(text.split())

def get_words_from_file(path):
	words = []
	tree = etree.parse(path)
	root = tree.getroot()
	nsmap = {'tei': "http://www.tei-c.org/ns/1.0"}
	bodies = root.findall('.//tei:body', namespaces=nsmap)
	for body in bodies:
		editions = body.findall(".//tei:div[@type='edition']", namespaces=nsmap)
		for edition in editions:
			text = "" 
			for e in edition.iter():
				#print_debug(e)
				if e.tag == ns + "lb":
					if 'break' in e.attrib:
						if e.attrib['break'] != "no":
							text += " "
					else:
						text += " "
				if (e.text != None):
					#print_debug(whitespace_to_space(e.text))
					text += whitespace_to_space(e.text)
				#print_debug("tail" + whitespace_to_space(str(e.tail)))
				text += whitespace_to_space(e.tail)
			for item in ignore:
				text = text.replace(item, "")
			print_debug(text)

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
		print(word)
	
	sys.exit(0)


