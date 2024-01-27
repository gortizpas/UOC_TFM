#! /bin/bash

folders=$(find . -type d -name "*lig_*" | sed 's/\/\.//')

for f in $folders
do
	cd $f
	./grid_prep.sh
	cd ..
done
