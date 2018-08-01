noun = "noun"
verb = "verb"
part = "participle"
adj = "adjective"
adv = "adverb"
conj = "conjunction"
prep = "preposition"
pron = "pronoun"
num = "numeral"
interj = "interjection"
excl = "exclamation"
punc = "punctuation"
det = "determiner"
part = "particle"

nltk_dict = {
	"CC": conj,
	"CD": num,
	"DT": det,
	"EX": "existential there",
	"FW": "foreign word",
	"IN": prep,
	"JJ": adj,
	"JJR": adj,
	"JJS": adj,
	"LS": "list item marker",
	"MD": verb,
	"NN": noun,
	"NNP": noun,
	"NNPS": noun,
	"NNS": noun,
	"PDT": "pre-determiner",
	"POS": "genitive marker",
	"PRP": pron,
	"PRP$": pron,
	"RB": adv,
	"RBR": adv,
	"RBS": adv,
	"RP": part,
	"SYM": "symbol",
	"TO": prep,
	"UH": interj,
	"VB": verb,
	"VBD": verb,
	"VBG": verb,
	"VBN": verb,
	"VBP": verb,
	"VBZ": verb,
	"WDT": det,
	"WP": pron,
	"WP$": pron,
	"WRB": adv
}

# CLTK
cltk_dict = {
	"n": noun,
	"v": verb,
	"t": part,
	"a": adj,
	"d": adv,
	"l": det,
	"g": part,
	"c": conj,
	"r": prep,
	"p": pron,
	"m": num,
	"i": interj,
	"e": interj,
	"u": punc
}

def standardize_pos(s):
	if s in nltk_dict.keys():
		return nltk_dict[s]
	first = s[0].lower()
	if first in cltk_dict.keys():
		return cltk_dict[first]
	return s


