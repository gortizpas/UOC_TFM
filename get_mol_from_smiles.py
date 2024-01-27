# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# librerias
from rdkit import Chem
from rdkit.Chem import AllChem


#path del directorio donde se van a guardar los archivos
save = "/media/gorpas/linux-storage/UOC/docking/ligands/decoys/FXR/10rb/"

# extraccion de smiles
ligand_file = open(save + 'ligands.smi', 'r')
ligand = ligand_file.readlines()
decoys_file = open(save + 'decoys.smi', 'r')
decoys = decoys_file.readlines()

smiles = []
smiles.append(ligand).append(decoys)

iter = 0
# crea ficheros .mol con coordenadas 3D de las moleculas a partir de los inchi.
# tambien incluye el inchi y nombre normal de la molecula separado por ; entre tabuladores
# añade hidrogenos y minimaza estructura con MMFF2
# va creando una lista con los smiles
for molecule in smiles:
    m = Chem.MolFromSmiles(molecule)
    m.SetProp("_Name", molecule)
    m2 = Chem.AddHs(m)
    AllChem.EmbedMolecule(m2, randomSeed=0xf00d)
    AllChem.MMFFOptimizeMolecule(m2)
    print(Chem.MolToMolBlock(m2), file=open(save + "decoy_" + str(iter) + ".mol",'w'))
    iter = iter + 1

