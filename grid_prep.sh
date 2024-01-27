#! /bin/bash

# Code to make pdbqt, gpf & dpf files directly for AD4
# Must call from directory with files?
# It is possible to change other parameters of AD4. Refer to respective scripts for more info

# default AD4 parameters for carbamate dockings on CES1
ligand=$(find . -type f -name "*lig*.pdbqt")
enzyme=$(find . -type f -name "*prepared.pdbqt" | sed 's/\/\.//')
grid_size="48,56,58"
grid_size_2="prueba"
grid_center="4.919,14.993,34.320"
spacing="0.375"
desired="0.564"
increment=$(echo "-($spacing-$desired)" | bc)
run_num="1000"

# location of AD4 utility scripts
py_location="/home/gorpas/ChemSoft/MGLTools/MGLToolsPckgs/AutoDockTools/Utilities24"

# name variable editing
file=$(echo $ligand | sed 's/.pdbqt//')
gpf=$file.$grid_size_2"g".gpf
dpf=$file.$grid_size_2"g".lga.dpf
glf=$file.$grid_size_2"g".glf
dlf=$file.$grid_size_2"g".lga.dlf

# gpf file preparation
    # changes output filename, spacing, grid size, and grid center
pythonsh $py_location/prepare_gpf4.py -l $ligand -r $enzyme -o $gpf -p npts="$grid_size" -p gridcenter="$grid_center"

if [ $spacing != $desired ]
then
	sed -i "s/spacing 0.375/spacing ${desired}/" ./$gpf
fi


# map file preparation
autogrid4 -p $gpf -l $glf

# docking calculations
#autodock4 -p $dpf -l $dlf
