from lxml import etree
from lxml.etree import _Element

def create(element_tag, *args):
	new_element = etree.Element(element_tag)
	new_element.text = ""
	new_element.tail = ""
	last_child = None
	for arg in args:
		if type(arg) is dict:
			for key in arg:
				new_element.attrib[key] = arg[key]
		elif type(arg) is list:
			for e in arg:
				new_element.append(e)
				last_child = e
		elif type(arg) is _Element:
			new_element.append(arg)
			last_child = arg
		elif type(arg) is str:
			if last_child == None:
				new_element.text += arg
			else:
				last_child.tail += arg
		else:
			raise ValueError("Unknown argument type for create()")
	return new_element

	
