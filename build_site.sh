#!/usr/bin/env bash

rm -rf docs
mkdir docs
mkdir temp;
cd temp;
wget https://github.com/Brown-University-Library/iip-texts/archive/master.zip;
unzip master.zip;
cp -r iip-texts-master/epidoc-files/ ../docs/texts;
cd ..;
rm -rf temp;
cp viewer.html docs/index.html;
cp wordlist.css docs/;
cd docs;
../wordlist.py texts/* --silent --csv --sort aefl --nodiplomatic;
#cp wordlist-0.html index.html;

