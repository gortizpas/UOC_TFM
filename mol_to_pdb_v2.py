#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 09:08:57 2023
@author: gorpas
"""
# librerias - Subprocess necesary to call "prepare_ligand" since its in python 2.4
from openbabel import openbabel as ob
import glob
import os
import subprocess
import multiprocessing as mp

# Carpetas donde se instaló MGLTools y donde se encuentran los principales scripts de preparacion.
tool_location="/home/gorpas/ChemSoft/MGLTools/MGLToolsPckgs/AutoDockTools/Utilities24/"
python_loc="/home/gorpas/ChemSoft/MGLTools/lib/libpython2.7.so"

# Carpeta con archivos a transformar
save = "/media/gorpas/linux-storage/UOC/docking/ligands/decoys/AHR/10rb/pH/"

# Lista de archivos a transformar
archivos = glob.glob(save + "*.mol")

# Definimos el formato de entrada y salida para hacer la transformacion
input_format = "mol"
output_format = "pdb"

# Creacion de carpetas para guardar los nuevos ficheros
isExist = os.path.exists(save + "pdb")
if not isExist:
    os.makedirs(save + "pdb")

isExist = os.path.exists(save + "pdbqt")
if not isExist:
    os.makedirs(save + "pdbqt")

    
# preparacion de openbabel    
inputMol = ob.OBMol()
fileConversion = ob.OBConversion()
fileConversion.SetInAndOutFormats(input_format, output_format)

# transformacion de archivos
for file in archivos:
    infile = file
    outfile = file.replace("mol","pdb").replace(save, save + "pdb/")

    fileConversion.ReadFile( inputMol, infile )
    fileConversion.WriteFile( inputMol, outfile )
    
# movemos mols a un fichero nuevo
isExist = os.path.exists(save + "mols")
if not isExist:
    os.makedirs(save + "mols")
    
mols = glob.glob(save + "*.mol")
for file in mols:
    os.rename(file, file.replace("original/", "original/mols/"))

# Preparacion de pdb a pdbqt con MGLTools
pdbs = glob.glob(save + "pdb/*.pdb")

# Por lo que sea, MGLTools solo coge el nombre del archivo y no su path, pasando solo eso
# a otros programas, que no acaban encontrando los ficheros, por lo que hay que ayudarle.
# sin embargo, a la hora de escribir, no tiene problema pasandole el path directamente.

# se puede tratar de optimizar mas, porque por cada molecula tiene que inicializar el ambiente de python
# intentar con un fichero que lo haga de golpe
# tambien habia visto a alguien que habia modificado el codigo directamente para conseguir esto:
#    https://stackoverflow.com/questions/35259327/how-to-speed-up-a-py-script-refering-to-millions-of-files

# para unos 5300 compuestos tarda menos de 45s en generar los pdbs
# y unos 3min 15s más en generar los pdbqts
# comparar con script en bash

os.chdir(save + "pdb/")

# transformacion de pdb a pdbqt con paralelizacion asincrona.
def pdb_to_pdbqt(file, save, tool_location):
    subprocess.run(["pythonsh",
                    tool_location + "prepare_ligand4.py",
                    "-l", file,
                    "-U", "nphs",
                    "-o", file.replace(".pdb",".pdbqt").replace(save + "pdb/", save + "pdbqt/")])

pool = mp.Pool(mp.cpu_count())
pool.starmap_async(pdb_to_pdbqt, [(file, save, tool_location) for file in pdbs])
pool.close()

