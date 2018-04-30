from wordlist_constants import *
import os

def word_list_to_csv(full_list, output_name=DEFAULT_OUTPUT_NAME, langfiles=False):
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
		word_output_file.write(word.text + ", " + word.lemmatization + ", " + word.language + ", " + word.edition_type + ", " + word.xml_context.replace(",", "&#44;") + ", " + word.file_name + "\n")

def word_list_to_plain_text(word_list, output_name, lemmatize=True):
	text_buffer = ""
	for word in word_list:
		if lemmatize and word.lemmatization != None and word.lemmatization != "":
			text_buffer += word.lemmatization + " "
		else:
			text_buffer += word.text + " "
	text_buffer += "\n\n"
	filename = output_name + ".txt"
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	output_file = open(filename, 'w+')
	output_file.write(text_buffer)

def word_list_to_html(full_list, num=0, output_name=DEFAULT_OUTPUT_NAME, langfiles=False):	
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
		prev_link.attrib["href"] = output_name + "-" + str(num - 1) + ".html"
		body.append(prev_link)
	if len(next_list) > 0:
		next_link = etree.Element("a")
		next_link.text = "Next Page"
		next_link.attrib["href"] = output_name + "-" + str(num + 1) + ".html"
		body.append(next_link)
	output_file = open(output_name + "-" + str(num) + ".html", "w")
	output_file.write(etree.tostring(html, pretty_print=True).decode())
	output_file.close()
	#style_file = open("wordlist.css", "w")
	#style_file.write("""
		#table {
			#border-collapse: collapse;
		#}
		#th {
			#background-color: black;
			#color: white;
			#text-align: left;
			#border: 1px solid black;
		#}
		#th, td {
			#padding: 3px;
			#padding-right: 3ch;
		#}
		#td {
			#border: 1px solid grey;
		#}
	#""")
	#style_file.close()
	if (len(next_list) > 0):
		word_list_to_html(next_list, num + 1, output_name)
