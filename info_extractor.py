#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 11:51:17 2023

@author: gorpas
"""

import os
import re
import pandas as pd
# info extractor

# pone variables de path, ficheros en carpeta y nombre del log del docking
path = os.getcwd() + "/"
folder = os.listdir()
reg_expr = re.compile(".*dlg")
dock_log_name = filter(reg_expr.match, folder)


data = pd.read_csv(dock_log_name, header = "none")

# search for CLUSTERING HISTOGRAM y RMSD table
hist_row = (data == "CLUSTERING HISTOGRAM").any().idxmax()
poses_row = (data == "RMSD TABLE").any().idmax()

hist = data[hist_row:poses_row]
poses = data[poses_row:]


# dos ultimas lineas con tiempo de computo
time = data[-2:]


# coger primer rank del cluster histogram

# los 3 mas numerosos
