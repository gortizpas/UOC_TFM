#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 04 14:00:00 2023
@author: Guillermo Ortiz Pasamontes

Considerations:
    The script must be run from the folder where the main script of dimorphite is,
    since I have not been able to make python know where dimorphite is installed
    in order to be able to use it from anywhere.
    
    The script might fail at the optimisation steps due to "Bad conformer Id".
    Searching in rdkit forums, it might be due to isomerism lables incongruent 
    with other info, or to highly flexible ligands, in theory solved by using
    the option "random coordinates", but is still fails in some cases. Thats why
    errors at that step are catched, and a file with the index of ligands failed
    returned.
    
    RDkit must be installed
    
    The only things to modify to adapt to your use case are:
        - paths of files and folder where to save
        - extraction of relevant information from files
        - pH range used by Dimorphite-DL
        - number of threads to use in parallelisation
        
        started at 19:20-20:20 = 1h para la primera vuelta a los compuestos
        
"""

# Libraries
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
import dimorphite_dl
import os
import multiprocessing as mp

# Path of file with molecule data
data = pd.read_csv('/media/gorpas/linux-storage/UOC/docking/ligands/ligands_<10rb.csv', sep=';', header=0 )

# Path of folder where data will be stored.
save = "/media/gorpas/linux-storage/UOC/docking/ligands/dimorphite/"

# Extraction of relevant columns
inchis = pd.DataFrame(data.iloc[:,[3,12]])
inchis['index'] = range(1, len(inchis) + 1)
inchis = inchis.values.tolist()


def inchi_to_mol(name, inchi, index):
    """
    # Generates .mol files with 3D coordinates from inchi strings of the molecules.
    # Includes the inchi, name and smile string separated by ; between tabs (\t)
    # For that, it adds hydrogens and optimises structure with the MMFF2?? forcefield
    # Finally, writes a file with one smile per row for each ligand.

    Parameters
    ----------
    name : string
        String with name of ligand
    inchi : string
        String with inchi of ligand
    index : int
        Index by position in list used to keep track of molecules used as input.
    Returns
    -------
    mols : list
        Returns a list of lists with the index of the molecule in the 1st postion
        and an rdkit mol object in the second, per ligand 
    """
    
    mols = []
    opt_fail = []
    
    # Generates mol object from inchi, adds
    m = Chem.inchi.MolFromInchi(inchi)
    m.SetProp("_Name", str(inchi) + "\t;\t" + str(name) + "\t;\t" + Chem.MolToSmiles(m))
    
    # Structure optimisation step
    m2 = Chem.AddHs(m)
    AllChem.EmbedMolecule(m2, useRandomCoords=True, randomSeed=0xf00d)
    try:
        AllChem.MMFFOptimizeMolecule(m2)
    except ValueError:
        opt_fail.append(str("lig_unopt_" + str(index)))
        print("Optimisation failed after pH evaluation for molecule " + str(index))
    
    # Generates one file per ligand with 3D coordinates. (mol format)
    mols.extend([index, m2])
    print(Chem.MolToMolBlock(m2), file=open(save + "original/lig_" + str(index) + ".mol",'w'))

    return mols, opt_fail


def mol_to_smiles(index, mols):
    """
    Parameters
    ----------
    index : int
        Index by position in list used to keep track of molecules used as input.
    mols : rdkit mol object

    Returns
    -------
    smiles : list
        List with canonical isomeric SMILES of molecules used as input.
    """
    
    smiles = []
    smiles.extend([index, Chem.MolToSmiles(mols, isomericSmiles=True)])
    
    return smiles

def prot_mol_to_smiles(index, version, mols):
    """
    Parameters
    ----------
    index : int
        Index by position in list used to keep track of molecules used as input.
    version: int
        Indicates the version of the ligand after protonation with dimorphite.
    mols : rdkit mol object

    Returns
    -------
    smiles : list
        List with canonical isomeric SMILES of molecules protonated according to pH used 
        as input.
    """
    
    smiles = []
    smiles.extend([index, version, Chem.MolToSmiles(mols, isomericSmiles=True)])
    
    return smiles


def protonation(index, mols):
    """
    # Evaluates protonation state of ligands using Dimorphite-DL

    Parameters
    ----------
    index : int
        Index by position in list used to keep track of molecules used as input.
    mols : rdkit mol object

    Returns
    -------
    prot_mols : list
        List containing the index of the molecule, the version after pH evaluation and
        a rdkit mol object after pH evaluation
    opt_fail : list
        Molecules that have failed the optimisation step
    """
    molec = [mols]

    # Evaluation of pH of molecules
    protonated_mol = dimorphite_dl.run_with_mol_list(
        molec,
        pka_precision=0.25,
        min_ph=7.4,
        max_ph=7.4,
        #output_file = str(path) # Optional to output a file with SMILES of the molecules after pH evaluation
        )


    iter = 1
    prot_mols = []
    
    for m in protonated_mol:
        opt_pH_fail = []

        # optimisation of structure after pH evaluation
        m = Chem.AddHs(m)
        AllChem.EmbedMolecule(m, useRandomCoords=True, randomSeed=0xf00d)
        # Error catching if optimisation fails, also stores which molecule has failed
        try:
            AllChem.MMFFOptimizeMolecule(m)
        except ValueError:
            opt_pH_fail.append(str("dim_lig_unopt_" + str(index) + "_v" + str(iter)))
            print("Optimisation failed for molecule " + str(index) + "_v" + str(iter))
            
        # Generation of 3D mol file of ligands after pH evaluation
        print(Chem.MolToMolBlock(m), file=open(save + "pH/dim_lig_" + str(index) + "_v" + str(iter) + ".mol",'w'))
        prot_mols.append([index, iter, m])
        iter = iter + 1
            
    return prot_mols, opt_pH_fail


def main(params=None):
    
    # Generates a folder to store molecules after pH evaluation, if it doesnt exist already.
    isExist = os.path.exists(save + "pH")
    if not isExist:
        os.makedirs(save + "pH")
        
    # Generates a folder to store molecules after pH evaluation, if it doesnt exist already.
    isExist = os.path.exists(save + "original")
    if not isExist:
        os.makedirs(save + "original")   
                    
    # Generates a folder to store molecules after pH evaluation, if it doesnt exist already.
    isExist = os.path.exists(save + "docs")
    if not isExist:
        os.makedirs(save + "docs")
        
    # Generates a pool of threads, with threads = max - 2
    pool = mp.Pool(mp.cpu_count())

    # Parallel asynchronous generation of mol objects and ligand files.
    mols = pool.starmap_async(inchi_to_mol, [row for row in inchis]).get()
    
    # Separation of previous output
    opt_fail = []
    only_mols = []
    
    for item in mols:        
        opt_fail.append(item[-1])
        only_mols.append(item[0]) 

    # Parallel asynchronous generation of SMILES of ligands, with index
    smiles_unprot = pool.starmap_async(mol_to_smiles, [row for row in only_mols]).get()

    # Parallel asynchronous generation of mol objects after pH evaluation
    # Couldnt use ->  prot_mols, opt_fail = pool.starmap_async(protonation, [row for row in mols]).get()
    # so need to separate output later on
    prot_mols = pool.starmap_async(protonation, [row for row in only_mols]).get()
               
    # Separation of previous output
    opt_pH_fail = []
    only_prot_mols = []
    
    for item in prot_mols:        
        opt_pH_fail.append(item[-1])
        for list in item[0]:
           only_prot_mols.append(list)            
    
    # Parallel asynchronous generation of SMILES of ligands after pH evaluation, with index and version
    smiles_prot = pool.starmap_async(prot_mol_to_smiles, [row for row in only_prot_mols]).get()
    
    # Close pool
    pool.close()
    
    # Generation of file with molecules that failed to optimise (just in case)
    file = open(save + 'docs/opt_fail.txt', 'w')
    for item in opt_fail:
        file.write((str(item) + "\n").replace("[]\n", ""))
    file.close() 
    
    # Generation of file with molecules that failed to optimise after pH evaluation (just in case)
    file = open(save + 'docs/opt_pH_fail.txt', 'w')
    for item in opt_pH_fail:
        file.write((str(item) + "\n").replace("[]\n", ""))
    file.close() 
    
    # Generates a file with SMILES of ligands
    file = open(save + 'docs/smiles_unprot.txt', 'w')
    for item in smiles_unprot:
        file.write(str(item) + "\n")
    file.close()

    # Generates a file with SMILES of ligands after pH evaluation
    file = open(save + 'docs/smiles_prot.txt', 'w')
    for item in smiles_prot:
        file.write(str(item) + "\n")
    file.close()

if __name__ == "__main__":
    main()