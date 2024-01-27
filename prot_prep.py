#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 10:27:39 2023

@author: gorpas
"""
# librerias - Subprocess necesary to call "prepare_ligand" since its in python 2.4
import glob
import os
import subprocess
import multiprocessing as mp

# Carpetas donde se instaló MGLTools y donde se encuentran los principales scripts de preparacion.
tool_location="/home/gorpas/ChemSoft/MGLTools/MGLToolsPckgs/AutoDockTools/Utilities24/"

# Carpeta con archivos a transformar
save = "/media/gorpas/linux-storage/UOC/docking/proteins/original/mod/prueba-htmd/"


# transformacion de pdb a pdbqt con paralelizacion asincrona.
def pdb_to_pdbqt(file, save, tool_location):
    subprocess.run(["pythonsh",
                    tool_location + "prepare_receptor4.py",
                    "-r", file,
                    "-U", "nphs",
                    "-o", file.replace(".pdb",".pdbqt").replace(save + "pdb/", save + "pdbqt/")])


def main ():
    
    # Creacion de carpetas para guardar los nuevos ficheros
    isExist = os.path.exists(save + "pdb")
    if not isExist:
        os.makedirs(save + "pdb")
        
    isExist = os.path.exists(save + "pdbqt")
    if not isExist:
        os.makedirs(save + "pdbqt")
        
    prots = glob.glob(save + "*.pdb")    
    for file in prots:        
        os.rename(file, file.replace("prueba-htmd/", "prueba-htmd/pdb/"))

#    os.chdir(save + "pdb/")
    prots = glob.glob(save + "pdb/*_*.pdb")

        
    pool = mp.Pool(mp.cpu_count())
    pool.starmap_async(pdb_to_pdbqt, [(file, save, tool_location) for file in prots])
    pool.close()



if __name__ == "__main__":
    main()