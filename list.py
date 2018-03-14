#!/usr/bin/env python3

import os
import sys
from lxml import etree

words = []

def descend_until_reach(node, tag):
	iterator = node.iterdescendants()
	descendant = next(iterator)
	while (descendant != None):
		if descendant.tag == tag:
			return descendant
		try:
			descendant = iterator.next()
		except:
			break


for file in os.listdir("selection"):
	tree = etree.parse("selection/" + file)
	root = tree.getroot()
	body = descend_until_reach(root, "{http://www.tei-c.org/ns/1.0}body")
	print(body)
	for child in list(body):
		if child.tag == "{http://www.tei-c.org/ns/1.0}div":
			if child.get("type") == "edition":
				sys.stdout.write("    ")
				sys.stdout.flush()
				print(child)
				for e in child.getchildren():
					sys.stdout.write("        ")
					sys.stdout.flush()
					iterator = e.itertext()
					text = iterator.next().split()
					for f in text:
							sys.stdout.write("            ")
							sys.stdout.flush()
							print(f)
					while text != None:
						for f in text:
							sys.stdout.write("            ")
							sys.stdout.flush()
							print(f)
						try:
							text = iterator.next().split()
						except:
							break
	
	
