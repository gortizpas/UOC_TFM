# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# librerias
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
#import dimorphite

# path del fichero con datos de moleculas
data = pd.read_csv('/media/gorpas/linux-storage/docking/ligands/comp_sets.csv', sep=';', header=0 )

#path del directorio donde se van a guardar los archivos
save = "/media/gorpas/linux-storage/docking/ligands/"

# extraccion de columnas relevantes
inchis = pd.DataFrame(data.iloc[:,[2,11]])
inchis = inchis.set_index('name')

smiles = []
iter = 1
# crea ficheros .mol con coordenadas 3D de las moleculas a partir de los inchi.
# tambien incluye el inchi y nombre normal de la molecula separado por ; entre tabuladores
# añade hidrogenos y minimaza estructura con MMFF2
# va creando una lista con los smiles
for molecule in inchis.itertuples(name=None):
    m = Chem.inchi.MolFromInchi(molecule[1])
    m.SetProp("_Name", molecule[1] + "\t;\t" + molecule[0] + "\t;\t" + Chem.MolToSmiles(m))
    m2 = Chem.AddHs(m)
    AllChem.EmbedMolecule(m2, randomSeed=0xf00d)
    AllChem.MMFFOptimizeMolecule(m2)
    print(Chem.MolToMolBlock(m2), file=open(save + "lig_" + str(iter) + ".mol",'w'))
    smiles.append(Chem.MolToSmiles(m))
    iter = iter + 1

# devuelve un fichero con los smiles de las moleculas
file = open(save + 'smiles.txt', 'w')
for item in smiles:
    file.write(item+"\n")
file.close()

# necesito que compruebe estado de protonacion y cambie la estrucutra acorde con el mismo
# no consigo que funcione dimorphite, pero hay otro programa de los mismos autores que lo incluye
# gypsum-DL, pero me crea muchos tautomeros que no se como escoger.


# caca = inchis['inchi'].tolist()
# lista = [Chem.inchi.MolFromInchi(molecule) for molecule in caca]

#protonated_mols = dimorphite.run_with_mol_list(
#    lista,
#    min_ph=5.0,
#    max_ph=9.0,
#)