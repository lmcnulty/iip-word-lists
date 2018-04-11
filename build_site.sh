#!/usr/bin/env bash

update=1;
exceptions=0;
for word in $*; do 
	if [ "$word" == "--no_update" ]; then
		update=0;
	elif [ "$word" == "--exceptions" ]; then
		exceptions=1;
	fi
done

echo "Removing old site...";
if [ $update == 0 ]; then
	cd docs;
	mv texts ..;
	cd ..;
fi
rm -rf docs
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

echo "Constructing word list..."
cd docs;
if [ $exceptions == 1 ]; then
	../wordlist.py texts/* --silent --csv --sort aefl --nodiplomatic --langfiles --fileexception;
else
	../wordlist.py texts/* --silent --csv --sort aefl --nodiplomatic --langfiles;
fi
cd ..;

echo "Updating files...";
cd docs;
for csvfile in *.csv; do 
	first=$csvfile
	second="html"
	htmlfile=${first/csv/$second}
	cp ../viewer.html $htmlfile;
	replacestring="s/DATA_FILE/$csvfile/g"
	sed -i -e "$replacestring" $htmlfile
done
cd ..;
cp index.html docs/index.html;
cp wordlist.css docs/;
cd docs;
