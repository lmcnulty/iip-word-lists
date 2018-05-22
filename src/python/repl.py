#!/usr/bin/env python3

import readline
import os

class repl_command:
	def __init__(self, invocation, execute_function, description=""):
		self.invocation = invocation
		self.description = description
		self.execute_function = execute_function
	def execute(self, line):
		self.execute_function(line)

class help_command(repl_command):
	def __init__(self, loop):
		self.invocation = "help"
		self.description = "Print each command and its description."
		self.loop = loop
	def execute(self, line):
		for command in self.loop.repl_commands:
			print(command.invocation + " - " + command.description)

class exit_command(repl_command):
	def __init__(self, loop):
		self.invocation = "exit"
		self.description = "Exit the repl."
		self.loop = loop
	def execute(self, line):
		self.loop.repl_exit = True

class repl_instance:
	def __init__(self, prompt="> "):
		self.repl_commands = []
		self.repl_exit = False
		self.prompt = prompt

	def read_input(self, user_input):
		initial_token = user_input.split()[0]	
		for command in self.repl_commands:
			if command.invocation == initial_token:
				command.execute(user_input)
				return
		print('"' + initial_token + '" - Command not found')
	
	def add_repl_command(self, command):
		self.repl_commands.append(command)
	
	def add_repl_commands(self, *args):
		commands = []
		for arg in args:	
			if isinstance(arg, repl_command):
				commands.append(arg)
			else:
				raise ValueError('"' + str(arg) + 
				                 '" is not a repl_command.')
		for command in commands:
			self.add_repl_command(command)
	
	def run_repl(self):
		readline.set_completer_delims(' \t\n;')
		readline.parse_and_bind('tab: complete')
		self.add_repl_commands(help_command(loop=self), 
		                       exit_command(loop=self),
		                       repl_command("clear", 
		                                    lambda line: \
		                                    os.system("clear"), 
		                                    description=\
		                                    "Clear the screen."))
		while not self.repl_exit:
			try:
				self.read_input(input(self.prompt))
			except (EOFError, KeyboardInterrupt) as e:
				print("")
				self.repl_exit = True
		
if __name__ == "__main__":
	repl_instance().run_repl()
