#!/usr/bin/env bash

update=1;
exceptions=0;
use_existing=0;
for word in $*; do 
	if [ "$word" == "--help" ] || [ "$word" == "-h" ]; then
		printf "Usage:\n\n-h, --help           \t Print this message.\n--no-update, -nu\t Do not fetch epidoc files from github.\n--exceptions, -e\t If an exception occurs in the python code, print the error message.\n--use-existing, -ue\t Do not rebuild the word lists.\n";
		exit;
	elif [ "$word" == "--no-update" ] || [ "$word" == "-nu" ]; then
		update=0;
	elif [ "$word" == "--exceptions" ] || [ "$word" == "-e" ]; then
		exceptions=1;
	elif [ "$word" == "--use-existing" ] || [ "$word" == "-ue" ]; then
		use_existing=1;
	fi
done

echo "Removing old site...";
if [ -d docs ]; then
	cd docs;
	if [ $update == 0 ]; then
		mv texts ..;
	fi
	if [ $use_existing == 1 ]; then
		mv *.csv ..;
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
	cp -r iip-texts-master/epidoc-files/ ../docs/texts;
	cd ..;
	rm -rf temp;
else
	mv texts docs;
fi
if [ -f texts/interpretations.xml ]; then
	rm texts/interpretations.xml;
fi

if [ $use_existing == 0 ]; then
	echo "Constructing word list..."
	cd docs;
	if [ $exceptions == 1 ]; then
		../src/wordlist.py texts/* --silent --csv --sort aefl --nodiplomatic --langfiles --fileexception;
	else
		../src/wordlist.py texts/* --silent --csv --sort aefl --nodiplomatic --langfiles;
	fi
	cd ..;
else
	mv *.csv docs;
fi

echo "Updating files...";
cd docs;
for csvfile in *.csv; do 
	first=$csvfile
	second="html"
	htmlfile=${first/csv/$second}
	cp ../src/viewer.html $htmlfile;
	replacestring="s/DATA_FILE/$csvfile/g"
	sed -i -e "$replacestring" $htmlfile
done
cd ..;
cp src/index.html docs/index.html;
cp src/wordlist.css docs/;
cd docs;
