DEFAULT_OUTPUT_NAME = "wordlist"
DEBUG = True 
TEI_NS = "{http://www.tei-c.org/ns/1.0}"
XML_NS = "{http://www.w3.org/XML/1998/namespace}"
IGNORE = ['⎜', '{', '}', '|', '(', '?', ')', ',', ';', '.', ':', 
           '"', "'", "<", ">", "+", "[", "]", "_", "/", "#", "*", '~', 
           '´', '=', '·', '‧', '⋅', '•', '∙']
INCLUDE_TRAILING_LINEBREAK = [TEI_NS + "persName", TEI_NS + "expan", 
                              TEI_NS + "choice", TEI_NS + "hi", TEI_NS +
                              "supplied", TEI_NS + "num", TEI_NS + 
                              "div", TEI_NS + "unclear", TEI_NS + "placeName"]
LATIN_CODES = ["la", "lat"]
GREEK_CODES = ["grc"]
codes = [
	["latin",["la", "lat"]],
	["hebrew",["heb", "he"]],
	["greek",["grc", "grk"]],
	["aramaic",["arc"]],
	["unknown", ["unk"]]
]

INFO_PAGE_HTML = """
<html>
	<head>
		<meta charset='UTF-8' />
		<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"> </script>
	</head>
	<body>
		<h1></h1>
		<table>
			<tr>
				<td>Occurences: </td><td id='num-occurences'></td>
			</tr>
		</table>
		<h2>Variations</h2>
		<ul id='variations'>
		</ul>
		<h2>Files</h2>
		<ul id='files'>
		</ul>
		<h2>Regions</h2>
		<ul id='regions'>
		</ul>
		<h2>Occurences</h2>
		<table id="occurences">
			<tr>
				<th>Variation</th>
				<th>File</th>
				<th>XML</th>
				<th>Region</th>
			</tr>
		</table>
	</body>
</html>
""".replace("\t", "")

INDEX_PAGE_HTML = """
<html>
	<head>
		<meta charset='UTF-8' />
		<title></title>
		<link rel="stylesheet" type="text/css" href="../style.css" />
	</head>
	<body>
		<h1></h1>
		<ul id='words'>
			<noscript id="wordList">
			
			</noscript>
		</ul>
		<script>
			wordsArray = [
				$WORDS_OBJECT
			];
		</script>
		<script src='../index_search.js'>   </script>
	</body>
</html>
""".replace("\t", "")

FRONT_PAGE_HTML = """
<html>
	<head>
		<meta charset='UTF-8' />
		<title>Language Selection</title>
	</head>
	<body>
		<h1>Languages</h1>
		<ul id='language-list-html'></ul>
	</body>
</html>
""".replace("\t", "")

OCCURENCE_TABLE_ROW_HTML = """
<tr>
	<td id="variation"></td>
	<td id="file"></td>
	<td><code id="xml" class="prettyprint"></code></td>
	<td id="region"></td>
</tr>
""".replace("\t", "")
