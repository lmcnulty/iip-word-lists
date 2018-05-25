class iip_word:
	def __init__(self):
		self.lemma = ""
		self.occurences = []
		self.variations = set()
		self.language = ""
		self.files = set()
		self.regions = set()
		self.suspicious = False

class iip_file:
	def __init__(self, file_name, region):
		self.file_name = file_name
		self.region = region

class iip_word_occurence:
	equivilence = ["edition_type", "language", "text", "file_name"]
	def __init__(self, edition_type, language,  text, file_name, region,
	                                          contains_gap=False):
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
	def __hash__(self):
		new_hash = 0
		for e in iip_word_occurence.equivilence:
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
		print(self.text + " | " + self.lemmatization + " | " + 
		      self.language + " | " + self.edition_type + " | " + 
		                  self.file_name + "|" + self.xml_context)
