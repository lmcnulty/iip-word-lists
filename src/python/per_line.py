#!/usr/bin/env python3

import sys

if (len(sys.argv) < 2):
	print("Usage: per_line.py [input_file] [output_file]")
	print("\t If no output file is specified, this program prints to stdout")
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

