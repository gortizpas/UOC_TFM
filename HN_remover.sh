#! /bin/bash

files=$(find . -name "*lig*")

for f in $files
do
	grep -v "HN" $f >> temp.txt && mv temp.txt $f 
done
