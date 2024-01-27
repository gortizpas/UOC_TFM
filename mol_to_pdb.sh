#!/bin/bash

FILES="/media/gorpas/linux-storage/docking/ligands/*.mol"

for f in $FILES;
  do
    obabel -i mol $f -o pdb -O $f.pdb
  done
