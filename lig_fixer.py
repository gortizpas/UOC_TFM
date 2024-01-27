#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:05:04 2023

@author: gorpas
"""

import glob
import os
import re

path = os.getcwd()
subdirs = [x[0] for x in os.walk(path)][5:]

#real_subdirs = []
#for folder in subdirs:
#    if "prank" in folder:
#        real_subdirs.append(folder)

for folder in subdirs:
#for folder in real_subdirs:
    files = os.listdir(folder)
    for file in files:
        with open(folder + "/" + file, "r") as sources:
            lines = sources.readlines()
        with open(folder + "/" + file, "w") as sources:
            for line in lines:
                sources.write(re.sub(r'UNL  ', 'LIG A', line))   