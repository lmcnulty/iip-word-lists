#!/usr/bin/env python3

from xml_walker import *
from wordlist_classes import iip_word_occurence
from wordlist_constants import *

class internal_element_index:
	def __init__(self):
		self.start_index = None
		self.end_index = None

class walker_word:
	def __init__(self):
		self.text = ""
		self.surrounding_elements = []
		self.internal_elements = defaultdict(lambda: internal_element_index())
		
def is_word_terminating(a_step, walker):
	if a_step == None:
		return True
	if a_step.character.isspace():
		if a_step.character == "\n" and preceding_element(a_step, walker) != None and preceding_element(a_step, walker).tag in INCLUDE_TRAILING_LINEBREAK:
			return False
		return True
	for element in a_step.self_closing:
		if element.tag == "lb" and element.attrib["break"] != "no":
			return True
	return False

def get_words_from_element(root):
	walker = walkable_xml(root, ignore=[","])
	new_word = walker_word()
	words = []
	within = []
	for a_step in walker:
		# Add starting elements
		for element in a_step.starting:
			within.append(element)
			if len(new_word.text) > 0:
				new_word.internal_elements[element].start_index = len(new_word.text)
			else:
				new_word.surrounding_elements.append(element)
		
		# Add self-closing elements
		for element in a_step.self_closing:
			if len(new_word.text) > 0:
				new_word.internal_elements[element].start_index = len(new_word.text)
				new_word.internal_elements[element].end_index = len(new_word.text)
			else:
				new_word.surrounding_elements.append(element)
		
		# Add the character to the word's text
		if not is_word_terminating(a_step, walker) and not a_step.character == "\n":
			new_word.text += a_step.character
			
		# If necessary, end the word and begin a new one
		if is_word_terminating(a_step, walker) or walker.at_end():
			if new_word.text != "":
				words.append(new_word)
				new_word = walker_word()
			
		# Remove closing elements
		for element in a_step.ending: 
			within.remove(element)
			if len(new_word.text) > 0 and  walker.get_neighbor(1) != None and not is_word_terminating(walker.get_neighbor(1), walker) and element in new_word.surrounding_elements:
				new_word.surrounding_elements.remove(element)
				new_word.internal_elements[element].end_index = len(new_word.text)
		
		# Update surrounding elements of newly beginning word
		if (is_word_terminating(a_step, walker) or walker.at_end()) and len(new_word.surrounding_elements) == 0:
			for element in within:
				new_word.surrounding_elements.append(element)
		
		#print(a_step.character + str(within))
	return words
	# for word in words:
		# print(word.text + "\t", end="")
		# for e in word.surrounding_elements:
			# print(e.tag, end=" ")
		# print("\t", end="")
		# #for e in word.internal_elements:
		# #	print(e.tag + "[" + str(word.internal_elements[e].start_index) + "]" + "[" + str(word.internal_elements[e].end_index) + "]", end=" ")
		# for i in range(0, len(word.text)):
			# for e in word.internal_elements:
				# if word.internal_elements[e].start_index == i and word.internal_elements[e].end_index == i:
					# print("<" + e.tag + "/>", end="")
				# else:
					# if word.internal_elements[e].start_index == i:
						# print("<" + e.tag + ">", end="")
					# if word.internal_elements[e].end_index == i:
						# print("</" + e.tag + ">", end="")
			# print(word.text[i], end="")
		# print("")

if __name__ == '__main__':
	print("To import this library, add 'from wordlist_getter import *' to your python script")
	


