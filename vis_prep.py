#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 04:13:21 2023

@author: gorpas

vis prep

"""

import shutil
import glob
import os
import multiprocessing as mp
import pandas as pd


working_dir = os.getcwd()
folders = glob.glob(working_dir + "/[0-9]*/")

pareto_table = pd.read_excel(working_dir + "/prueba.xlsx")
pareto_table = pareto_table[pareto_table['prank'] <= 3]

prank_1 = pareto_table[pareto_table['prank'] == 1]['ligand'].values.tolist()
prank_2 = pareto_table[pareto_table['prank'] == 2]['ligand'].values.tolist()
prank_3 = pareto_table[pareto_table['prank'] == 3]['ligand'].values.tolist()

isExist = os.path.exists(working_dir + "/visualisations")
if not isExist:
    os.makedirs(working_dir + "/visualisations")

for folder in folders:
    isExist = os.path.exists(working_dir + "/visualisations/" + folder.split("/")[-2])
    if not isExist:
        os.mkdir(working_dir + "/visualisations/" + folder.split("/")[-2])
    
    isExist = os.path.exists(working_dir + "/visualisations/" + folder.split("/")[-2] + "/prank_1")
    if not isExist:
        os.makedirs(working_dir + "/visualisations/" + folder.split("/")[-2] + "/prank_1")
    
    isExist = os.path.exists(working_dir + "/visualisations/" + folder.split("/")[-2] + "/prank_2")
    if not isExist:
        os.makedirs(working_dir + "/visualisations/" + folder.split("/")[-2] + "/prank_2")
        
    isExist = os.path.exists(working_dir + "/visualisations/" + folder.split("/")[-2] + "/prank_3")
    if not isExist:
        os.makedirs(working_dir + "/visualisations/" + folder.split("/")[-2]  + "/prank_3")
        
    shutil.copy(glob.glob(working_dir + "/" + folder.split("/")[-2] + "/*mod*")[0], 
                working_dir + "/visualisations/" + folder.split("/")[-2]  + "/prank_1/")
    shutil.copy(glob.glob(working_dir + "/" + folder.split("/")[-2] + "/*mod*")[0], 
                working_dir + "/visualisations/" + folder.split("/")[-2]  + "/prank_2/")
    shutil.copy(glob.glob(working_dir + "/" + folder.split("/")[-2] + "/*mod*")[0], 
                working_dir + "/visualisations/" + folder.split("/")[-2]  + "/prank_3/")
        
    for ligand in prank_1:
        shutil.copy(glob.glob(working_dir + "/" + folder.split("/")[-2] + "/data/LBECs/" + ligand + "*")[0],
                    working_dir + "/visualisations/" + folder.split("/")[-2]  + "/prank_1/")
    for ligand in prank_2:
        shutil.copy(glob.glob(working_dir + "/" + folder.split("/")[-2] + "/data/LBECs/" + ligand + "*")[0],
                    working_dir + "/visualisations/" + folder.split("/")[-2]  + "/prank_2/")
    for ligand in prank_3:
        shutil.copy(glob.glob(working_dir + "/" + folder.split("/")[-2] + "/data/LBECs/" + ligand + "*")[0],
                    working_dir + "/visualisations/" + folder.split("/")[-2]  + "/prank_3/")

        