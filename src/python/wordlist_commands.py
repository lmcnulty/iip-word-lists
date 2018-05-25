from repl import *

class word_info_command(repl_command):
	def __init__(self, word_dict):
		self.word_dict = word_dict
		self.invocation = "info"
		self.description ="Get information on the given word."
	def execute(self, line):
		word = line.split()[1]
		if word in self.word_dict:
			print_word_info(word, word_dict)
		else:
			print('"' + word + '" not found.')
