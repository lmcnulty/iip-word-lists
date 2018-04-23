# iip-word-lists

## Introduction

This code in this repository is intended for use in the [Inscriptions of Israel / Palestine project](http://library.brown.edu/cds/projects/iip/search/). It uses Python and LXML to generate word lists from [epidoc](http://www.stoa.org/epidoc/gl/latest/) files and includes a simple web interface.

## Project structure

* `docs` contains the files for the [github pages site](lmcnulty.github.io/iip-word-lists).
* `selection` contains a subset of the xml files used for testing. 
* `src` contains the list creation script and the html and css templates for the site.
  * `wordlist.py` is the python script that generates word lists. The basic usage is `./wordlist.py <epidoc files to process>`. By default, the list will be printed to the terminal, other output formats can be specified with flags. Run `./wordlist.py --help` for information on usage.
  * `viewer.html` is a template used to display a single word list.
  * `index.html` is the page which displays tabs several pages generated from viewer.html. It is the page that is displayed when a user first visits the site.
* `.gitignore` lists files that should not be included in the repository, such as lock files, etc.
* `README.md` lists information about the project.
* `build_site.sh` is a bash script that rebuilds the site, outputting to the `docs` directory. It can be run by typing `./build_site` in the terminal from the root project directory. To rebuild the site without re-downloading the epidoc files, run `./build_site --use-existing`. To rebuild the site without updating the word-lists (for example, when working on the frontend), run `./build_site --no-update`. For help, run `./build_site --help`.

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
