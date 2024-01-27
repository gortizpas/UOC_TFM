#! /bin/bash


ligand=$(find . -type f -name "*.pdbqt" | sed 's/.pdbqt//')

for f in $ligand
do
	name=$f
	mkdir "$f/"
	cp $f.pdbqt "$name/"
	rm $f.pdbqt
done



