folders=$(find . -type d -name "*lig_*" | sed 's/\/\.//')
path_ADGPU="/home/gorpas/ChemSoft/AutoDock-GPU/"
ADGPU_version="autodock_gpu_32wi"


for f in $folders
do
	cd $f
        $path_ADGPU$ADGPU_version --ffile *fld --lfile *lig_*.pdbqt --nrun 1000
        cd ..
done

