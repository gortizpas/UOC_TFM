#! /bin/bash


ligand=$(find . -type f -name "*.mol.pdb" | sed 's/\/\.//')
enzyme=$(find . -type f -name "*.FH.pdb" | sed 's/\/\.//')


# location of AD4 utility scripts
py_location="/home/gorpas/ChemSoft/MGLTools/MGLToolsPckgs/AutoDockTools/Utilities24"


for f in $ligand:
do 
# ligand preparation
    # Adds AD4 type atoms and Gasteiger charges by default, and additionally it merges non-polar hydrogens (default also merges lone pairs)
pythonsh $py_location/prepare_ligand4.py -l $f -U "nphs"
done

for g in $enzyme:
do
# receptor preparation
    # Adds AD4 type atoms and Gasteiger charges by default, and additionally it merges non-polar hydrogens (default also merges lone pairs)
pythonsh $py_location/prepare_receptor4.py -r $g -U "nphs"
done
