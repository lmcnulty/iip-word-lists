import unicodedata
import re

def check_suspicious(word):
	if len(word.lemma) > 15:
		word.suspicious = True
	contains_numbers = False
	contains_letters = False
	contains_lowercase = False
	contains_intermediate_uppercase = False
	for index, e in enumerate(word.lemma):
		if unicodedata.category(e) == "Nd":
			contains_numbers = True
		if not unicodedata.category(e) in ["Nd", "Po"]:
			contains_letters = True
		if e.islower():
			contains_lowercase = True
		if index > 0 and e.isupper():
			contains_intermediate_uppercase = True
		if word.language == "la":
			if not unicodedata.category(e) in ["Ll", "Lu", "Po"]:
				word.suspicious = True
	if (contains_letters and contains_numbers and not ("transl" in word.language and re.match("[0-9]*th|[0-9]*2nd|[0-9]*3rd|[0-9]*1st", word.lemma) != None)):
		word.suspicious = True
	if contains_lowercase and contains_intermediate_uppercase:
		word.suspicious = True
