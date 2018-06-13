from wordlist_constants import *
from copy import copy

def add_kwic_to_occurences(occurences_list):
	last = []
	for e in occurences_list:
		for f in last:
			if f.language == e.language:
				e.preceding.append(f)
				f.following.append(e)
		last.append(e)
		if len(last) > NUM_CONTEXT:
			last.pop(0)
	
