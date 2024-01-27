#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 12:48:03 2023

@author: gorpas

funciona desde la carpeta de visualizaciones ejecutandose con spider para las proteinas
para las que se hacen pareto, pero no para las que estan solas

para estas ultimas hay que quitar adaptar la parte de real_subdirs, eliminando el bucle for
y quitando de subdirs, el que tiene solo visualisations

"""

import glob
import os
import subprocess
import multiprocessing as mp
from fnmatch import fnmatch

path = os.getcwd()
subdirs = [x[0] for x in os.walk(path)]


real_subdirs = subdirs[1:]

#real_subdirs = []
#for folder in subdirs:
#    if "prank" in folder:
#        real_subdirs.append(folder)
        
isExist = os.path.exists(path + "/charm_gui_prep")
if not isExist:
    os.makedirs(path + "/charm_gui_prep")
    
for folder in real_subdirs:
    new_path = folder.replace("/visualisations", "/visualisations/charm_gui_prep")
    
    isExist = os.path.exists(new_path)
    if not isExist:
        os.makedirs(new_path)
        
    prot = glob.glob(folder + "/*mod*")[0]
    ligands = glob.glob(folder + "/dim*")
    prot_name = prot.split("/")[-1]
    
    for lig in ligands:
        lig_name = lig.split("/")[-1]
        new_name = prot_name + lig_name
        with open(new_path + "/" + new_name, 'w') as outfile:
            with open(prot) as infile:
                outfile.write(infile.read())
                infile.close()
            with open(lig) as infile:
                outfile.write(infile.read())
                infile.close()
                
        outfile.close()