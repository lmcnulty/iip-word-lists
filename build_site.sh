#!/usr/bin/env bash

update=1;
exceptions=0;
use_existing=0;

run_script() {
	source environment/bin/activate;
	cd docs;
	if [ $exceptions == 1 ]; then
		../src/python/wordlist.py texts/xml/* --silent --nodiplomatic --fileexception --html_general --plaintext --flat texts/plain;
	else
		../src/python/wordlist.py texts/xml/* --silent --nodiplomatic --html_general --plaintext --flat texts/plain;
	fi
	cd ..;
}

for word in $*; do 
	if [ "$word" == "--help" ] || [ "$word" == "-h" ]; then
		printf "Usage:\n\n-h, --help           \t Print this message.\n--no-update, -nu\t Do not fetch epidoc files from github.\n--exceptions, -e\t If an exception occurs in the python code, print the error message.\n--use-existing, -ue\t Do not rebuild the word lists.\n";
		exit;
	elif [ "$word" == "--no-update" ] || [ "$word" == "-nu" ]; then
		update=0;
	elif [ "$word" == "--exceptions" ] || [ "$word" == "-e" ]; then
		exceptions=1;
	fi
done

echo "Removing old site...";
if [ -d docs ]; then
	cd docs;
	if [ $update == 0 ]; then
		mv texts ..;
	fi
	cd ..;
	rm -rf docs
fi
mkdir docs

if [ $update == 1 ]; then
	echo "Updating texts...";
	mkdir temp;
	cd temp;
	wget https://github.com/Brown-University-Library/iip-texts/archive/master.zip;
	unzip master.zip;
	mkdir ../docs/texts;
	cp -r iip-texts-master/epidoc-files/ ../docs/texts/xml;
	cd ..;
	rm -rf temp;
	cd docs/texts/xml;
	if [ -f interpretations.xml ]; then
		rm interpretations.xml;
	fi
	if [ -f include_publicationStmt.xml ]; then
		rm include_publicationStmt.xml;
	fi
	cd ../../..;
else
	mv texts docs;
fi

run_script;

cp src/web/wordlist.css docs/;
cp src/web/style.css docs/;
cp src/web/index_search.js docs/;
