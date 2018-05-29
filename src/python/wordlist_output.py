from wordlist_constants import *
import os
from lxml import etree
from collections import defaultdict

def add_to_html_list(element, some_list):
	for e in some_list:
		new_element = etree.Element("li")
		new_element.text = e
		element.append(new_element)

def full_language(abbr):
	for codelist in codes:
		for code in codelist[1]:
			if code == abbr:
				return codelist[0]
	return abbr

def word_list_to_html(word_dict, languages, output_name=DEFAULT_OUTPUT_NAME):
	# Create top level directory
	if not os.path.exists(output_name):
		os.makedirs(output_name)
		
	# Create directory for each language
	for language in languages:
		if not os.path.exists(output_name + '/' + language):
			os.makedirs(output_name + '/' + language)
			
	# Create file for each word
	word_lists = defaultdict(lambda: [])
	for word in word_dict:
		for language in word_dict[word]:
			word_lists[language].append(word)
			root = etree.fromstring(INFO_PAGE_HTML)
			word_obj = word_dict[word][language]
			occurences = word_obj.occurences
			root.find(".//h1").text = (word + " [" + full_language(language).title() + "]")
			root.find(".//td[@id='num-occurences']").text = str(len(word_obj.occurences))
			add_to_html_list(root.find(".//ul[@id='variations']"), word_obj.variations)
			add_to_html_list(root.find(".//ul[@id='regions']"), word_obj.regions)
			xml_contexts = []
			for e in word_obj.occurences:
				row = etree.fromstring(OCCURENCE_TABLE_ROW_HTML)
				row.find(".//td[@id='variation']").text = e.text
				link = etree.Element('a')
				link.attrib['href'] = "../" + e.file_name
				link.text = e.file_name.split('/')[-1]
				row.find(".//td[@id='file']").append(link)
				row.find(".//td[@id='xml']").text = e.xml_context
				row.find(".//td[@id='region']").text = e.region
				root.find(".//table[@id='occurences']").append(row)
				xml_contexts.append(e.xml_context)
			files_list_html = root.find(".//ul[@id='files']")
			for e in word_obj.files:
				list_element = etree.Element("li")
				link = etree.Element("a")
				link.text = e.split('/')[-1]
				link.attrib["href"] = "../" + e
				list_element.append(link)
				files_list_html.append(list_element)
			try: 
				info_file = open(output_name + '/' + language + '/' + word + "_.html", 'w')
				info_file.write("<!DOCTYPE HTML>\n" + etree.tostring(root).decode("utf-8"))
				info_file.close()
			except:
				continue

	# Create index list for each language
	for language in word_lists:
		root = etree.fromstring(INDEX_PAGE_HTML)
		root.find(".//title").text = full_language(language).title()
		root.find(".//h1").text = full_language(language).title()
		word_list_html = root.find(".//noscript[@id='wordList']")
		words_object_string = ""
		for e in sorted(word_lists[language]):
			num_occurences = str(len(word_dict[e][language].occurences))
			
			# Write to javascript object (necessary for performance)
			words_object_string += '{'
			words_object_string += ("text: '" + e + "',").replace("\n", "").replace("\\", "");
			words_object_string += "occurences: " + num_occurences + ','
			if (word_dict[e][language].suspicious):
				words_object_string += "suspicious: true,"
			else:
				words_object_string += "suspicious: false,"
			words_object_string += '},\n'
			
			# Write directly to tags for noscript users
			list_element = etree.Element("li")
			list_element.attrib["data-num-occurences"] = num_occurences
			
			link = etree.Element("a")
			link.text = e
			link.attrib["href"] = "./" + e + "_.html"
			if (word_dict[e][language].suspicious):
				list_element.attrib["class"] = "suspicious"
			list_element.append(link)
			word_list_html.append(list_element)
			
		language_index_file = open(output_name + '/' + language + '/index.html', "w")
		language_index_file.write("<!DOCTYPE HTML>\n" + etree.tostring(root).decode("utf-8").replace("$WORDS_OBJECT", words_object_string))
		language_index_file.close()
		
	# Create front page for language selection
	root = etree.fromstring(FRONT_PAGE_HTML)
	for e in sorted(languages):
		list_element = etree.Element("li")
		link = etree.Element("a")
		link.text = e
		link.attrib["href"] = "./" + e
		list_element.append(link)
		root.find(".//ul").append(list_element)
	index_file = open(output_name + "/index.html", "w")
	index_file.write("<!DOCTYPE HTML>\n" + etree.tostring(root).decode("utf-8"))
	index_file.close()

def occurence_list_to_csv(full_list, output_name=DEFAULT_OUTPUT_NAME + "_occurences", langfiles=False):
	files = {}
	if not langfiles:
		if os.path.isfile(output_name + '.csv'):
			os.remove(output_name + '.csv')
		if os.path.isdir(output_name + '.csv'):
			sys.stderr.write(output_name + '.csv is a directory.')
			return
		output_file = open(output_name + ".csv", "a")
	
	for word in full_list:
		word_output_file = None
		if langfiles:
			if not word.language in files:
				if os.path.isfile(output_name + '.csv'):
					os.remove(output_name + '.csv')
				if os.path.isdir(output_name + '.csv'):
					sys.stderr.write(output_name + '.csv is a directory.')
				files[word.language] = open(output_name + "_" + word.language + ".csv", "a")
			word_output_file = files[word.language]
		else:
			word_output_file = output_file
		word_output_file.write(word.text + ", ") 
		word_output_file.write(word.lemmatization + ", ") 
		word_output_file.write(word.language + ", ")
		word_output_file.write(word.edition_type + ", ")
		word_output_file.write(word.xml_context.replace(",", "&#44;") + ", ")
		word_output_file.write(word.file_name + "\n")   

def occurence_list_to_plain_text(word_list, output_name, lemmatize=True):
	text_buffer = ""
	for word in word_list:
		if (lemmatize and word.lemmatization != None and word.lemmatization != ""):
			text_buffer += word.lemmatization + " "
		else:
			text_buffer += word.text + " "
	text_buffer += "\n\n"
	filename = output_name + ".txt"
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	output_file = open(filename, 'w+')
	output_file.write(text_buffer)

def occurence_list_to_html(full_list, num=0, output_name=DEFAULT_OUTPUT_NAME + "_occurences", langfiles=False):	
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
	table_header_xml = etree.Element("th")
	table_header_xml.text = "Xml"
	table_header.append(table_header_word)
	table_header.append(table_header_language)
	table_header.append(table_header_edition)
	table_header.append(table_header_xml)
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
		xml_context = etree.Element("td")
		xml_context.text = word.xml_context
		row.append(text)
		row.append(language)
		row.append(edition_type)
		row.append(xml_context)
		row.append(file_name)
		table.append(row)
	if num > 0:
		prev_link = etree.Element("a")
		prev_link.text = "Previous Page"
		prev_link.attrib["href"] = (output_name + "-" + str(num - 1) + ".html")
		body.append(prev_link)
	if len(next_list) > 0:
		next_link = etree.Element("a")
		next_link.text = "Next Page"
		next_link.attrib["href"] = (output_name + "-" + str(num + 1) + ".html")
		body.append(next_link)
	output_file = open(output_name + "-" + str(num) + ".html", "w")
	output_file.write(etree.tostring(html, pretty_print=True).decode())
	output_file.close()
	if (len(next_list) > 0):
		word_list_to_html(next_list, num + 1, output_name)
