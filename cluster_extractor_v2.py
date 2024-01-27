#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 17:59:07 2023

@author: gorpas

se ejecuta bien desde spyder
con el script en la carpeta de la proteina donde estan el resto de carpetas con los ligandos
"""
import shutil
import glob
import os
import multiprocessing as mp
import pandas as pd

def extractor(path, working_dir):
    #cargamos fichero con los resultados de los dockings


    dlg = open(glob.glob(path + "*dlg")[0], 'r')
    lines = dlg.readlines()
    
    # determinamos donde empieza cada pose
    run_start_lines = []
    for line in lines:
        if line.find("Run:") != -1:
            run_start_lines.append(lines.index(line))
            
            # obtenemos el numero de lineas que ocupa cada pose            
    lines_to_get = run_start_lines[1]-run_start_lines[0] - 7

    # extraemos poses con sus metadatos
    molecs = []
    run_nums = []
    energies = []


    for item in run_start_lines:
        run_lines = lines[item:(item+lines_to_get)]

        run_num = run_lines[0]
        energy = run_lines[6:16]

        for line in run_lines:
            if line.find("DOCKED: ROOT") != -1:
                start_line = run_lines.index(line)
                continue
            elif line.find("DOCKED: ENDMDL") != -1:
                end_line = run_lines.index(line)
            else:
                continue

            mol = run_lines[start_line + 1 : end_line + 1]
            
        for line in range(len(mol)):
            mol[line] = mol[line].replace("DOCKED: ", "")
                
        molecs.append(mol)
        run_nums.append(run_num)
        energies.append(energy)

    # creamos carpetas
    isExist = os.path.exists(path + "poses")
    if not isExist:
        os.makedirs(path + "poses")

    isExist = os.path.exists(path + "clusters")
    if not isExist:
        os.makedirs(path + "clusters")
        
    isExist = os.path.exists(path + "clusters/top")
    if not isExist:
        os.makedirs(path + "clusters/top")
        
    isExist = os.path.exists(path + "metadata")
    if not isExist:
        os.makedirs(path + "metadata")
    
    # generamos ficheros con las estructuras 3D de las distintas poses en pdbqt.
    for mol in range(len(molecs)):
        file = open(path + 'poses/pose_' + str(mol + 1) + '.pdbqt', 'w')
        file.writelines(molecs[mol])
        file.close()
        
    # extraemos histograma
    for line in lines:
        if line.find("CLUSTERING HISTOGRAM") != -1:
            hist_start = lines.index(line)
            continue
        elif line.find("RMSD TABLE") != -1:
            hist_end = lines.index(line)
        else:
            continue
        
    histogram = lines[hist_start:hist_end-2]
    
    for line in range(len(histogram)):
        histogram[line] = histogram[line].split("|")
        
    df_hist = pd.DataFrame(histogram[10:-1])
    df_hist = df_hist.astype({col: float for col in df_hist.columns[:-1]})
    
    df_hist.columns = ["Rank", "LBE", "Run", "MBE", "Nº poses", "Histogram"]
    #    df.set_index(df[0])
    df_hist.to_excel(path + 'metadata/histogram.xlsx',)
    
    #    file = open(path + 'metadata/histograma.txt', 'w')
    #    file.write(histogram)
    #    file.close()

    # extraemos tabla RMSD
    RMSD_table = lines[hist_end : lines.index(lines[-2]) - 1]
    
    for line in range(len(RMSD_table)):
        RMSD_table[line] = RMSD_table[line].split()
        
    df_RMSD = pd.DataFrame(RMSD_table[9:]).drop(columns=6)
    
    df_RMSD.columns = ["Rank", "sub-Rank", "Run", "BE", "Cluster RMSD", "Reference RMSD"]
    
    df_RMSD = df_RMSD.astype(float)
    #    df.set_index(df[0])
    df_RMSD.to_excel(path + 'metadata/RMSD_table.xlsx',)
    
    #    file = open(path + 'metadata/RMSD_table.txt', 'w')
    #    file.write(RMSD_table)
    #    file.close()
    

    # seleccionamos poses de cada cluster
    cluster_poses = df_hist.iloc[:,2].astype(int).values
    for pose in cluster_poses:
        shutil.copy(path + "poses/pose_" + str(pose) + ".pdbqt", path + "clusters/pose_" + str(pose) + ".pdbqt")

    # seleccionamos la mejor pose y el cluster mas numeroso
    MNC_row = df_hist.idxmax(axis=0, numeric_only=True)[-1:].values
    MNC_pose = int(df_hist.iloc[MNC_row, 2].values[0])
    
    LBEC_pose = int(df_hist.iloc[0,2])

    shutil.copy(path + "poses/pose_" + str(MNC_pose) + ".pdbqt", path + "clusters/top/MNC_pose_" + str(MNC_pose) + ".pdbqt")
    shutil.copy(path + "poses/pose_" + str(LBEC_pose) + ".pdbqt", path + "clusters/top/LBEC_pose_" + str(LBEC_pose) + ".pdbqt")
    
    shutil.copy(path + "poses/pose_" + str(LBEC_pose) + ".pdbqt", working_dir + "/data/LBECs/" + path.split("/")[-2] + "-" + str(LBEC_pose) + ".pdbqt")
    
    # extraemos tiempo de computo
    run_time = lines[-2]
    idle_time = lines[-1]
    
    file = open(path + 'metadata/tiempo_de_computo.txt', 'w')
    file.write(run_time + "\n" + idle_time + "\n" + "Total time: " + 
               str(float(run_time.split()[2]) + float(idle_time.split()[2]) ))
    file.close()
        
    print("DONE")

    # retorna energía y run del ligando x
    return [df_hist.iloc[0, 1], path.split("/")[-2], str(df_hist.iloc[0, 2])]

def main():
    working_dir = os.getcwd()
    folders = glob.glob(working_dir + "/*decoy*/")
#    dummy = [0]

    # creamos carpetas
    isExist = os.path.exists(working_dir + "/data")
    if not isExist:
        os.makedirs(working_dir + "/data")

    isExist = os.path.exists(working_dir + "/data/LBECs")
    if not isExist:
        os.makedirs(working_dir + "/data/LBECs")

    # esto va a ver que ajustarlo
    pool = mp.Pool(mp.cpu_count()-2)

# parece que hace algo, pero no me termina de generar los ficheros bien.
    LBECs = pool.starmap_async(extractor, [(path, working_dir) for path in folders]).get()
    
    df_LBECs = pd.DataFrame(LBECs, columns = ['energy', 'ligand', 'run'])
    df_LBECs.to_excel(working_dir + '/data/' + working_dir.split("/")[-1] + '_LBECs.xlsx',)

    pool.close()
    
if __name__ == "__main__":
    main()
