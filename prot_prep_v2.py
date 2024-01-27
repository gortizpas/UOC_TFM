#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 10:27:39 2023

@author: gorpas

# no consigo hacer que funcione desde la terminal (bash -> python prot_prep_v2.py)
# pero si desde spyder
"""
# librerias - Subprocess necesary to call "prepare_ligand" since its in python 2.4
import glob
import os
import subprocess
import multiprocessing as mp

# Carpetas donde se instaló MGLTools y donde se encuentran los principales scripts de preparacion.
tool_location="/home/gorpas/ChemSoft/MGLTools/MGLToolsPckgs/AutoDockTools/Utilities24/"


# transformacion de pdb a pdbqt con paralelizacion asincrona.
def pdb_to_pdbqt(file, working_dir, tool_location):
    
    print(file)
    print(working_dir)
    subprocess.run(["pythonsh",
                    tool_location + "prepare_receptor4.py",
                    "-r", file,
                    "-U", "nphs",
                    "-o", working_dir + "/pdbqt/" + file.replace(".pdb",".pdbqt")])


def main ():
    working_dir = os.getcwd()
    
    # Creacion de carpetas para guardar los nuevos ficheros
    isExist = os.path.exists("pdb")
    if not isExist:
        os.makedirs("pdb")
        
    isExist = os.path.exists("pdbqt")
    if not isExist:
        os.makedirs("pdbqt")
        
    prots = glob.glob("*.pdb")    
    for file in prots:        
        os.rename(file, "./pdb/" + file)

    os.chdir(working_dir + "/pdb/")
    prots = glob.glob("*_prepared.pdb")

        
    pool = mp.Pool(mp.cpu_count())
    pool.starmap(pdb_to_pdbqt, [(file, working_dir, tool_location) for file in prots])
    pool.close()



if __name__ == "__main__":
    main()
