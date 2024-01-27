from htmd.ui import *
import pandas
import os

config(viewer='ngl')

folder = os.listdir()
# folder = os.listdir().remove("htmd_protein_prep.py")
# por lo que sea si trato de quitar el script de python corrompe todo el objeto "folder
path = os.getcwd() + "/"


folder.remove("htmd_protein_prep.py")
folder.remove("prot_prep_v2.py")

for file in folder:
    name = file.replace(".pdb", "")
    protein = Molecule(name + '.pdb')
    protein_opt, df = systemPrepare(protein,
                                    titration = True,
                                    pH = 7.4,
                                    verbose = 0,
                                    return_details = True,
                                    hydrophobic_thickness = None,
                                    plot_pka = path + name + '_pka.png')
    protein_opt.write(path + name + '_prepared.pdb')
    df.to_excel(path + name + '-report.xlsx')
