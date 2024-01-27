#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 11:09:58 2024

dude extractor

@author: gorpas
"""

import pandas as pd
import glob
import os


path=os.getcwd() + "/"

files=glob.glob(path + "*picked")


isExist = os.path.exists(path + "all")
if not isExist:
    os.makedirs(path + "all")
    
ligands = []
decoys = []
all_things = []
    
for file in files:
    data = pd.read_csv(file, sep='\t', header=None)
    ligand = [data.loc[0,1]]
    decoy = data[0][1:]
    
    ligands.extend(ligand)
    decoys.extend(decoy)
    
all_things.extend(ligands)
all_things.extend(decoys)

file = open(path + 'ligands.smi', 'w')
for item in ligands:
    file.write(item+"\n")
file.close()

file = open(path + 'decoys.smi', 'w')
for item in decoys:
    file.write(item+"\n")
file.close()

file = open(path + 'all.smi', 'w')
for item in all_things:
    file.write(item+"\n")
file.close()