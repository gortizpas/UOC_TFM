#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 22:37:47 2023

@author: gorpas
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.Descriptors import CalcMolDescriptors  # falla aqui

def calc_properties (molecule):
    
    mol = Chem.inchi.MolFromInchi(molecule)

    mwt = Chem.rdMolDescriptors.CalcExactMolWt(mol)
    logP = Chem.Crippen.MolLogP(mol)          
    rb = Chem.rdMolDescriptors.CalcNumRotatableBonds(mol)
    hba = Chem.rdMolDescriptors.CalcNumHBA(mol)            
    hbd = Chem.rdMolDescriptors.CalcNumHBD(mol)
#    charge = Chem.rdMolDescriptors.CalcExactMolWt(mol)
    
    
    
    
    # calculo de cargas de gasteiger y suma de todo, no se si se puede hacer así para conseguir cargas formales
    Chem.AllChem.ComputeGasteigerCharges(mol)
    charges = []
    
    for atom in range(mol.GetNumAtoms()):    
        charges.append(mol.GetAtomWithIdx(atom).GetDoubleProp('_GasteigerCharge'))
    charge = sum(charges)
    
    # obtiene la carga de la molecula, pero teniendo en cuenta que no se han computado 
    # y que provienen de smiles genericos, ninguno va a tener
#    charge = Chem.GetFormalCharge(mol) 
    
    return mwt, logP, rb, hba, hbd, charge
    
    
    
#    alternativas   
#    mwt = []                rdkit.Chem.rdMolDescriptors.CalcExactMolWt
#    logP = []               rdkit.Chem.rdMolDescriptors.BCUT2D
#    rb = []                 rdkit.Chem.rdMolDescriptors.CalcNumRotatableBonds
#    hba = []                rdkit.Chem.rdMolDescriptors.CalcNumHBA
#    hbd = []                rdkit.Chem.rdMolDescriptors.CalcNumHBD
#    charge = []             rdkit.Chem.rdMolDescriptors.BCUT2D


# Path of folder where data will be stored.
save = "/media/gorpas/linux-storage/UOC/docking/ligands/"

# extraccion de INCHIS
decoys = open(save + "FXR_decoys.txt").read().split()

