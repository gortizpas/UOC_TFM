#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 13:14:32 2024


mol from pdb


@author: gorpas
"""

# librerias
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
import glob
import os
import shutil

# path de los pdb a convertir
path=os.getcwd()
files=glob.glob(path + "*.pdb")

# Generates a folder to store molecules after pH evaluation, if it doesnt exist already.
isExist = os.path.exists(path + "original")
if not isExist:
    os.makedirs(path + "original")
    
# Generates a folder to store molecules after pH evaluation, if it doesnt exist already.
isExist = os.path.exists(path + "mols")
if not isExist:
    os.makedirs(path + "mols")

#path del directorio donde se van a guardar los archivos
save = path + "mols/"


smiles = []
inchis = []

# crea ficheros .mol con coordenadas 3D de las moleculas a partir de los inchi.
# tambien incluye el inchi y nombre normal de la molecula separado por ; entre tabuladores
# añade hidrogenos y minimaza estructura con MMFF2
# va creando una lista con los smiles
for file in files:
    m = Chem.rdmolfiles.MolFromPDBFile(file)
    m.SetProp("_Name", file + "\t;\t" + Chem.MolToInchi(m) + "\t;\t" + Chem.MolToSmiles(m))
    m2 = Chem.AddHs(m)
    AllChem.EmbedMolecule(m2, randomSeed=0xf00d)
    AllChem.MMFFOptimizeMolecule(m2)
    
    print(Chem.MolToMolBlock(m2), file=open(save + "lig_" + str(iter) + ".mol",'w'))
    
    smiles.append(Chem.MolToSmiles(m))
    inchis.append(Chem.inchi.MolToInchi(m))
    iter = iter + 1



    

file = open(path + 'smiles.txt', 'w')
for item in smiles:
    file.write(item+"\n")
file.close()

file = open(path + 'inchis.txt', 'w')
for item in inchis:
    file.write(item+"\n")
file.close()
    