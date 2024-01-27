#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 13:08:01 2023

@author: gorpas
# No consigo que me funcione desde la terminal, solo desde spyder.
"""
import shutil
import glob
import os
import subprocess
import multiprocessing as mp

# location of AD4 utility scripts
tool_location = "/home/gorpas/ChemSoft/MGLTools/MGLToolsPckgs/AutoDockTools/Utilities24/"
autogrid_location = "/home/gorpas/ChemSoft/AutoDock4/"

def copy_prot(protein, folder):
    shutil.copy(protein[0], folder)


def grid_prep(folder, tool_location, autogrid_location):
    os.chdir(folder)
    
    # Get ligand and receptor
    ligand = glob.glob("*decoy*.pdbqt")[0]   
    enzyme = glob.glob("*prepared.pdbqt")[0] 
    
    
    # Docking parameters
    # ha sido necesario añadir el grid_size_round, para que ejecute bien, ya que falla si tiene decimales
    # y luego se cambia por el que tiene decimales.
    grid_size = "13.065,14.588,18.769"
    grid_size_round = "13,14,18"
    grid_size_name = ""
    grid_center = "160.5345,163.892,159.4165"
    spacing = "1.000"
    
  
    # name variable editing
    file = ligand.replace(".pdbqt", "")
    gpf = str(file + grid_size_name + ".g.gpf")
    glf = str(file + grid_size_name + ".g.glf")


    # gpf file preparation
    # changes output filename, spacing, grid size, and grid center
    subprocess.run(["pythonsh",
                    tool_location + "prepare_gpf4.py",
                    "-l", ligand,
                    "-r", enzyme,
                    "-o", gpf,
                    "-p", str("npts=" + grid_size_round),
                    "-p", str("gridcenter=" + grid_center)])


    # modification of spacing for .gpf file
    with open(gpf, "r") as file:
       lines = file.readlines()
       
    lines[2] = lines[2].replace("0.375", spacing)
    lines[0] = lines[0].replace(grid_size_round, grid_size)
    
    with open(gpf, "w") as file:
       lines = file.writelines(lines)
    
    
    # map file generation
    subprocess.run([autogrid_location + "autogrid4",
                    "-p", gpf,
                    "-l", glf])


def main():
    working_dir = os.getcwd()
    folders = glob.glob(working_dir + "/*decoy*")
    protein = glob.glob(working_dir + "/*prepared.pdbqt")
    
    pool = mp.Pool(mp.cpu_count()-2)
    
    pool.starmap_async(copy_prot, [(protein, folder) for folder in folders])
    pool.starmap_async(grid_prep, [(folder, tool_location, autogrid_location) for folder in folders])
    pool.close()
    
if __name__ == "__main__":
    main()
