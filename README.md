## Problems Encountered

* Line breaks following certain tags indicate the start of a new word. 
  These are currently listed in the global variable `include_trailing_linebreak`.
  However, this is not comprehensive. A complete list based on the epidoc
  spec should be added.
* How should gaps be handled?
* Graffiti: some transcriptions, such as masa09390.xml, are of graffiti
  and do not contain complete words but just jumbles of characters.
  Currently these are added to the word list as if they were words, 
  leading to some strange results. However, if we ignored all files
  marked as containing graffiti, we could potentially lose some words.
* Should `<num>` elements always indicate the start of a new word?


## Probable Mistakes found in iip-texts

* caes0004.xml, line 187: <lb> should have attribute break="no"
* jeru0003.xml, line 127: <lb> should have attribute break="no"
* zoor0013.xml, line 136: 'expan="ἔτους"&gt;' appears outside of tag
* zoor0136.xml, line 156: 'expan="ἡμέρᾳ"&gt;' appears outside of tag
