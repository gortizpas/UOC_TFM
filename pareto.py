#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 23:47:44 2023

@author: gorpas
"""

import numpy as np
import pandas as pd
import os


def is_pareto_efficient_simple(costs):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient]>c, axis=1)  # Keep any point with a lower cost
            is_efficient[i] = True  # And keep self
    return is_efficient

def pareto_rank(df, ligand, cost_ids):
    """ 
    Pareto rank
    """
    nrows = df.shape[0]
    df["prank"] = [np.nan]*nrows 
    df_aux = df
    score = 1
    
    while df.prank.isnull().sum() > 0:
        costs = df_aux[cost_ids].to_numpy()
        effs = df_aux.ligand[is_pareto_efficient_simple(costs)]
        df.loc[df.ligand.isin(effs),"prank"] = score
        df_aux = df_aux[~df_aux.ligand.isin(effs)]
        score = score + 1
        df_aux
    return df



######################################
###### SELECT TOP HITS
######################################

path = os.getcwd()
folders = next(os.walk('.'))[1]

df1 = pd.read_excel(path + "/" + folders[0] + "/data/" + folders[0] + "_LBECs.xlsx")[["energy", "ligand"]]
df2 = pd.read_excel(path + "/" + folders[1] + "/data/" + folders[1] + "_LBECs.xlsx")[["energy", "ligand"]]
df3 = pd.read_excel(path + "/" + folders[2] + "/data/" + folders[2] + "_LBECs.xlsx")[["energy", "ligand"]]


df1["energy"] = df1.energy.apply(lambda x: float(x))
df2["energy"] = df2.energy.apply(lambda x: float(x))
df3["energy"] = df3.energy.apply(lambda x: float(x))
df3.dtypes
df3.columns

df1 = df1.groupby(["ligand"]).apply(lambda x: min(x.energy)).reset_index()
df2 = df2.groupby(["ligand"]).apply(lambda x: min(x.energy)).reset_index()
df3 = df3.groupby(["ligand"]).apply(lambda x: min(x.energy)).reset_index()
df1.shape
df2.shape
df3.shape

df = pd.merge(df1, df2, on = ["ligand"], how = "outer")
df = pd.merge(df, df3, on = ["ligand"], how = "outer")
df.columns = ["ligand","en1","en2","en3"]
df.shape
df.columns
pd.plotting.scatter_matrix(df[["en1","en2","en3"]], alpha=0.9, hist_kwds={'bins':300}, s = 0.1)

df["en1m"] = df.en1.apply(lambda x: -1*x)
df["en2m"] = df.en2.apply(lambda x: -1*x) 
df["en3m"] = df.en3.apply(lambda x: -1*x)
df = pareto_rank(df, "ligand", ["en1m","en2m","en3m"])
df["rankcent"] = df.prank * df.prank.min() / df.prank.max()*100
df.prank.max()
df.prank.min()

df[df.prank <= 20][["ligand","prank","rankcent"]].to_csv(path+"/foodsel-dnmt3b.csv", sep = ";", index = False)
