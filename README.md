## Introduction

The code in this repository is intended for use in the [Inscriptions of Israel / Palestine project](http://library.brown.edu/cds/projects/iip/search/). It uses Python and LXML to generate word lists from [epidoc](http://www.stoa.org/epidoc/gl/latest/) files and includes a simple web interface.

## Setup

0. Clone or download the repository.
1. Enter the project directory with `cd iip-word-lists`
2. Create a virtual environment with the appropriate dependencies by 
   running `virtualenv -p python3 environment`. If you do not have 
   virtualenv installed, install it using your system's package manager,
   or with pip by running `pip install virtualenv`.
3. Activate the virtual environment by running `source environment/bin/activate`
   (The virtual environment must be active whenever you run the python 
   code or rebuild the site. If it is active, you should see `(environment)`
   before the prompt in your terminal.)
4. Install the necessary dependencies by running `pip install -r requirements.txt`


### To run the site locally

0. Enter the docs directory with `cd docs`
1. Start an http server by running `python -m SimpleHTTPServer 8000` 
2. Open `localhost:8000` in your web browser

(You can view the files without running the server, but some links will
not work.)

### To build the site

0. from the root project directory, run `./build_site.sh`. Add `-nu` if
   you are updating the site and do not wish to download the xml files.

## Project structure

* `docs` contains the files for the [github pages site](https://lmcnulty.github.io/iip-word-lists).
  * `texts` contains the files representing individual inscription.
    * `xml` contains these files in their original XML form.
    * `plain` contains plain text representations of the inscriptions
    * `plain_lemma` contains the same as above, but using lemmas of each word instead of the actual text as it appeared in the inscription.
  * each language has its own directory containing its data in html format.
  * `doubletreejs` contains code for the [DoubleTreeJS](http://www.sfs.uni-tuebingen.de/~cculy/software/DoubleTreeJS/index.html) visualization library.
* `src` contains the list creation script and the html and css templates for the site.
  * `python` contains the python scripts for processing the data
    * `wordlist.py` is the python script that generates word lists. The basic usage is `./wordlist.py <epidoc files to process>`. By default, the list will be printed to the terminal, other output formats can be specified with flags. Run `./wordlist.py --help` for information on usage.
  * `web` contains the css, and javascript and html templates used to build the site.
* `.gitignore` lists files that should not be included in the repository, such as lock files, etc.
* `README.md` lists information about the project.
* `build_site.sh` is a bash script that rebuilds the site, outputting to the `docs` directory. It can be run by typing `./build_site` in the terminal from the root project directory. To rebuild the site without re-downloading the epidoc files, run `./build_site --use-existing`. To rebuild the site without updating the word-lists (for example, when working on the frontend), run `./build_site --no-update`. For help, run `./build_site --help`.

## Functionality

### Lemmatization

A word's *lemma* is its "basic" form as it might appear in a dictionary. For instance, the lemma of "rethinking" is "think." The process of getting a lemma from a word is called "lemmatization." Lemmatization allows this project to recognize different strings as instances of the same word, which is very useful for learning about the usage and distributions of specific words. 

Lemmatization is currently done only for Latin and Greek, as provided by [CLTK](https://cltk.org).

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

## To do

- [x] Geographic Word Counts
- [x] Filter by Region
- [x] Word in Context
- [x] Default to sort by occurrence
- [x] Frontend Redesign
- [x] Add Alphabet links to frontend
- [x] Fuzzy Search
- [x] Wildcard Search
- [ ] Word Frequency by Geography
- [ ] Part of Speech Tagging
- [ ] Display for `<corr>` `<reg>`
- [ ] Stems
- [ ] Named Entity Recognition?
- [ ] Fix alphabet selection for Greek
- [ ] Fix punctuation characters in alphabet selection
- [ ] Add general English category
- [x] Fix KWIC alignment
- [ ] Add option to disable special searching
- [ ] Ignore soft hyphens in suspicion check
- [ ] Add regex explanation/tutorial
- [ ] Collapse occurrence metadata under dropdown arrow 
- [ ] Add explanation of libraries in README
- [ ] Ignore capitalization differences in variations section

## Misc

Thank you to the [Unicode Consortium](unicode.org) for keeping us on our
toes by including all these as separate characters: · ‧ ⋅ • ∙.
