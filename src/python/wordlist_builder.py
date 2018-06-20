"""
This file contains code used to retrieve word occurences from the xml
files when the script is invoked with `--old_system`.
"""

from lxml import etree
from wordlist_constants import *
from wordlist_classes import *
import copy

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
                      lang, path, include_initial_line_break, region, 
                      within, xml_context=""):
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
                                edition_type, lang, "", path, region, 
                                within))
	# If the text in question is the inner text of the element, add it 
	# to the xml field of the generated word.
	#if (trailing_text == element.text):
		#try:
			#word_list[-1].xml_context += \
			#"<" + element.tag.replace(ns, "").replace(xmlNs, "") + ">"
		#except:
			#pass
			
	# If there is no trailing text, return.
	if len(trailing_text_list) < 1:
		return

	# Append first token of the trailing text to the last word in the 
	# list.
	append_string_to_word_list_end(word_list, trailing_text_list[0])
	
	if (trailing_text == element.text):
		word_list[-1].within = within
	
	# For all following words, add a new element to the words list.
	if len(word_list) > 1:
		for i in range(1, len(trailing_text_list)):
			new_word = iip_word_occurence(edition_type, lang, 
			                              trailing_text_list[i], path, 
			                              region, within)
			append_to_word_list(word_list, new_word)
	
	# If the last word is complete, add an empty word to the end of the
	# list.
	if (trailing_text[-1] == ' ' or trailing_text[-1] == '\n'):
		if word_list[-1].text != "":
			append_to_word_list(word_list, iip_word_occurence( 
			                    edition_type, lang, "", path, region, 
			                    within))

def add_element_to_word_list(e, word_list, edition, mainLang, path, 
                             region, within):	
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
		                    editionLang, "", path, region, within))
	previous = e.getprevious()
	if (e.tag == TEI_NS + "expan" and previous != None and previous.tag 
			== TEI_NS + "abbr"):
		if len(word_list[-1].text) < 1:
			del(word_list[-1])
		word_list[-1].text = ""
		word_list[-1].edition = edition

	# Add the text within the element not inside any child element
	if (e.text != None):	
		add_trailing_text(word_list, e, e.text, subtype, wordLang, path,
		                  True, region, within + [e])
	# Add each child element
	children = e.getchildren()
	for i in range(0, len(children)):
		# When adding children of a <choice> element, the preceding word
		# is added between children so that each possible version of the
		# word will appear in the final word list.
		if (e.tag == TEI_NS + "choice" and i > 0):
			append_to_word_list(word_list, prev_word)
		add_element_to_word_list(children[i], word_list, edition, 
		                         mainLang, path, region, within + [e])
	try:
		if not word_list[-1].text in ["", " ", "\n", None]:
			word_list[-1].xml_context += \
			"</" + e.tag.replace(TEI_NS, "").replace(XML_NS, "") + ">"
	except:
		pass
		
	# Add the words following the element which are not in any sibling
	if (e.tail != None):
		add_trailing_text(word_list, e, e.tail, subtype, wordLang, 
		                  path, (e.tag in INCLUDE_TRAILING_LINEBREAK), 
		                  region, within)


