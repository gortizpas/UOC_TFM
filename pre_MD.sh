#! /bin/bash
# el script habria que ejecutarlo una vez por cada proteina y ligando ahora mismo.


# obtenemos ficheros
folders=$(find . -type d -name "*lig_*")

# cambiamos variables de ambiente para encontrar los ejecutables y usar la 2ª grafica
AMBERHOME=/usr/local/amber22
export CUDA_VISIBLE_DEVICES="1"

for f in $folders
do 
	cd $f
	lig_num=$(echo $f | sed 's/_/ /g' | awk '{print $3}')
	charge=$(grep $lig_num ../*charges* | awk '{print $2}')
	
	echo $f

	# pasamos el ligando por antechamber para generar 
	
	echo "ANTECHAMBER"
	antechamber -i ./lig.mol2 -fi mol2 -o ligand_antechamber.mol2 -fo mol2 -at gaff2 -c bcc -rn LIG -nc $charge
	echo "PARMCHK2"
	parmchk2 -i ligand_antechamber.mol2 -f mol2 -o ligand.am1bcc.frcmod
	
	cd ../
done
