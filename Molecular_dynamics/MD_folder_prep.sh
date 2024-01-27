#! /bin/bash

files=$(find . -name "*lig_*")
protein=$(find . -name "*prepared*")

for f in $files
do
	folder=$(echo $f | sed 's/.pdbqt//')
	mkdir $folder
	
	cp $f $folder	
	cp $protein $folder/receptor.pdb

	cd $folder

	# convertir a mol2 y añadimos hidrogenos
	obabel -i pdbqt $f -o mol2 >> lig.mol2
	
	cp /data/guillermo/MDs/input_params/density.in .
	cp /data/guillermo/MDs/input_params/equil.in .
	cp /data/guillermo/MDs/input_params/heat.in .
	cp /data/guillermo/MDs/input_params/min.in .
	cp /data/guillermo/MDs/input_params/mmgbsa.in .
	cp /data/guillermo/MDs/input_params/prod.in .
	cp /data/guillermo/MDs/input_params/tleap.in .

	cd ..
	rm $f
	
done
