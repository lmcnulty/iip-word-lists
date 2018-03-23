#!/usr/bin/env python3

import os
import sys
from lxml import etree
import glob

DEBUG = True 
ns = "{http://www.tei-c.org/ns/1.0}"
xmlNs = "{http://www.w3.org/XML/1998/namespace}"

ignore = ['(', '?', ')', ',', ';', '.', ':', '"', "'", "<", ">", "+", "[", "]", "∙"]
include_trailing_linebreak = [ns+"expan"]

class iip_word:
	def __init__(self, edition_type, language,  text, file_name):
		# eg: diplomatic
		self.edition_type = edition_type
		# eg: grc
		self.language = language
		# eg: Πἁποϲ
		self.text = text
		# eg: jeru00001.xml
		self.file_name = file_name
	def print(self):
		print(self.text + " | " + self.language + " | " + self.edition_type + " | " + self.file_name)

def word_list_to_table(full_list, num=0):
	
	word_list = full_list[0:1000]
	next_list = full_list[1000:len(full_list)]

	html = etree.Element("html")
	head = etree.Element("head")
	title = etree.Element("title")
	title.text = "Word List"
	style_link = etree.Element("link")
	style_link.attrib["rel"] = "stylesheet"
	style_link.attrib["type"] = "text/css"
	style_link.attrib["href"] = "wordlist.css"
	body = etree.Element("body")
	table = etree.Element("table")
	body.append(table)
	head.append(title)
	head.append(style_link)
	html.append(head)
	html.append(body)

	table_header = etree.Element("tr")
	table_header_word = etree.Element("th")
	table_header_word.text = "Word"
	table_header_language = etree.Element("th")
	table_header_language.text = "Language"
	table_header_edition = etree.Element("th")
	table_header_edition.text = "Edition"
	table_header_file = etree.Element("th")
	table_header_file.text = "File"
	table_header.append(table_header_word)
	table_header.append(table_header_language)
	table_header.append(table_header_edition)
	table_header.append(table_header_file)
	table.append(table_header)
	
	for word in word_list:
		row = etree.Element("tr")
		text = etree.Element("td")
		text.text = (word.text)
		language = etree.Element("td")
		language.text = (word.language)
		edition_type = etree.Element("td")
		edition_type.text = (word.edition_type)
		file_name = etree.Element("td")
		file_name_link = etree.Element("a")
		file_name_link.text = (word.file_name)
		file_name_link.attrib["href"] = word.file_name
		file_name.append(file_name_link)

		row.append(text)
		row.append(language)
		row.append(edition_type)
		row.append(file_name)
		table.append(row)
	if num > 0:
		prev_link = etree.Element("a")
		prev_link.text = "Previous Page"
		prev_link.attrib["href"] = "wordlist-" + str(num - 1) + ".html"
		body.append(prev_link)
	if len(next_list) > 0:
		next_link = etree.Element("a")
		next_link.text = "Next Page"
		next_link.attrib["href"] = "wordlist-" + str(num + 1) + ".html"
		body.append(next_link)
	

	output_file = open("wordlist-" + str(num) + ".html", "w")
	output_file.write(etree.tostring(html, pretty_print=True).decode())
	output_file.close()

	style_file = open("wordlist.css", "w")
	style_file.write("""
		table {
			border-collapse: collapse;
		}
		th {
			background-color: black;
			color: white;
			text-align: left;
			border: 1px solid black;
		}
		th, td {
			padding: 3px;
			padding-right: 3ch;
		}
		td {
			border: 1px solid grey;
		}
	""")
	style_file.close()
	if (len(next_list) > 0):
		word_list_to_table(next_list, num + 1)

def whitespace_to_space(text):
	if text == None or len(text) < 1:
		return ""
	return " ".join(text.split())

def word_list_to_str_list(word_list):
	str_list = ""
	for e in word_list:
		str_list += e.text + " "
	return str_list

def add_trailing_text(word_list, trailing_text, edition_type, lang, path, include_initial_line_break):
	trailing_text_list = trailing_text.split() 
	if len(word_list) == 0 or trailing_text[0] == ' ' or (trailing_text[0] == '\n' and include_initial_line_break):
		if word_list[-1].text != "":
			word_list.append(iip_word(edition_type, lang, "", path))
	if len(trailing_text_list) < 1:
		return
	word_list[-1].text += trailing_text_list[0]
	if len(word_list) > 1:
		for i in range(1, len(trailing_text_list)):
			new_word = iip_word(edition_type, lang, trailing_text_list[i], path)
			word_list.append(new_word)
	if (trailing_text[-1] == ' ' or trailing_text[-1] == '\n'):
		if word_list[-1].text != "":
			word_list.append(iip_word(edition_type, lang, "", path))
				
def add_element_to_word_list(e, new_words, edition, mainLang, path):
	editionLang = mainLang
	if (xmlNs+'lang' in edition.keys()):
		editionLang = edition.attrib[xmlNs+'lang']
	wordLang = editionLang
	if e.tag == ns + "lb" and not ('break' in e.attrib and e.attrib['break'] == "yes"):
		new_words.append(iip_word(edition.attrib['subtype'], editionLang, "", path))
	if (e.text != None):
		add_trailing_text(new_words, e.text, edition.attrib['subtype'], wordLang, path, True)
	for child in e.getchildren():
		add_element_to_word_list(child, new_words, edition, mainLang, path)
	if (e.tail != None):
		add_trailing_text(new_words, e.tail, edition.attrib['subtype'], wordLang, path, (e.tag in include_trailing_linebreak))

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
		new_words = [iip_word(edition.attrib['subtype'], mainLang, "", path)]
		add_element_to_word_list(edition, new_words, edition, mainLang, path)
		words += new_words	
	null_words = []
	for word in words:
		word.text = str(word.text)
		if (len(word.text) < 1 or word.text == "" or word.text == '\n' or word.text == '\t' or word.text.isspace()):
			null_words.append(word)
		for pattern in ignore:
			word.text = word.text.replace(pattern, "")
	words = [x for x in words if x not in null_words]
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
		#try:
		words += get_words_from_file(file)
		#except:
		#	sys.stderr.write("Cannot read " + file + "\n")

	# Print each extracted word on a new line	
	for word in words:		
		word.print()

	word_list_to_table(words)

	sys.exit(0)


