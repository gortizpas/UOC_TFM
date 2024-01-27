#! /bin/bash


folders=$(find . -type d -name "*lig_*")


for f in $folders
do
	cp *prepared.pdbqt $f
	cp grid_prep.sh $f
done
