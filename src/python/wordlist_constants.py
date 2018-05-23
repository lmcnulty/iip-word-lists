DEFAULT_OUTPUT_NAME = "wordlist"
DEBUG = True 
TEI_NS = "{http://www.tei-c.org/ns/1.0}"
XML_NS = "{http://www.w3.org/XML/1998/namespace}"
IGNORE = ['⎜', '{', '}', '|', '-', '(', '?', ')', ',', ';', '.', ':', 
           '"', "'", "<", ">", "+", "[", "]", "∙", "_", "/", "#", "*"]
INCLUDE_TRAILING_LINEBREAK = [TEI_NS + "persName", TEI_NS + "expan", 
                              TEI_NS + "choice", TEI_NS + "hi", TEI_NS +
                              "supplied", TEI_NS + "num", TEI_NS + 
                              "div", TEI_NS + "unclear"]
LATIN_CODES = ["la", "lat"]
GREEK_CODES = ["grc"]
codes = [
	["latin",["la", "lat"]],
	["hebrew",["heb", "he"]],
	["greek",["grc", "grk"]],
	["aramaic",["arc"]],
]
