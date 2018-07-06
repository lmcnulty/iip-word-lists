from collections import defaultdict

class iip_word:
	def __init__(self):
		self.lemma = ""
		self.occurrences = []
		self.variations = set()
		self.language = ""
		self.files = set()
		self.regions = set()
		self.suspicious = False
		self.alternatives = []
		self.frequency_total = 0
		self.frequency_language = 0
		self.stem = ""

class iip_file:
	def __init__(self, file_name, region):
		self.file_name = file_name
		self.region = region

def format_element_list(element_list):
	result = ""
	for e in element_list:
		tag = e.tag.split("}")[1]
		if tag == "div":
			continue
		result += tag
		for attribute in e.attrib:
			result += "[" + attribute + "="
			result += e.attrib[attribute] + "]"
		result += " "
	return result

class iip_word_occurrence:
	equivilence = ["edition_type", "language", "text", "file_name"]
	def __init__(self, edition_type, language,  text, file_name, region,
	                                        within, contains_gap=False):
		# eg: diplomatic
		self.edition_type = edition_type
		# eg: grc
		if (language == "he"):
			self.language = "heb"
		elif (language == "lat"):
			self.language = "la"
		else:
			self.language = language
		# eg: Πἁποϲ
		self.text = text
		# eg: jeru00001.xml
		self.file_name = file_name
		# eg: happ<unclear>i</unclear>n<supplied>ess</supplied>
		self.xml_context = text
		self.lemmatization = ""
		self.suspicious = False
		self.abbreviations = []
		self.followups = []
		self.region = region
		self.within = within
		self.surrounding_elements = []
		self.alternatives = []
		self.internal_elements = defaultdict(lambda: internal_element_index())
		self.previous = []
		self.following = []
		self.pos = ""
		
		
	def __hash__(self):
		new_hash = 0
		for e in iip_word_occurrence.equivilence:
			new_hash += hash(getattr(self, e))
		return new_hash
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return hash(self) == hash(other)
		else:
			return False
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def append_string(self, string):
		self.text += string
		self.xml_context += string
	
	def print(self):
		print(self.text + " | " + self.lemmatization + " | "  
		      + self.language + " | " + self.edition_type + " | "  
		      + self.file_name + "|" + self.xml_context + "|" 
		      + str(self.alternatives) + "|" + str(self.pos))
		      #+ "|" + format_element_list(self.within))

