"""
The code in this file is used to extract word occurences from XML files.
"""

from xml_walker import *
from wordlist_classes import iip_word_occurence
from wordlist_constants import *
from strip_namespace import *
from copy import copy

class internal_element_index:
	def __init__(self):
		self.start_index = None
		self.end_index = None

class walker_word:
	def __init__(self):
		self.text = ""
		self.alternatives = []
		self.surrounding_elements = []
		self.following = []
		self.preceding = []
		self.internal_elements = defaultdict(
			lambda: internal_element_index())
		
def is_word_terminating(a_step, walker):
	if a_step == None:
		return True
	if a_step.character.isspace():
		if a_step.character == "\n":
			the_preceding_element = preceding_element(a_step, walker, 
		                                          whitespace_only=True) 
			if (the_preceding_element != None 
			and the_preceding_element in INCLUDE_TRAILING_LINEBREAK):
				return False
		return True
	for element in a_step.self_closing:
		if strip_namespace(element.tag) == "lb":
			if "break" in element.attrib and element.attrib["break"] == "no":
				return False
			return True
	return False

class choice:
	def __init__(self, element, preceding_text, word_index):
		self.element = element
		self.preceding_text = preceding_text
		self.word_index = word_index

def index_of(element, a_list):
	try:
		return a_list.index(element)
	except:
		return -.1

def get_words_from_element(root):
	walker = walkable_xml(root, ignore=[","])
	new_word = walker_word()
	words = []
	within = []
	choice_stack = []
	for a_step in walker:
		# Add starting elements
		for element in a_step.starting:
			if type(element.tag) is str and strip_namespace(element.tag) == "choice":
				choice_stack.append(choice(element, copy(new_word.text),
				                    len(words)))
			if (len(choice_stack) > 0 and 
			index_of(element, choice_stack[-1].element.getchildren()) > 0):
				new_word.alternatives.append(
					"" + choice_stack[-1].preceding_text)
			within.append(element)
			if len(new_word.text) > 0:
				new_word.internal_elements[element].start_index \
					= len(new_word.text)
			else:
				new_word.surrounding_elements.append(element)
		
		# Add self-closing elements
		for element in a_step.self_closing:
			if len(new_word.text) > 0:
				new_word.internal_elements[element].start_index \
					= len(new_word.text)
				new_word.internal_elements[element].end_index \
					= len(new_word.text)
			else:
				new_word.surrounding_elements.append(element)
		
		# Add the character to the word's text
		if (not is_word_terminating(a_step, walker) 
		and not a_step.character == "\n"):
			if len(choice_stack) > 0 and choice_stack[-1].element.getchildren()[0] in within:
				 new_word.text += a_step.character
			elif len(choice_stack) > 0 and set(choice_stack[-1].element.getchildren()).intersection(set(within)):
				if len(words) > choice_stack[-1].word_index:
					if len(words[choice_stack[-1].word_index].alternatives) > 0:
						words[choice_stack[-1].word_index].alternatives[-1] += a_step.character
					else:
						words[choice_stack[-1].word_index].alternatives.append("" + a_step.character)
				else:
					new_word.alternatives[-1] += a_step.character
			else:
				new_word.text += a_step.character
				for alternative in new_word.alternatives:
					alternative += a_step.character
			
		# If necessary, end the word and begin a new one
		if is_word_terminating(a_step, walker) or walker.at_end():
			if new_word.text != "":
				# for i in range(0, NUM_CONTEXT):
					# if len(words) > i:
						# words[-i].following.append(new_word)
						# new_word.preceding.append(words[-i])
				words.append(new_word)
				new_word = walker_word()
			for self_closing_element in a_step.self_closing:
				if strip_namespace(self_closing_element.tag) == "lb":
					new_word.text += (a_step.character)
			
		# Remove closing elements
		for element in a_step.ending: 
			if type(element.tag) is str and strip_namespace(element.tag) == "choice":
				choice_stack.pop()
			within.remove(element)
			if (len(new_word.text) > 0 
			and walker.get_neighbor(1) != None 
			and not is_word_terminating(walker.get_neighbor(1), walker) 
			and element in new_word.surrounding_elements):
				new_word.surrounding_elements.remove(element)
				new_word.internal_elements[element].end_index = \
					len(new_word.text)
		
		# Update surrounding elements of newly beginning word
		if ((is_word_terminating(a_step, walker) or walker.at_end()) 
		and len(new_word.surrounding_elements) == 0):
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
		
