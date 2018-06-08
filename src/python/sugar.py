def null_len(x):
	if x == None:
		return 0
	return len(x)
	
def null_add(x, s):
	if x != None:
		s += x

class mutable_text:
	def __init__(self, value):
		self.value = value
	def append(self, s):
		if s != None:
			self.value = self.value + s	
