#!/usr/bin/env python3

import readline
import os

repl_commands = []

class repl_command:
	def __init__(self, invocation, execute_function, description=""):
		self.invocation = invocation
		self.description = description
		self.execute_function = execute_function
	def execute(self, line):
		self.execute_function(line)

class help_command(repl_command):
	def __init__(self):
		self.invocation = "help"
		self.description = "Print each command and its description."
	def execute(self, line):
		for command in repl_commands:
			print(command.invocation + " - " + command.description)

def read_input(user_input):
	initial_token = user_input.split()[0]	
	for command in repl_commands:
		if command.invocation == initial_token:
			command.execute(user_input)
			return
	print('"' + initial_token + '" - Command not found')

def add_repl_command(command):
	repl_commands.append(command)

def add_repl_commands(*args):
	commands = []
	for arg in args:	
		if isinstance(arg, repl_command):
			commands.append(arg)
		else:
			raise ValueError('"' + str(arg) + '" is not a repl_command.')
	for command in commands:
		add_repl_command(command)

def run_repl():
	readline.set_completer_delims(' \t\n;')
	readline.parse_and_bind('tab: complete')
	
	add_repl_commands(help_command(), repl_command("clear", lambda line: os.system("clear"), description="Clear the screen"))
	
	while True:
		read_input(input("> "))
		
if __name__ == "__main__":
	run_repl()
