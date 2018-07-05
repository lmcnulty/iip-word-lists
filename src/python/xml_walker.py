"""
Provides a character-based approach to reading and modifying XML. The
system is based on steps which contain 

ex)
                                    Self-closing br   End i, End p
                                           |             |
<p>This <br>is <i>good</i></p>  =  T.h.i.s. .i.s. .g.o.o.d
                                   |               | 
                                   Begin p      Begin i
"""

from lxml import etree
from collections import defaultdict
from sugar import *

# Returns the number of characters advanced through
def get_indices(element, starting_elements, ending_elements, self_closing_elements, text, base_index, ignore):
	element_text = element.text
	element_tail = element.tail
	for e in ignore:
		if element_text != None:
			element_text = element_text.replace(e, "")
		if element_tail != None:
			element_tail = element_tail.replace(e, "")
	starting_elements[base_index].append(element)
	index = base_index + null_len(element_text)
	text.append(s=element_text)
	for child in element.getchildren():
		index += get_indices(child, starting_elements, ending_elements, self_closing_elements, text, index, ignore)
	if element in starting_elements[index]:
		starting_elements[index].remove(element)
		self_closing_elements[index].append(element)
	else:
		ending_elements[index - 1].append(element)
	index += null_len(element_tail)
	text.append(s=element_tail)
	
	return index - base_index

class step:
	def __init__(self, starting, ending, self_closing, character, index):
		self.starting = starting
		self.ending = ending
		self.self_closing = self_closing
		self.character = character 
		self.index = index
		self.is_indent = False

class walkable_xml:
	def __init__(self, xml, ignore = []):
		if type(xml) is str:
			root = etree.fromstring(xml)
		else:
			root = xml
		self.starting_elements = defaultdict(lambda: [])
		self.ending_elements = defaultdict(lambda: [])
		self.self_closing_elements = defaultdict(lambda: [])
		self.text = mutable_text("")
		self.index = -1
		get_indices(root, self.starting_elements, 
		            self.ending_elements, self.self_closing_elements,
		            self.text, 0, ignore)
	def __iter__(self):
		return self
	def at_end(self):
		return (self.index >= len(self.text.value) - 1)
	def get_step(self, step_index):
		if step_index >= len(self.text.value) or step_index < 0:
			return None
		return step(self.starting_elements[step_index],
		            self.ending_elements[step_index],
		            self.self_closing_elements[step_index],
		            self.text.value[step_index],
		            step_index)
	def get_neighbor(self, offset, step_index=None):
		if step_index == None:
			return self.get_step(self.index + offset)
		return self.get_step(step_index + offset)
	def __next__(self):
		self.index += 1
		if (self.index >= len(self.text.value)):
			raise StopIteration
		return self.get_step(self.index)
		
def preceding_element(a_step, walker, whitespace_only=False):
	previous_step = walker.get_neighbor(-1, step_index=a_step.index)
	if previous_step == None:
		return None
	while len(previous_step.self_closing + previous_step.ending) == 0:
		if whitespace_only and not previous_step.character.isspace():
			return None
		previous_step = walker.get_neighbor(
			-1, step_index=previous_step.index)
		if previous_step == None:
			return None
	return (previous_step.self_closing + previous_step.ending)[-1]
