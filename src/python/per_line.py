#!/usr/bin/env python3
"""
Usage: per_line.py [input_file] [output_file]

This script reads a text file and outputs each word, as seperated by 
whitespace, on a seperate line. If no output file is specified, prints 
to stdout 
"""

import sys

if (len(sys.argv) < 2):
	print(__doc__)
	exit()
file = open(sys.argv[1], "r+")
text = file.read()
words = text.split()
file.close()
if (len(sys.argv) < 3):
	file = sys.stdout
else:
	file = open(sys.argv[2], "w")
	file.write("")
for word in words:
	print(word, file=file)

	
